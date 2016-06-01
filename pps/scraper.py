# encoding=utf8

import logging
import sys
import requests
from cliff.command import Command
from bs4 import BeautifulSoup
from html2text import html2text as gauss



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
        option = str(parsed_args.url)
        self.log.info('Arguments: '+str(argx)+'\n')
        self.log.info(option+'\n')
        r_ob = requests.get(option)
        gaussian = BeautifulSoup(r_ob.content, "html.parser")
        abstract = gaussian.find_all("p", {"id": "p-2"})[0]
        self.app.stdout.write(str(abstract)+'\n\n\n\n\n\n')
        abs_text = abstract.text.encode('ascii','ignore')
        self.app.stdout.write(abs_text)
        # self.app.stdout.write(str(abstract.text).encode('ascii','ignore')+'\n\n\n\n\n\n')

        # self.app.stdout.write()

        # self.app.stdout.write(str(abstract.text)+'\n')
        # self.app.stdout.write(str( gauss(   str(abstract.decode('utf-8'))   )) )
        self.app.stdout.write(str( gauss(   str(abstract.text.decode('utf-8'))   )) )





class Error(Command):

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('causing error')
        raise RuntimeError('this is the expected exception')
