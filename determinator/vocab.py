

class DC():

    def __init__(self):

        self.rights = "http://purl.org/dc/terms/rights"
        self.source = "http://purl.org/dc/terms/source"
        self.attribution = "http://creativecommons.org/ns#attributionName"
        self.language = "http://purl.org/dc/terms/language"

class IATE():

    def __init__(self):

        self.rights = "http://iate.europa.eu/copyright.html"
        self.iate = "http://iate.europa.eu/"
        self.Lexicon = "http://tbx2rdf.lider-project.eu/data/iate#subjectField"

class LIME():

    def __init__(self):

        self.Lexicon = "http://www.w3.org/ns/lemon/lime#Lexicon"
        self.entry = "http://www.w3.org/ns/lemon/lime#entry"
        self.language = "http://www.w3.org/ns/lemon/lime#language"
    
class ONTOLEX():

    def __init__(self):
        
        self.lexicalizedSense = "http://www.w3.org/ns/lemon/ontolex#lexicalizedSense"
        self.writtenRep = "http://www.w3.org/ns/lemon/ontolex#writtenRep"
        self.sense = "http://www.w3.org/ns/lemon/ontolex#sense"
        self.canonicalForm = "http://www.w3.org/ns/lemon/ontolex#canonicalForm"
        self.constituent = "http://www.w3.org/ns/lemon/decomp#constituent"
        self.otherForm = "http://www.w3.org/ns/lemon/ontolex#otherForm"
        self.identifies = "http://www.w3.org/ns/lemon/decomp#identifies"
        self.reference = "http://www.w3.org/ns/lemon/ontolex#reference"
        self.LexicalEntry = "http://www.w3.org/ns/lemon/ontolex#LexicalEntry"
        self.SenseEntry = "http://www.w3.org/ns/lemon/ontolex#LexicalSense"
        self.Concept = "http://www.w3.org/ns/lemon/ontolex#LexicalConcept"
        self.isLexicalizedSenseOf = "http://www.w3.org/ns/lemon/ontolex#isLexicalizedSenseOf"
    
class PROVO():

    def __init__(self):
    
        self.Activity = "http://www.w3.org/ns/prov#Activity"
        self.Agent = "http://www.w3.org/ns/prov#Agent"
        self.wasGeneratedBy = "http://www.w3.org/ns/prov#wasGeneratedBy"
        self.endedAtTime = "http://www.w3.org/ns/prov#endedAtTime"
        self.wasAssociatedWith = "http://www.w3.org/ns/prov#wasAssociatedWith"

class SKOS():
    
    def __init__(self):
    
        self.Concept = "http://www.w3.org/2004/02/skos/core#Concept"
     
class TBX():

    def __init__(self):

        self.SkosConcept = "http://www.w3.org/2004/02/skos/core#Concept"

        self.Context = "http://tbx2rdf.lider-project.eu/tbx#Context"
        self.Descrip = "http://tbx2rdf.lider-project.eu/tbx#Descrip"
        self.MartifHeader = "http://tbx2rdf.lider-project.eu/tbx#MartifHeader"
        self.Admin = "http://tbx2rdf.lider-project.eu/tbx#Admin"
        self.TermNote = "http://tbx2rdf.lider-project.eu/tbx#TermNote"
        self.Transaction = "http://tbx2rdf.lider-project.eu/tbx#transaction"
        self.SubjectField = "http://tbx2rdf.lider-project.eu/tbx#SubjectField"
        self.description = "http://tbx2rdf.lider-project.eu/tbx#description"
        self.target = "http://tbx2rdf.lider-project.eu/tbx#target"
        self.type = "http://tbx2rdf.lider-project.eu/tbx#type"
        self.context = "http://tbx2rdf.lider-project.eu/tbx#context"
        self.value = "http://tbx2rdf.lider-project.eu/tbx#value"
        self.status = "http://tbx2rdf.lider-project.eu/tbx#status"
        self.definition = "http://tbx2rdf.lider-project.eu/tbx#definition"
        self.source = "http://tbx2rdf.lider-project.eu/tbx#source"
        self.xref = "http://tbx2rdf.lider-project.eu/tbx#xreference"
        self.datatype = "http://tbx2rdf.lider-project.eu/tbx#datatype"
        self.language = "http://tbx2rdf.lider-project.eu/tbx#language"
        self.note = "http://tbx2rdf.lider-project.eu/tbx#note"
        self.encodingDesc = "http://tbx2rdf.lider-project.eu/tbx#encodingDesc"
        self.revisionDesc = "http://tbx2rdf.lider-project.eu/tbx#revisionDesc"
        self.publicationStmt = "http://tbx2rdf.lider-project.eu/tbx#publicationStmt"
        self.sourceDesc = "http://tbx2rdf.lider-project.eu/tbx#sourceDesc"
        self.admin = "http://tbx2rdf.lider-project.eu/tbx#admin"
        self.termNote = "http://tbx2rdf.lider-project.eu/tbx#termNote"
        self.transaction = "http://tbx2rdf.lider-project.eu/tbx#transaction"
        self.reliabilityCode = "http://tbx2rdf.lider-project.eu/tbx#reliabilityCode"
        self.termType = "http://www.lexinfo.net/ontology/2.0/lexinfo#termType"
        self.partOfSpeech = "http://tbx2rdf.lider-project.eu/tbx#partOfSpeech"
        self.grammaticalNumber = "http://tbx2rdf.lider-project.eu/tbx#grammaticalNumber"
        self.transactionType = "http://tbx2rdf.lider-project.eu/tbx#transactionType"
         
        self.reliabilityCode1 = "http://tbx2rdf.lider-project.eu/tbx#reliabilityCode1"
        self.reliabilityCode2 = "http://tbx2rdf.lider-project.eu/tbx#reliabilityCode2"
        self.reliabilityCode3 = "http://tbx2rdf.lider-project.eu/tbx#reliabilityCode3"
        self.reliabilityCode4 = "http://tbx2rdf.lider-project.eu/tbx#reliabilityCode4"
        self.reliabilityCode5 = "http://tbx2rdf.lider-project.eu/tbx#reliabilityCode5"
        self.reliabilityCode6 = "http://tbx2rdf.lider-project.eu/tbx#reliabilityCode6"
        self.reliabilityCode7 = "http://tbx2rdf.lider-project.eu/tbx#reliabilityCode7"
        self.reliabilityCode8 = "http://tbx2rdf.lider-project.eu/tbx#reliabilityCode8"
        self.reliabilityCode9 = "http://tbx2rdf.lider-project.eu/tbx#reliabilityCode9"
        self.reliabilityCode10 = "http://tbx2rdf.lider-project.eu/tbx#reliabilityCode10"
        self.noun = "http://tbx2rdf.lider-project.eu/tbx#noun"
        self.properNoun = "http://tbx2rdf.lider-project.eu/tbx#properNoun"
        self.adverb = "http://tbx2rdf.lider-project.eu/tbx#adverb"
        self.adjective = "http://tbx2rdf.lider-project.eu/tbx#adjective"
        self.verb = "http://tbx2rdf.lider-project.eu/tbx#verb"
        self.other = "http://tbx2rdf.lider-project.eu/tbx#other"
        self.singular = "http://tbx2rdf.lider-project.eu/tbx#singular"
        self.plural = "http://tbx2rdf.lider-project.eu/tbx#plural"
         
        # Adds the most common prefixes to the generated model
        # def addPrefixesToModel(self):

        #     model.setNsPrefix("tbx", "http://tbx2rdf.lider-project.eu/tbx#")
        #     model.setNsPrefix("ontolex", "http://www.w3.org/ns/lemon/ontolex#")
        #     model.setNsPrefix("skos", "http://www.w3.org/2004/02/skos/core#")
        #     model.setNsPrefix("odrl", "http://www.w3.org/ns/odrl/2/")
        #     model.setNsPrefix("dct", "http://purl.org/dc/terms/")
        #     model.setNsPrefix("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        #     model.setNsPrefix("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
        #     model.setNsPrefix("cc", "http://creativecommons.org/ns#")
        #     model.setNsPrefix("ldr", "http://purl.oclc.org/NET/ldr/ns#")
        #     model.setNsPrefix("void", "http://rdfs.org/ns/void#")
        #     model.setNsPrefix("dcat", "http://www.w3.org/ns/dcat#")
        #     model.setNsPrefix("prov", "http://www.w3.org/ns/prov#")
        #     model.setNsPrefix("decomp", "http://www.w3.org/ns/lemon/decomp#")
        
