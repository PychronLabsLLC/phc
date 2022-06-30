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
# from threading import Thread
import pyface
from pyface.qt.QtCore import QThread

import paths
from loggable import Loggable
from traits.api import Dict

class StreamThread(QThread):
    def __init__(self, func, *args, **kw):
        super(StreamThread, self).__init__(*args, **kw)
        self._func = func

    def run(self):
        self._func()


def invoke_in_main_thread(fn, *args, **kw):
    from pyface.gui import GUI

    GUI.invoke_later(fn, *args, **kw)


class Script(Loggable):
    _text = None
    _estimated_duration = 0
    devices = Dict

    # commands
    def get_device(self, devname):
        return self.devices.get(devname)

    def stream_device(self, devname, start_stop_stream):
        dev = self.get_device(devname)
        if dev:
            if start_stop_stream:
                invoke_in_main_thread(dev.start_stream)
            else:
                invoke_in_main_thread(dev.stop_stream)

    def sleep(self, seconds):
        time.sleep(seconds)

    def execute(self):
        self._thread = StreamThread(self._execute)
        self._thread.start()

    def _get_context(self):
        ctx = {'info': self.info,
               'get_device': self.get_device,
               'stream_device': self.stream_device,
               'sleep': self.sleep}
        return ctx

    def _execute(self):
        p = os.path.join(paths.SCRIPTS, f'{self.name}.py')
        with open(p, 'r') as rfile:
            self._text = rfile.read()
        self._execute_snippet(self._text)

    def _execute_snippet(self, snippet, argv=None):
        safe_dict = self._get_context()
        try:
            code = compile(snippet, "<string>", "exec")
        except BaseException as e:
            self.debug_exception()
            return
        # print(safe_dict), code
        try:
            exec(code, safe_dict)
            func = safe_dict["main"]
        except KeyError as e:
            exc = self.debug_exception()
            return
            # self.exception_trace = exc
            # return MainError()

        try:
            if argv is None:
                argv = tuple()

            st = time.time()
            func(*argv)
            self.debug(
                "executed snippet estimated_duration={}, duration={}".format(
                    self._estimated_duration, time.time() - st
                )
            )
        except Exception as e:
            exc = self.debug_exception()
# ============= EOF =============================================
