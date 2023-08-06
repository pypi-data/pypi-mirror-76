#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io

try:
    from Registry.Registry import Registry
except ModuleNotFoundError:
    Registry = None

from . import PathExtractorUnit, UnpackResult


class winreg(PathExtractorUnit):
    """
    Extract values from a Windows registry hive.
    """
    def _walk(self, key, *path):
        here = '/'.join(path)
        if not self._check_reachable(here):
            return
        for value in key.values():
            vpath = F'{here}/{value.name()}'
            yield UnpackResult(vpath, lambda v=value: v.raw_data())
        for subkey in key.subkeys():
            yield from self._walk(subkey, *path, subkey.name())

    def unpack(self, data):
        with io.BytesIO(data) as stream:
            yield from self._walk(Registry(stream).root())
