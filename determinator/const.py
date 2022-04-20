# -*- coding: utf-8 -*-

"""
This module contains constants from determinator

"""

from lxml import etree


NAMESPACES = {
    None: "urn:iso:std:iso:30042:ed-2",
}
RELAXNG_TBX_BASIC = 'href="https://raw.githubusercontent.com/LTAC-Global/TBX-Basic_dialect/master/DCA/TBXcoreStructV03_TBX-Basic_integrated.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"'
SCHEMA_TBX_BASIC = 'href="https://raw.githubusercontent.com/LTAC-Global/TBX-Basic_dialect/master/DCA/TBX-Basic_DCA.sch" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"'

XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"

TBX_HEADER = "tbxHeader"
FILEDESC = "fileDesc"
SOURCEDESC = "sourceDesc"
TEXT = "text"
BODY = "body"
TITLE = "title"


def QName(prefix: str = None, name: str = None):
    """ """
    if prefix is None:
        qname = etree.QName("{urn:iso:std:iso:30042:ed-2}" + name, name)
    else:
        qname = etree.QName("{" + namespaces[prefix] + "}" + name, name)
    return qname
