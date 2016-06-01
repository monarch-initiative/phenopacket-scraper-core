import sys
import argparse


from cliff.app import App
from cliff.commandmanager import CommandManager


class Phenopacketscraper(App):

    def __init__(self):
        super(Phenopacketscraper, self).__init__(
            description='Phenopacket Scraping Tool',
            version='0.1',
            command_manager=CommandManager('pps_commands'),
            deferred_help=True,
            )

    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')


    def build_option_parser(self, description, version,
                            argparse_kwargs=None):

        argparse_kwargs = argparse_kwargs or {}
        parser = argparse.ArgumentParser(
            description=description,
            add_help=False,
            **argparse_kwargs
        )
        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s {0}'.format(version),
        )
        parser.add_argument(
            '-v', '--verbose',
            action='count',
            dest='verbose_level',
            default=self.DEFAULT_VERBOSE_LEVEL,
            help='Increase verbosity of output. Can be repeated.',
        )
        parser.add_argument(
            '--log-file',
            action='store',
            default=None,
            help='Specify a file to log output. Disabled by default.',
        )
        parser.add_argument(
            '-q', '--quiet',
            action='store_const',
            dest='verbose_level',
            const=0,
            help='suppress output except warnings and errors',
        )
        if self.deferred_help:
            parser.add_argument(
                '-h', '--help',
                dest='deferred_help',
                action='store_true',
                help="show this help message and exit",
            )
        else:
            parser.add_argument(
                '-h', '--help',
                action=HelpAction,
                nargs=0,
                default=self,  # tricky
                help="show this help message and exit",
            )
        parser.add_argument(
            '--debug',
            default=False,
            action='store_true',
            help='show tracebacks on errors',
        )


        return parser



    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    myapp = Phenopacketscraper()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
