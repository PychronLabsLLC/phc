# ===============================================================================
# Copyright 2022 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
import glob
import os.path

HOME = os.path.join(os.path.expanduser('~'), 'phc')
INITIALIZATION = os.path.join(HOME, 'initialization.yaml')
LOGS = os.path.join(HOME, 'logs')
SCRIPTS = os.path.join(HOME, 'scripts')
DEVICES = os.path.join(HOME, 'devices')
DATA_DIR = os.path.join(HOME, 'data')

if not os.path.isdir(DATA_DIR):
    os.mkdir(DATA_DIR)

DEVICE_POLL = os.path.join(DATA_DIR, 'device_poll')
if not os.path.isdir(DEVICE_POLL):
    os.mkdir(DEVICE_POLL)


def max_path_cnt(root, base, delimiter="-", extension=".txt", ndigits=5):
    """

    :param root:
    :param base:
    :param extension:
    :return: int max+1
    """

    ndigits = "[0-9]" * ndigits
    basename = "{}{}{}{}".format(base, delimiter, ndigits, extension)
    cnt = 0
    for p in glob.glob(os.path.join(root, basename)):
        p = os.path.basename(p)
        head, tail = os.path.splitext(p)

        cnt = max(int(head.split(delimiter)[-1]), cnt)
    cnt += 1
    return cnt


def unique_path(root, base, delimiter="-", extension=".txt", width=3):
    """
    unique_path suffers from the fact that it starts at 001.
    this is a problem for log files because the logs are periodically archived which means
    low paths are removed.

    unique_path2 solves this by finding the max path then incrementing by 1
    """
    if not extension.startswith("."):
        extension = ".{}".format(extension)

    cnt = max_path_cnt(
        root, base, delimiter=delimiter, extension=extension, ndigits=width
    )
    p = os.path.join(
        root, "{{}}-{{:0{}d}}{{}}".format(width).format(base, cnt, extension)
    )
    return p, cnt
# ============= EOF =============================================
