# Copyright (C) 2020 Jochen Keil <jochen.keil@gmail.com> and contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import zlib
import base64
import codecs
import struct

class XCoder():
    def __init__(self):
        self.hex_encoder = codecs.getencoder('hex_codec')
        self.hex_decoder = codecs.getdecoder('hex_codec')

    def decode(self, cformat, params):
        ps = None
        if params[0:2] == 'gz':
            ps = zlib.decompress(base64.b64decode(params[4:]))
        else:
            ps = self.hex_decoder(params)[0]
        return struct.unpack(cformat, ps)

    def encode(self, cformat, *cparams):
        return self.hex_encoder(struct.pack(cformat, *cparams))[0]
