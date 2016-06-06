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
        parser.add_argument('-f', '--filename', type=str)
        parser.add_argument('-o', '--output', type=str)
        return parser

    def take_action(self, parsed_args):
        args = sys.argv[1:]
        self.log.info('testing')
        self.log.debug('debugging')
 
        url = parsed_args.url
        fname = parsed_args.filename

        self.log.info('Arguments: '+ str(args) + '\n')

        self.log.info( str(fname) + '\n')       
# Implementation of taking a URL as input

        if url:

            req_ob = requests.get(str(url).strip())
            
            gaussian = BeautifulSoup(req_ob.content, "html.parser")
            
            try:
                title = gaussian.find_all("title")[0]
                self.app.stdout.write("Title: " + str(title.text.decode('utf-8')) + "\n\n")
            except:
                pass
            
            try:        
                abstract = gaussian.find_all("p", {"id" : "p-2"})[0]
                abs_text = abstract.text.encode('ascii','ignore')
                self.app.stdout.write("Abstract:\n")
                # self.app.stdout.write(abs_text)
                self.app.stdout.write(abs_text.decode('utf-8'))
                self.app.stdout.write('\n')

                if parsed_args.output:
                    fopen = open(str(parsed_args.output) + '_abstract.txt', 'w')
                    fopen.write(abs_text + '\n')
                    fopen.close()

            except:
                self.app.stdout.write("Abstract Not found\n")


            hpo_obs = gaussian.find_all("a", {"class": "kwd-search"})

            if hpo_obs:
                # self.app.stdout.write(str(hpo_obs)+'\n\n')
                self.app.stdout.write('HPO Terms:\n')
                for ob in hpo_obs:
                    self.app.stdout.write(ob.text + '\n')
                    # self.app.stdout.write('\n')

                if parsed_args.output:
                    fopen = open(str(parsed_args.output) + '_hpo_terms.txt', 'w')
                    for ob in hpo_obs:
                        fopen.write(ob.text + '\n')

                    fopen.close()
            else:
                self.app.stdout.write("HPO Terms Not found")


# Implementation of taking Input from files

        if fname:
            fname = str(fname).strip()
            file_open = open(fname , 'r')
            rline = file_open.readline()
            count=0

            while rline:
                url = str(rline).strip()
                req_ob = requests.get(url)
                gaussian = BeautifulSoup(req_ob.content, "html.parser")
                 
                try:
                    title = gaussian.find_all("title")[0]
                    self.app.stdout.write("\nTitle: " + str(title.text.decode('utf-8')) + "\n\n")
                except:
                    pass
                
                try:        
                    abstract = gaussian.find_all("p", {"id" : "p-2"})[0]
                    abs_text = abstract.text.encode('ascii','ignore')
                    self.app.stdout.write("Abstract:\n")
                    # self.app.stdout.write(abs_text)
                    self.app.stdout.write(abs_text.decode('utf-8'))
                    self.app.stdout.write('\n')

                    if parsed_args.output:
                        fopen = open(str(count) + "_" + str(parsed_args.output) + '_abstract.txt', 'w')
                        fopen.write(abs_text + '\n')
                        fopen.close()

                except:
                    self.app.stdout.write("Abstract Not found\n")


                hpo_obs = gaussian.find_all("a", {"class": "kwd-search"})

                if hpo_obs:
                    # self.app.stdout.write(str(hpo_obs)+'\n\n')
                    self.app.stdout.write('HPO Terms:\n')
                    for ob in hpo_obs:
                        self.app.stdout.write(ob.text + '\n')
                        # self.app.stdout.write('\n')

                    if parsed_args.output:
                        fopen = open(str(count) + "_" + str(parsed_args.output) + '_hpo_terms.txt', 'w')
                        for ob in hpo_obs:
                            fopen.write(ob.text + '\n')

                        fopen.close()
                else:
                    self.app.stdout.write("HPO Terms Not found")

                count+=1
                rline = file_open.readline()

            file_open.close()




class Error(Command):

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('causing error')
        raise RuntimeError('this is the expected exception')
