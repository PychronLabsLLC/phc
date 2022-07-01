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
from traits.api import Float

from hardware.device import StreamableDevice


class Motor(StreamableDevice):
    def set_position(self, pos, block=True):
        self.ask(f"MoveTo {pos}")
        self._software_position = pos
        if block:
            self.block()

    def block(self, threshold=3):
        cnt = 0
        while 1:
            if not self._moving():
                cnt += 1
                if cnt > threshold:
                    break
            else:
                cnt = 0

    def get_hardware_position(self):
        return self.ask(f"GetPosition")

    def get_software_position(self):
        return self._software_position

    def _moving(self):
        return False


class LinearDriver(Motor):
    min_value = Float(0)
    max_value = Float(1)

    min_index = Float(0)
    max_index = Float(1)

    def get_hardware_position(self):
        r = super(LinearDriver, self).get_hardware_position()
        return (r - self.min_value) / (
            self.max_value - self.min_value
        ) * self.max_index + self.min_index


if __name__ == "__main__":
    l = LinearDriver()
    print(l.get_hardware_position())
# ============= EOF =============================================
