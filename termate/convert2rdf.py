# -*- coding: utf-8 -*-

"""Convert2rdf module.

This module contains RDF conversion functions for termate package

"""
from .vocab import ONTOLEX
from .vocab import SKOS
from .vocab import TBX
from .vocab import DC
from .vocab import IATE
from .vocab import LIME
from .types import NoteLinkInfo
from .types import LexicalEntry
from .types import Term
from .types import Mappings
from lxml import etree

# from .const.types import LexicalEntry
# from .const.types import Describable
# from .const.types import TbxHeader
# from .const.types import TBX_Terminology
# from .const.types import Descrip
# from .const.types import XReference
# from .const.types import Term
# from .const.types import AdminGrp
# from .const.types import AdminInfo
# from .const.types import DescripGrp
# from .const.types import DescripNote;
# from .const.types import Note
# from .const.types import NoteLinkInfo
# from .const.types import Reference
# from .const.types import TermComp
# from .const.types import TermCompGrp
# from .const.types import TermCompList
# from .const.types import TermNote
# from .const.types import TermNoteGrp
# from .const.types import TransacGrp
# from .const.types import TransacNote
# from .const.types import Transaction


class TBX2RDF_Converter:

    # Converts a TBX string into a RDF. Parses the XML searching for termEntry
    # elements.
    # Then, Serializes Terms and Lexicons

    def convert(self, s: str = "", mappings: Mappings = None, resourceURI: str = ""):
        """
        @param str The TBX XML as a String.
        @return str A Turtle string with the equivalent information
        """
        result = convert(s, mappings)
        stringIO = StringIO()
        RDFDataMgr.write(
            stringIO, result.getModel(resourceURI), RDFFormat.TURTLE_PRETTY
        )
        return stringIO.getvalue()

    #     public TBX_Terminology convert(Reader input, Mappings mappings) throws IOException, ParserConfigurationException, TBXFormatException, SAXException {
    #         DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
    #         DocumentBuilder db = dbf.newDocumentBuilder();
    #         TransacNote.mapAgents.clear();
    #         db.setEntityResolver(new EntityResolver() {
    #                 @Override
    #                 public InputSource resolveEntity(String publicId, String systemId) throws SAXException, IOException {
    #                     if (systemId.endsWith(".dtd")) {
    #                         return new InputSource(new StringReader(""));
    #                     } else {
    #                         return null;
    #                     }
    #                 }
    #             });

    #         // parse the input document
    #         Document doc = db.parse(new InputSource(input));

    #         // extract here tbx metadata
    #         Element root = doc.getDocumentElement();

    #         return createTerminology(root, mappings);

    #     }

    def createTerminology(self, root: etree.Element = None, mappings: Mappings = None):
        """
        Processes the whole TBX file from the root XML element (once built the DOM model)
        @param root The root element
        """
        header = processTbxHeader(XMLUtils.child(root, "tbxHeader"), mappings)
        terminology = TBX_Terminology(root.getAttribute("type"), header)
        mappings.defaultLanguage = "en"
        for element in root:
            if element.tag == "text":
                for term in processText(element, mappings):
                    terminology.addTerm(term)
            elif element.tag != "tbx":
                logging.error("Unknown root element found")
        return terminology

    def processTbxHeader(self, root: etree.Element = None, mappings: Mappings = None):
        """
        Given a XML root element, processes the tbx Header
        @param root XML root element
        @param mappings Mappings
        """
        header = TbxHeader(
            processFileDescrip(XMLUtils.child(root, "fileDesc"), mappings)
        )
        processID(header, root)
        for element in root:
            if element.tag == "encodingDesc":
                header.encodingDesc = e.getChildNodes()
            elif element.tag == "revisionDesc":
                header.revisionDesc = e.getChildNodes()
            elif element.tag != "fileDesc":
                logging.error("Unknown element in Tbxheader")
        return header

    def processFileDescrip(self, root: etree.Element = None, mappings: Mappings = None):
        """
        Obtains a FileDesc object by parsing a XML element.
        <filedesc>: A nesting element containing child elements that describe the TBX document instance.
        """
        fileDesc = FileDesc()
        for element in root:
            if element.tag == "titleStmt":
                fileDesc.titleStmt = processTitleStmt(element, mappings)
            elif element.tag == "publicationStmt":
                fileDesc.publicationStmt = element
            elif element.tag == "sourceDesc":
                fileDesc.sourceDesc.append(element)
            else:
                logging.error("Unknown filedesc element")
        return fileDesc

    def processTitleStmt(self, root: etree.Element = None, mappings: Mappings = None):
        """
        Processes some metadata elements from the root element
        """
        titleStmt = TitleStmt(XMLUtils.child(root, "title").getTextContent())
        titleStmt.lang = root.attrib.get("xml:lang", None)
        titleStmt.id = root.attrib.get("id", None)
        title = XMLUtils.child(root, "title")
        titleStmt.title_lang = title.attrib.get("xml:lang", None)
        titleStmt.title_id = title.attrib.get("id", None)
        for element in root:
            if element.tag == "note":
                titleStmt.notes.append(eelement)
        return titleStmt

    def processText(self, root: etree.Element = None, mappings: Mappings = None):
        """
        Processes the body element and the back element.
        We arrive here with a <text> element.
        """
        terms = dict()
        for element in root:
            if element.tag == "body":
                terms.addAll(processBody(element, mappings))
            elif element.tag == "back":
                terms.addAll(processBack(element, mappings))
            else:
                logging.error("Unknown element in text")
        return terms

    def processBody(self, root: etree.Element = None, mappings: Mappings = None):
        """
        Processes the collection of terms
        We arrive here with a <body> element
        """
        terms = list()
        for element in root:
            if element.tag == "termEntry":
                terms.append(processTermEntry(element, mappings))
            else:
                logging.error("Unknown element in body")
        return terms

    def processBack(self, root: etree.Element = None, mappings: Mappings = None):
        # TODO: This should do something right?
        return []

    def processTermEntry(self, node: etree.Element = None, mappings: Mappings = None):
        """
        Processes, from a node, a termEntry
        @return A Term
        # // create new Term
        # // add subjectField
        # // add ID

        # // <!ELEMENT termEntry  ((%auxInfo;),(langSet+)) >
        # // <!ATTLIST termEntry
        # // id ID #IMPLIED >
        # // <!ENTITY % auxInfo '(descrip | descripGrp | admin | adminGrp | transacGrp | note | ref | xref)*' >
        """
        term = Term()
        langsetcount = 0
        sid = node.getAttribute("id")
        term.setID(sid)
        for element in node:
            if element.tag == "langSet":
                langsetcount += 1
                self.processLangSet(term, element, mappings)
            else:
                processAuxInfo(term, sub, mappings)
        if langsetcount == 0:
            logger.warning("No langSet element in termEntry")
        return term

    def processReference(
        self,
        descr: NoteLinkInfo = None,
        sub: etree.Element = None,
        mappings: Mappings = None,
    ):
        # // <!ELEMENT ref (#PCDATA) >
        # // <!ATTLIST ref
        # //    %impIDLangTypTgtDtyp;
        # // >

        # //<!ENTITY % impIDLangTypTgtDtyp ' id ID #IMPLIED
        # //xml:lang CDATA #IMPLIED
        # // type CDATA #REQUIRED
        # // target IDREF #IMPLIED
        # // datatype CDATA #IMPLIED
        # //'>
        ref = Reference(
            processType(sub, mappings, true),
            sub.getAttribute("xml:lang"),
            mappings,
            sub.getChildNodes(),
        )
        ref.setID(sub.attrib.get("id", None))
        ref.target = sub.attrib.get("target", None)
        ref.datatype = sub.attrib.get("datatype", None)
        descr.References.append(ref)

    def processAdminGrp(
        self,
        descr: NoteLinkInfo = None,
        node: etree.Element = None,
        mappings: Mappings = None,
    ):
        """
        #         // <!ELEMENT adminGrp (admin, (adminNote|note|ref|xref)*) >
        #         // <!ATTLIST adminGrp
        #         // id ID #IMPLIED >
        """
        processID(descr, node)
        i = 0
        for element in node:
            name = element.text
            if i == 0 and not name == "admin":
                logging.error(
                    "First element of TIG is not term !\n"
                )  # incorrect string
            if name == "admin":
                processAdmin(descr, element, mappings)
            elif name == "adminNote":
                processAdminGrp(descr, element, mappings)
            elif name == "note":
                processNote(descr, element, mappings)
            elif name == "ref":
                self.processReference(descr, element, mappings)
            elif name == "xref":
                self.processXReference(descr, element, mappings)
            else:
                logging.error("Element " + name + "not defined by TBX standard")
            i += 1

    def processLangSet(
        self,
        term: Term = None,
        langSet: etree.Element = None,
        mappings: Mappings = None,
    ):
        """
        Processes the langset (xml:lang)
        @return a LexicalEntry
        """
        #         // <!ELEMENT langSet ((%auxInfo;), (tig | ntig)+) >
        #         // <!ATTLIST langSet
        #         // id ID #IMPLIED
        #         // xml:lang CDATA #REQUIRED >

        language = XMLUtils.getValueOfAttribute(langSet, "xml:lang")
        if language is None:
            logging.error("Language not specified for langSet!")
        termCount = 0
        processID(term, langSet)
        for element in langSet:
            name = element.text
            if name == "ntig":
                termCount += 1
                entry = LexicalEntry(language, mappings)
                self.processNTIG(entry, sub, mappings)
                term.Lex_entries.append(entry)
            elif name == "tig":
                termCount += 1
                entry = LexicalEntry(language, mappings)
                self.processTIG(entry, sub, mappings)
                term.Lex_entries.append(entry)
            else:
                processAuxInfo(term, sub, mappings)
        if termCount == 0:
            logging.error("No TIG nor NTIG in langSet!")
        return term

    def processTIG(
        self,
        entry: LexicalEntry = None,
        tig: etree.Element = None,
        mappings: Mappings = None,
    ):
        """
        <!ELEMENT tig (term, (termNote)*, %auxInfo;) >
        <!ATTLIST tig
        id ID #IMPLIED >
        """
        i = 0
        processID(entry, tig)
        for element in tig:
            name = element.text
            if i == 0 and not name == "term":
                logging.error("First element of TIG is not term !\n")
            if name == "term":
                self.processTerm(entry, element, mappings)
            elif name == "termNote":
                entry.TermNotes.add(
                    TermNoteGrp(
                        self.processTermNote(element, mappings),
                        mappings.defaultLanguage,
                        mappings,
                    )
                )
            else:
                processAuxInfo(entry, tig_child, mappings)
            i += 1

    def processTerm(
        self,
        entry: LexicalEntry = None,
        node: etree.Element = None,
        mappings: Mappings = None,
    ):
        """
        Processes a term within a termEntry
        // <!ELEMENT term %basicText; >
        // <!ATTLIST term
        // id ID #IMPLIED >
        """
        entry.Lemma = node.getTextContent()

    def processTermNote(
        self, tig_child: etree.Element = None, mappings: Mappings = None
    ):
        """
        <!ELEMENT termNote %noteText; >
        <!ATTLIST termNote
        %impIDLangTypTgtDtyp;
        >
        <!ENTITY % impIDLangTypTgtDtyp ' id ID #IMPLIED
        xml:lang CDATA #IMPLIED type CDATA #REQUIRED target IDREF #IMPLIED datatype CDATA #IMPLIED
        '>
        """
        note = TermNote(
            tig_child.getChildNodes(),
            processType(tig_child, mappings, true),
            tig_child.getAttribute("xml:lang"),
            mappings,
        )
        processImpIDLangTypeTgtDType(note, tig_child, mappings)
        return note

    def processNTIG(
        self,
        entry: LexicalEntry = None,
        ntig: etree.Element = None,
        mappings: Mappings = None,
    ):
        """
        // <!ELEMENT ntig (termGrp, %auxInfo;) >
        // <!ATTLIST ntig
        // id ID #IMPLIED
        // >
        """
        i = 0
        for element in ntig:
            name = element.getNodeName()
            if i == 0 and not name == "termGrp":
                if Main.lenient == false:
                    logging.error("First element of NTIG is not termGrp !\n")
            if name == "termGrp":
                self.processTermGroup(entry, ntig_child, mappings)
            else:
                processAuxInfo(entry, ntig_child, mappings)
            i += 1

    def processXReference(
        self,
        descr: NoteLinkInfo = None,
        node: etree.Element = None,
        mappings: Mappings = None,
    ):
        """
        // <!ELEMENT xref (#PCDATA) >
        // <!ATTLIST xref
        // %impIDType;
        // target CDATA #REQUIRED >
        """
        xref = XReference(
            XMLUtils.getValueOfAttribute(node, "target"), node.getTextContent()
        )
        processID(xref, node)
        xref.type = processType(node, mappings, false)
        descr.Xreferences.add(xref)


#     def processDescripGroup(descr: Describable = None, node: etree.Element, mappings: Mappings = None):
#         """
#         // The DTD for a DescripGroup is as follows
#         // <!ELEMENT descripGrp (descrip, (descripNote|admin|adminGrp|transacGrp|note|ref|xref)*)
#         // >
#         // <!ATTLIST descripGrp
#         //  id ID #IMPLIED >
#         """
#         descrip = DescripGrp(processDescrip(XMLUtils.firstChild("descrip", node), mappings))
#         processID(descrip, node);
#         for element in node:
#             name = element.text
#             if (name.equalsIgnoreCase("descrip")) {
#                 // ignore
#             } else if (name.equalsIgnoreCase("descripNote")) {
#                 processDescripNote(descrip, sub, mappings);
#             } else if (name.equalsIgnoreCase("admin")) {
#                 this.processAdmin(descrip, sub, mappings);
#             } else if (name.equalsIgnoreCase("adminGrp")) {
#                 this.processAdminGrp(descrip, sub, mappings);
#             } else if (name.equalsIgnoreCase("transacGrp")) {
#                 this.processTransactionGroup(descrip, sub, mappings);
#             } else if (name.equalsIgnoreCase("note")) {
#                 this.processTransactionGroup(descrip, sub, mappings);
#             } else if (name.equalsIgnoreCase("ref")) {
#                 this.processReference(descrip, sub, mappings);
#             } else if (name.equalsIgnoreCase("xref")) {
#                 this.processXReference(descrip, sub, mappings);
#             } else {
#                 throw new TBXFormatException("Unexpected subnode " + node.getTagName());
#             }
#         descr.Descriptions.add(descrip);

#     def processAdmin(NoteLinkInfo descr, Element node, Mappings mappings):

# #         // <!ELEMENT admin %noteText; >
# #         // <!ATTLIST admin
# #         //  %impIDLangTypTgtDtyp;
# #         //>
#         admin = AdminInfo(node.getChildNodes(), processType(node, mappings, true), node.getAttribute("xml:lang"), mappings)
#         processImpIDLangTypeTgtDType(admin, node, mappings)
#         descr.AdminInfos.add(new AdminGrp(admin))

#     /**
#      * Processes a Transaction Group www.isocat.org/datcat/DC-162 A transacGrp
#      * element can contain either one transacNote element, or one date element,
#      * or both. Example:
#      * <transacGrp>
#      * <transac type="transactionType">creation</transac>
#      * <transacNote type="responsibility" target="CA5365">John
#      * Harris</transacNote>
#      * <date>2008‐05‐12</date>
#      * </transacGrp>
#      *
#      * @param transacGroup A Transaction group in XML // According to the TBX
#      * DTD, a transacGroup looks as follows: // <!ELEMENT transacGrp (transac,
#      * (transacNote|date|note|ref|xref)* ) >
#      * // <!ATTLIST transacGrp // id ID #IMPLIED >
#      * // Transaction transaction = new Transaction(lex);
#      */
#     void processTransactionGroup(NoteLinkInfo descr, Element elem, Mappings mappings) {

#         // <!ELEMENT transacGrp (transac, (transacNote|date|note|ref|xref)* ) >
#         // <!ATTLIST transacGrp
#         // id ID #IMPLIED >
#         Element elemTransac = null;
#         try {
#             elemTransac = XMLUtils.firstChild("transac", elem);
#         } catch (Exception e) {
#             return;
#         }
#         final TransacGrp transacGrp = new TransacGrp(processTransac(elemTransac, mappings));

#         int i = 0;
#         for (Element child : XMLUtils.children(elem)) {

#             String name = child.getNodeName();

#             if (i == 0 && !name.equals("transac")) {
#                 throw new TBXFormatException("First element of transacGrp is not termGrp !\n");
#             }

#             if (name.equals("transac")) {
#                 //processTransac(transacGrp, child, mappings);
#             } else if (name.equals("transacNote")) {
#                 processTransacNote(transacGrp, child, mappings);
#             } else if (name.equals("date")) {
#                 processDate(transacGrp, child, mappings);
#             } else if (name.equals("note")) {
#                 processNote(transacGrp, child, mappings);
#             } else if (name.equals("xref")) {
#                 processXReference(transacGrp, child, mappings);
#             } else if (name.equals("ref")) {
#                 this.processReference(transacGrp, child, mappings);
#             } else {
#                 throw new TBXFormatException("Element " + name + " not defined by TBX standard\n");
#             }
#             i++;
#         }
#         descr.Transactions.add(transacGrp);
#     }

#     void processTermGroup(LexicalEntry entry, Element node, Mappings mappings) {
#         // <!ELEMENT termGrp (term, (termNote|termNoteGrp)*, (termCompList)* ) >
#         // <!ATTLIST termGrp
#         //  id ID #IMPLIED
#         //>
#         for (Element elem : XMLUtils.children(node)) {
#             final String name = elem.getTagName();
#             if (name.equalsIgnoreCase("term")) {
#                 processTerm(entry, elem, mappings);
#             } else if (name.equalsIgnoreCase("termNote")) {
#                 entry.TermNotes.add(new TermNoteGrp(processTermNote(elem, mappings), mappings.defaultLanguage, mappings));
#             } else if (name.equalsIgnoreCase("termNoteGrp")) {
#                 entry.TermNotes.add(processTermNoteGrp(elem, mappings));
#             } else if (name.equalsIgnoreCase("termCompList")) {
#                 processTermCompList(entry, elem, mappings);
#             }
#         }
#     }

#     void processNote(NoteLinkInfo descr, Element elem, Mappings mappings) {
#         //<!ELEMENT note %noteText; >
#         //<!ATTLIST note %impIDLang;
#         //>
#         final Note note = new Note(elem.getChildNodes(), elem.getAttribute("xml:lang"), mappings);
#         processID(note, elem);
#         descr.notes.add(note);
#     }

#     Descrip processDescrip(Element elem, Mappings mappings) {
#         //<!ELEMENT descrip %noteText; >
#         //<!ATTLIST descrip
#         //%impIDLangTypTgtDtyp;
#         //>
#         final Descrip descrip = new Descrip(elem.getChildNodes(), processType(elem, mappings, true), elem.getAttribute("xml:lang"), mappings);
#         processImpIDLangTypeTgtDType(descrip, elem, mappings);
#         return descrip;
#     }

#     void processDescripNote(DescripGrp descrip, Element sub, Mappings mappings) {
#         // <!ELEMENT descripNote (#PCDATA) >
#         //<!ATTLIST descripNote
#         //%impIDLangTypTgtDtyp;
#         //>
#         final DescripNote descripNote = new DescripNote(sub.getChildNodes(), processType(sub, mappings, true), sub.getAttribute("xml:lang"), mappings);
#         processImpIDLangTypeTgtDType(descripNote, sub, mappings);
#         descrip.descripNote.add(descripNote);
#     }

#     Transaction processTransac(Element child, Mappings mappings) {
#         //  <!ELEMENT transac (#PCDATA) >
#         //<!ATTLIST transac
#         //%impIDLangTypTgtDtyp;
#         //>
#         final Transaction transaction = new Transaction(child.getChildNodes(), processType(child, mappings, true), child.getAttribute("xml:lang"), mappings);
#         processImpIDLangTypeTgtDType(transaction, child, mappings);
#         return transaction;
#     }

#     void processTransacNote(TransacGrp transacGrp, Element child, Mappings mappings) {

#         //<!ELEMENT transacNote (#PCDATA) >
#         //<!ATTLIST transacNote
#         //%impIDLangTypTgtDtyp;
#         //>
#         final TransacNote transacNote = new TransacNote(child.getChildNodes(), processType(child, mappings, true), child.getAttribute("xml:lang"), mappings);
#         processImpIDLangTypeTgtDType(transacNote, child, mappings);
#         transacGrp.transacNotes.add(transacNote);
#     }

#     void processDate(TransacGrp transacGrp, Element child, Mappings mappings) {
#         //  <!ELEMENT date (#PCDATA) >
#         //<!ATTLIST date
#         //id ID #IMPLIED
#         //>
#         transacGrp.date = child.getTextContent();
#     }

#     TermNoteGrp processTermNoteGrp(Element elem, Mappings mappings) {
#         //  <!ELEMENT termNoteGrp (termNote, %noteLinkInfo;) >
#         //<!ATTLIST termNoteGrp
#         //id ID #IMPLIED
#         //>
#         final TermNoteGrp termNoteGrp = new TermNoteGrp(processTermNote(XMLUtils.firstChild("termNote", elem), mappings), elem.getAttribute("xml:lang"), mappings);
#         for (Element e : XMLUtils.children(elem)) {
#             final String name = e.getTagName();
#             if (name.equalsIgnoreCase("termNote")) {
#                 // Do nothing
#             } else if (name.equalsIgnoreCase("admin")) {
#                 processAdmin(termNoteGrp, e, mappings);
#             } else if (name.equalsIgnoreCase("adminGrp")) {
#                 processAdminGrp(termNoteGrp, e, mappings);
#             } else if (name.equalsIgnoreCase("transacGrp")) {
#                 processTransactionGroup(termNoteGrp, e, mappings);
#             } else if (name.equalsIgnoreCase("note")) {
#                 processNote(termNoteGrp, e, mappings);
#             } else if (name.equalsIgnoreCase("ref")) {
#                 processReference(termNoteGrp, e, mappings);
#             } else if (name.equalsIgnoreCase("xref")) {
#                 processXReference(termNoteGrp, e, mappings);
#             }
#         }
#         return termNoteGrp;
#     }

#     void processTermCompList(LexicalEntry entry, Element elem, Mappings mappings) {
#         // <!ELEMENT termCompList ((%auxInfo;), (termComp | termCompGrp)+) >
#         //<!ATTLIST termCompList
#         //id ID #IMPLIED
#         //type CDATA #REQUIRED
#         //>
#         final TermCompList termCompList = new TermCompList(mappings.getMapping("termCompList", "type", elem.getAttribute("type")));
#         processID(termCompList, elem);
#         for (Element e : XMLUtils.children(elem)) {
#             final String name = e.getTagName();
#             if (name.equalsIgnoreCase("termComp")) {
#                 final TermComp termComp = processTermComp(e, mappings);
#                 termCompList.termComp.add(new TermCompGrp(termComp, null, mappings));
#             } else if (name.equalsIgnoreCase("termCompGrp")) {
#                 processTermCompGrp(termCompList, e, mappings);
#             } else if (name.equalsIgnoreCase("admin")) {
#                 processAdmin(termCompList, e, mappings);
#             } else if (name.equalsIgnoreCase("adminGrp")) {
#                 processAdminGrp(termCompList, e, mappings);
#             } else if (name.equalsIgnoreCase("transacGrp")) {
#                 processTransactionGroup(termCompList, e, mappings);
#             } else if (name.equalsIgnoreCase("note")) {
#                 processNote(termCompList, e, mappings);
#             } else if (name.equalsIgnoreCase("ref")) {
#                 processReference(termCompList, e, mappings);
#             } else if (name.equalsIgnoreCase("xref")) {
#                 processXReference(termCompList, e, mappings);
#             }
#         }
#         entry.Decomposition.add(termCompList);

#     }

#     TermComp processTermComp(Element e, Mappings mappings) {
#         //<!ELEMENT termComp (#PCDATA) >
#         //<!ATTLIST termComp
#         // %impIDLang;
#         //>
#         final TermComp termComp = new TermComp(e.getTextContent(), e.getAttribute("xml:lang"), mappings);
#         processID(termComp, e);
#         return termComp;
#     }

#     void processTermCompGrp(TermCompList termCompList, Element elem, Mappings mappings) {
#         //<!ELEMENT termCompGrp (termComp, (termNote|termNoteGrp)*, %noteLinkInfo;) >
#         //<!ATTLIST termCompGrp
#         //id ID #IMPLIED
#         //>
#         final TermCompGrp termCompGrp = new TermCompGrp(processTermComp(XMLUtils.firstChild("termComp", elem), mappings), null, mappings);
#         for (Element e : XMLUtils.children(elem)) {
#             final String name = e.getTagName();
#             if (name.equalsIgnoreCase("termNote")) {
#                 termCompGrp.termNoteGrps.add(new TermNoteGrp(processTermNote(e, mappings), null, mappings));
#             } else if (name.equalsIgnoreCase("termNoteGrp")) {
#                 termCompGrp.termNoteGrps.add(processTermNoteGrp(e, mappings));
#             } else if (name.equalsIgnoreCase("admin")) {
#                 processAdmin(termCompList, e, mappings);
#             } else if (name.equalsIgnoreCase("adminGrp")) {
#                 processAdminGrp(termCompList, e, mappings);
#             } else if (name.equalsIgnoreCase("transacGrp")) {
#                 processTransactionGroup(termCompList, e, mappings);
#             } else if (name.equalsIgnoreCase("note")) {
#                 processNote(termCompList, e, mappings);
#             } else if (name.equalsIgnoreCase("ref")) {
#                 processReference(termCompList, e, mappings);
#             } else if (name.equalsIgnoreCase("xref")) {
#                 processXReference(termCompList, e, mappings);
#             }
#         }
#         termCompList.termComp.add(termCompGrp);
#     }


#     /**
#      *
#      */
#     private void unexpected(Node n) {
#         if (n instanceof Element) {
#             throw new TBXFormatException("Unexpected " + ((Element) n).getTagName());
#         } else {
#             throw new TBXFormatException("Unexpected");
#         }
#     }

#     private void processID(impID elem, Element node) {
#         if (node.hasAttribute("id")) {
#             elem.setID(node.getAttribute("id"));
#         }
#     }

#     /**
#      *
#      */
#     private void processImpIDLangTypeTgtDType(impIDLangTypeTgtDtyp ref, Element sub, Mappings mappings) {
#         // <!ENTITY % impIDLangTypTgtDtyp '
#         //  id ID #IMPLIED
#         //  xml:lang CDATA #IMPLIED
#         //  type CDATA #REQUIRED
#         //  target IDREF #IMPLIED
#         //  datatype CDATA #IMPLIED
#         // '>
#         if (sub.hasAttribute("id")) {
#             ref.setID(sub.getAttribute("id"));
#         }
#         if (sub.hasAttribute("target")) {
#             ref.target = sub.getAttribute("target");
#         }
#         if (sub.hasAttribute("datatype")) {
#             ref.datatype = sub.getAttribute("datatype");
#         }
#         if (sub.hasAttribute("subjectField"))
#         {
# //            System.out.println("uy");
#         }
#     }

#     private void processAuxInfo(Describable term, Element sub, Mappings mappings) {
#         //   <!ENTITY % auxInfo '(descrip | descripGrp | admin | adminGrp | transacGrp | note | ref
#         //        | xref)*' >
#         final String name = sub.getTagName();
#         if (name.equalsIgnoreCase("descrip")) {
#             term.Descriptions.add(new DescripGrp(processDescrip(sub, mappings)));
#         } else if (name.equalsIgnoreCase("descripGrp")) {
#             this.processDescripGroup(term, sub, mappings);
#         } else if (name.equalsIgnoreCase("admin")) {
#             this.processAdmin(term, sub, mappings);
#         } else if (name.equalsIgnoreCase("adminGrp")) {
#             this.processAdminGrp(term, sub, mappings);
#         } else if (name.equalsIgnoreCase("transacGrp")) {
#             this.processTransactionGroup(term, sub, mappings);
#         } else if (name.equalsIgnoreCase("note")) {
#             this.processNote(term, sub, mappings);
#         } else if (name.equalsIgnoreCase("ref")) {
#             this.processReference(term, sub, mappings);
#         } else if (name.equalsIgnoreCase("xref")) {
#             this.processXReference(term, sub, mappings);
#         } else {
#             throw new TBXFormatException("Element " + name + " not defined by TBX standard");
#         }

#     }


#     /**
#      *
#      */
#     private Mapping processType(Element sub, Mappings mappings, boolean required) {
#         if (sub.hasAttribute("type")) {
#             final Mapping m = mappings.getMapping(sub.getTagName(), "type", sub.getAttribute("type"));
#             if (m == null && required) {
#                 logger.warn("Unrecognised mapping for <" + sub.getTagName() + " type=\"" + sub.getAttribute("type") + "\">");
#             }
#             return m;
#         } else if (required) {
#             throw new TBXFormatException("type expected");
#         } else {
#             System.err.println("Null type on " + sub.getTagName());
#             return null;
#         }
#     }


#     /**
#      * Converts a XML TBX file (handling large files...)
#      * It does not hold in memory the whole dataset, but parses it as it comes.
#      *
#      * A TBX file root element is called "tbx". It has two childre: marthifHeader and text
#      *
#      *
#      * @param file Path to the input file
#      * @param mappings Mappings
#      * @return The TBX terminology
#      */
#     public TBX_Terminology convertAndSerializeLargeFile(String file, PrintStream fos, Mappings mappings) {
#         String resourceURI = new String(Main.DATA_NAMESPACE);
#         FileInputStream inputStream = null;
#         Scanner sc = null;
#         int count = 0;
#         int errors = 0;

#         //We first count the lexicons we have
#         SAXHandler handler = null;
#         HashMap<String, Resource> lexicons = new HashMap();
#         try {
#             InputStream xmlInput = new FileInputStream(file);
#             SAXParserFactory factory = SAXParserFactory.newInstance();
#             SAXParser saxParser = factory.newSAXParser();
#             handler = new SAXHandler(mappings);
#             saxParser.parse(xmlInput, handler);
#             lexicons = handler.getLexicons();
#             xmlInput.close();
#         } catch (Exception e) {
#         	logger.warn("There was an error while reading/creting the lexicons, this could affect the rest of the code");
#             logger.warn(e.getMessage());
#         }

#         //WE PROCESS HERE THE TBX HEADER
#         TbxHeader tbxheader = extractAndReadTbxHeader(file, mappings);


#         if (tbxheader==null)
#             return null;

#         //First we serialize the header
#         Model mdataset = ModelFactory.createDefaultModel();
#         //The whole dataset!
#         final Resource rdataset = mdataset.createResource(resourceURI);
#         rdataset.addProperty(DCTerms.type, handler.getTbxType());
#         //This should be generalized
#         rdataset.addProperty(RDF.type, mdataset.createResource("http://www.w3.org/ns/dcat#Dataset"));
#         rdataset.addProperty(DC.rights, IATE.rights);
#         rdataset.addProperty(DC.source, IATE.iate);
#         rdataset.addProperty(DC.attribution, "Download IATE, European Union, 2014");
#         tbxheader.toRDF(mdataset, rdataset);
#         RDFDataMgr.write(fos, mdataset, Lang.NTRIPLES);


#         Model msubjectFields = SubjectFields.generateSubjectFields();
#         RDFDataMgr.write(fos, msubjectFields, Lang.NTRIPLES);


#         //We declare that every lexicon belongs to
#         Iterator it = lexicons.entrySet().iterator();
#         Property prootresource=mdataset.createProperty("http://www.w3.org/TR/void/rootResource");
#         while (it.hasNext()) {
#             Map.Entry e = (Map.Entry) it.next();
#             Resource rlexicon = (Resource) e.getValue();
#             rlexicon.addProperty(prootresource, rdataset);
#         }


#         boolean dentro = false;
#         try {
#             inputStream = new FileInputStream(file);
#             sc = new Scanner(inputStream, "UTF-8");
#             String xml = "";

#             while (sc.hasNextLine()) {
#                 String line = sc.nextLine();
#                 //We identify the terms by scanning the strings. Not a very nice practice, though.
#                 int index = line.indexOf("<termEntry");
#                 if (index != -1) {
#                     dentro = true;
#                     xml = line.substring(index) + "\n";
#                 }
#                 if (dentro == true && index == -1) {
#                     xml = xml + line + "\n";
#                 }
#                 index = line.indexOf("</termEntry>");
#                 if (index != -1) {
#                     xml = xml + line.substring(0, index) + "\n";
#                     count++;
#                     //We do a partial parsing of this XML fragment
#                     Document doc = loadXMLFromString(xml);
#                     if (doc == null) {
#                         continue;
#                     }
#                     Element root = doc.getDocumentElement();
#                     if (root != null) {
#                         try {
#                             Term term = processTermEntry(root, mappings);
#                             Model model = ModelFactory.createDefaultModel();
#                             TBX.addPrefixesToModel(model);
#                             model.setNsPrefix("", Main.DATA_NAMESPACE);
#                             final Resource rterm = term.getRes(model);
#                             rterm.addProperty(RDF.type, ONTOLEX.Concept);
#                             term.toRDF(model, rterm);
#                             for (LexicalEntry le : term.Lex_entries) {
#                                 final Resource lexicon = lexicons.get(le.lang);
#                                 lexicon.addProperty(LIME.entry, le.getRes(model));
#                                 le.toRDF(model, rterm);
#                             }
#                             RDFDataMgr.write(fos, model, Lang.NTRIPLES);
#                         } catch (Exception e) {
#                             errors++;
#                             System.err.println("Error " + e.getMessage());
#                         }
#                         if (count % 1000 == 0) {
#                             System.err.println("Total: " + count + " Errors: " + errors);
#                         }
#                     }
#                     xml = "";
#                 }
#             } //end of while

#             //Now we serialize the lexicons
#             RDFDataMgr.write(fos, handler.getLexiconsModel(), Lang.NTRIPLES);


#             // note that Scanner suppresses exceptions
#             if (sc.ioException() != null) {
#                 throw sc.ioException();
#             }
#         } catch (Exception e) {
#             e.printStackTrace();
#         } finally {
#             if (sc != null) {
#                 sc.close();
#             }
#         }
#         return null;
#     }
#     /**
#      * Gently loads a DOM XML document from a XML fragment.
#      * If it fails, it returns null;
#      */
#     private static Document loadXMLFromString(String xml) throws Exception {
#         try {
#             DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
#             DocumentBuilder builder = factory.newDocumentBuilder();
#             builder.setEntityResolver(new EntityResolver() {
#                 @Override
#                 public InputSource resolveEntity(String publicId, String systemId)
#                         throws SAXException, IOException {
#                     if (systemId.endsWith(".dtd")) {
#                         return new InputSource(new StringReader(""));
#                     } else {
#                         return null;
#                     }
#                 }
#             });
#             InputSource is = new InputSource(new StringReader(xml));
#             return builder.parse(is);
#         } catch (Exception e) {
#             return null;
#         }
#     }


#     /**
#      * Parses the text manually, extracting as text the fragment where the TbxHeader is and then parses it as XML.
#      */
#     public MartifHeader extractAndReadMartifHeader(String file, Mappings mappings)
#     {
#         MartifHeader martifheader = null;
#         boolean dentro = false;
#         try {
#             FileInputStream inputStream = new FileInputStream(file);
#             Scanner sc = new Scanner(inputStream, "UTF-8");
#             String xml = "";
#             while (sc.hasNextLine()) {
#                 String line = sc.nextLine();
#                 //We identify the terms by scanning the strings. Not a very nice practice, though.
#                 int index = line.indexOf("<martifHeader");
#                 if (index != -1) {
#                     dentro = true;
#                     xml = line.substring(index) + "\n";
#                 }
#                 if (dentro == true && index == -1) {
#                     xml = xml + line + "\n";
#                 }
#                 index = line.indexOf("</martifHeader>");
#                 if (index != -1) {
#                     xml = xml + line.substring(0, index) + "\n";
#                     //We do a partial parsing of this XML fragment
#                     Document doc = loadXMLFromString(xml);
#                     Element root = doc.getDocumentElement();
#                     martifheader = this.processMartifHeader(root, mappings);
#                     break;
#                 }

#             }
#             inputStream.close();
#         } catch (Exception e) {
#             logger.warn("Could not parse well the general metadata (MartifHeader)" + e.getMessage());
#         }
#         return martifheader;
# }

# }
