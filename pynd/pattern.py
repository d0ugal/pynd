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


class Compare(object):

    def __init__(self, pattern, flags):
        self.pat = re.compile(pattern, flags=flags)
        LOG.debug("Regular expression %r", self.pat)
        self.pattern = pattern
        self.count = 0

    def __call__(self, value):
        try:
            self.count += 1
            return self.pat.search(value)
        except Exception:
            LOG.exception("Failed to match the pattern %r to the value %r",
                          self.pattern, value)
            return False

    def __repr__(self):
        return repr(self.pat)


def compile(pattern, flags=0):
    return Compare(pattern, flags)


def matchers(args):

    patterns = []

    if args.private:
        patterns.append(compile(args.private))

    if args.public:
        patterns.append(compile(args.public))

    flags = 0
    if args.ignore_case:
        LOG.debug("Lowercase flag added to regular expression")
        flags = re.IGNORECASE
    patterns.append(compile(args.pattern, flags))

    return patterns
