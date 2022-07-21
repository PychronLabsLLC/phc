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
from random import random

from hardware.device import Device, StreamableDevice


class HeiseST2H(StreamableDevice):
    def read_stream(self):
        l, r = self.read()
        return [{'name': 'left', 'value': l},
                {'name': 'right', 'value': r}]

    def read(self):
        resp = self.ask('?')
        if resp:
            resp = resp[1:]
            left, right = resp.split(',')
        elif self.simulation:
            left, right = random(), random()

        return float(left), float(right)

    def zero(self, left=False, right=False):
        self.ask(f'ZERO_{int(left)},_{int(right)}')

# ============= EOF =============================================
