Usage
-----

Using existing termbases
========================

The IATE termbase can be found here:

* `Interactive Terminology for Europe <https://iate.europa.eu/home/>`_

Specific termbases are published in the `Termbase repository <https://data.world/wjwillemse/termbases>`_. They include:

- EIOPA SolvencyII XBRL Taxonomy, version 2.6.0

- EBA CRD XBRL Taxonomy, version 3.2.1.0

These termbases are based on supervisory XBRL Taxonomies (Solvency 2 and CRD). They contain all terms from a XBRL Taxonomy (derived from the labels of XBRL elements) combined with related IATE concepts and thereby available in all official European languages.

If you have a TBX termbase available then you can read it in the following way:

::

    IATE_FILE = os.path.join("..", "data", "termbases", "IATE_export.tbx")
    termbase = determinator.TbxDocument().open(IATE_FILE)

To get the concepts in the termbase as a list of dictionaries use:

::

    concepts = termbase.concepts_list

The results of the first concept in the list then look for example like this:

:: 

    {
    'id': 'iate_127562',
    'lang': {
      'en': [[
      {'type': 'term', 
       'attr': {}, 
       'text': 'services agreement'
      },
      {'type': 'termNote', 
       'attr': {'type': 'termType'}, 
       'text': 'fullForm'
      },
      {'type': 'descrip', 
       'attr': {'type': 'reliabilityCode'}, 
       'text': '1'
      }
    ]]
    ...

Create a termbase from extracted terms
======================================

We generate an empty TBX document with

::

    termbase = determinator.TbxDocument()
    termbase.generate(params = {
        determinator.TBX_DIALECT: "TBX-DNB",
        determinator.TBX_STYLE: "dca",
        determinator.TBX_RELAXNG: "https://github.com/DeNederlandscheBank/determinator/blob/main/data/dialects/TBX-DNB.rng",
        determinator.SOURCEDESC: ["TBX file, created via dnb/determinator"],
        determinator.TITLE: ["Example termbase"],
        determinator.PUBLICATION: ["Created on ..."]
    })

Then we extract terms from the Solvency II Delegated Acts (Dutch version) in NAF:

::

    # create terms dictionary of subset of languages
    terms = {}
    for language in ['NL', 'EN', 'DE', 'FR', 'ES', 'ET', 'DA', 'SV']:
        DOC_FILE = "..\\..\\nafigator-data\\data\\legislation\\Solvency II Delegated Acts - "+language+".naf.xml"
        doc = nafigator.NafDocument().open(DOC_FILE)
        determinator.merge_terms_dict(terms, nafigator.extract_terms(doc))

Then we create a termbase

::

    # add concepts from a dictionary of terms
    termbase.create_tbx_from_terms_dict(terms=terms, 
                                 params={'concept_id_prefix': 'tbx_'})

Then we add references from the InterActive Terminology for Europe (IATE) dataset:

::

    # read the IATE file
    IATE_FILE = "..//data//iate//IATE_export.tbx"
    ref = determinator.TbxDocument().open(IATE_FILE)
    termbase.copy_from_tbx(reference=ref)

Then we add termnotes from the Dutch Lassy dataset (the small one) including basic insurance terms:

::

    # read the lassy file
    LASSY_FILE = "..//data//lassy//lassy_with_insurance.tbx"
    lassy = determinator.TbxDocument().open(LASSY_FILE)
    termbase.add_termnotes_from_tbx(reference=lassy, params={'number_of_word_components':  5})

Then we have a termbase with:

::

    <conceptEntry id="249">
     <descrip type="subjectField">insurance</descrip>
     <xref>IATE_2246604</xref>
     <ref>https://iate.europa.eu/entry/result/2246604/en</ref>
     <langSec xml:lang="nl">
      <termSec>
       <term>solvabiliteitskapitaalvereiste</term>
       <termNote type="partOfSpeech">noun</termNote>
       <note>source: data/Solvency II Delegated Acts - NL.txt (#hits=331)</note>
       <termNote type="termType">fullForm</termNote>
       <descrip type="reliabilityCode">9</descrip>
       <termNote type="lemma">solvabiliteits_kapitaalvereiste</termNote>
       <termNote type="grammaticalNumber">singular</termNote>
       <termNoteGrp>
        <termNote type="component">solvabiliteits-</termNote>
        <termNote type="component">kapitaal-</termNote>
        <termNote type="component">vereiste</termNote>
       </termNoteGrp>
      </termSec>
     </langSec>
     <langSec xml:lang="en">
      <termSec>
       <term>SCR</term>
       <termNote type="termType">abbreviation</termNote>
       <descrip type="reliabilityCode">9</descrip>
      </termSec>
      <termSec>
       <term>solvency capital requirement</term>
       <termNote type="termType">fullForm</termNote>
       <descrip type="reliabilityCode">9</descrip>
       <termNote type="partOfSpeech">noun, noun, noun</termNote>
       <note>source: data/Solvency II Delegated Acts - EN.txt (#hits=266)</note>
      </termSec>
     </langSec>
     <langSec xml:lang="fr">
      <termSec>
       <term>capital de solvabilité requis</term>
       <termNote type="termType">fullForm</termNote>
       <descrip type="reliabilityCode">9</descrip>
       <termNote type="partOfSpeech">noun, adp, noun, adj</termNote>
       <note>source: ../nafigator-data/data/legislation/Solvency II Delegated Acts - FR.txt (#hits=198)</note>
      </termSec>
      <termSec>
       <term>CSR</term>
       <termNote type="termType">abbreviation</termNote>
       <descrip type="reliabilityCode">9</descrip>
      </termSec>
     </langSec>
    </conceptEntry>

* a reference is included to concept '2246604' from the IATE dataset. From that reference, we can for example derive that the official European term for this concept in English is 'solvency capital requirement' and in German 'Solvenzkapitalanforderung' and that the term is defined in Directive 2009/138/EC (Solvency II).

* termNotes include the partOfSpeech, lemma and morpohoFeats derived from the Lassy dataset (in Dutch). This dataset was extended with insurance related word components and terms that were not included in the Lassy dataset.

* also included are the word components of a term. The Dutch language, like the German language, often glues components together to construct new words instead of using separate words like the English language.
