Available termbases
===================

A terminology database (termbase) forms a structured way to store and exchange dictionaries and lexicographical data of related terms. Termate provides a way to use these termbases in NLP analyses.

The IATE termbase
-----------------

The IATE termbase can be found here

* `Interactive Terminology for Europe <https://iate.europa.eu/home/>`_.

A conceptEntry looks like this:

::

    <conceptEntry id="iate_3515206">
      <descrip type="subjectField">insurance</descrip>
      <langSec xml:lang="en">
        <termSec>
          <term>risk margin</term>
          <termNote type="termType">fullForm</termNote>
          <descrip type="reliabilityCode">9</descrip>
        </termSec>
      </langSec>
      <langSec xml:lang="fi">
        <termSec>
          <term>riskimarginaali</term>
          <termNote type="termType">fullForm</termNote>
          <descrip type="reliabilityCode">9</descrip>
        </termSec>
      </langSec>
      <langSec xml:lang="fr">
        <termSec>
          <term>marge de risque</term>
          <termNote type="termType">fullForm</termNote>
          <descrip type="reliabilityCode">9</descrip>
        </termSec>
      </langSec>
      ...
      </conceptEntry>


The Supervisory termbases
-------------------------

Specific termbases are published on data.world in the `Termbase repository <https://data.world/wjwillemse/termbases>`_. They include:

* EIOPA Solvency 2 XBRL Taxonomy, version 2.6.0

* EBA CRD XBRL Taxonomy, version 3.2.1.0

These termbases combine three data sources: terms from a supervisory XBRL Taxonomy (derived from the labels of XBRL elements), terms from the IATE termbase that match the labels of the XBRL elements (available in all official European languages) and language-specific linguistic annotations to each term from an NLP processor.

References to XBRL elements are added as cross references directly under the conceptEntry (with match type fullMatch and partialMatch to specify whether the term is an exact match with a label of the XBRL element or that the term is a substring of the label). 

Two linguistic annotations are added to each term in the termbase: the lemma and the part of speech tags. The linguistic annotations are added as termNotes in the term section of a term (with type termLemma and partOfSpeech). If a term contains more than one word then the part of speech tags are in a comma-separated string.

::

    <conceptEntry id="iate_3515206">
      <descrip type="subjectField">insurance</descrip>
      <langSec xml:lang="en">
        <termSec>
          <term>risk margin</term>
          <termNote type="termType">fullForm</termNote>
          <descrip type="reliabilityCode">9</descrip>
          <termNote type="termLemma">risk margin</termNote>
          <termNote type="partOfSpeech">noun, noun</termNote>
        </termSec>
      </langSec>
      <langSec xml:lang="fi">
        <termSec>
          <term>riskimarginaali</term>
          <termNote type="termType">fullForm</termNote>
          <descrip type="reliabilityCode">9</descrip>
          <termNote type="termLemma">riski#marginaali</termNote>
          <termNote type="partOfSpeech">noun</termNote>
        </termSec>
      </langSec>
      <langSec xml:lang="fr">
        <termSec>
          <term>marge de risque</term>
          <termNote type="termType">fullForm</termNote>
          <descrip type="reliabilityCode">9</descrip>
          <termNote type="termLemma">marge de risque</termNote>
          <termNote type="partOfSpeech">noun, adp, noun</termNote>
        </termSec>
      </langSec>
      ...
      <ref type="crossReference" match="fullMatch">http://eiopa.europa.eu/xbrl/s2c/dict/dom/vm#x47</ref>
      <ref type="crossReference" match="fullMatch">http://eiopa.europa.eu/xbrl/s2md/fws/solvency/solvency2/2021-07-15/tab/s.02.01.01.01#s2md_c653</ref>
      <ref type="crossReference" match="partialMatch">http://eiopa.europa.eu/xbrl/s2md/fws/solvency/solvency2/2021-07-15/tab/s.26.06.01.01#s2md_c6792</ref>
        ...
      </conceptEntry>


For terms that are included in the XBRL Taxonomy for which no match could be found in the IATE database new conceptEntries were added. For example the term "valuation of recoverables":

::

    <conceptEntry id="eiopa_23">
      <ref type="crossReference" match="fullMatch">http://eiopa.europa.eu/xbrl/s2c/dict/dim#rr</ref>
      <langSec xml:lang="en">
        <termSec>
          <term>Valuation of recoverables</term>
          <termNote type="termType">fullForm</termNote>
          <termNote type="termLemma">valuation of recoverable</termNote>
          <termNote type="partOfSpeech">noun, adp, noun</termNote>
        </termSec>
      </langSec>
    /conceptEntry>

This term is only available in the language of the XBRL Taxonomy. If translations are available then they can be included in the termbase by adding lines to the TBX Resource.

Using a termbase
----------------

If you have a TBX termbase available then you can read it in the following way:

::

    IATE_FILE = os.path.join("..", "data", "termbases", "IATE_export.tbx")
    termbase = termate.TbxDocument().open(IATE_FILE)

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
    

Annotating NAF files
--------------------

To annotate a NAF file with the content of a termbase open both files:

::

    naf_file = "P:\\projects\\naf-data\\data\examples\\exmaple.naf.xml"
    doc = nafigator.NafDocument().open(naf_file)

    tbx_file = "P:\\projects\\tbx-data\\termbases\\EIOPA_SolvencyII_XBRL_Taxonomy_2.6.0_PWD_with_External_Files.tbx"
    termbase = termate.TbxDocument().open(tbx_file)

Then create a termbase processor and process with the processor the document:

::

    t = nafigator.TermbaseProcessor(termbase)
    t.process(doc=doc)

On initialization the TermbaseProcessor creates a fast way to access the terms in the termbase. After initialization you can process multiple documents with the same termbase by calling the process function.

Now you can overwrite the existing NAF file or store it under a different name

::

    doc.write(naf_file)
