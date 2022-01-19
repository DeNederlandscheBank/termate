==========
terminator
==========


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

to terminate [ **term**-i-nate ]
------------------------------

    *v.intr*, **terminated**, **terminating**

    1. To extract terms from one of more text documents and output results in the TermBase eXchange (TBX) format.

Features
--------

- Extract expert terminology from documents in the NLP Annotation Format (NAF)

- Generate and read TermBase eXchange (TBX) files according to ISO 30042:2019 (currently TBX-Core)

- Add references and term notes from other sources (for example European IATE term bases)


Overview of the idea
--------------------

We generate an empty TBX document with

::

    t = terminator.TbxDocument()
    t.generate(params = {"sourceDesc": "TBX file, created via dnb/terminator"})

Then we extract terms from the Solvency II Delegated Acts (Dutch version) in NAF:

::

    file = "..\\data\\naf\\Solvency II Delegated Acts - NL.naf.xml"
    doc = nafigator.NafDocument().open(file)
    t.extract_terms(doc)

Then we add references from the InterActive Terminology for Europe (IATE) dataset:

::

    iate_file = "..//data//IATE//IATE_export.tbx"
    ref = terminator.TbxDocument().open(iate_file)
    t.add_references_from_tbx(reference=ref, prefix="IATE_")

Then we add termnotes from the Dutch Lassy dataset (the small one) including basic insurance terms:

::

    lassy = terminator.TbxDocument().open("..//data//lassy_with_insurance.tbx")
    t.add_termnotes_from_tbx(reference=lassy)

Then we have 4289 Dutch legal insurance terms with linguistical properties (lemma, part-of-speech, morphological properties and components) in TermBase eXchange format, for example concept 'c69' defined as (in xml):

::

      <conceptEntry id="c69">
        <langSec xml:lang="nl">
          <termSec>
            <term>solvabiliteitskapitaalvereiste</term>
            <termNote type="termType">fullForm</termNote>
            <termNote type="partOfSpeech">NOUN</termNote>
            <note>extracted from: data/Solvency II Delegated Acts - NL.txt (#hits=331)</note>
            <ref>IATE_2246604</ref>
            <termNote type="lemma">solvabiliteits_kapitaalvereiste</termNote>
            <termNote type="morphoFeats">(soort,mv,basis)</termNote>
            <termNote type="component">solvabiliteits-</termNote>
            <termNote type="component">kapitaal-</termNote>
            <termNote type="component">vereiste</termNote>
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


The TermBase eXchange format
----------------------------

* `Introduction to TermBase eXchange (TBX) Version 3 <https://www.tbxinfo.net/>`_

* `Converting TBX to RDF <https://www.w3.org/community/bpmlod/wiki/Converting_TBX_to_RDF/>`_

* `The Lexicon Model for Ontologies <https://lemon-model.net/>`_
