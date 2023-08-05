#!/usr/bin/env python3

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

import os
import re
import glob
import json
import zlib
import base64
import codecs
import shutil
import struct
import argparse
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import scipy.interpolate as interpolate
import xml.etree.ElementTree as ET
from attrdict import AttrDict

import dtlapse.args.help as args_help

hex_encoder = codecs.getencoder('hex_codec')
hex_decoder = codecs.getdecoder('hex_codec')

def decode(cformat, params):
    ps = None
    if params[0:2] == 'gz':
        ps = zlib.decompress(base64.b64decode(params[4:]))
    else:
        ps = hex_decoder(params)[0]
    return struct.unpack(cformat, ps)

def encode(cformat, *cparams):
    return hex_encoder(struct.pack(cformat, *cparams))[0]

def find_history(root):
    items = root[0][0].findall('darktable:history', ns)
    if len(items) == 0:
        raise ValueError
    else:
        return items[0]

def get_modversion(operation, xmp):
    with open(xmp) as f:
        history = find_history(ET.parse(f).getroot())
        for item in history[0]:
            for tag, value in item.attrib.items():
                if tag == '{' + ns['darktable'] + '}' + 'operation':
                    if value == operation:
                        for tag, value in item.attrib.items():
                            if tag == '{' + ns['darktable'] + '}modversion':
                                return int(value)

def get_description(root):
    for elem in root:
        for e in elem:
            if re.match('{.*}Description', e.tag) is not None:
                return e
    raise ValueError

def get_tags(root):
    tags = []
    desc = get_description(root)
    for subject in desc.findall('dc:subject', ns):
        for bag in subject.findall('rdf:Bag', ns):
            for li in bag.findall('rdf:li', ns):
                tags.append(li.text)
    return tags

# return operation params from history stack (usually a base64 string)
def get_params(history, operation):
    if history is not None:
        # reversed is necessary to access the last operation in the history stack
        for item in reversed(history[0]):
            for tag, value in item.attrib.items():
                if tag == '{' + ns['darktable'] + '}' + 'operation':
                    if value == operation:
                        return item.attrib['{' + ns['darktable'] + '}' + 'params']
        raise ValueError
    raise ValueError

def build_iop_element(iop, num, params):
    return ET.Element("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}li",
                     { "{http://darktable.sf.net/}operation": iop.operation
                     , "{http://darktable.sf.net/}enabled": "1"
                     , "{http://darktable.sf.net/}modversion": str(iop.modversion)
                     , "{http://darktable.sf.net/}iop_order": str(iop.iop_order)
                     , "{http://darktable.sf.net/}num": str(num)
                     , "{http://darktable.sf.net/}params": params
                     })

# new_params: list of base64 encoded parameters
def write_xmp_files(iop, new_params, xmp_files):
    for n, xmp_file in enumerate(xmp_files):
        with open(xmp_file) as xmp:
            tree = ET.parse(xmp)
            root = tree.getroot()
            history = None

            history = find_history(root)
            if history is not None:
                num = None

                for i, item in enumerate(root[0]):
                    for tag, value in item.attrib.items():
                        if tag == '{' + ns['darktable'] + '}' + 'history_end':
                            num = value
                            value = str(int(value) + 1)
                            item.attrib[tag] = value

                if num is None:
                    raise ValueError

                element = build_iop_element(iop, num, new_params[n])
                history[0].append(element)

                tree.write(xmp_file)

# if __name__ == "__main__":
def main():

    # XML Namespaces (taken from darktable's XMP files)
    ns = { 'darktable': 'http://darktable.sf.net/'
         , 'x': 'adobe:ns:meta/'
         , 'xmp': 'http://ns.adobe.com/xap/1.0/'
         , 'dc': 'http://purl.org/dc/elements/1.1/'
         , 'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
         }

    # Register namespaces for write()
    # Without, write() will use generic names like ns0, ns1, etc. which
    # darktable won't accept
    for prefix, uri in ns.items():
        ET.register_namespace(prefix, uri)

    opfilepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'iops')

    iops = []
    for opfile in glob.glob(os.path.join(opfilepath, '*.json')):
        try:
            with open(opfile) as f:
                iop = AttrDict(json.load(f))
                for iopdata in iop['iopdata']:
                    if iopdata['smooth'][0:5] == 'eval:':
                        iopdata['smooth'] = eval(iopdata['smooth'][5:])
                    if iopdata['cformat'][0:5] == 'eval:':
                        iopdata['cformat'] = eval(iopdata['cformat'][5:])
                iops.append(iop)
        except Exception as e:
            print('Failed to load ' + opfile + ': ' + str(e))

    parser = argparse.ArgumentParser(description=args_help.parser)

    subparsers = parser.add_subparsers(help=args_help.subparsers,
            dest='operation', required=True)

    for iop in iops:
        parser_iop = subparsers.add_parser(iop.operation, help=iop.help)

        parser_iop.add_argument('--dry-run', dest='dry_run',
                action='store_true', help=args_help.dry_run)
        parser_iop.add_argument('--no-backup', dest='no_backup', default=False,
                action='store_true', help=args_help.no_backup)
        parser_iop.add_argument('--plot', dest='plot', action='store_true',
                help=args_help.plot)
        parser_iop.add_argument('--xmps', dest='xmps', type=str, nargs='+',
                required=True, help=args_help.xmps)
        parser_iop.add_argument('--keyframes', dest='keyframes', type=str,
                nargs='+', help=args_help.keyframes)
        parser_iop.add_argument('--keyframe-tag', dest='keyframe_tag', type=str,
                default='Keyframe', help=args_help.keyframe_tag)
        parser_iop.add_argument('--interpolation', dest='interp_method',
                type=str, default='quadratic', help=args_help.interpolation)
        parser_iop.add_argument('--smooth', default=False, action='store_true',
                help=args_help.smooth)
        parser_iop.add_argument('--window', type=int, help=args_help.window)
        parser_iop.add_argument('--order', type=int, default=3,
                help=args_help.order)

    args = parser.parse_args()

    picture_xmps = args.xmps
    keyframe_xmps = args.keyframes

    picture_cparams = []
    keyframe_cparams = []
    keyframe_indices = []

    if not keyframe_xmps:
        keyframe_xmps = []
        for picture_xmp in picture_xmps:
            with open(picture_xmp) as f:
                tags = get_tags(ET.parse(f).getroot())
                if args.keyframe_tag in tags:
                    keyframe_xmps.append(picture_xmp)

    if (picture_xmps[0] != keyframe_xmps[0] and
            picture_xmps[-1] != keyframe_xmps[-1]):
        print('The first and the last XMP must be keyframes')
        exit()

    modversion = get_modversion(args.operation, keyframe_xmps[0])

    iop = None
    for op in iops:
        if op.operation == args.operation:
            for iopdata in op.iopdata:
                if iopdata.modversion == modversion:
                    iopdata['operation'] = op.operation
                    iop = AttrDict(iopdata)
                    break

    if iop is None:
        print('Could not find modversion ' + str(modversion) + ' for the '
                + args.operation + ' module.')
        exit()

    # store keyframe indices and params independently
    for keyframe_xmp in keyframe_xmps:
        with open(keyframe_xmp) as f:
            history = find_history(ET.parse(f).getroot())
            params = get_params(history, iop.operation)
            cparams = decode(iop.cformat, params)
            keyframe_cparams.append(cparams)
            keyframe_indices.append(picture_xmps.index(keyframe_xmp))

    # Check if there is a boolean for every parameter so that we can decide
    # whether we want the parameter to be interpolated or not
    # We can do this here after the C struct got unpacked. The previous check
    # based on the format string was error prone, because the specification does
    # not necessarily match the amount of values. For details check the `struct`
    # documentation and gitlab issue #4
    assert(len(iop.smooth) == len(keyframe_cparams[0]))

    # transpose params lists
    # https://note.nkmk.me/en/python-list-transpose/
    # [[P1, P2, P3, ..], [P1, P2, P3, ..]
    # -> [[P1, P1, ..], [P2, P2, ..], [P3, P3, ..], ..]
    picture_cparams = list(zip(*picture_cparams))
    keyframe_cparams = list(zip(*keyframe_cparams))

    xs = np.linspace(0, len(picture_xmps)-1, len(picture_xmps))
    ys = []

    for n, do_smooth in enumerate(iop.smooth):
        if do_smooth:
            f = interpolate.interp1d(keyframe_indices,
                                     keyframe_cparams[n],
                                     kind=args.interp_method)

            if args.smooth:
                # Savitzky-Golay filter needs two crucial parameters:
                # window size:
                # How many data points are used for smoothing?
                # For maximum smoothing I've decided to incorporate all data points.
                # (Minus one in case of an even size. An odd number is another requirement)
                # polynominal order:
                # The order of 3 was chosen by trying out various factors:
                # https://de.mathworks.com/help/signal/ref/sgolayfilt.html
                # A higher order means less smoothing, however a very low
                # order gives an almost linear curve
                window = args.window
                if window is None:
                    window = len(picture_xmps)
                    if window % 2 == 0:
                        window = window - 1
                elif window % 2 == 0:
                    sys.stderr.write('Window size must be odd!\n')
                    exit(1)

                order = args.order

                ys.append(signal.savgol_filter(f(xs), window, order))

            else:
                ys.append(f(xs))

        else:
            ys.append(len(picture_xmps) * [keyframe_cparams[n][0]])

    if args.plot:
        for n, _ in enumerate(iop.smooth):
            plt.plot(keyframe_indices, keyframe_cparams[n], 'o', xs, ys[n], '-')
        plt.show()
        exit()

    if args.dry_run:
        exit()

    # backup xmp files if not disabled
    if not args.no_backup:
        for xmp in picture_xmps:
            shutil.copy2(xmp, xmp + '.bkp')

    picture_new_cparams = []

    # transpose params lists
    # https://note.nkmk.me/en/python-list-transpose/
    # [[P1, P1, ..], [P2, P2, ..], [P3, P3, ..], ..]
    # -> [[P1, P2, P3, ..], [P1, P2, P3, ..]
    for ps in zip(*ys):
        picture_new_cparams.append(str(encode(iop.cformat, *ps), 'utf-8'))

    write_xmp_files(iop, picture_new_cparams, picture_xmps)
