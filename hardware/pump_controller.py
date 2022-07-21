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
from hardware.device import Device


class PumpController(Device):
    pass


class ISCOPumpController(PumpController):
    def _calculate_checksum(self, *args):
        s = self._sum_frame(*args)
        cs = 256 - s % 256
        return f'{cs:X}'

    def _sum_frame(self, *args):
        return sum([ord(a) for a in args])

    def get(self):
        frame = self.make_frame('G')
        self._communicator.ask(frame)

    def parse_frame(self, frame):
        frame = frame.strip()

        destination = frame[:1]
        acknowledgement = frame[1:2]
        message_source = frame[3:5]
        length = int(frame[5:7], 16)
        message = frame[7:7 + length]
        checksum = int(frame[-2:], 16)

        s = self._sum_message(destination, acknowledgement, message_source, length, message)
        if (s + checksum) % 256:
            self.debug(f'invalid frame checksum failed s={s}, checksum={checksum}')
        else:
            return message

    def make_frame(self, message):
        """{destination}{acknowledgement}{message source}{length}{message}{checksum}[CR]"""
        destination = '1'
        acknowledgement = 'R'
        messagesource = ' '
        length = len(message)

        checksum = self._calculate_checksum(destination, acknowledgement, messagesource, length, message)
        # f'{destination:X}{acknowledgement:X}{messagesource:X}{length:X}{message:X}{checksum:X}\r'
        return f'{destination}{acknowledgement}{messagesource}{length:X}{message}{checksum:X}\r'
# ============= EOF =============================================
