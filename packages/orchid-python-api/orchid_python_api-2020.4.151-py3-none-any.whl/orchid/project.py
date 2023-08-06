#  Copyright 2017-2020 Reveal Energy Services, Inc 
#
#  Licensed under the Apache License, Version 2.0 (the "License"); 
#  you may not use this file except in compliance with the License. 
#  You may obtain a copy of the License at 
#
#      http://www.apache.org/licenses/LICENSE-2.0 
#
#  Unless required by applicable law or agreed to in writing, software 
#  distributed under the License is distributed on an "AS IS" BASIS, 
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
#  See the License for the specific language governing permissions and 
#  limitations under the License. 
#
# This file is part of Orchid and related technologies.
#

from typing import List, Tuple, Iterable

import deal
import toolz.curried as toolz

import orchid.dot_net_dom_access as dna
from orchid.native_well_adapter import NativeWellAdapter
from orchid.project_loader import ProjectLoader
from orchid.project_monitor_pressure_curves import ProjectMonitorPressureCurves
import orchid.project_units as project_units
from orchid.project_wells import ProjectWells

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IWell
# noinspection PyUnresolvedReferences
import UnitsNet


class Project(dna.DotNetAdapter):
    """Adapts a .NET `IProject` to a Pythonic interface."""

    @deal.pre(lambda self, project_loader: project_loader is not None)
    def __init__(self, project_loader: ProjectLoader):
        """
        Construct an instance adapting he project available from net_project.

        :param project_loader: Loads an IProject to be adapted.
        """
        super().__init__(project_loader.native_project())
        self._project_loader = project_loader
        self._are_well_loaded = False
        self._wells = []

    name = dna.dom_property('name', 'The name of this project.')
    wells = dna.transformed_dom_property_iterator('wells', 'An iterator of all the wells in this project.',
                                                  NativeWellAdapter)

    def all_wells(self):
        """
        Return an object managing all wells from this project.

        :return: The object managing all wells for this project.
        """
        result = ProjectWells(self._project_loader)
        return result

    def default_well_colors(self) -> List[Tuple[float, float, float]]:
        """
        Calculate the default well colors for this project.
        :return: A list of RGB tuples.
        """
        result = list(map(tuple, self._project_loader.native_project().PlottingSettings.GetDefaultWellColors()))
        return result

    def monitor_pressure_curves(self):
        """
        Return a container of pressure curves indexed by time series id.
        :return: The container of pressure curves.
        """
        result = ProjectMonitorPressureCurves(self._project_loader)
        return result

    def unit(self, physical_quantity):
        """
        Return the abbreviation for the specified `physical_quantity` of this project.
        :param physical_quantity: The name of the physical quantity.
        :return: The abbreviation of the specified physical quantity.
        """
        return project_units.unit(self._project_loader.native_project(), physical_quantity)

    def wells_by_name(self, name) -> Iterable[IWell]:
        """
        Return all the wells in this project with the specified name.
        :param name: The name of the well(s) of interest.
        :return: A list of all the wells in this project.
        """
        return toolz.filter(lambda w: name == w.name, self.wells)
