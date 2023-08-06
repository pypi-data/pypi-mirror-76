#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A simple tool to output binary data. Multiple arguments are output in framed
format, see `refinery.lib.frame`.
"""
from .. import arg, Unit


class emit(Unit):

    def __init__(self, *data: arg(help=(
        'Data to be emitted. If no argument is specified, data '
        'is retrieved from the clipboard. Multiple arguments are '
        'output in framed format.'
    ))):
        super().__init__(data=data)

    def process(self, data):
        if not self.args.data:
            import pyperclip
            data = pyperclip.paste()
            try:
                data = data.encode(self.codec)
            except AttributeError:
                # data is None
                data = B''
            except UnicodeDecodeError:
                data = data.encode('utf-16le')
            yield data
        else:
            yield from self.args.data

    @classmethod
    def run(cls, argv=None, stream=None):
        super(emit, cls).run(
            argv=argv,
            stream=stream or open(__import__('os').devnull, 'rb')
        )
