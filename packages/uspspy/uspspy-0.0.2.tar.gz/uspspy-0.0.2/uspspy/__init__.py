"""pyusps core

A pure python implementation of usps-api https://github.com/BuluBox/usps-api/
"""
import json

import xmltodict
from xml.etree import ElementTree as etree
from xml.parsers.expat import ExpatError

import requests
from requests.exceptions import (RequestException, Timeout)
from urllib.parse import quote

from uspspy.constants import (SAFE, REQUEST_TIMEOUT,
                              DPV_MAP, DPV_FOOTNOTES, FOOTNOTES)

class USPSError(RuntimeError):
    pass

class Address(object):

    def __init__(self, address1, city, state, postal, country="US",
                 address2="", company="", name="", phone=""):
        self.name = quote(name, safe=SAFE)
        self.company = quote(company, safe=SAFE)
        self.address1 = quote(address1, safe=SAFE)
        self.address2 = quote(address2, safe=SAFE)
        self.city = quote(city, safe=SAFE)
        self.state = quote(state, safe=SAFE)
        self.postal = quote(postal, safe=SAFE)
        self.country = quote(country, safe=SAFE)
        self.phone = quote(phone, safe=SAFE)

    def __str__(self):
        return "{}\n{}\n{}\n{} {} {}".format(
                self.name, self.address1, self.address2,
                self.city, self.state, self.postal)

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

        address1 = etree.SubElement(root, prefix + 'Address1')
        address1.text = self.address1

        address2 = etree.SubElement(root, prefix + 'Address2')
        address2.text = self.address2 or '-'

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
    """USPS API client object.

    :param username: Username obtained by registering with USPS
    :type username: str
    """
    BASE_URL = 'https://secure.shippingapis.com/ShippingAPI.dll?API='
    urls = {
        'validate': 'Verify&XML={xml}',
    }

    def __init__(self, usps_username, test=False):
        self.username = usps_username
        self.test = test

    def get_url(self, action, xml):
        """Get the endpoint specific URL for an action.

        All requests to the API are carried out using GET requests with
        extended query params that contain the raw XML request. The API
        supports many ``actions``, such as address validation, tracking,
        label printing.

        Given request XML and an action, this method returns the correct
        URL with XML included in the query params.

        :param action: the name of the action.
        :type action: str
        :param xml: the full XML document for the request.
        :type xml: str
        :returns: URL for the given action and xml.
        :rtype: str
        """
        return self.BASE_URL + self.urls[action].format(
            **{'test': 'Certify' if self.test else '', 'xml': xml}
        )

    def send_request(self, action, xml):
        """Send an HTTP request to the USPS API.

        Create and execute a request for an action with the given XML document.

        The implementation is based on the best practices laid out in the
        deveoper guide:
        https://www.usps.com/business/web-tools-apis/general-api-developer-guide.htm)

        :param action: the action to execute.
        :type action: str
        :param xml: the XML document to send for the action.
        :type xml: str
        :returns: API response
        :rtype: dict
        :raises: USPSError
        """
        # The developer guide says ISO-8859-1 encoding is the expected charset
        xml = etree.tostring(xml, encoding='iso-8859-1').decode()
        url = self.get_url(action, xml)

        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            xml_response = response.content
        except Timeout:
            raise USPSError("Timed out communicating with the USPS API.")
        except RequestException as e:
            raise USPSError("General error from the USPS API, {}.".format(e))
        except ConnectionError:
            raise USPSError("Connection error raised from USPS API.")

        try:
            result = json.loads(json.dumps(xmltodict.parse(xml_response)))
        except ValueError:
            raise USPSError("Failed to parse USPS API response (JSON).")
        except ExpatError:
            raise USPSError("Failed to parse USPS API response (XML).")

        if 'Error' in result:
            raise USPSError(result['Error']['Description'])

        return result

    def validate_address(self, address, revision="1"):
        xml = etree.Element('AddressValidateRequest',
                            {'USERID': self.username})
        _revision = etree.SubElement(xml, "Revision", )
        _revision.text = revision
        _address = etree.SubElement(xml, 'Address', {'ID': '0'})
        address.add_to_xml(_address, prefix='', validate=True)
        self.result = self.send_request('validate', xml)
        return self.result

    def footnotes(self):
        """Get the list of human readable footnotes for the results."""
        footnotes = []
        fns = self.result.get("AddressValidateResponse", {}).get(
                              'Address', {}).get(
                              'Footnotes')

        for fn in FOOTNOTES:
            if fn in fns:
                footnotes.append(FOOTNOTES[fn])

        return footnotes

    def dpv_footnotes(self):
        """Get the list of human readable DPV footnotes for the results."""
        footnotes = []
        fns = self.result.get("AddressValidateResponse", {}).get(
                              'Address', {}).get(
                              'DPVFootnotes')

        for fn in DPV_FOOTNOTES:
            if fn in fns:
                footnotes.append(DPV_FOOTNOTES[fn])

        return footnotes

    @property
    def result_address(self):
        if self.result:
            return self.result.get(
                    "AddressValidateResponse", {}).get("Address", {})
        return {}

    def dpv_status(self):
        """Get the human readable DPV status."""
        dpvc = self.result_address.get('DPVConfirmation')
        if dpvc:
            return DPV_MAP.get(dpvc, "No map entry.")
        return None
