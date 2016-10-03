import requests # that module need to be install
from xml.etree import ElementTree


email = "email=saurabhkumar.spsu@gmail.com"

base_url  = "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi?verb="

base_date = "2002-01-01"#year-month-date

until = "2002-01-02"#year-month-date

# To get the document ID

#Dont even think of to change below
name_space = '{http://www.openarchives.org/OAI/2.0/}'
full_text = "pmc" #https://www.ncbi.nlm.nih.gov/pmc/tools/oai/#examples -supported documents 

data = []
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
    document_id_verb = "ListIdentifiers"
    metadataPrefix_doc_id = "pmc_fm"
    document_id = []
    url1 = base_url + document_id_verb +"&"+ "from=" + base_date + "&" + "until=" + until + "&" + "metadataPrefix=" + metadataPrefix_doc_id
    doc_id_response = requests.get(url1)
    #XML tree
    tree = ElementTree.fromstring(doc_id_response.content)
    documents = tree.find(name_space + document_id_verb)
    document_id = []
    for document in documents:
        document_id.append(document.find(name_space + 'identifier').text)
    return document_id