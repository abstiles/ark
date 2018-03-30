#!/usr/bin/env python

import sys
import argparse
import logging
import traceback

DEFAULT_LOG_LEVEL = logging.WARNING


class Context(object):
    def __init__(self, options_dict):
        self.verbosity = (options_dict.pop('verbose') -
                          options_dict.pop('quiet'))
        self.__dict__.update(options_dict)

    @staticmethod
    def argument_parser(prog=None):
        parser = argparse.ArgumentParser(
            prog=prog,
            description='A simple template for a Python script')
        parser.add_argument('--verbose', '-v', action='count', default=0)
        parser.add_argument('--quiet', '-q', action='count', default=0)

        return parser

    @classmethod
    def from_args(cls, cli_args, prog=None):
        parser = cls.argument_parser(prog=prog)
        parsed_options = parser.parse_args(cli_args)
        return cls(vars(parsed_options))

    def setup_logging(self):
        log_level = DEFAULT_LOG_LEVEL - (self.verbosity * 10)
        logging.basicConfig(format='%(message)s', level=log_level)

    def run(self):
        self.setup_logging()
        _execute()


class ScriptError(StandardError):
    """Base exception for all exceptions raised by this script."""

    message_template = '{}'
    code = 64

    def __init__(self, *args, **kwargs):
        message = self.message_template.format(*args, **kwargs)
        super(ScriptError, self).__init__(message)


def _main(prog, *args):
    context = Context.from_args(args, prog=prog)
    try:
        return context.run()
    except ScriptError as err:
        logging.error(str(err))
        return err.code
    except KeyboardInterrupt:
        return 130  # Bash convention for exiting due to SIGINT
    except Exception as err:  # pylint: disable=broad-except
        # Using a broad except clause to handle the logging more nicely.
        logging.debug(traceback.format_exc())
        logging.error('Unexpected error ({type}): {message}'.format(
            type=err.__class__.__name__, message=str(err)))
        return 1


def _execute(**kwargs):
    _ = kwargs  # TODO: main program execution logic here.


if __name__ == '__main__':
    sys.exit(_main(*sys.argv))
