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
        self.log.info('Development')
        self.log.debug('debugging')
 
        url = parsed_args.url
        fname = parsed_args.filename

        self.log.info('Arguments: '+ str(args) + '\n')


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
            count=1

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



server_url = 'https://scigraph-ontology-dev.monarchinitiative.org/scigraph'



class Annotate(Command):

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Annotate, self).get_parser(prog_name)
        parser.add_argument('-u', '--url', type=str)
        parser.add_argument('-f', '--filename', type=str)
        parser.add_argument('-o', '--output', type=str)
        return parser


    def take_action(self, parsed_args):
        args = sys.argv[1:]
        
        self.log.info('Annotation Development')
        self.log.debug('debugging [Annotation]')
 
        url = parsed_args.url

        self.log.info('Arguments: '+ str(args) + '\n')

        if url:

            req_ob = requests.get(str(url).strip())
            
            gaussian = BeautifulSoup(req_ob.content, "html.parser")
            
            try:        
                abstract = gaussian.find_all("p", {"id" : "p-2"})[0]
                abs_text = abstract.text.encode('ascii','ignore')
                data = {'content' : str(abs_text)}

                response = requests.get(server_url + '/annotations/entities', params = data)

                if response.status_code == 200:
                    annotated_data = response.json()
                    self.app.stdout.write(str(annotated_data))
                    hpo_terms = []

                    if parsed_args.output:
                        fopen = open(str(parsed_args.output) + '_annotated_data.txt', 'w')
                        fopen.write(str(annotated_data) + '\n')

                        fopen.close()

                    for ob in annotated_data:
                        token = ob['token']
                        if 'Phenotype' in token['categories']:
                            term = str(token['terms'][0])
                            if term not in hpo_terms:
                                hpo_terms.append(token['terms'][0])

                    self.app.stdout.write('\n HPO Terms:\n')
                    for term in hpo_terms:
                        self.app.stdout.write(str(term) + '\n')

                    if parsed_args.output:
                        fopen = open(str(parsed_args.output) + '_hpo_terms.txt', 'w' )
                        fopen.write('HPO Terms:\n')
                        for term in hpo_terms:
                            fopen.write(str(term) + '\n')

                        fopen.close()

                else:
                    self.app.stdout.write(str(response.status_code))


            except:
                self.app.stdout.write("Abstract Not found\n")








class Error(Command):

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('causing error')
        raise RuntimeError('this is the expected exception')
