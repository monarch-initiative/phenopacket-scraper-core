=================
Phenopacket-scraper-core
=================

Extracts information from life-science websites and texts, generating phenopackets with the extracted information and correct external ontology references.


=================
 Running PhenopacketScraper Tool
=================

Setup
-----

To get the project's source code, clone the github repository:

::

  $ git clone https://github.com/monarch-initiative/phenopacket-scraper-core.git

First, you need to create a virtual environment and activate it.

::

  $ [sudo] pip install virtualenv
  $ virtualenv venv
  $ source venv/bin/activate
  (venv)$ 

Next, install all the dependencies in the environment.

::

  (venv)$ venv/bin/pip install -r requirements.txt

Now, install the application into the virtual environment.

::

  (venv)$ python setup.py install

Usage
-----
::

  (venv)$ pps --help
  (venv)$ pps scrape -u (url)

Example:

::

  (venv)$ pps scrape -u http://molecularcasestudies.cshlp.org/content/early/2016/02/09/mcs.a000786.abstract
  (venv)$ pps -q scrape -u (Url)

  Title: Mutations in the substrate ...

  Abstract:
  We describe a large Lebanese fa...

  HPO Terms:
  Diffuse cerebellar atrophy
  Generalized hypotoni...

To store the output in a file:

::

  (venv)$ pps scrape -u (Url) -o (Filename)

This will create two files for now, (Filename)_abstract.txt will contain the abstract and the (Filename)_hpo_terms.txt will contain the hpo terms.

Cleaning Up
-----------

Finally, when done, deactivate your virtual environment::

  (venv)$ deactivate
  $
