============
determinator
============


.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
        :target: https://opensource.org/licenses/MIT
        :alt: License: MIT

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
        :target: https://github.com/psf/black
        :alt: Code style: black

**DISCLAIMER - BETA PHASE**

*This package is currently in a beta phase.*

Package for terminology management with the TermBase eXchange (TBX) format

* Free software: MIT license


Features
--------

- Use existing TBX termbases within NLP analyses (TBX version 3)

- Create TBX termbases based on extracted terms from documents


Overview of the idea
--------------------

Read an existing termbase
=========================

If you already have a termbase available then you can read it in the following way:

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
    'en': [
    [
    {'type': 'term', 
     'attr': {}, 
     'text': 'SA'
    },
    {'type': 'termNote', 
     'attr': {'type': 'termType'}, 
     'text': 'abbreviation'
    },
    {'type': 'descrip', 
     'attr': {'type': 'reliabilityCode'}, 
     'text': '1'}
    ],
    [
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
        determinator.SOURCEDESC: "TBX file, created via dnb/determinator"
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

Datasets
--------

* `Interactive Terminology for Europe <https://iate.europa.eu/home/>`_

* `Lassy klein corpus <https://taalmaterialen.ivdnt.org/download/lassy-klein-corpus6/>`_


The TermBase eXchange format (version 3)
----------------------------------------

TBX, or TermBase eXchange, is an international standard for representing and exchanging information from termbases. TBX version 3 is published as ISO 30042:2019. A TBX Resource represents a collection of terminological concepts and is expressed as an XML file. It contains a header and a body of text with the terminological concepts. The main elements are described below.

- Header (tbxHeader): represents the metadata of the TBX Resource and contains the file description (fileDesc). The file description (fileDesc) contains (optional) title statement (titleStmt), publication statement (publicationStmt) and source description (sourceDesc).

- Terminological concept (conceptEntry): represents a language-independent concept. Each terminological concept has a unique IS, is described by a set of properties, such as the subject field it belongs to, and is associated to language sections, which are sets of language-specific terms that express the terminological concept.

- Language section (langSec): a language section is a language-specific container for all terms that represent a terminological concept in a given language. The language section contains simple terms.

- Term section (termSec): represents a language-specific term. A term section always contains a term with the text of the term and zero or more term notes (with term properties and linguistical properties) and descriptions (such as the reliability code of the term in relation to the concept). Related term notes are grouped in a term note group (termNoteGrp).

Version 3 of TBX provides dialect-specific schema to constrain TBX files. The TBX Resource contains the dialect name associated with a corresponding external schema. In this package a provisional private dialect TBX-DNB is used that extends the public dialect TBX-Basic with additional linguistic annotations.

* `Introduction to TermBase eXchange (TBX) Version 3 <https://www.tbxinfo.net/>`_

* `Converting TBX to RDF <https://www.w3.org/community/bpmlod/wiki/Converting_TBX_to_RDF/>`_

* `The Lexicon Model for Ontologies <https://lemon-model.net/>`_
