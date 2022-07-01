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
import os
import time
from threading import Thread, Event

import yaml
from pyface.timer.timer import Timer
from traits.api import Float, Int
from numpy import hstack

import paths
from hardware.communicator import SerialCommunicator
from loggable import Loggable
from strutil import streq


class Device(Loggable):
    _stream_thread = None

    def bootstrap(self):
        p = self._config_path
        if os.path.isfile(p):
            with open(p, "r") as rfile:
                cfg = yaml.load(rfile, Loader=yaml.SafeLoader)
                self._cfg = cfg
                self._load_communicator(cfg)
        else:
            self.warning(f"No config path. {p}")

    def get_configuration(self, cfgpath, default=""):
        obj = self._cfg
        for p in cfgpath.split("."):
            if obj:
                obj = obj.get(p)

        return obj or default

    def _load_communicator(self, cfg):
        comms = cfg.get("communications")
        if comms:
            kind = comms.get("kind", "serial")
            if streq(kind, "serial"):
                self._communicator = SerialCommunicator()
                self._communicator.init(comms)

    @property
    def _config_path(self):
        return os.path.join(paths.DEVICES, f"{self.name}.yaml")


class StreamableDevice(Device):
    period = Float(200)
    stream_window = Int(25)

    def start_stream(self):
        self._stream_start_time = time.time()
        self._stream_timer = Timer(self.period, self._stream)

    def stop_stream(self):
        if self._stream_timer:
            self._stream_timer.Stop()

    def _stream(self):
        stream = self.read_stream()

        xname = "{}.x".format(self.name)
        yname = "{}.y".format(self.name)
        xs = self.plot.data.get_data(xname)
        ys = self.plot.data.get_data(yname)

        xs = hstack(
            (xs[-self.stream_window :], [time.time() - self._stream_start_time])
        )
        ys = hstack((ys[-self.stream_window :], [stream]))
        self.plot.data.set_data(xname, xs)
        self.plot.data.set_data(yname, ys)

    def read_stream(self):
        raise NotImplementedError


# ============= EOF =============================================
