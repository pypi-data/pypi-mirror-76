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

import xml.etree.ElementTree as ET

# XML Namespaces (taken from darktable's XMP files)
ns = { 'darktable': 'http://darktable.sf.net/'
     , 'dc': 'http://purl.org/dc/elements/1.1/'
     , 'exif': 'http://ns.adobe.com/exif/1.0/'
     , 'lr': 'http://ns.adobe.com/lightroom/1.0/'
     , 'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
     , 'x': 'adobe:ns:meta/'
     , 'xmp': 'http://ns.adobe.com/xap/1.0/'
     , 'xmpMM': 'http://ns.adobe.com/xap/1.0/mm/'
     }

# Register namespaces for write()
# Without, write() will use generic names like ns0, ns1, etc. which
# darktable won't accept
def register_namespace():
    for prefix, uri in ns.items():
        ET.register_namespace(prefix, uri)
