import requests # that module need to be install
from xml.etree import ElementTree
base_url  = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
query  = "email=saurabhkumar.spsu@gmail.com&db=pubmed&term=science%5bjournal%5d+AND+breast+cancer+AND+2008%5bpdat%5d"
url = base_url + query

response = requests.get(url)
import re

tree = ElementTree.fromstring(response.content)

content = response.content 