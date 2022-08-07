# -*- coding: utf-8 -*-

"""
This module contains constants from determinator

"""

from lxml import etree


NAMESPACES = {
    None: "urn:iso:std:iso:30042:ed-2",
}
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"
TBX_RELAXNG = "relaxng_tbx"
TBX_SCHEMA = "schema_tbx"
TBX_DIALECT = "dialect"
TBX_STYLE = "style"
TBX_HEADER = "tbxHeader"
FILEDESC = "fileDesc"
TITLESTMT = "titleStmt"
PUBLICATIONSTMT = "publicationStmt"
SOURCEDESC = "sourceDesc"
TEXT = "text"
BODY = "body"
TITLE = "title"
PUBLICATION = "publication"
LANGSEC = "langSec"


def QName(prefix: str = None, name: str = None):
    """ """
    if prefix is None:
        qname = etree.QName("{urn:iso:std:iso:30042:ed-2}" + name, name)
    else:
        qname = etree.QName("{" + namespaces[prefix] + "}" + name, name)
    return qname
