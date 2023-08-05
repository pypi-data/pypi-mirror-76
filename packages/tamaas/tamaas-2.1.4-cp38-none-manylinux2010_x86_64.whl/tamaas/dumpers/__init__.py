# -*- mode:python; coding: utf-8 -*-
# @file
# @section LICENSE
#
# Copyright (©) 2016-2020 EPFL (École Polytechnique Fédérale de Lausanne),
# Laboratory (LSMS - Laboratoire de Simulation en Mécanique des Solides)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Dumpers for the class tamaas.Model
"""
from __future__ import print_function
from sys import stderr
from os import makedirs
import os.path

import numpy as np

from .. import ModelDumper, model_type
from ._helper import make_periodic, step_dump, directory_dump


class FieldDumper(ModelDumper):
    """Abstract dumper for python classes using fields"""
    postfix = ''
    extension = ''
    name_format = "{basename}{postfix}.{extension}"

    def __init__(self, basename, *fields, **kwargs):
        """Construct with desired fields"""
        super(FieldDumper, self).__init__()
        self.basename = basename
        self.fields = fields
        self.all_fields = kwargs.get('all_fields', False)

    def add_field(self, field):
        """Add another field to the dump"""
        if field not in self.fields:
            self.fields.append(field)

    def dump_to_file(self, fd, model):
        """Dump to a file (name or handle)"""
        pass

    def get_fields(self, model):
        """Get the desired fields"""
        if not self.all_fields:
            requested_fields = self.fields
        else:
            requested_fields = model.getFields()

        return {field: model.getField(field) for field in requested_fields}

    def get_attributes(self, model):
        """Get model attributes"""
        return {
            'model_type': str(model.type),
            'system_size': model.getSystemSize(),
            'discretization': model.getDiscretization()
        }

    def dump(self, model):
        self.dump_to_file(self.file_path, model)

    @property
    def file_path(self):
        """Get the default filename"""
        return self.name_format.format(basename=self.basename,
                                       postfix=self.postfix,
                                       extension=self.extension)


@directory_dump('numpys')
@step_dump
class NumpyDumper(FieldDumper):
    """Dumper to compressed numpy files"""
    extension = 'npz'

    def dump_to_file(self, fd, model):
        """Saving to compressed multi-field Numpy format"""
        np.savez_compressed(fd, attrs=self.get_attributes(model),
                            **self.get_fields(model))


try:
    import h5py

    @directory_dump('hdf5')
    @step_dump
    class H5Dumper(FieldDumper):
        """Dumper to HDF5 file format"""
        extension = 'h5'

        def dump_to_file(self, fd, model):
            """Saving to HDF5 with metadata about the model"""
            with h5py.File(fd, 'w') as fh:
                # Writing data
                for name, field in self.get_fields(model).items():
                    dset = fh.create_dataset(name, field.shape, field.dtype,
                                             compression='gzip',
                                             compression_opts=7)
                    dset[:] = field

                # Writing metadata
                for name, attr in self.get_attributes(model).items():
                    fh.attrs[name] = attr
except ImportError:
    pass

try:
    import uvw  # noqa

    @directory_dump('paraview')
    @step_dump
    class UVWDumper(FieldDumper):
        """Dumper to VTK files for elasto-plastic calculations"""
        extension = 'vtr'
        forbidden_fields = ['traction', 'gap']  # TODO make generic

        def dump_to_file(self, fd, model):
            """Dump displacements, plastic deformations and stresses"""
            discretization = model.getDiscretization().copy()

            # Because we make fields periodic
            discretization[1] += 1
            discretization[2] += 1

            # Space coordinates
            coordinates = [np.linspace(0, L, N)
                           for L, N in zip(model.getSystemSize(),
                                           discretization)]

            # Correct order of coordinate dimensions
            dimension_indices = [1, 2, 0]

            # Creating rectilinear grid with correct order for components
            grid = uvw.RectilinearGrid(
                fd, (coordinates[i] for i in dimension_indices),
                compression=True,
            )

            # Iterator over fields we want to dump
            # Avoid 2D fields (TODO make generic)
            fields_it = filter(lambda t: t[0] not in self.forbidden_fields,
                               self.get_fields(model).items())

            # We make fields periodic for visualization
            for name, field in fields_it:
                array = uvw.DataArray(np.array(make_periodic[name](field),
                                               dtype=np.double),
                                      dimension_indices, name)
                grid.addPointData(array)

            grid.write()

    @directory_dump('paraview')
    class UVWGroupDumper(FieldDumper):
        "Dumper to ParaViewData files"
        extension = 'pvd'

        def __init__(self, basename, *fields, **kwargs):
            """Construct with desired fields"""
            super(UVWGroupDumper, self).__init__(basename, *fields, **kwargs)

            subdir = os.path.join('paraview', basename + '-VTR')
            if not os.path.exists(subdir):
                makedirs(subdir)

            self.uvw_dumper = UVWDumper(
                os.path.join(basename + '-VTR', basename), *fields, **kwargs
            )

            self.group = uvw.ParaViewData(self.file_path, compression=True)

        def dump_to_file(self, fd, model):
            self.group.addFile(
                self.uvw_dumper.file_path.replace('paraview/', ''),
                timestep=self.uvw_dumper.count
            )
            self.group.write()
            self.uvw_dumper.dump(model)
except ImportError as error:
    print(error, file=stderr)


try:
    from netCDF4 import Dataset

    @directory_dump('netcdf')
    class NetCDFDumper(FieldDumper):
        """Dumper to netCDF4 files"""

        extension = "nc"
        boundary_fields = ['traction', 'gap']

        def _file_setup(self, grp, model):
            grp.createDimension('frame', None)

            # Local dimensions
            model_dim = len(model.getDiscretization())
            self._vec = grp.createDimension('spatial', model_dim)
            self._tens = grp.createDimension('Voigt', 2*model_dim)
            self.model_info = model.getDiscretization(), model.type

            # Create boundary dimensions
            it = zip("xy", model.getBoundaryDiscretization(),
                     model.getBoundarySystemSize())

            for label, size, length in it:
                grp.createDimension(label, size)
                coord = grp.createVariable(label, 'f8', (label,))
                coord[:] = np.linspace(0, length, size, endpoint=False)

            self._create_variables(
                grp, model,
                lambda f: f[0] in self.boundary_fields,
                model.getBoundaryDiscretization(), "xy"
            )

            # Create volume dimension
            if model.type in {model_type.volume_1d, model_type.volume_2d}:
                size = model.getDiscretization()[0]
                grp.createDimension("z", size)
                coord = grp.createVariable("z", 'f8', ("z",))
                coord[:] = np.linspace(0, model.getSystemSize()[0], size)

                self._create_variables(
                    grp, model,
                    lambda f: f[0] not in self.boundary_fields,
                    model.getDiscretization(), "zxy"
                )

            self.has_setup = True

        def dump_to_file(self, fd, model):
            mode = 'a' if os.path.isfile(fd) \
                and getattr(self, 'has_setup', False) else 'w'

            with Dataset(fd, mode, format='NETCDF4_CLASSIC') as rootgrp:
                if rootgrp.dimensions == {}:
                    self._file_setup(rootgrp, model)

                if self.model_info != (model.getDiscretization(), model.type):
                    raise Exception("Unexpected model {}".format(model))

                self._dump_generic(rootgrp, model)

        def _create_variables(self, grp, model, predicate,
                              shape, dimensions):
            field_dim = len(shape)
            fields = filter(predicate, self.get_fields(model).items())
            dim_labels = list(dimensions[:field_dim])

            for label, data in fields:
                local_dim = []

                # If we have an extra component
                if data.ndim > field_dim:
                    if data.shape[-1] == self._tens.size:
                        local_dim = [self._tens.name]
                    elif data.shape[-1] == self._vec.size:
                        local_dim = [self._vec.name]

                grp.createVariable(label, 'f8',
                                   ['frame'] + dim_labels + local_dim,
                                   zlib=True)

        def _dump_generic(self, grp, model):
            fields = self.get_fields(model).items()

            new_frame = grp.dimensions['frame'].size
            for label, data in fields:
                var = grp[label]
                var[new_frame, :] = np.array(data, dtype=np.double)


except ImportError:
    pass
