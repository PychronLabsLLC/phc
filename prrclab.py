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
from hardware.pump_controller import PumpController
from main import Application, launch
from traits.api import Instance, Button
from traitsui.api import VGroup, HGroup, UItem, Item, View


class PRRCLab(Application):
    pump_controller = Instance(PumpController)

    loadcell_button = Button('Load Cell')
    unloadcell_button = Button('Unload Cell')

    def _loadcell_button_fired(self):
        self.debug('loading cell')

    def _unloadcell_button_fired(self):
        self.debug('unloading cell')

    def _register_device_hook(self, dev):
        if isinstance(dev, PumpController):
            self.pump_controller = dev

    def traits_view(self):
        scripts = VGroup(UItem('start_all_button'),
                         UItem('stop_all_button'),
                         UItem('do_script_button'),
                         show_border=True, label='Scripts')
        pumps = VGroup(UItem('pump_controller', style='custom'),
                       show_border=True, label='Pump')
        actions = VGroup(UItem('loadcell_button'),
                         UItem('unloadcell_button'),
                         show_border=True, label='Actions')
        controls = VGroup(scripts, pumps, actions)
        graph = VGroup(UItem('graph_area', style='custom'), )
        grp = HGroup(controls, graph)
        v = View(grp,
                 resizable=True,
                 title='PRRC Lab')
        return v


if __name__ == '__main__':
    launch(PRRCLab())
# ============= EOF =============================================
