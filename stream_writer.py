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
from loggable import Loggable


class StreamWriter(Loggable):
    def register_device(self, dev):
        dev.observe(self._handle_stream, "stream_event")

    def _handle_stream(self, event):
        self.debug('handle stream event', event)
# ============= EOF =============================================
