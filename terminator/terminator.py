"""Main module."""

from lxml import etree
import xlsxwriter
from io import StringIO
import nafigator

NAMESPACES = {
    None: "urn:iso:std:iso:30042:ed-2",
}
RELAXNG_TBX_BASIC = 'href="https://raw.githubusercontent.com/LTAC-Global/TBX-Core_dialect/master/Schemas/TBXcoreStructV03_TBX-Basic_integrated.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"'
SCHEMA_TBX_BASIC = 'href="https://raw.githubusercontent.com/LTAC-Global/TBX-Core_dialect/master/Schemas/TBX-Basic.sch" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"'

XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"

TBXHEADER = "tbxHeader"
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


class TbxDocument(etree._ElementTree):
    """The TbxDocument class"""

    def generate(self, params: dict = {}):
        """Initialize a TbxDocument with data from the params dict"""
        self._setroot(
            etree.Element(
                "tbx", attrib={"type": "TBX-Basic", "style": "dca"}, nsmap=NAMESPACES
            )
        )
        pi1 = etree.ProcessingInstruction("xml-model", RELAXNG_TBX_BASIC)
        pi2 = etree.ProcessingInstruction("xml-model", SCHEMA_TBX_BASIC)
        self.getroot().addprevious(pi1)
        self.getroot().addprevious(pi2)
        self.set_language("en")
        self.setup_tbx(params)
        return None

    def open(self, input: str):
        """Function to open a TbxDocument

        Args:
            input: the location of the TbxDocument to be opened

        Returns:
            NafDocument: the TbxDocument that is opened

        """
        with open(input, "r", encoding="utf-8") as f:
            self._setroot(etree.parse(f).getroot())
        return self

    def setup_tbx(self, params: dict = {}):
        """ """
        sub = etree.SubElement(self.getroot(), TBXHEADER)
        filedesc = etree.SubElement(sub, QName(name=FILEDESC))

        if TITLE in params.keys():
            s = etree.SubElement(filedesc, QName(name="titleStmt"))
            p = etree.SubElement(s, QName(name=TITLE))
            p.text = params.get(TITLE)

        if SOURCEDESC in params.keys():
            s = etree.SubElement(filedesc, QName(name=SOURCEDESC))
            p = etree.SubElement(s, QName(name="p"))
            p.text = params.get(SOURCEDESC)

        text = etree.SubElement(self.getroot(), QName(name=TEXT))
        body = etree.SubElement(text, QName(name=BODY))

    @property
    def concepts_list(self):
        concepts = []
        for xml_concept in self.findall("text/body/conceptEntry", namespaces=NAMESPACES):
            concept = {}
            concept['id'] = xml_concept.attrib["id"]
            concept['lang'] = {}
            for xml_lang_sec in xml_concept:
                if xml_lang_sec.tag == QName(name="langSec"):
                    lang = xml_lang_sec.attrib[XML_LANG]
                    concept['lang'][lang] = list()
                    for xml_term_sec in xml_lang_sec:
                        termsec = list()
                        for item in xml_term_sec:
                            termsec.append(
                                {
                                    "type": etree.QName(item.tag).localname,
                                    "attr": item.attrib,
                                    "text": item.text})
                        concept['lang'][lang].append(termsec)
                else:
                    concept[etree.QName(xml_lang_sec.tag).localname] = {
                                    "attr": xml_lang_sec.attrib,
                                    "text": xml_lang_sec.text}
            concepts.append(concept)
        return concepts        

    @property
    def concepts_dict(self):
        d = {}
        for concept in self.concepts_list:
            for lang in concept['lang'].values():
                terms = [item['text'] for termsec in lang for item in termsec if item['type']=="term"]
                termnotes = [item for termsec in lang for item in termsec if item['type']=="termNote"]
                refs = [item for termsec in lang for item in termsec if item['type']=="ref"]
            termnotes = {termnote['attr']['type']: termnote['text'] for termnote in termnotes}
            refs = [ref['text'] for ref in refs]
            for term in terms:
                d[term] = [termnotes]
        return d

    def add_conceptEntry(self, concept: dict = {}, params: dict = {}):
        """ """
        body = self.find(TEXT + "/" + BODY, namespaces=NAMESPACES)
        concept_id = concept["id"]
        concept_langSec = concept["langSec"]

        concept_entry = etree.SubElement(
            body, QName(name="conceptEntry"), attrib={"id": concept_id}
        )
        concept_descrip = concept.get("descrip", None)
        if concept_descrip is not None:
            descrip = etree.SubElement(
                concept_entry,
                QName(name="descrip"),
                attrib=concept_descrip,
            )
        for lang in concept_langSec.keys():
            lang_sec = etree.SubElement(
                concept_entry,
                QName(name="langSec"),
                attrib={XML_LANG: lang},
            )
            items = concept_langSec[lang]
            term_sec = etree.SubElement(lang_sec, QName(name="termSec"))
            for item in items:
                term = etree.SubElement(
                    term_sec,
                    QName(name=item.get("type")),
                    attrib=item.get("attr", None),
                )
                term.text = item.get("text", None)

    def set_language(self, language: str):
        """Set language of the TbxDocument"""
        self.getroot().set(XML_LANG, language)

    def validate(self, validation_file: str=None):
        if validation_file is not None:
            if validation_file[-3:].lower()=="rng":
                stream = open(validation_file)
                relaxng = etree.RelaxNG(etree.parse(stream))
                success = relaxng.validate(self.getroot())
                if not success:
                    print(relaxng.error_log)
                return success
        return None

    def write(self, output: str):
        """Function to write a TbxDocument

        Args:
            output: the location of the TbxDocument to be stored

        Returns:
            None

        """
        super().write(output, encoding="utf-8", pretty_print=True, xml_declaration=True)

    def copy_terms_from_tbx(
        self, terms: dict = {}, reference = None, prefix: str = "", params: dict = {}
    ):
        """ 
        This function adds references to the current TbxDocument from another TbXDocument
        for example a IATE tbx-file if the term text of a concept coincides

        """

        # def most_appropriate(l: list = []):

        #     relevance = 0
        #     for item in l:
        #         subject = item['descrip']['text']
        #         if 'insurance' in subject.lower():
        #             result = item
        #             relevance = 10
        #         if ('finance' in subject.lower()) or ('accounting' in subject.lower()):
        #             if relevance < 8:
        #                 result = item
        #                 relevance = 8
        #         if 'economics' in subject.lower():
        #             if relevance < 6:
        #                 result = item
        #                 relevance = 6
        #         if ('law' in subject.lower()) or ('EU act' in subject.lower()):
        #             if relevance < 4:
        #                 result = item
        #                 relevance = 4
        #         if 'statistics' in subject.lower():
        #             if relevance < 2:
        #                 result = item
        #                 relevance = 2
        #         if 'credit policy' in subject.lower():
        #             if relevance < 1:
        #                 result = item
        #                 relevance = 1
        #         if relevance == 0:
        #             result = item

        #     return result

        reference_concepts = {}
        for item in reference.concepts_list:
            for language in item['lang'].keys():
                if language not in reference_concepts.keys():
                    reference_concepts[language] = {}
                for termsec in item['lang'][language]:
                    for term in termsec:
                        if term['text'].lower() in reference_concepts[language].keys():
                            reference_concepts[language][term['text'].lower()].append(item)
                        else:
                            reference_concepts[language][term['text'].lower()] = [item]

        added_references = dict()

        body = self.find(TEXT + "/" + BODY, namespaces=NAMESPACES)
        count = len(body)+1
        for key in terms.keys():
            language = terms[key]['dc:language']
            if key in reference_concepts[language].keys():
                # found = most_appropriate(nl_concepts[key])
                for found in reference_concepts[language][key]:
                    if found['id'] in added_references.keys():
                        concept_entry = added_references[found['id']]
                        for langSec in concept_entry:
                            if langSec.tag == QName(name="langSec") and langSec.attrib.get(XML_LANG, "") == language:
                                for termSec in langSec:
                                    for item in termSec:
                                        if key == item.text.lower():
                                            pos_el = etree.SubElement(termSec, QName(name="termNote"), {"type": "partOfSpeech"})
                                            pos_el.text = ", ".join(terms[key]['partOfSpeech']).lower()
                                            count_el = etree.SubElement(termSec, QName(name="note"), {})
                                            count_el.text = "source: " + str(terms[key]['dc:source']['{http://purl.org/dc/elements/1.1/}uri']) + " (#hits="+str(terms[key]['count'])+")"
                    else:
                        concept_entry = etree.SubElement(
                            body, QName(name="conceptEntry"), attrib={"id": str(count)}
                        )
                        descrip = etree.SubElement(concept_entry, QName(name="descrip"), found['descrip']['attr'])
                        descrip.text = str(found['descrip']['text'])
                        note = etree.SubElement(concept_entry, QName(name="xref"))
                        note.text = prefix + str(found['id'])
                        note = etree.SubElement(concept_entry, QName(name="ref"))
                        note.text = "https://iate.europa.eu/entry/result/"+str(found['id']+"/en")
                        for lang in found['lang'].keys():
                            langSec = etree.SubElement(concept_entry, QName(name="langSec"), {XML_LANG: lang})
                            for item in found['lang'][lang]:
                                termSec = etree.SubElement(langSec, QName(name="termSec"))                    
                                for item2 in item:
                                    term_item = etree.SubElement(termSec, QName(name=item2.get('type', "empty")), item2.get('attr', {}))
                                    term_item.text = item2['text']
                                    if langSec.tag == QName(name="langSec") and langSec.attrib.get(XML_LANG, "") == language:
                                        if key == item2['text'].lower():
                                            pos_el = etree.SubElement(termSec, QName(name="termNote"), {"type": "partOfSpeech"})
                                            pos_el.text = ", ".join(terms[key]['partOfSpeech']).lower()
                                            count_el = etree.SubElement(termSec, QName(name="note"), {})
                                            count_el.text = "source: " + str(terms[key]['dc:source']['{http://purl.org/dc/elements/1.1/}uri']) + " (#hits="+str(terms[key]['count'])+")"

                        count += 1
                        added_references[found['id']] = concept_entry
            else:
                # not found
                if language == "nl":
                    concept_entry = etree.SubElement(
                        body, QName(name="conceptEntry"), attrib={"id": str(count)}
                    )
                    count += 1
                    descrip = etree.SubElement(concept_entry, QName(name="descrip"))
                    descrip.text = "Unknown"
                    langSec = etree.SubElement(concept_entry, QName(name="langSec"), {XML_LANG: "nl"})
                    termSec = etree.SubElement(langSec, QName(name="termSec"))                  
                    term_item = etree.SubElement(termSec, QName(name="term"))
                    term_item.text = key
                    term_item = etree.SubElement(termSec, QName(name="termNote"), {"type": "language-planningQualifier"})
                    term_item.text = "newTerm"
                    pos_el = etree.SubElement(termSec, QName(name="termNote"), {"type": "partOfSpeech"})
                    pos_el.text = ", ".join(terms[key]['partOfSpeech']).lower()
                    count_el = etree.SubElement(termSec, QName(name="note"), {})
                    count_el.text = "source: " + str(terms[key]['dc:source']['{http://purl.org/dc/elements/1.1/}uri']) + " (#hits="+str(terms[key]['count'])+")"
            # concept_id = concept.attrib["id"]
            # found = None
            # for item in concept:
            #     if item.tag == QName(name="langSec"):
            #         if item.attrib.get(XML_LANG, None) == "nl":
            #             for item2 in item: #termsec
            #                 for item3 in item2: #termsec item
            #                     if item3.tag == QName(name="term"):
            #                         if item3.text in nl_concepts.keys():
            #                             found = nl_concepts[item3.text]
            #                             found_text = item3.text
            # if found is not None:
            #     descrip = etree.SubElement(concept, QName(name="descrip"), found['descrip']['attr'])
            #     descrip.text = str(found['descrip']['text'])
            #     note = etree.SubElement(concept, QName(name="xref"))
            #     note.text = prefix + str(nl_concepts[found_text]['id'])
            #     for lang in found['lang'].keys():
            #         langSec = etree.SubElement(concept, QName(name="langSec"), {XML_LANG: lang})
            #         for item in found['lang'][lang]:
            #             termSec = etree.SubElement(langSec, QName(name="termSec"))                    
            #             for item2 in item:
            #                 term_item = etree.SubElement(termSec, QName(name=item2.get('type', "empty")), item2.get('attr', {}))
            #                 term_item.text = item2['text']

    def add_termnotes_from_tbx(
        self, reference=None, params: dict = {}
    ):
        """ 
        This functions add termnotes to the current TbxDocument from another TbXDocument
        for example a lassy tbx-file

        """
        reference = reference.concepts_dict

        def retrieve_component_data(parts: list=[], reference: dict={}, pos: str=""):
            norm_parts = [part if part[-1]=="-" else part+"-" for part in parts[:-1]]+[parts[-1]]
            if all([(part in reference.keys()) for part in norm_parts]):
                ref_components = [ref_pos for ref_pos in reference[norm_parts[-1]] if ref_pos['partOfSpeech'] == pos]
                if ref_components != []:
                    full_lemma = "_".join(parts[:-1])+("" if len(parts)>1 else "")+ref_components[0]['lemma']
                    full_morphoFeats = ref_components[0]['morphoFeats']
                    return (full_lemma,
                            full_morphoFeats,
                            norm_parts)
            return None

        number_of_word_components = params.get("number_of_word_components", 4)

        for concept in self.findall("text/body/conceptEntry", namespaces=NAMESPACES):
            concept_id = concept.attrib["id"]
            for item in concept:
                if item.tag == QName(name="langSec"):
                    if item.attrib.get(XML_LANG, "") == "nl":
                        for item2 in item: # termsec
                            original_term_pos = None
                            for item3 in item2:
                                if item3.tag == QName(name="termNote") and item3.attrib['type']=="partOfSpeech":
                                    original_term_pos = item3.text.split(", ")

                            for item3 in item2:
                                if item3.tag == QName(name="term") and original_term_pos is not None:
                                    term_text = item3.text
                                    components_completely_found = []

                                    for component_idx, component in enumerate(term_text.split(" ")):
                                        
                                        original_pos = original_term_pos[component_idx]
                                        data = None
                                        # first the complete term
                                        parts = [component]
                                        data = retrieve_component_data(parts=parts, reference=reference, pos=original_pos)
                                        if data is None and number_of_word_components >= 2: 
                                            i = 2
                                            while (i < len(component) - 2) and data is None:
                                                parts = [component[:i], component[i:]]
                                                data = retrieve_component_data(parts=parts, reference=reference, pos=original_pos)
                                                i += 1
                                        if data is None and number_of_word_components >= 3: 
                                            i = 2
                                            while (i < len(component) - 2) and data is None:
                                                j = 2
                                                while (j < i) and data is None:
                                                    parts = [component[:j], component[j:i], component[i:]]
                                                    data = retrieve_component_data(parts=parts, reference=reference, pos=original_pos)
                                                    j += 1
                                                i += 1
                                        if data is None and number_of_word_components >= 4: 
                                            i = 2
                                            while (i < len(component) - 2) and data is None:
                                                j = 2
                                                while (j < i) and data is None:
                                                    k = 2
                                                    while (k < j) and data is None:
                                                        parts = [component[:k], component[k:j], component[j:i], component[i:]]
                                                        data = retrieve_component_data(parts=parts, reference=reference, pos=original_pos)
                                                        k += 1
                                                    j += 1
                                                i += 1
                                        if data is None and number_of_word_components >= 5: 
                                            i = 2
                                            while (i < len(component) - 2) and data is None:
                                                j = 2
                                                while (j < i) and data is None:
                                                    k = 2
                                                    while (k < j) and data is None:
                                                        l = 2
                                                        while (l < k) and data is None:
                                                            parts = [component[:l], component[l:k], component[k:j], component[j:i], component[i:]]
                                                            data = retrieve_component_data(parts=parts, reference=reference, pos=original_pos)
                                                            l += 1
                                                        k += 1
                                                    j += 1
                                                i += 1
                                        components_completely_found.append(data)

                                    if all([component is not None for component in components_completely_found]):
                                        note = etree.SubElement(item2, QName(name="termNote"), attrib={"type": "lemma"})
                                        note.text = " ".join(c[0] for c in components_completely_found)
                                        note = etree.SubElement(item2, QName(name="termNote"), attrib={"type": "grammaticalNumber"})
                                        if ",ev," in components_completely_found[-1][1]:
                                            note.text = "singular"
                                        elif ",mv," in components_completely_found[-1][1]:
                                            note.text = "plural"
                                        termgroup = etree.SubElement(item2, QName(name="termNoteGrp"))
                                        components = [c[2] for c in components_completely_found]
                                        for c in components:
                                            for cc in c:
                                                note = etree.SubElement(termgroup, QName(name="termNote"), attrib={"type": "component"})
                                                note.text = cc

    def to_excel(self, output: str):
        """Function to write a TbxDocument to Excel

        Args:
            output: the location of the Excel to be stored

        Returns:
            None

        """
        body = self.find(TEXT + "/" + BODY)
        wb = xlsxwriter.Workbook(output)
        worksheet = wb.add_worksheet("Tbx")
        worksheet.write_row(0, 0, ["id", "dc:language", "term", "termType", "partOfSpeech", "grammaticalNumber", "xref"])
        row = 1
        for concept in self.findall("text/body/conceptEntry", namespaces=NAMESPACES):
            for lang_sec in concept:
                for term_sec in lang_sec:
                    term_text = ""
                    term_type = ""
                    term_pos = ""
                    term_number = ""
                    term_xref = ""
                    for item in term_sec:
                        if item.tag == QName(name="term"):
                            term_text = item.text
                        if item.tag == QName(name="termNote") and item.attrib['type']=='termType':
                            term_type = item.text
                        if item.tag == QName(name="termNote") and item.attrib['type']=='partOfSpeech':
                            term_pos = item.text
                        if item.tag == QName(name="termNote") and item.attrib['type']=='grammaticalNumber':
                            term_number = item.text
                        if item.tag == QName(name="xref"):
                            term_xref = item.text
                    worksheet.write_row(
                        row,
                        0,
                        [
                            concept.attrib["id"],
                            lang_sec.attrib[XML_LANG],
                            term_text,
                            term_type,
                            term_pos,
                            term_number,
                            term_xref
                        ],
                    )
                    row += 1
        wb.close()

