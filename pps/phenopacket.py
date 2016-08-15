# encoding=utf8

import logging
import sys
import requests
from cliff.command import Command
from bs4 import BeautifulSoup
from phenopacket.PhenoPacket import *
from phenopacket.models.Meta import *
import json


server_url = 'https://scigraph-ontology.monarchinitiative.org/scigraph'

def create_phenopacket(hpo_terms,url, title):
    phenotype_data = []
    print('Creating Phenopacket\n')
    for term in hpo_terms:
        data={'content' : str(term)}
        response = requests.get(server_url+ '/annotations/entities', params = data)
        if response.status_code == 200:
            annotated_data = response.json()
            for ob in annotated_data:
                token = ob['token']
                token_term = str(token['terms'][0])
                if str(token_term).lower() == str(term).lower():
                    term_id = token['id']                       #Taking The ID of the HPO term from Scigraph Annotator
                    if term_id not in [k[0] for k in phenotype_data]:
                        phenotype_data.append((term_id, term))
        else:
            print(str(response.status_code))

# Code to generate phenopacket below

    journal = Entity(
                    id = str(url),
                    type = EntityType.paper)
    print('\n0.5\n')
    phenopacket_entities = [journal]

    environment = Environment()
    severity = ConditionSeverity()
    onset = TemporalRegion()
    offset = TemporalRegion()

    evidence_type = OntologyClass(
                                class_id="ECO:0000501",
                                label="Evidence used in automatic assertion")

    evidence = Evidence(types= [evidence_type])

    phenotype_profile = []
    
    for element in phenotype_data:
        types_ob = OntologyClass(
                                class_id= element[0],
                                label= element[1])
        types=[types_ob]

        phenotype  =    Phenotype(
                            types= types,
                            environment=environment,
                            severity=severity,
                            onset=onset,
                            offset=offset)

        phenotype_association   = PhenotypeAssociation(
                                    entity = journal.id,
                                    evidence_list = [evidence],                                                    
                                    phenotype = phenotype)

        phenotype_profile.append(phenotype_association)

    phenopacket = PhenoPacket(
                        packet_id = "gauss-packet",
                        title = title,
                        entities = phenopacket_entities,
                        phenotype_profile = phenotype_profile)

    return phenopacket



class GenPhenoPacket(Command):

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """
         The list of available parameters 
         for `pps phenopacket` command.

        """
        parser = super(GenPhenoPacket, self).get_parser(prog_name)
        parser.add_argument('-u', '--url', type=str)
        parser.add_argument('-f', '--filename', type=str)
        parser.add_argument('-o', '--output', type=str)
        parser.add_argument('-d', '--doc', type=str)
        return parser


    def take_action(self, parsed_args):
        """
        Takes a url, scrapes the HPO Terms,
        annotates them using scigraph-annotator
        to extract HPO Term ids.

        Creates a phenopacket using phenopacket-
        python. 

        """
        args = sys.argv[1:] 
        self.log.info('Phenopacket Development')
        self.log.debug('debugging [GenPhenoPacket]')
        url = parsed_args.url
        doc = parsed_args.doc
        self.log.info('Arguments: '+ str(args) + '\n')

        if url:
            req_ob = requests.get(str(url).strip())
            gaussian = BeautifulSoup(req_ob.content, "html.parser")

            try:
                title = gaussian.find_all("title")[0]
                title = str(title.text.decode('utf-8'))
            except:
                title= ""

            try:     
                hpo_obs = gaussian.find_all("a", {"class": "kwd-search"})

                if hpo_obs:
                    hpo_terms=[]
                    self.app.stdout.write('HPO Terms:\n')

                    for ob in hpo_obs:
                        self.app.stdout.write(ob.text + '\n')
                        hpo_terms.append(str(ob.text).strip())

                    phenopacket = create_phenopacket(hpo_terms, url, title)
    
                    self.app.stdout.write(str(phenopacket))


                    if parsed_args.output:
                        fopen = open(str(parsed_args.output)+ ".json", 'w')
                        fopen.write(str(phenopacket))
                        fopen.close()
               
                else:
                    self.app.stdout.write("HPO Terms Not found\n")

            except:
                self.app.stdout.write("HPO Terms Not found\n")

        if doc:
            html_doc = open(str(doc), 'r')
            soup = BeautifulSoup(html_doc, 'html.parser')
            try:
                title= str(soup.title.get_text())
            except:
                title=''
            try:
                meta_list = soup.find_all('meta', {'name' : 'dc.Description'})
                content_list= [k.get('content') for k in meta_list]
                content = ' '.join(content_list)
                data = {'content' : str(content)}
              
                response = requests.get(server_url + '/annotations/entities', params = data)

                # Extracting Phenotypes using SciGraph Annotator
                if response.status_code == 200:
                    annotated_data = response.json()
                    # self.app.stdout.write(str(annotated_data))
                    hpo_terms = []
                    for ob in annotated_data:
                        token = ob['token']
                        if 'Phenotype' in token['categories']:
                            term = str(token['terms'][0])
                            if term not in hpo_terms:
                                hpo_terms.append(token['terms'][0])

                    self.app.stdout.write('\n HPO Terms:\n')
                    for term in hpo_terms:
                        self.app.stdout.write(str(term) + '\n')
                else:
                    self.app.stdout.write(str(response.status_code)+ '\n')
                try:
                    phenopacket = create_phenopacket(hpo_terms,'Nejm Test', title)
                    self.app.stdout.write(str(phenopacket))
                    if parsed_args.output:
                        fopen = open(str(parsed_args.output)+ ".json", 'w')
                        fopen.write(str(phenopacket))
                        fopen.close()                                
                except:
                    self.app.stdout.write('Unable to create phenopacket\n')
            except:
                self.app.stdout.write('Meta Data not Found\n')