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

import logging
import re

LOG = logging.getLogger()


def compile(pattern, flags=0):
    pat = re.compile(pattern, flags=flags)
    LOG.debug("Regular expression %r", pat)
    return pat.search


def matcher(args):
    flags = 0
    if args.ignore_case:
        LOG.debug("Lowercase flag added to regular expression")
        flags = re.IGNORECASE
    return compile(args.pattern, flags)
