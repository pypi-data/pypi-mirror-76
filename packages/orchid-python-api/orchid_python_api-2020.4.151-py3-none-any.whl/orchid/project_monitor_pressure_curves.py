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

from typing import Sequence

import deal
import pandas as pd

from orchid.project_loader import ProjectLoader
from orchid.time_series import transform_net_time_series
import orchid.validation

# noinspection PyUnresolvedReferences
import UnitsNet


class ProjectMonitorPressureCurves:
    """
    A container for .NET Wells indexed by time series IDs.
    """

    @deal.pre(orchid.validation.arg_not_none)
    def __init__(self, net_project: ProjectLoader):
        """
        Construct an instance wrapping the native .NET `IProject`.

        :param net_project: The `IProject` being wrapped.
        """
        self._project_loader = net_project

        self._monitor_pressure_curves = {}

    def _monitor_pressure_curve_map(self):
        if not self._monitor_pressure_curves:
            self._monitor_pressure_curves.update({c.DisplayName: c for
                                                  c in self._project_loader.native_project().WellTimeSeriesList.Items if
                                                  c.SampledQuantityType == UnitsNet.QuantityType.Pressure})
        return self._monitor_pressure_curves

    def monitor_pressure_curve_ids(self) -> Sequence[str]:
        """
        Return the pressure curve identifiers for all pressure curves.
        :return: A list of all pressure curve identifiers.
        """

        return list(self._monitor_pressure_curve_map().keys())

    @deal.pre(orchid.validation.arg_not_none)
    @deal.pre(orchid.validation.arg_neither_empty_nor_all_whitespace)
    def monitor_pressure_curve_time_series(self, curve_id: str) -> pd.Series:
        """
        Return a pandas time series containing the samples for the pressure curve identified by `curve_id`.

        :param curve_id: Identifies a specific pressure curve in the project.

        :return: A sequence of sample pressures (implicitly in the project pressure units)."""
        curve = self._monitor_pressure_curve_map()[curve_id]

        # TODO: Premature optimization?
        # The following code uses a technique from a StackOverflow post on creating a pandas `Series` from a
        # sequence of Python tuples. All the code is less clear, it avoids looping over a relatively "large"
        # array (> 100k items) multiple time.
        # https://stackoverflow.com/questions/53363688/converting-a-list-of-tuples-to-a-pandas-series
        result = transform_net_time_series(curve.GetOrderedTimeSeriesHistory())
        return result

    @deal.pre(orchid.validation.arg_not_none)
    @deal.pre(orchid.validation.arg_neither_empty_nor_all_whitespace)
    def display_name(self, curve_id: str) -> str:
        """
        Return the name used to recognize the pressure curve identified by curve_id.

        :param curve_id: The value used to identify a specific pressure curve.
        :return: The name used by engineers to describe this curve.
        """
        return self._monitor_pressure_curve_map()[curve_id].DisplayName
