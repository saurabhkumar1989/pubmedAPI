from time import sleep
from files import pubmedQuery   
document_ids = pubmedQuery.documentIds()
data = []

for document_id in document_ids:
    sleep(1)
    data.append(pubmedQuery.documentText(document_id))
print data
    
#simple xml data
#content = response.content 
#exp = re.compile(r'<.*?>')
#text_only = exp.sub('',content).strip()
#a = text_only.replace('\n','')
#print a.replace('\t','')
