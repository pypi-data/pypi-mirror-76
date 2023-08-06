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

parser = \
'''
Interpolate and optionally smooth parameters for darktable modules based on
keyframes.
'''

subparsers = \
'''
Available operations to apply smoothing on. Refer to the documentation on how
to add more.
'''

dry_run = \
'''
Do not modify XMP files.
'''

no_backup = \
'''
By default all XMP files will be copied to a new file with the suffix "*.bkp".
Use this flag to disable this behaviour.
'''

plot = \
'''
Plot a graph for fine tuning parameters. XMPs will not be modified.
'''

xmps = \
'''
XMP files. Mandatory.
'''

keyframes = \
'''
A list of XMP files which serve as keyframes. If this is used, keyframe tags
will be ignored, even if specified with the --keyframe-tag switch.
'''

keyframe_tag = \
'''
Tag used for selecting Keyframes. Default: "Keyframe".
'''

interpolation = \
'''
Interpolation method. One of linear, nearest, zero, slinear, quadratic, cubic,
previous, next. See scipy.interpolate.interp1d documentation for details.
Default: quadratic.
'''

window = \
'''
Window size for the smoothing filter. Must be odd. Default: length of input
values. Greater values result in more smoothing.
'''

order = \
'''
The order of the polynom for the filter function. Smaller values result in more
smoothing. Default value: 3.
'''

smooth = \
'''
Use a Savitzky-Golay filter to smooth the data points. Use --window and --order
to fine tune the result.
'''
