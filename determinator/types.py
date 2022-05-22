import uuid
import regex
from lxml import etree

class IndividualMapping():

    def __init__(self):
        self.url = None

    def IndividualMapping(self, url: str = ""):
        self.url = url

    def getURL(self):
        return self.url

    def toString(self):
        return url.format("Individual <%s>")

class Mappings():

    def __init__(self):
        """
        """
        self.mappings = None
        self.individualMappings = None;
        self.defaultLanguage = "en"
    
    def readInMappings(self, mapping_file):
        """
        Creates a Mappings object from a reader
        """
        self.mappings = dict()

        mapping1 = regex.compile("^(\\S*?)\\s+<(\\S*?)>$")
        mapping2 = regex.compile("^(\\S*?)\\s+(\\S*?)\\s+(\\S*?)\\s+<(\\S*)>\\s+OP(\\s*\\{(.*?)\\})?$")
        mapping3 = regex.compile("^(\\S*?)\\s+(\\S*?)\\s+(\\S*?)\\s+<(\\S*)>\\s+DP(\\s*<(.*?)>)?$")
        mapping4 = regex.compile("^(\\S*?)\\s+(\\S*?)\\s+(\\S*?)\\s+<(\\S*)>\\s+EX(\\s*\\{(.*?)\\})?$")

        fstream = open(mapping_file, 'r')
        for line in fstream.readlines():
            strLine = line.strip()
            matcher = re.fullmatch(mapping1, strLine)
            if matcher is not None:
                mappings.addMapping(matcher.group(1), IndividualMapping(matcher.group(2)))
            else:
                matcher = re.fullmatch(mapping3, strLine)
                if matcher is not None:
                    mappings.addMapping(matcher.group(1), matcher.group(2), matcher.group(3), DatatypePropertyMapping(matcher.group(4), matcher.group(6)))
                else:
                    matcher = re.fullmatch(mapping2, strLine)
                    if matcher is not None:
                        new_set = dict()
                        if matcher.group(6) is not None:
                            values = matcher.group(6).split(",")
                            for i in range(len(values)):
                                new_set.add(values[i])
                            objectPropertyMapping = ObjectPropertyMapping(matcher.group(4), new_set, mappings.individualMappings)
                            mappings.addMapping(matcher.group(1), matcher.group(2), matcher.group(3), objectPropertyMapping)
                        else:
                            objectPropertyMapping = ObjectPropertyMapping(matcher.group(4), mappings.individualMappings)
                            mappings.addMapping(matcher.group(1), matcher.group(2), matcher.group(3), objectPropertyMapping)
                    else:
                        matcher = re.fullmatch(mapping4, strLine)
                        if matcher is not None:
                            em = ExceptionMapping(matcher.group(4), "")
                            mappings.addMapping(matcher.group(1), matcher.group(2), matcher.group(3), em)
                        else:
                            logging.error("Bad line in mapping file: " + strLine);

        return mappings


    def addMapping(self, name: str = "", target: IndividualMapping = None):
        """
        """
        individualMappings[name] = target

    def addMapping(self, element: str = "", attribute: str = "", value: str = "", mapping: str = None):
        """
        """
        # HashMap<String, HashMap<String, Mapping>> element2attr;
        # HashMap<String, Mapping> attr2mappings;
        if element in mappings.keys():
            element2attr = mappings.get(element);
        else:
            element2attr = dict()
            mappings[element] = element2attr
        if attribute in element2attr.keys():
            attr2mappings = element2attr.get(attribute)
        else:
            attr2mappings = dict()
            element2attr[attribute] = attr2mappings
        attr2mappings[value] = mapping

    def getMapping(self, element: str = "", attribute: str = "", value: str = ""):
        """
        Gets the mapping for an element, attribute and value
        @param element XML element, for example "descrip"
        @param attribute XML attribute, for example, "subjectField"
        @param value String literal with the value
        """
        if element in mappings.keys():
            element2attr = mappings.get(element)
            if attribute in element2attr.keys():
                attr2mappings = element2attr.get(attribute)
                if value in attr2mappings.keys():
                    return attr2mappings.get(value)
                else:
                    return None
            else:
                return None
        else:
            return None

class Mapping():
    def __init__(self):
        return None

class Resource():
    def __init__(self):
        return None

class impID():

    def __init__(self):
        self.id = None

    def setID(self, str_id: str = ""):
        """
        Set the ID of the object
        @param id
        """
        self.id = str_id;

    def getID(self):
        """
        Get the ID, or a randomly generated identifier if this ID is not set
        @return A unique string ID
        """
        if self.id is not None:
            return self.id
        else:
            return type(self)+"-"+str(uuid.uuid4())

    def getRes(self):
        """
        Get the RDF resource corresponding to this ID
        @return A valid and unique RDF element
        """
        return "_:" + self.getID()

    def getSubRes(self, name: str = ""):
        """
        Get a RDF resource for a subelement with the corresponding name. Normally
        this is simply the resource id with the name attached
        @param name
        @return
        """
        return "_:" + self.getID() + "#" + name

    # protected static final RDFDatatype XMLLiteral = NodeFactory.getType(RDF.getURI() + "#XMLLiteral");

    def removeWhitespaceNode(self, node: etree.Element = None):
        if node.isinstance(etree.Element):
            nl = node.getChildNodes()
            for i in range(len(nl)):
                n = nl.item(i)
                if (n.instanceof(etree.Element)):
                    removeWhitespaceNode(n)
                elif n.getTextContent().matches("\\s+"):
                    n.setTextContent("")
                else:
                    n.setTextContent(n.getTextContent().trim())

    def nodeToString(self, node: etree.Element = None):
        """
        Convert an XML Node to a string
        @param node The node
        @return The string serialization of the node
        """
        removeWhitespaceNode(node)
        stringIO = StringIO()
        try:
            t = TransformerFactory.newInstance().newTransformer()
            t.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes")
            t.setOutputProperty(OutputKeys.INDENT, "no")
            t.transform(DOMSource(node), StreamResult(stringIO))
        except:
            System.out.println("nodeToString Transformer Exception")
        return stringIO.getvalue()

    def nodelistToString(self, node: list = []):
        """
        convert an XML NodeList to a string
        @param node The node
        @return The string serialization of the node
        """
        stringIO = StringIO()
        for element in node:
            removeWhitespaceNode(element)
            if element.isinstance(etree.Element) or element.getTextContent().matches("\\s*"):
                stringIO.append(nodeToString(n));
        return stringIO

    def toRDF(self, parent: Resource = None):
        """
        Convert this element to RDF
        @param parent The node created by the element that called this, triples
        should be added to this resource
        """

class impIDLang(impID):

    def __init__(self, lang: str = "", mappings: Mappings = None):
        if lang is None or lang == "":
            if (mappings is not None and mappings.defaultLanguage is not None):
                self.lang = mappings.defaultLanguage
            else:
                self.lang = "en"
        else:
            self.lang = lang;
        super().__init__()

class NoteLinkInfo(impIDLang):
    
    def __init__(self, language: str = "", mappings: Mapping = None):
        super().__init__(language, mappings)
        self.References = list()
        self.AdminInfos = list()
        self.notes = list()
        self.Xreferences = list()
        self.Transactions = list()

    def toRDF(self, parent: Resource = None):
        for ref in self.References:
            ref.toRDF(parent)
        for adminInfo in self.AdminInfos:
            adminInfo.toRDF(parent)
        for note in self.notes:
            note.toRDF(parent)
        for xReference in self.Xreferences:
            xReference.toRDF(parent)
        for transac in self.Transactions:
            transac.toRDF(parent);

class Describable(NoteLinkInfo):

    # This interface corresponds to an XML Element in the tbx spec that can have auxInfo
    # where auxInfo is defined as follows
    
    # <!ENTITY % auxInfo '(descrip | descripGrp | admin | adminGrp | transacGrp | note | ref
    # | xref)*' >

    def __init__(self, language: str = "", mappings: Mapping = None):
        self.Descriptions = list()
        super().__init__(language, mappings)

    def toRDF(self, parent: Resource = None):
        super().toRDF(parent)
        for descrip in self.Descriptions:
            descrip.toRDF(parent)

class Term(Describable):

    # This class represents a Term
    # There are only two mandatory data categories in TBX-Basic: term, and language.

    def __init__(self):
        self.Lex_entries = dict()
        super().__init__()

    def Term(self):
        super(None, Mappings())


class NoteLinkInfo(impIDLang):

    def __init__(self):
        self.References = list()
        self.AdminInfos = list()
        self.notes = list()
        self.Xreferences = list()
        self.Transactions = list()
        super().__init__()

    def NoteLinkInfo(self, language: str = "", mappings: Mappings = None):
        super(language, mappings)

    def toRDF(self, parent: Resource = None):
        
        for ref in References:
            ref.toRDF(parent)
        for adminInfo in AdminInfos:
            adminInfo.toRDF(parent)
        for note in Notes:
            note.toRDF(parent)
        for xReference in Xreferences:
            xReference.toRDF(parent)
        for transac in Transactions:
            transac.toRDF(parent)
    

class LexicalEntry(Describable):

    def __init__(self, lemma: str = None, language: str = "", mappings: Mappings = None):

        # static LexicalEntry createFromSPARQL(String uri, Model model) {
        #     throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
        # }

        self.Decomposition = list()
        self.TermNotes = list()
        if lemma is not None:
            self.Lemma = lemma
        super().__init__(language, mappings)

    def getID(self):
        if self.id is not None:
            return self.id
        else:
            return self.Lemma+"-"+self.lang

    def toRDF(self, parent: Resource = None):
        
        term = self.getRes()
        
        super().toRDF(term)
    
        term.addProperty(RDF.type, ONTOLEX.LexicalEntry)

        # rlan = LexvoManager.mgr.getLexvoFromISO2(lang)
        # term.addProperty(DC.language, rlan) # before it was the mere constant "language"
        # term.addProperty(LIME.language, lang) # before it was the mere constant "language"
        
        # sense = getSubRes("Sense")

        # sense.addProperty(ONTOLEX.isLexicalizedSenseOf, parent)
        
        # term.addProperty(ONTOLEX.sense, sense)
        
        # sense.addProperty(RDF.type, ONTOLEX.SenseEntry)

        # canonicalForm = getSubRes(model, "CanonicalForm")

        # term.addProperty(ONTOLEX.canonicalForm, canonicalForm)

        # canonicalForm.addProperty(ONTOLEX.writtenRep, Lemma, lang)
        
        # for decomposition in Decomposition:
        #     decomposition.toRDF(model, term)
        # for note in TermNotes:
        #     note.toRDF(model, term)
