import logging
import sys

from . import cli
from . import search


def main(sysargs=None):

    sysargs = sys.argv[1:] if sysargs is None else sysargs
    args = cli.parse_args(sysargs)
    cli.setup_logging(args)

    LOG = logging.getLogger(__name__)
    LOG.debug("Started with args: %r", args)

    if len(sysargs) == 0:
        parser = cli.create_parser()
        parser.print_help()
        return 1

    try:
        search.search(args)
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    sys.exit(main())
