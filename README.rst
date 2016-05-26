=================
Phenopacket-scraper-core
=================

Extracts information from life-science websites and texts, generating phenopackets with the extracted information and correct external ontology references.


=================
 Running PhenopacketScraper Tool
=================

Setup
-----

First, you need to create a virtual environment and activate it.

::

  $ pip install virtualenv
  $ virtualenv venv
  $ source venv/bin/activate
  (venv)$ 

Next, install ``cliff`` in the environment.

::

  (venv)$ venv/bin/pip install cliff

Now, install the application into the virtual environment.

::

  (venv)$ cd pps
  (venv)$ python setup.py install

Usage
-----
::

  (venv)$ pps test
  (venv)$ pps --help


Cleaning Up
-----------

Finally, when done, deactivate your virtual environment::

  (.venv)$ deactivate
  $
