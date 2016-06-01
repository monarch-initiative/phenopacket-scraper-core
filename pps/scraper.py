import logging
import sys
import requests
from cliff.command import Command
from bs4 import BeautifulSoup

class Scraper(Command):

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Scraper, self).get_parser(prog_name)
        parser.add_argument('-u', '--url', type=str)
        return parser

    def take_action(self, parsed_args):
        argx = sys.argv[1:]
        self.log.info('testing')
        self.log.debug('debugging')
        option = parsed_args.url
        self.app.stdout.info('Arguments: '+str(argx)+'\n')
        self.app.stdout.info(str(option)+'\n')


        # self.app.stdout.write(str(self.parsed_args))



class Error(Command):

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('causing error')
        raise RuntimeError('this is the expected exception')
