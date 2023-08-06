"""pyusps core

A pure python implementation of usps-api https://github.com/BuluBox/usps-api/
"""
import json
import xmltodict
import requests
from urllib.parse import quote as quote_plus
from xml.etree import ElementTree as etree

SAFE = " "

class USPSError(RuntimeError):
    pass

class Address(object):

    def __init__(self, address1, city, state, postal, country="US",
                 address2="", company="", name="", phone=""):
        self.name = quote_plus(name, safe=SAFE)
        self.company = quote_plus(company, safe=SAFE)
        self.address1 = quote_plus(address1, safe=SAFE)
        self.address2 = quote_plus(address2, safe=SAFE)
        self.city = quote_plus(city, safe=SAFE)
        self.state = quote_plus(state, safe=SAFE)
        self.postal = quote_plus(postal, safe=SAFE)
        self.country = quote_plus(country, safe=SAFE)
        self.phone = quote_plus(phone, safe=SAFE)

    @property
    def zip5(self):
        return self.postal.split("-")[0]

    @property
    def zip4(self):
        if "-" in self.postal:
            return self.postal.split("-")[-1]
        return ''

    def add_to_xml(self, root, prefix='To', validate=False):
        if not validate:
            name = etree.SubElement(root, prefix + 'Name')
            name.text = self.name

        company = etree.SubElement(
                root, prefix + 'Firm' + ('Name' if validate else ''))
        company.text = self.company

        address_1 = etree.SubElement(root, prefix + 'Address1')
        address_1.text = self.address1

        address_2 = etree.SubElement(root, prefix + 'Address2')
        address_2.text = self.address2 or '-'

        city = etree.SubElement(root, prefix + 'City')
        city.text = self.city

        state = etree.SubElement(root, prefix + 'State')
        state.text = self.state

        zipcode = etree.SubElement(root, prefix + 'Zip5')
        zipcode.text = self.zip5

        zipcode_ext = etree.SubElement(root, prefix + 'Zip4')
        zipcode_ext.text = self.zip4

        if not validate:
            phone = etree.SubElement(root, prefix + 'Phone')
            phone.text = self.phone

class USPS(object):
    """Get an instance of the USPS API client."""
    BASE_URL = 'https://secure.shippingapis.com/ShippingAPI.dll?API='
    urls = {
        'tracking': 'TrackV2{test}&XML={xml}',
        'label': 'eVS{test}&XML={xml}',
        'validate': 'Verify&XML={xml}',
    }

    def __init__(self, usps_username, test=False):
        self.username = usps_username
        self.test = test

    def get_url(self, action, xml):
        return self.BASE_URL + self.urls[action].format(
            **{'test': 'Certify' if self.test else '', 'xml': xml}
        )

    def send_request(self, action, xml):
        # The USPS developer guide says "ISO-8859-1 encoding is the expected
        # character set for the request." (see
        # https://www.usps.com/business/web-tools-apis/general-api-developer-guide.htm)
        xml = etree.tostring(xml, encoding='iso-8859-1').decode()
        url = self.get_url(action, xml)
        print(url)
        xml_response = requests.get(url).content
        response = json.loads(json.dumps(xmltodict.parse(xml_response)))
        if 'Error' in response:
            raise USPSError(response['Error']['Description'])
        return response

    def validate_address(self, address):
        xml = etree.Element('AddressValidateRequest', {'USERID': self.username})
        _address = etree.SubElement(xml, 'Address', {'ID': '0'})
        address.add_to_xml(_address, prefix='', validate=True)

        self.result = self.send_request('validate', xml)
        return self.result
