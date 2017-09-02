import requests # that module need to be install
from xml.etree import ElementTree
import re
from time import sleep

#### DB Connection 
from mysql.connector import connect, Error

#### DB Configuration
config = {
  'user': 'root',
  'password': 'XXXXXX',
  'host': '127.0.0.1',
  'database': 'pubmed',
  'raise_on_warnings': True,
}
# Db insert query
add_data = ("INSERT IGNORE INTO articledata "
              "(articleId,abstract, link) "
              "VALUES (%s,%s,%s)")

email = "email=saurabhkumar.spsu@gmail.com"

base_url  = "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi?verb="

base_date = "2002-01-01"#year-month-date

until = "2002-01-30"#year-month-date

# To get the document ID

#Dont even think of to change below
name_space = '{http://www.openarchives.org/OAI/2.0/}'
full_text = "pmc" #https://www.ncbi.nlm.nih.gov/pmc/tools/oai/#examples -supported documents 

data = []
###

a= []
##############################################################################

def data_insert(document,documet_id):
    documet_id = documet_id[26:]
    data = (documet_id, document, 'htttp:&%@')
    try:
        cnx = connect(**config)
        cursor = cnx.cursor()
            # Insert new data
        cursor.execute(add_data, data)
            #    emp_no = cursor.lastrowid
            #    print emp_no
            # Make sure data is committed to the database
        cnx.commit()
    except Error as error:
        print(error)
            
    finally:
        cursor.close()
        cnx.close()    

# To find out whether resumption token available or not
def isResumptionToken(documents):
    result = {}    
    token = None
    tag_name = ''
    tag_name = documents[-1].tag
    tag_name = tag_name[len(name_space):]
    if (tag_name == "resumptionToken"):
        #token = documents[-1].text
        result["documents"] = documents[:len(documents)-1]
        result["token"] = documents[-1].text
        return result# to remove the token from the tree
    else:
        result["documents"] = documents
        result["token"] = token
        return result 
# XML to text
def toText(document):
    content = document
    exp = re.compile(r'<.*?>')
    text_only = exp.sub('',content).strip()
    a = text_only.replace('\n','')
    return a
    
#Check available data format as not every document is available as full
def documentFormat(document_id):
    document_format_verb = "ListMetadataFormats"
    document_format_identifier = document_id
    url2 = base_url + document_format_verb + "&" + "identifier=" + document_format_identifier
    doc_format_response = requests.get(url2)
    tree = ElementTree.fromstring(doc_format_response.content)
    document_formats = tree.find(name_space + document_format_verb)
    formats = []
    for document_format in document_formats:
      formats.append(document_format.find(name_space + 'metadataPrefix').text)      
    return formats
# Check whether document available in full text     
def isAvailableFull(formats):
    isAvailable = full_text in formats    
    return isAvailable

#Return document text
def documentText(document_id=0):
    metadataPrefix_doc = "pmc"
    document_data_verb = "GetRecord"
    fullText = isAvailableFull(documentFormat(document_id))
    if fullText:
        url2 = base_url + document_data_verb + "&" + "identifier=" + document_id +"&" +"metadataPrefix=" +  metadataPrefix_doc
    else:
        url2 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&rettype=abstract&id="+ document_id[26:]
    response = requests.get(url2)
    return response.text

# Return document Ids for specific dates   
def documentIds():
    #for document Id's
    token = None
    document_id_verb = "ListIdentifiers"
    metadataPrefix_doc_id = "pmc_fm"
    document_id = []      
    url = base_url + document_id_verb +"&"+ "from=" + base_date + "&" + "until=" + until + "&" + "metadataPrefix=" + metadataPrefix_doc_id
    doc_id_response = requests.get(url)
    tree = ElementTree.fromstring(doc_id_response.content)
    allDocuments = tree.find(name_space + document_id_verb)# that might have resumption token also
    result = isResumptionToken(allDocuments)
    token = result["token"]
    for document in result["documents"]:
        document_id.append(document.find(name_space + 'identifier').text)
        
    while token:
        #sleep(.1)
        url = base_url + document_id_verb +"&"+ "resumptionToken=" + token
        doc_id_response = requests.get(url)
        tree = ElementTree.fromstring(doc_id_response.content)
        allDocuments = tree.find(name_space + document_id_verb)# that might have resumption token also
        result = isResumptionToken(allDocuments)
        token = result["token"]
        for document in result["documents"]:
            print "inside function "
            document_id.append(document.find(name_space + 'identifier').text)         
        
    return document_id
    
    
document_ids = documentIds()

for document_id in document_ids:    
    print "docuemtn append"
    sleep(.1)
    document = documentText(document_id)
    data.append(document)
    data_insert(document,document_id)
