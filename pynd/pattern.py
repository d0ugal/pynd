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
