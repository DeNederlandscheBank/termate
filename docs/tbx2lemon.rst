OntoLex Lemon format
====================

Termate provides an easy way to convert termbases to a `OntoLex Lemon vocabulary <https://lemon-model.net/>`_. OntoLex Lemon is used to model lexicon and machine-readable dictionaries linked to the Semantic Web. The implementation in termate follows the `W3C guidelines for converting TBX to RDF <https://www.w3.org/community/bpmlod/wiki/Converting_TBX_to_RDF>`_ except that this implementation is based op TBX version 3.

Below you find examples from the converted Solvency 2 termbase. The termbase can be found `here <https://data.world/wjwillemse/termbases>`_.


Header information
------------------

The header of the termbase 

::

    @prefix dcterms: <http://purl.org/dc/terms/> .
    @prefix decomp: <http://www.w3.org/ns/lemon/decomp#> .
    @prefix lexinfo: <http://www.lexinfo.net/ontology/3.0/lexinfo#> .
    @prefix ontolex: <http://www.w3.org/ns/lemon/ontolex#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix tbx: <http://tbx2rdf.lider-project.eu/tbx#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <https://dnb.nl/rdf-data/vocabulary/insurance/solvency2/header> a tbx:Header,
            <http://www.w3.org/ns/dcat#Dataset> ;
        dcterms:type "TBX-DNB" ;
        tbx:encodingDesc "<p type=\"XCSURI\">TBXXCS.xcs</p>" ;
        tbx:sourceDesc "EIOPA_SolvencyII_XBRL_Taxonomy_2.6.0_PWD_with_External_Files" .

Terminological concepts
-----------------------

::

    <https://iate.europa.eu/entry/result/2149365> a skos:Concept ;
        tbx:subjectField "insurance"^^xsd:string ;
        skos:prefLabel "risikodæmpning"@da,
            "risikoreduktion"@da,
            "Risikominderung"@de,
            "risk mitigation"@en,
            "riski maandamine"@et,
            "riskimaandamine"@et,
            "atténuation des risques"@fr,
            "réduction des risques"@fr,
            "kockázatcsökkentés"@hu,
            "ograniczanie ryzyka"@pl,
            "minimizare a riscului"@ro .

For concepts in the Solvency 2 reporting framework that do not have a corresponding concept in the IATE entries, we added additional EIOPA concepts that refer to the reporting framework. For example for the concept 'type 1 exposures' we have:

::

    <https://eiopa.europa.eu/rdf-data/vocabulary/insurance/solvency2/2224> a skos:Concept ;
        tbx:subjectField "insurance"^^xsd:string ;
        skos:altLabel "S.26.02.01.01,R0100"@en,
            "S.26.02.04.01,R0100"@en,
            "SR.26.02.01.01,R0100"@en ;
        skos:prefLabel "Type 1 exposures"@en ;
        skos:related <http://eiopa.europa.eu/xbrl/s2c/dict/dom/rt#x146>,
            <http://eiopa.europa.eu/xbrl/s2md/fws/solvency/solvency2/2021-07-15/tab/s.26.02.01.01#s2md_c6074>,
            <http://eiopa.europa.eu/xbrl/s2md/fws/solvency/solvency2/2021-07-15/tab/s.26.02.04.01#s2md_c6107>,
            <http://eiopa.europa.eu/xbrl/s2md/fws/solvency/solvency2/2021-07-15/tab/sr.26.02.01.01#s2md_c6140> .

Note that the prefLabel is "Type 1 exposures"@en and that altLabel refer to datapoint locations (template plus row-column code) in the Solvency 2 reporting framework with that label. Also included are the related concepts within the XBRL taxonomy (linked via skos:related).

Lexical entries
---------------

The lexicon (only a few entries are shown):

::

    <https://dnb.nl/rdf-data/vocabulary/insurance/solvency2/lexicon/en> a ontolex:Lexicon ;
        ontolex:entry <https://dnb.nl/rdf-data/vocabulary/insurance/solvency2/lexicon/en/risk+mitigation>,
            <https://dnb.nl/rdf-data/vocabulary/insurance/solvency2/lexicon/en/risk>,
            <https://dnb.nl/rdf-data/vocabulary/insurance/solvency2/lexicon/en/mitigation>;
        ontolex:language "en" .

The LexicalEntry of *risk mitigation*:

::

    <https://dnb.nl/rdf-data/vocabulary/insurance/solvency2/lexicon/en/risk+mitigation> a ontolex:LexicalEntry,
            ontolex:MultiWordExpression ;
        tbx:reliabilityCode "9"^^xsd:nonNegativeInteger ;
        tbx:termType "fullForm" ;
        decomp:constituent <https://dnb.nl/rdf-data/vocabulary/insurance/solvency2/lexicon/en/risk+mitigation#component1>,
            <https://dnb.nl/rdf-data/vocabulary/insurance/solvency2/lexicon/en/risk+mitigation#component2> ;
        ontolex:canonicalForm <https://dnb.nl/rdf-data/vocabulary/insurance/solvency2/lexicon/en/risk+mitigation#canonicalForm> ;
        ontolex:language "en" ;
        ontolex:sense <https://dnb.nl/rdf-data/vocabulary/insurance/solvency2/lexicon/en/risk+mitigation#Sense> .

The components:

::

    <https://dnb.nl/rdf-data/vocabulary/insurance/solvency2/lexicon/en/risk+mitigation#component1> a decomp:Component ;
        decomp:correspondsTo <https://dnb.nl/rdf-data/vocabulary/insurance/solvency2/lexicon/en/risk> .

    <https://dnb.nl/rdf-data/vocabulary/insurance/solvency2/lexicon/en/risk+mitigation#component2> a decomp:Component ;
        decomp:correspondsTo <https://dnb.nl/rdf-data/vocabulary/insurance/solvency2/lexicon/en/mitigation> .

The sense:

::

    <https://dnb.nl/rdf-data/vocabulary/insurance/solvency2/lexicon/en/risk+mitigation#Sense> ontolex:reference <https://iate.europa.eu/entry/result/2149365> .

And the other two LexicalEntries for *mitigation* and *risk*:

::

    <https://dnb.nl/rdf-data/vocabulary/insurance/solvency2/lexicon/en/risk> a ontolex:LexicalEntry,
            ontolex:Word ;
        tbx:reliabilityCode "9"^^xsd:nonNegativeInteger ;
        tbx:termType "fullForm" ;
        lexinfo:partOfSpeech <http://purl.org/olia/olia.owl#CommonNoun>,
            <http://purl.org/olia/olia.owl#Verb> ;
        ontolex:canonicalForm <https://dnb.nl/rdf-data/vocabulary/insurance/solvency2/lexicon/en/risk#canonicalForm> ;
        ontolex:language "en" ;
        ontolex:sense <https://dnb.nl/rdf-data/vocabulary/insurance/solvency2/lexicon/en/risk#Sense> .


::

    <https://dnb.nl/rdf-data/vocabulary/insurance/solvency2/lexicon/en/mitigation> a ontolex:LexicalEntry,
            ontolex:Word ;
        lexinfo:partOfSpeech <http://purl.org/olia/olia.owl#CommonNoun> ;
        ontolex:canonicalForm <https://dnb.nl/rdf-data/vocabulary/insurance/solvency2/lexicon/en/mitigation#canonicalForm> ;
        ontolex:language "en" .

The CanonicalForm (the lemmatized version of the term):

::

    <https://dnb.nl/rdf-data/vocabulary/insurance/solvency2/lexicon/en/risk+mitigation#canonicalForm> a ontolex:Form ;
        rdfs:label "risk mitigation"^^xsd:string ;
        ontolex:writtenRep "risk mitigation"@en .
