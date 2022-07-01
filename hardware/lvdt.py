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
import math
import time
from random import random
from traits.api import Float
from hardware.device import Device, StreamableDevice
from loggable import Loggable


class LVDT(StreamableDevice):
    pass


class MTH100(LVDT):
    def read_stream(self):
        if not self._simulation:
            v = self._communicator.ask()
        else:
            t = time.time() - self._stream_start_time
            v = self._cfg.get('amplitude', 1) * math.sin(self._cfg.get('frequency', 1) * t)

        return v

# ============= EOF =============================================
