import requests # that module need to be install
from xml.etree import ElementTree
base_url  = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
query  = "email=saurabhkumar.spsu@gmail.com&db=pubmed&term=science%5bjournal%5d+AND+breast+cancer+AND+2008%5bpdat%5d"
url = base_url + query

response = requests.get(url)
import re
#XML tree
tree = ElementTree.fromstring(response.content)
#simple xml data
content = response.content 
exp = re.compile(r'<.*?>')
text_only = exp.sub('',content).strip()
a = text_only.replace('\n','')
print a.replace('\t','')