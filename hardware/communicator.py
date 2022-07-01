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
from serial import SerialException

from loggable import Loggable
import serial


class Communicator(Loggable):
    def init(self, cfg):
        pass


class SerialCommunicator(Communicator):
    _handle = None

    def init(self, cfg):
        self._report_cfg(cfg)
        try:
            self._handle = serial.Serial(
                port=cfg["port"], timeout=cfg.get("timeout", 1)
            )

            return True
        except SerialException:
            self.warning(f'no serial port: {cfg["port"]}')

    def _report_cfg(self, cfg):
        self.debug("#-------------------------------")
        for k, v in cfg.items():
            self.debug(f"{k}:   {v}")
        self.debug("#-------------------------------")

    def ask(self, msg):
        payload = msg
        self._handle.write(payload)
        resp = self._handle.readline()


# ============= EOF =============================================
