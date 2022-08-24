Available termbases
-------------------

A terminology database (termbase) forms a structured way to store and exchange dictionaries and lexicographical data of related terms. Termate provides a way to use these termbases in NLP analyses.

The IATE termbase
=================

The IATE termbase can be found here:


* `Interactive Terminology for Europe <https://iate.europa.eu/home/>`_


The XBRL Taxonomy termbases
===========================

Specific termbases are published in the `Termbase repository <https://data.world/wjwillemse/termbases>`_. They include:


* EIOPA Solvency 2 XBRL Taxonomy, version 2.6.0


* EBA CRD XBRL Taxonomy, version 3.2.1.0


These termbases are based on supervisory XBRL Taxonomies (Solvency 2 and CRD). They contain all terms from a XBRL Taxonomy (derived from the labels of XBRL elements) combined with related IATE concepts and thereby available in all official European languages.


Using an existing termbase
==========================

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
    