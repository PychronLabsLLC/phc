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
import time
from threading import Thread
from traits.api import Float, List

import paths
from loggable import Loggable
from paths import unique_path


class DevicePoller(Loggable):
    poll_period = Float(10)
    devices = List
    _active_path = None

    _alive = False
    _starttime = 0
    _poll_thread = None

    def register_device(self, dev):
        self.devices.append(dev)

    def run(self):
        self._alive = True
        self._active_path = None
        self._starttime = time.time()
        self._poll_thread = Thread(target=self._run)
        self._poll_thread.setDaemon(True)
        self._poll_thread.start()

    def stop(self):
        self._alive = False

    def _run(self):
        while self._alive:
            t = time.time()
            rt = t-self._starttime
            values = []
            labels = []
            for dev in self.devices:
                _, stream = dev.poll_stream()
                if isinstance(stream, list):
                    keys = sorted([s['name'] for s in stream])
                    vs = [next((s for s in stream if s['name']==k), None)['value'] for k in keys]
                    values.extend(vs)
                    labels.extend([f'{dev.name}.{k}' for k in keys])
                else:
                    values.append(stream)
                    labels.append(dev.name)

            self.write_record(t, rt, labels, values)
            time.sleep(self.poll_period)

    def write_record(self, t, rt, labels, values):
        self.debug('write record', t, rt, labels, values)
        if not self._active_path:
            self._active_path, _ = unique_path(paths.DEVICE_POLL, 'device_poll')

            with open(self._active_path, 'w') as wfile:
                row = ','.join(labels)
                wfile.write(f'timestamp,relative_time,{row}\n')

        with open(self._active_path, 'a') as wfile:
            row = ','.join((str(v) for v in values))
            wfile.write(f'{t},{rt},{row}\n')
# ============= EOF =============================================
