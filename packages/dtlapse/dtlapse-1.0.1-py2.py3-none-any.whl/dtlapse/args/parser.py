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

import argparse

import dtlapse.args.help as args_help

# dtlapse \
#   [--frames ${xmps} | --frame-tag frame-tag ] \
#   [--first-frame-tag first-frame-tag --final-frame-tag final-frame-tag] \
#   [--keyframes ${keyframes} | --keyframe-tag keyframe-tag ] \
#   [--overwrite] \
#   [[-m|--module] module1, module2, .., moduleN [--copy | [[--interpolate method] | [--smooth [--window] [--order]]]]


parser = argparse.ArgumentParser(description=args_help.parser)

frames = parser.add_mutually_exclusive_group(required=True)

frames.add_argument('--frames')
frames.add_argument('--frames-tag')

first = parser.add_mutually_exclusive_group()

first.add_argument('--first-frame-tag')
first.add_argument('--final-frame-tag')

keyframes = parser.add_mutually_exclusive_group()

keyframes.add_argument('--keyframes')
keyframes.add_argument('--keyframes-tag')

parser.add_argument('--overwrite', action='store_true')

parser.add_parser('--module')

# module.add_argument('--copy')

# subparsers = parser.add_subparsers()
# module = subparsers.add_parser('--module')
# module.add_argument('--copy')

# module_options = module_parser.add_mutually_exclusive_group()

# module_options.add_argument('--copy', action='store_true')
# module_options.add_argument('--interpolate')

        # parser_iop = subparsers.add_parser(iop.operation, help=iop.help)

        # parser_iop.add_argument('--dry-run', dest='dry_run',
        #         action='store_true', help=args_help.dry_run)
        # parser_iop.add_argument('--no-backup', dest='no_backup', default=False,
        #         action='store_true', help=args_help.no_backup)
        # parser_iop.add_argument('--plot', dest='plot', action='store_true',
        #         help=args_help.plot)
        # parser_iop.add_argument('--xmps', dest='xmps', type=str, nargs='+',
        #         required=True, help=args_help.xmps)
        # parser_iop.add_argument('--keyframes', dest='keyframes', type=str,
        #         nargs='+', help=args_help.keyframes)
        # parser_iop.add_argument('--keyframe-tag', dest='keyframe_tag', type=str,
        #         default='Keyframe', help=args_help.keyframe_tag)
        # parser_iop.add_argument('--interpolation', dest='interp_method',
        #         type=str, default='quadratic', help=args_help.interpolation)
        # parser_iop.add_argument('--smooth', default=False, action='store_true',
        #         help=args_help.smooth)
        # parser_iop.add_argument('--window', type=int, help=args_help.window)
        # parser_iop.add_argument('--order', type=int, default=3,
        #         help=args_help.order)

    # args = parser.parse_args()

if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
