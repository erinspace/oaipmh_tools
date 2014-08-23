import time
import requests
from lxml import etree


NAMESPACES = {'dc': 'http://purl.org/dc/elements/1.1/', 
            'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
            'ns0': 'http://www.openarchives.org/OAI/2.0/',
            'arch': 'http://dtd.nlm.nih.gov/2.0/xsd/archivearticle'}

def get_records(base_url, resumption_url):
    ''' takes in a url to harvest, and returns individual records from query'''
    data = requests.get(base_url)
    doc = etree.XML(data.content)
    records = doc.xpath('//ns0:record', namespaces=NAMESPACES)
    token = doc.xpath('//ns0:resumptionToken/node()', namespaces=NAMESPACES)

    if len(token) == 1:
        time.sleep(0.5)
        url = resumption_url + token[0]
        records += get_records(url, namespace=NAMESPACES)

    return records

def get_title(record):
    ''' returns a list of any fields labeled as title
        the title from a oai-pmh record '''

    return record.xpath('//dc:title/node()', namespaces=NAMESPACES)

def get_identifier(record):
    ''' returns the API-specific identifier in the header of
        each request '''
    return record.xpath('ns0:header/ns0:identifier/node()', namespaces=NAMESPACES)[0]
