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

import unittest.mock

from hamcrest import assert_that, is_, equal_to, calling, raises, has_properties

import orchid.project_wells

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import (WellReferenceFrameXy, DepthDatum, IWell)


class TestNetWellId(unittest.TestCase):
    def test_canary(self):
        assert_that(2 + 2, is_(equal_to(4)))

    def test_well_id_is_uwi_if_net_well_has_uwi(self):
        stub_well = unittest.mock.MagicMock(name='mock_net_well', spec=IWell)
        stub_well.Name = None
        stub_well.DisplayName = None
        stub_well.Uwi = '49-240-45978-50-76'

        assert_that(orchid.project_wells.net_well_id(stub_well), is_(equal_to('49-240-45978-50-76')))

    def test_well_id_is_display_name_if_net_well_uwi_is_none(self):
        stub_well = unittest.mock.MagicMock(name='mock_net_well', spec=IWell)
        stub_well.Name = None
        stub_well.DisplayName = 'paries'
        stub_well.Uwi = None

        assert_that(orchid.project_wells.net_well_id(stub_well), is_(equal_to('paries')))

    def test_well_id_is_display_name_if_net_well_uwi_is_empty(self):
        stub_well = unittest.mock.MagicMock(name='mock_net_well', spec=IWell)
        stub_well.Name = None
        stub_well.DisplayName = 'paries'
        stub_well.Uwi = ''

        assert_that(orchid.project_wells.net_well_id(stub_well), is_(equal_to('paries')))

    def test_well_id_is_display_name_if_net_well_uwi_is_white_space(self):
        stub_well = unittest.mock.MagicMock(name='mock_net_well', spec=IWell)
        stub_well.Name = None
        stub_well.DisplayName = 'paries'
        stub_well.Uwi = '\n'

        assert_that(orchid.project_wells.net_well_id(stub_well), is_(equal_to('paries')))

    def test_well_id_is_name_if_net_well_display_name_is_none(self):
        stub_well = unittest.mock.MagicMock(name='mock_net_well', spec=IWell)
        stub_well.Name = 'cibus'
        stub_well.DisplayName = None
        stub_well.Uwi = None

        assert_that(orchid.project_wells.net_well_id(stub_well), is_(equal_to('cibus')))

    def test_well_id_is_name_if_net_well_display_name_is_empty(self):
        stub_well = unittest.mock.MagicMock(name='mock_net_well', spec=IWell)
        stub_well.Name = 'cibus'
        stub_well.DisplayName = ''
        stub_well.Uwi = None

        assert_that(orchid.project_wells.net_well_id(stub_well), is_(equal_to('cibus')))

    def test_well_id_is_name_if_net_well_display_name_is_white_space(self):
        stub_well = unittest.mock.MagicMock(name='mock_net_well', spec=IWell)
        stub_well.Name = 'cibus'
        stub_well.DisplayName = '\f'
        stub_well.Uwi = None

        assert_that(orchid.project_wells.net_well_id(stub_well), is_(equal_to('cibus')))

    def test_well_id_raises_exception_if_all_candidates_none(self):
        stub_well = unittest.mock.MagicMock(name='mock_net_well', spec=IWell)
        stub_well.Name = None
        stub_well.DisplayName = None
        stub_well.Uwi = None

        assert_that(calling(orchid.project_wells.net_well_id).with_args(stub_well),
                    raises(ValueError, matching=has_properties(args=('No well ID available.',))))

    def test_well_id_raises_exception_if_well_name_empty(self):
        stub_well = unittest.mock.MagicMock(name='mock_net_well', spec=IWell)
        stub_well.Name = ''
        stub_well.DisplayName = None
        stub_well.Uwi = None

        assert_that(calling(orchid.project_wells.net_well_id).with_args(stub_well),
                    raises(ValueError, matching=has_properties(args=('No well ID available.',))))

    def test_well_id_raises_exception_if_well_name_white_space(self):
        stub_well = unittest.mock.MagicMock(name='mock_net_well', spec=IWell)
        stub_well.Name = '  '
        stub_well.DisplayName = None
        stub_well.Uwi = None

        assert_that(calling(orchid.project_wells.net_well_id).with_args(stub_well),
                    raises(ValueError, matching=has_properties(args=('No well ID available.',))))


if __name__ == '__main__':
    unittest.main()
