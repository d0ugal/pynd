#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import mock

from pynd import __main__
from pynd import cli


def test_main():
    with mock.patch("pynd.search.search") as mocked_search:
        __main__.main(['.'])
    mocked_search.assert_called_once_with(cli.parse_args(['.']))


def test_main_no_args():
    """Should display the help only and exist. Not starting a search."""
    with mock.patch("pynd.search.search") as mocked_search:
        __main__.main([])
    assert mocked_search.call_count == 0


def test_main_interrupt():
    with mock.patch("pynd.search.search", side_effect=KeyboardInterrupt()):
        __main__.main(['.'])
