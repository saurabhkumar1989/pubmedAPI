import requests # that module need to be install
from xml.etree import ElementTree
from time import sleep

email = "email=saurabhkumar.spsu@gmail.com"

base_url  = "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi?verb="

base_date = "2002-01-01"#year-month-date

until = "2002-01-02"#year-month-date

# To get the document ID

#Dont even think of to change below
name_space = '{http://www.openarchives.org/OAI/2.0/}'


#for document Id's

document_id_verb = "ListIdentifiers"

metadataPrefix_doc_id = "pmc_fm"

url1 = base_url + document_id_verb +"&"+ "from=" + base_date + "&" + "until=" + until + "&" + "metadataPrefix=" + metadataPrefix_doc_id

doc_id_response = requests.get(url1)

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