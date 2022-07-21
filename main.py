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
from datetime import datetime
import glob
import logging
import os
import shutil
from logging.handlers import RotatingFileHandler
import yaml
from chaco.array_plot_data import ArrayPlotData
# from chaco.base_plot_container import BasePlotContainer
from chaco.plot import Plot
from chaco.plot_containers import GridPlotContainer, HPlotContainer, VPlotContainer
from chaco.plots.lineplot import LinePlot
from enable.api import ComponentEditor
from enable.container import Container
from traitsui.api import View, UItem, VGroup, HGroup
from traits.api import Instance, Any, Dict, Button

import paths
from hardware.device import StreamableDevice
from hardware.pump_controller import PumpController
from loggable import Loggable

from hardware import HARDWARE
from script import Script
from state import StateController


class GraphArea(Loggable):
    component = Instance(Container)
    plot = Instance(Plot)

    def add_dev_plot(self, dev):
        comp = self.component

        kw, xname, ynames = dev.make_plotnames()
        plot = Plot(data=ArrayPlotData(**kw), title=dev.name, padding=60, border_visible=True)
        for yi in ynames:
            plot.plot((xname, yi))

        plot.x_axis.title = 'Time (s)'
        plot.y_axis.title = dev.get_configuration('graph.yaxis.title.text')
        comp.add(plot)
        dev.plot = plot

    def _component_default(self):
        return VPlotContainer()

    def traits_view(self):
        return View(UItem('component', editor=ComponentEditor(size=(500, 500))))


class Application(Loggable):
    _initialization = None
    _devices = Dict
    graph_area = Instance(GraphArea, ())

    start_all_button = Button
    stop_all_button = Button
    do_script_button = Button
    state_controller = Instance(StateController, ())

    def initialize(self):
        """
        open the initialization.yaml file
        load each component
        :return:
        """
        self.state_controller.run()

        with open(paths.INITIALIZATION, 'r') as wfile:
            init = yaml.load(wfile, Loader=yaml.SafeLoader)
            devs = init.get('devices')
            if not devs:
                self.debug('no devices')
            else:
                for device_config in init.get('devices', []):
                    self.debug('loading device {}'.format(device_config))
                    if device_config.get('enabled', True):
                        dev = self.create_device(device_config)
                        if dev:
                            self.register_device(dev)

    def create_device(self, cfg):
        kind = cfg.get('kind')
        klass = HARDWARE.get(kind)
        dev = klass(name=cfg.get('name'),
                    configuration=cfg)
        dev.bootstrap()
        return dev

    def get_device(self, name):
        dev = self._devices.get(name)
        return dev

    def register_device(self, dev):
        # add device to registry
        self._devices[dev.name] = dev
        # add plot to graph_area
        if isinstance(dev, StreamableDevice):
            self.graph_area.add_dev_plot(dev)

        self._register_device_hook(dev)

    def _register_device_hook(self, dev):
        pass

    def _do_script_button_fired(self):
        s = Script(name='demo',
                   devices=self._devices)
        s.application = self
        s.execute()

    def _start_all_button_fired(self):
        for d in self._devices.values():
            if isinstance(d, StreamableDevice):
                d.start_stream()

    def _stop_all_button_fired(self):
        for d in self._devices.values():
            if isinstance(d, StreamableDevice):
                d.stop_stream()


def setup_paths():
    if not os.path.isdir(paths.LOGS):
        os.mkdir(paths.LOGS)


def setup_logging():
    root = logging.getLogger()

    root.setLevel(logging.DEBUG)
    shandler = logging.StreamHandler()

    logname = "pfm.log"
    logpath = os.path.join(paths.LOGS, logname)

    if os.path.isfile(logpath):
        # move all log files their own directory
        # name directory based on logpath create date
        result = os.stat(logpath)
        mt = result.st_mtime
        creation_date = datetime.fromtimestamp(mt)

        bk = os.path.join(paths.LOGS, creation_date.strftime("%y%m%d%H%M%S"))
        os.mkdir(bk)
        for src in glob.glob(os.path.join(paths.LOGS, "{}*".format(logname))):
            shutil.move(src, bk)

    handlers = [shandler]
    rhandler = RotatingFileHandler(logpath, maxBytes=1e8, backupCount=50)
    handlers.append(rhandler)

    fmt = logging.Formatter("%(name)-40s: %(asctime)s %(levelname)-9s (%(threadName)-10s) %(message)s")
    for hi in handlers:
        hi.setLevel(logging.DEBUG)
        hi.setFormatter(fmt)
        root.addHandler(hi)


def launch(app):
    setup_paths()

    setup_logging()

    app.initialize()
    app.configure_traits()


# if __name__ == '__main__':
#     launch()
# ============= EOF =============================================
