"""Main module."""

from lxml import etree
import xlsxwriter
from io import StringIO
import nafigator
import logging
from collections import defaultdict
from copy import deepcopy

from .const import NAMESPACES
from .const import XML_LANG
from .const import RELAXNG_TBX_BASIC
from .const import SCHEMA_TBX_BASIC
from .const import TBX_HEADER
from .const import FILEDESC
from .const import SOURCEDESC
from .const import TEXT
from .const import BODY
from .const import TITLE
from .const import QName

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
            the TbxDocument that is opened

        """
        with open(input, "r", encoding="utf-8") as f:
            self._setroot(etree.parse(f).getroot())
        return self

    def setup_tbx(self, params: dict = {}):
        """ """
        sub = etree.SubElement(self.getroot(), TBX_HEADER)
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

    def clean(self, params: dict = {}):
        for xml_concept in self.findall(
            "text/body/conceptEntry", namespaces=NAMESPACES
        ):
            if not any([element.tag == QName(name="langSec") for element in xml_concept]):
                parent = xml_concept.getparent()
                parent.remove(xml_concept)

    @property
    def header(self):
        """Returns header of the TBX document as a dict"""
        header = dict()
        for child in self.find(TBX_HEADER, namespaces=NAMESPACES):
            if child.tag == QName(name="fileDesc"):
                header["fileDesc"] = {}
                for child2 in child:
                    if child2.tag == QName(name="sourceDesc"):
                        header["fileDesc"]['sourceDesc'] = {}
                        for child3 in child2:
                            if child3.tag == QName(name="p"):
                                header["fileDesc"]['sourceDesc']['p'] = child3.text
            if child.tag == QName(name="public"):
                header["public"] = dict(child.attrib)
        return header

    @property
    def concepts_list(self):
        concepts = []
        for xml_concept in self.findall(
            "text/body/conceptEntry", namespaces=NAMESPACES
        ):
            concept = {}
            concept["id"] = xml_concept.attrib["id"]
            concept["lang"] = {}
            for xml_lang_sec in xml_concept:
                if xml_lang_sec.tag == QName(name="langSec"):
                    lang = xml_lang_sec.attrib[XML_LANG]
                    concept["lang"][lang] = list()
                    for xml_term_sec in xml_lang_sec:
                        termsec = list()
                        for item in xml_term_sec:
                            termsec.append(
                                {
                                    "type": etree.QName(item.tag).localname,
                                    "attr": item.attrib,
                                    "text": item.text,
                                }
                            )
                        concept["lang"][lang].append(termsec)
                else:
                    concept[etree.QName(xml_lang_sec.tag).localname] = {
                        "attr": xml_lang_sec.attrib,
                        "text": xml_lang_sec.text,
                    }
            concepts.append(concept)
        return concepts

    @property
    def concepts_dict(self):
        d = {}
        for concept in self.concepts_list:
            for lang in concept["lang"].values():
                terms = [
                    item["text"]
                    for termsec in lang
                    for item in termsec
                    if item["type"] == "term"
                ]
                termnotes = [
                    item
                    for termsec in lang
                    for item in termsec
                    if item["type"] == "termNote"
                ]
                refs = [
                    item
                    for termsec in lang
                    for item in termsec
                    if item["type"] == "ref"
                ]
            termnotes = {
                termnote["attr"]["type"]: termnote["text"] for termnote in termnotes
            }
            refs = [ref["text"] for ref in refs]
            for term in terms:
                if term not in d.keys():
                    d[term] = [termnotes]
                else:
                    d[term].append(termnotes)
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

    def validate(self, validation_file: str = None):
        if validation_file is not None:
            if validation_file[-3:].lower() == "rng":
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

    def create_tbx_from_terms_dict(self, terms: dict = {}, params: dict = {}):
        """ """

        concept_id_prefix = params.get('concept_id_prefix', 'tbx_')

        def add_termNotes(term_section, term_notes):

            for freq_idx, uri in enumerate(term_notes["dc:uri"]):
                frequency_el = etree.SubElement(
                    term_section, QName(name="termNote"), {"type": "termFrequency"}
                )
                frequency_el.text = uri + ":" + str(term_notes["frequency"][freq_idx])

            for term_type in term_notes.keys():
                if term_type not in ["frequency", "dc:uri", "dc:format", "dc:language"]:
                    term_el = etree.SubElement(
                        term_section, QName(name="termNote"), {"type": term_type}
                    )
                    term_el.text = str(term_notes[term_type])

        body = self.find(TEXT + "/" + BODY, namespaces=NAMESPACES)
        count = len(body) + 1
        for term_text in terms.keys():
            language = terms[term_text]["dc:language"]
            concept = etree.SubElement(
                body, QName(name="conceptEntry"), attrib={"id": concept_id_prefix + str(count)}
            )
            count += 1
            descrip = etree.SubElement(
                concept, QName(name="descrip"), {"type": "subjectField"}
            )
            descrip.text = params.get("default_domain", "Domain code not specified")
            lang_section = etree.SubElement(
                concept, QName(name="langSec"), {XML_LANG: language}
            )
            term_section = etree.SubElement(lang_section, QName(name="termSec"))
            term_item = etree.SubElement(term_section, QName(name="term"))
            term_item.text = term_text
            add_termNotes(term_section, terms[term_text])
            term_item = etree.SubElement(
                term_section,
                QName(name="termNote"),
                {"type": "language-planningQualifier"},
            )
            term_item.text = params.get("default_language-planningQualifier", "newTerm")

    def copy_from_tbx(self, reference=None, params: dict = {}):
        """
        This function adds references to the current TbxDocument from another TbXDocument
        for example a IATE tbx-file if the term text of a concept coincides

        """

        reference_concepts = {}
        for concept in reference.concepts_list:
            for language in concept["lang"].keys():
                if language not in reference_concepts.keys():
                    reference_concepts[language] = {}
                for term_section in concept["lang"][language]:
                    for term in term_section:
                        term_text = term["text"].lower()
                        if term_text in reference_concepts[language].keys():
                            reference_concepts[language][term_text].append(concept)
                        else:
                            reference_concepts[language][term_text] = [concept]

        body = self.find(TEXT + "/" + BODY, namespaces=NAMESPACES)
        for concept in body:
            concept_id = concept.attrib["id"]
            for element in concept:
                if element.tag == QName(name="langSec"):
                    language = element.attrib.get(XML_LANG, "")
                    for termSec in element:
                        for item in termSec:
                            if item.tag == QName(name="term"):
                                term_text = item.text
                                if term_text in reference_concepts[language].keys():
                                    refs = reference_concepts[language][term_text]
                                    for ref in refs:
                                        note = etree.SubElement(
                                            termSec,
                                            QName(name="xref"),
                                            {
                                                "type": "externalCrossReference",
                                                "target": "https://iate.europa.eu/entry/result/"
                                                + str(ref["id"] + "/en"),
                                            },
                                        )
                                        note.text = str(ref["id"])

        self.combine_concepts(reference, params)
        self.clean(params)

    def combine_concepts(self, reference=None, params: dict = {}):

        body = self.find(TEXT + "/" + BODY, namespaces=NAMESPACES)

        # create a dictionary with the xref and the langSec of the xref
        d = defaultdict(list)
        for concept in body:
            concept_id = concept.attrib["id"]
            for langSec in concept:
                if langSec.tag == QName(name="langSec"):
                    for termSec in langSec:
                        for item in termSec:
                            if item.tag == QName(name="xref"):
                                d[item.text].append(langSec)

        reference_concepts = {
            concept["id"]: concept for concept in reference.concepts_list
        }

        count = len(body)
        for key in d.keys():

            unique_languages = set(
                [langSec.attrib.get(XML_LANG, []) for langSec in d[key]]
            )

            if len(unique_languages) > 1 and "nl" in unique_languages:

                concept = etree.SubElement(
                    body, QName(name="conceptEntry"), attrib={"id": "iate:" + key}
                )
                note = etree.SubElement(
                    concept,
                    QName(name="xref"),
                    attrib={
                        "type": "externalCrossReference",
                        "target": "https://iate.europa.eu/entry/result/"
                        + str(key) + "/en",
                    },
                )
                note.text = key

                c = reference_concepts[key]
                descrip = etree.SubElement(
                    concept, QName(name="descrip"), {"type": "subjectField"}
                )
                descrip.text = c["descrip"]["text"]

                langSecs = {
                    lang: etree.SubElement(
                        concept, QName(name="langSec"), {XML_LANG: lang}
                    )
                    for lang in unique_languages
                }
                for langSec in d[key]:

                    language = langSec.attrib.get(XML_LANG, [])

                    ref_termSecs = c["lang"][language]

                    for termSec in langSec:

                        copied_termSec = deepcopy(termSec)

                        terms = copied_termSec.xpath(
                            "//x:term", namespaces={"x": "urn:iso:std:iso:30042:ed-2"}
                        )
                        for j in terms:
                            for ref_termSec in ref_termSecs:
                                # we copy the attributes from the ref_termSecs
                                if any(
                                    [
                                        t["type"] == "term"
                                        and t["text"].lower() == j.text.lower()
                                        for t in ref_termSec
                                    ]
                                ):
                                    for t in ref_termSec:
                                        if t["type"] != "term":
                                            termnote = etree.SubElement(
                                                j.getparent(),
                                                QName(name=t["type"]),
                                                t["attr"],
                                            )
                                            termnote.text = t["text"]

                        # for the new concept we remove all xrefs
                        for j in copied_termSec.xpath(
                            "//x:xref", namespaces={"x": "urn:iso:std:iso:30042:ed-2"}
                        ):
                            j.getparent().remove(j)
                        # and we set planningQualifier to recommendTerm
                        for j in copied_termSec.xpath(
                            "//x:termNote[@type='language-planningQualifier']",
                            namespaces={"x": "urn:iso:std:iso:30042:ed-2"},
                        ):
                            j.text = "recommendedTerm"

                        langSecs[language].append(copied_termSec)

                        # add terms from reference that are not included in the current tbx
                        for ref_termSec in ref_termSecs:
                            if not any(
                                [
                                    t["type"] == "term"
                                    and t["text"].lower()
                                    in [j.text.lower() for j in terms]
                                    for t in ref_termSec
                                ]
                            ):
                                new_termSec = etree.SubElement(
                                    langSecs[language], QName(name="termSec"), {}
                                )
                                for t in ref_termSec:
                                    termnote = etree.SubElement(
                                        new_termSec, QName(name=t["type"]), t["attr"]
                                    )
                                    termnote.text = t["text"]

                    parent = langSec.getparent()
                    if parent is not None:
                        parent.remove(langSec)

            count += 1

    def lookup_term(
        self,
        term_text: str = "",
        term_pos: list = [],
        reference: dict = {},
        params: dict = {},
    ):

        number_of_word_components = params.get("number_of_word_components", 4)

        components_completely_found = []

        for component_idx, component in enumerate(term_text.split(" ")):

            pos = term_pos[component_idx]

            # first the complete term
            parts = [component]
            data = self.retrieve_component_data(
                parts=parts, reference=reference, pos=pos
            )
            if data is None and number_of_word_components >= 2:
                i = 2
                while (i < len(component) - 2) and data is None:
                    parts = [component[:i], component[i:]]
                    data = self.retrieve_component_data(
                        parts=parts, reference=reference, pos=pos
                    )
                    i += 1
            if data is None and number_of_word_components >= 3:
                i = 2
                while (i < len(component) - 2) and data is None:
                    j = 2
                    while (j < i) and data is None:
                        parts = [component[:j], component[j:i], component[i:]]
                        data = self.retrieve_component_data(
                            parts=parts, reference=reference, pos=pos
                        )
                        j += 1
                    i += 1
            if data is None and number_of_word_components >= 4:
                i = 2
                while (i < len(component) - 2) and data is None:
                    j = 2
                    while (j < i) and data is None:
                        k = 2
                        while (k < j) and data is None:
                            parts = [
                                component[:k],
                                component[k:j],
                                component[j:i],
                                component[i:],
                            ]
                            data = self.retrieve_component_data(
                                parts=parts, reference=reference, pos=pos
                            )
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
                                parts = [
                                    component[:l],
                                    component[l:k],
                                    component[k:j],
                                    component[j:i],
                                    component[i:],
                                ]
                                data = self.retrieve_component_data(
                                    parts=parts, reference=reference, pos=pos
                                )
                                l += 1
                            k += 1
                        j += 1
                    i += 1

            components_completely_found.append(data)
        return components_completely_found

    def retrieve_component_data(
        self, parts: list = [], reference: dict = {}, pos: str = ""
    ):
        norm_parts = [
            part if part[-1] == "-" else part + "-" for part in parts[:-1]
        ] + [parts[-1]]
        if all([(part in reference.keys()) for part in norm_parts]):
            ref_components = [
                ref_pos
                for ref_pos in reference[norm_parts[-1]]
                if ref_pos["partOfSpeech"] == pos
            ]
            if ref_components != []:
                full_lemma = (
                    "_".join(parts[:-1])
                    + ("" if len(parts) > 1 else "")
                    + ref_components[0]["lemma"]
                )
                full_morphoFeats = ref_components[0]["morphoFeats"]
                return (full_lemma, full_morphoFeats, norm_parts)
        return None

    def add_termnotes_from_tbx(self, reference=None, params: dict = {}):
        """
        This functions add termnotes to the current TbxDocument from another TbXDocument
        for example a lassy tbx-file

        """
        reference = reference.concepts_dict

        for concept in self.findall("text/body/conceptEntry", namespaces=NAMESPACES):
            concept_id = concept.attrib["id"]
            for item in concept:
                if item.tag == QName(name="langSec"):
                    if item.attrib.get(XML_LANG, "") == "nl":
                        for termSec in item:  # termsec
                            term_pos = None
                            for item3 in termSec:
                                if (
                                    item3.tag == QName(name="termNote")
                                    and item3.attrib["type"] == "partOfSpeech"
                                ):
                                    term_pos = item3.text.split(", ")

                            for item3 in termSec:
                                if (
                                    item3.tag == QName(name="term")
                                    and term_pos is not None
                                ):
                                    term_text = item3.text.lower()

                                    components_completely_found = self.lookup_term(
                                        term_text, term_pos, reference, params
                                    )

                                    if all(
                                        [
                                            component is not None
                                            for component in components_completely_found
                                        ]
                                    ):
                                        note = etree.SubElement(
                                            termSec,
                                            QName(name="termNote"),
                                            attrib={"type": "termLemma"},
                                        )
                                        note.text = " ".join(
                                            c[0] for c in components_completely_found
                                        )
                                        note = etree.SubElement(
                                            termSec,
                                            QName(name="termNote"),
                                            attrib={"type": "grammaticalNumber"},
                                        )
                                        if ",ev," in components_completely_found[-1][1]:
                                            note.text = "singular"
                                        elif (
                                            ",mv," in components_completely_found[-1][1]
                                        ):
                                            note.text = "plural"
                                        note = etree.SubElement(
                                            termSec,
                                            QName(name="termNote"),
                                            attrib={"type": "termComponents"},
                                        )
                                        note.text = " ".join(
                                            [
                                                "".join([cc for cc in c])
                                                for c in [
                                                    c[2]
                                                    for c in components_completely_found
                                                ]
                                            ]
                                        )
                                    else:
                                        logging.warning(
                                            "Not completely found: "
                                            + term_text
                                            + " found="
                                            + str(components_completely_found)
                                            + " pos="
                                            + str(term_pos)
                                        )

    def to_excel(self, output: str, languages: list = []):
        """Function to write a TbxDocument to Excel

        Args:
            output: the location of the Excel to be stored

        Returns:
            None

        """
        body = self.find(TEXT + "/" + BODY)
        wb = xlsxwriter.Workbook(output)
        worksheet = wb.add_worksheet("Tbx")

        worksheet.write_row(
            0,
            0,
            [
                "id",
                "subjectField",
                "xref",
                "ref",
                "language",
                "term",
                "type",
                "partOfSpeech",
                "grammaticalNumber",
                "lemma",
                "normativeAuthorization",
                "language-planningQualifier",
            ],
        )
        row = 1
        for concept in self.findall("text/body/conceptEntry", namespaces=NAMESPACES):

            subjectField = ""
            xref = ""
            ref = ""

            term = dict()

            for element in concept:

                if (
                    element.tag == QName(name="descrip")
                    and element.attrib.get("type", None) == "subjectField"
                ):
                    subjectField = element.text

                if (
                    element.tag == QName(name="xref")
                    and element.attrib.get("type", None) == "externalCrossReference"
                ):
                    xref = element.attrib["target"]

                if (
                    element.tag == QName(name="ref")
                    and element.attrib.get("type", None) == "crossReference"
                ):
                    ref = element.text

                if element.tag == QName(name="langSec") and (
                    languages == [] or element.attrib.get(XML_LANG) in languages
                ):

                    lang = element.attrib.get(XML_LANG)

                    for term_sec in element:
                        termdata = dict()
                        for item in term_sec:
                            if item.tag == QName(name="term"):
                                termdata["text"] = item.text
                            if (
                                item.tag == QName(name="termNote")
                                and item.attrib["type"] == "termType"
                            ):
                                termdata["type"] = item.text
                            if (
                                item.tag == QName(name="termNote")
                                and item.attrib["type"] == "partOfSpeech"
                            ):
                                termdata["pos"] = item.text
                            if (
                                item.tag == QName(name="termNote")
                                and item.attrib["type"] == "grammaticalNumber"
                            ):
                                termdata["number"] = item.text
                            if (
                                item.tag == QName(name="termNote")
                                and item.attrib["type"] == "termLemma"
                            ):
                                termdata["lemma"] = item.text
                            if (
                                item.tag == QName(name="termNote")
                                and item.attrib["type"] == "normativeAuthorization"
                            ):
                                termdata["authorization"] = item.text
                            if (
                                item.tag == QName(name="termNote")
                                and item.attrib["type"] == "language-planningQualifier"
                            ):
                                termdata["qualifier"] = item.text

                        worksheet.write_row(
                            row,
                            0,
                            [
                                concept.attrib["id"],
                                subjectField,
                                xref,
                                ref,
                                element.attrib.get(XML_LANG, ""),
                                termdata.get("text", ""),
                                termdata.get("type", ""),
                                termdata.get("pos", ""),
                                termdata.get("number", ""),
                                termdata.get("lemma", ""),
                                termdata.get("authorization", ""),
                                termdata.get("qualifier", ""),
                            ],
                        )
                        row += 1
        wb.close()
