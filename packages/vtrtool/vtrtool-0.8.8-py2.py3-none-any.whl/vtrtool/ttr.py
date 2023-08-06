"""Python utilities for Fullwave3D TTR data files

 * Licensed under terms of 3-Clause BSD license (see LICENSE)
 * Copyright (c) 2017-2020 S-Cube, tlin@s-cube.com

"""
from __future__ import print_function
import os.path
# import struct
import json
import numpy


class TTRData(object):
    """
    Represents TTR data
    """

    def __init__(self, file_name="", read_data=True, use_memmap=False):
        """
        :param file_name: file name of TTR file to read
        :type file_name: str
        :param read_model: whether to read the actual data,
            defaults to True
        :type read_model: bool, optional
        """
        # instance variables
        self.file = file_name
        self.use_memmap = use_memmap
        self.count1 = None
        self.count2 = None
        self.nt = None
        self.total_time = None
        self.index1 = None
        self.index2 = None
        self.ntrace = None
        self.data = None

        if file_name:
            self._read_from_file()

    def __repr__(self):
        return "TTRData(count1=%i count2=%i nt=%i total_time=%f)" % (self.count1, self.count2, self.nt, self.total_time)

    def _read_from_file(self, read_data=True):
        if self._file_exists():
            self._parse_metadata()
            if read_data:
                self._read_data()
        else:
            raise IOError("Given file_name does not point to a valid file")

    def _file_exists(self):
        """
        Checks if the TTR file name points to a valid file that exists

        :returns: True if self.file is a valid file path and file exists
        :rtype: {bool}
        """
        return os.path.isfile(self.file)

    def _parse_metadata(self):
        """
        Fills in global header values of TTR files
        """
        with open(self.file, "rb") as f:
            f.seek(4)  # skip head Fortran record marker
            int_headers = numpy.fromfile(f, dtype=numpy.int32, count=3)
            float_headers = numpy.fromfile(f, dtype=numpy.float32, count=1)
            self.count1 = int_headers[0]
            self.count2 = int_headers[1]
            self.nt = int_headers[2]
            self.total_time = float_headers[0]

    def _read_data(self):
        """
        Reads the actual model properties from the VTR file, initializes and
        populates the self.arrays
        """
        with open(self.file, "rb") as f:
            f.seek(24)  # skip global headers
            raw_data = numpy.fromfile(f, dtype=numpy.uint32, count=-1)
        nbytes_trace = (self.nt + 4)
        raw_data = raw_data.reshape((-1, nbytes_trace))
        self.ntrace = raw_data.shape[1]
        self.index1 = raw_data[:, 1].view(dtype=numpy.int32)
        self.index2 = raw_data[:, 2].view(dtype=numpy.int32)
        self.data = raw_data[:, 3 : self.nt + 3].view(dtype=numpy.float32)

    # def save_vtr_file(self, out_filename=None):
    #     # saves to a VTR file

    #     if out_filename is None:
    #         if self.file is None:
    #             raise Exception("out_filename cannot be none")
    #         else:
    #             filename = self.file
    #     else:
    #         filename = out_filename

    #     meta_header = (12, self.num_properties, self.num_dimensions, 0, 12)
    #     meta_header_bytes = struct.pack("<" + ("i" * 5), *meta_header)

    #     dim_header = [4 * self.num_dimensions]
    #     dim_header.append(self.nx3)
    #     if self.num_dimensions == 2:
    #         dim_header.append(self.nx1)
    #     elif self.num_dimensions == 3:
    #         dim_header.append(self.nx2)
    #         dim_header.append(self.nx1)
    #     dim_header.append(4 * self.num_dimensions)
    #     dim_header_bytes = struct.pack("<" + ("i" * (self.num_dimensions + 2)), *dim_header)

    #     num_traces = self.nx2 * self.nx1
    #     trace_length = self.nx3 * self.num_properties
    #     trace_rec_byte = struct.pack("<i", 4 * trace_length)
    #     flat_model = self.model.reshape((num_traces, trace_length))

    #     with open(filename, "wb") as out_file:
    #         out_file.write(meta_header_bytes)
    #         out_file.write(dim_header_bytes)
    #         for tr in range(num_traces):
    #             out_file.write(trace_rec_byte)
    #             out_file.write(flat_model[tr, :].tobytes())
    #             out_file.write(trace_rec_byte)

    def meta_info(self, return_json=False):
        def _default_0(x):
            if x is None:
                return 0
            else:
                return x

        # returns a dict of meta info, a JSON string if flagged true
        meta = {}
        meta["filename"] = self.file
        meta["count1"] = _default_0(self.count1)
        meta["count2"] = _default_0(self.count2)
        meta["nt"] = _default_0(self.nt)
        meta["total_time"] = _default_0(self.total_time)
        meta["ntrace"] = _default_0(self.ntrace)

        if return_json:
            return json.dumps(meta)
        else:
            return meta

    @classmethod
    def from_ndarray(cls, array):
        """
        constructs a TTRData object from 1 or more arrays
        """
        # validate all input ad ndarrays
        if not isinstance(array, numpy.ndarray):
            raise ValueError("input must be numpy ndarray")

        # collect metadata from first input property
        first_prop = numpy.squeeze(first_prop)
        if first_prop.dtype is not numpy.dtype("float32"):
            first_prop = first_prop.astype("float32")
        vtr_shape = first_prop.shape
        num_dimensions = len(vtr_shape)

        # collect all properties and make sure they are consistent
        arrays = list()
        arrays.append(first_prop)

        for prop in remaining_props:
            if numpy.squeeze(prop).shape != vtr_shape:
                raise ValueError("all props must have the same dimensions")
            if prop.dtype is not numpy.dtype("float32"):
                prop = first_prop.astype("float32")
            arrays.append(prop)

        # zip all props up along fast dimension
        model = numpy.stack(arrays, axis=-1)

        # create object and populate metadata
        vtr = cls()
        vtr.num_dimensions = num_dimensions
        vtr.num_properties = len(arrays)
        vtr.shape = vtr_shape
        vtr.shape_fortran = vtr_shape[-1::-1]  # reverse
        vtr.arrays = [None] * vtr.num_properties

        if num_dimensions == 3:
            vtr.nx3 = vtr_shape[2]
            vtr.nx2 = vtr_shape[1]
            vtr.nx1 = vtr_shape[0]
            model = model.reshape((vtr.nx1, vtr.nx2, vtr.nx3, vtr.num_properties))
            for prop_index in range(0, vtr.num_properties):
                vtr.arrays[prop_index] = numpy.squeeze(model[:, :, :, prop_index])
        elif num_dimensions == 2:
            vtr.nx3 = vtr_shape[1]
            vtr.nx2 = 1
            vtr.nx1 = vtr_shape[0]
            model = model.reshape((vtr.nx1, vtr.nx3, vtr.num_properties))
            for prop_index in range(0, vtr.num_properties):
                vtr.arrays[prop_index] = numpy.squeeze(model[:, :, prop_index])
        elif num_dimensions == 1:
            vtr.nx3 = vtr_shape[0]
            vtr.nx2 = 1
            vtr.nx1 = 1
            model = model.reshape((vtr.nx3, vtr.num_properties))
            for prop_index in range(0, vtr.num_properties):
                vtr.arrays[prop_index] = numpy.squeeze(model[:, prop_index])

        vtr.model = model
        return vtr
