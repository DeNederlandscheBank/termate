"""Main module."""

from lxml import etree
import xlsxwriter
from io import StringIO
import nafigator

NAMESPACES = {
    None: "urn:iso:std:iso:30042:ed-2",
}
TBX_CORE = 'href="https://raw.githubusercontent.com/LTAC-Global/TBX-Core_dialect/master/Schemas/TBXcoreStructV03_TBX-Core_integrated.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"'
SCHEMATRON_CORE = 'href="https://raw.githubusercontent.com/LTAC-Global/TBX-Core_dialect/master/Schemas/TBX-Core.sch" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"'
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"

TBXHEADER = "tbxHeader"
FILEDESC = "fileDesc"
SOURCEDESC = "sourceDesc"
TEXT = "text"
BODY = "body"
TITLE = "title"

ILLEGAL_TERM_CHARACTERS = ["„", "”", ">", "<", ",", "α", "β", "σ", "ð", "þ", "%", "δ"]

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
                "tbx", attrib={"type": "TBX-Core", "style": "dca"}, nsmap=NAMESPACES
            )
        )
        pi1 = etree.ProcessingInstruction("xml-model", TBX_CORE)
        pi2 = etree.ProcessingInstruction("xml-model", SCHEMATRON_CORE)
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
            for xml_lang_sec in xml_concept:
                lang = xml_lang_sec.attrib[XML_LANG]
                concept['lang'] = {lang: list()}
                for xml_term_sec in xml_lang_sec:
                    for item in xml_term_sec:
                        concept['lang'][lang].append(
                            {
                                "type": etree.QName(item.tag).localname,
                                "attr": item.attrib,
                                "text": item.text})
            concepts.append(concept)
        return concepts        

    @property
    def concepts_dict(self):
        d = {}
        for concept in self.concepts_list:
            for lang in concept['lang'].values():
                terms = [item['text'] for item in lang if item['type']=="term"]
                termnotes = [item for item in lang if item['type']=="termNote"]
            termnotes = {term_note['attr']['type']: term_note['text'] for term_note in termnotes}
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

    def validate(self, validation_file: str=""):
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

    def extract_terms(self, doc: nafigator.NafDocument = None, params: dict = {}):
        """Function to extract terms from a NafDocument and add the terms to TbxDocument

        Args:
            output:

        Returns:
            None

        """
        patterns = [["NOUN"], 
                    ["ADJ", "NOUN"],
                    ["ADJ", "NOUN", "NOUN"],
                    ["ADJ", "ADJ", "NOUN"],
                    ]
        if doc is not None:
            d = {}
            for pattern in patterns:
                terms = nafigator.get_terms(pattern, doc)
                for term in terms:
                    if not any(
                        [
                            ((s in component) or (s == component))
                            for component in term
                            for s in ILLEGAL_TERM_CHARACTERS
                        ]) and "\xad"!=term[-1][-1] and "-"!=term[-1][-1] and "-"!=term[0][0] and not any([len(component)==1 for component in term]):
                        concept_text = " ".join(term)
                        concept_text = concept_text.replace(" \xad ", "")
                        concept_text = concept_text.replace("\xad ", "")
                        concept_text = concept_text.replace(" \xad", "")
                        concept_text = concept_text.replace("\xad", "")
                        if concept_text in d.keys():
                            d[concept_text]['count'] += 1
                        else:
                            d[concept_text] = {"count": 1, "partOfSpeech": pattern}

        for idx, concept_text in enumerate(d.keys()):
            concept = {
                "id": "c" + str(idx),
                "langSec": {
                    "nl": [
                        {"type": "term", "text": concept_text},
                        {
                            "type": "termNote",
                            "attr": {"type": "termType"},
                            "text": "fullForm",
                        },
                        {
                            "type": "termNote",
                            "attr": {"type": "partOfSpeech"},
                            "text": ", ".join(d[concept_text]['partOfSpeech']),
                        },
                        {
                            "type": "note",
                            "text": "extracted from: "
                            + str(doc.header["fileDesc"]["filename"])
                            + " (#hits="
                            + str(d[concept_text]['count'])
                            + ")",
                        },
                    ]
                },
            }
            self.add_conceptEntry(concept, params)

    def add_references_from_tbx(
        self, reference = None, prefix: str = "", params: dict = {}
    ):
        """ 
        This function adds references to the current TbxDocument from another TbXDocument
        for example a IATE tbx-file if the term text of a concept coincides

        """
        concepts = {}
        for concept in reference.findall("text/body/conceptEntry", namespaces=NAMESPACES):
            for item in concept.findall("langSec/termSec/term", namespaces=NAMESPACES):
                concepts[item.text] = concept.attrib["id"]

        for concept in self.findall("text/body/conceptEntry", namespaces=NAMESPACES):
            concept_id = concept.attrib["id"]
            for item in concept:
                if item.tag == "{urn:iso:std:iso:30042:ed-2}langSec":
                    if item.attrib.get(XML_LANG, "") == "nl":
                        for item2 in item:
                            for item3 in item2:
                                if item3.tag == "{urn:iso:std:iso:30042:ed-2}term":
                                    if item3.text in concepts.keys():
                                        note = etree.SubElement(item2, QName(name="ref"))
                                        note.text = prefix + str(
                                            concepts[item3.text]
                                        )

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
                if item.tag == "{urn:iso:std:iso:30042:ed-2}langSec":
                    if item.attrib.get(XML_LANG, "") == "nl":
                        for item2 in item:
                            for item3 in item2:
                                if item3.tag == "{urn:iso:std:iso:30042:ed-2}termNote" and item3.attrib['type']=="partOfSpeech":
                                    original_term_pos = item3.text.split(", ")

                            for item3 in item2:
                                if item3.tag == "{urn:iso:std:iso:30042:ed-2}term":
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
                                        note = etree.SubElement(item2, QName(name="termNote"), attrib={"type": "morphoFeats"})
                                        note.text = ", ".join(c[1] for c in components_completely_found)
                                        components = [c[2] for c in components_completely_found]
                                        for c in components:
                                            for cc in c:
                                                note = etree.SubElement(item2, QName(name="termNote"), attrib={"type": "component"})
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
        worksheet.write_row(0, 0, ["id", "language", "term", "notes"])
        row = 1
        for concept_entry in body:
            for lang_sec in concept_entry:
                for term_sec in lang_sec:
                    notes = []
                    for item in term_sec:
                        if item.tag == "term":
                            term = item.text
                        if item.tag == "note":
                            notes.append(item.text)
                    worksheet.write_row(
                        row,
                        0,
                        [
                            concept_entry.attrib["id"],
                            lang_sec.attrib[XML_LANG],
                            term,
                        ]
                        + notes,
                    )
                    row += 1
        wb.close()

