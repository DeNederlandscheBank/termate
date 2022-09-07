TBX to OntoLex Lemon
====================

Termate provides an easy way to convert termbases to the `OntoLex Lemon vocabulary <https://lemon-model.net/>`_. OntoLex Lemon is used to model lexicon and machine-readable dictionaries linked to the Semantic Web. The implementation in termate follows the `W3C guidelines for converting TBX to RDF <https://www.w3.org/community/bpmlod/wiki/Converting_TBX_to_RDF>`_ except that this implementation is based op TBX version 3.

Below you find examples from the converted Solvency 2 termbase.

Header information
------------------

The header of the termbase 

::

    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix dcterms: <http://purl.org/dc/terms/> .
    @prefix decomp: <http://www.w3.org/ns/lemon/decomp#> .
    @prefix lexinfo: <http://www.lexinfo.net/ontology/3.0/lexinfo#> .
    @prefix ontolex: <http://www.w3.org/ns/lemon/ontolex#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix tbx: <http://tbx2rdf.lider-project.eu/tbx#> .

    <https://dnb.nl/rdf-data/termbases/solvency2/header> a tbx:Header,
            dcat:Dataset ;
        dcterms:type "TBX-DNB" ;
        tbx:encodingDesc "<p type=\"XCSURI\">TBXXCS.xcs</p>" ;
        tbx:sourceDesc "EIOPA_SolvencyII_XBRL_Taxonomy_2.6.0_PWD_with_External_Files" .

Terminological concepts
-----------------------

::

    <https://dnb.nl/rdf-data/termbases/solvency2/iate_2149365> a skos:Concept ;
        tbx:subjectField "insurance" .

Lexical entries
---------------

The lexicon (only a few entries are shown):

::

    <https://dnb.nl/rdf-data/termbases/solvency2/lexicon/en> a ontolex:Lexicon ;
        ontolex:entry <https://dnb.nl/rdf-data/termbases/solvency2/risk+mitigation-en>,
        <https://dnb.nl/rdf-data/termbases/solvency2/mitigation-en>,
        <https://dnb.nl/rdf-data/termbases/solvency2/risk-en> ;
        ontolex:language "en" .

The LexicalEntry of *risk mitigation*:

::

    <https://dnb.nl/rdf-data/termbases/solvency2/risk+mitigation-en> a ontolex:LexicalEntry,
            ontolex:MultiWordExpression ;
        rdfs:label "risk mitigation"@en ;
        tbx:reliabilityCode "9" ;
        tbx:termType "fullForm" ;
        decomp:constituent <https://dnb.nl/rdf-data/termbases/solvency2/risk+mitigation-en#component1>,
            <https://dnb.nl/rdf-data/termbases/solvency2/risk+mitigation-en#component2> ;
        ontolex:canonicalForm <https://dnb.nl/rdf-data/termbases/solvency2/risk+mitigation-en#CanonicalForm> ;
        ontolex:language "en" ;
        ontolex:sense <https://dnb.nl/rdf-data/termbases/solvency2/risk+mitigation-en#Sense> .

The components:

::

    <https://dnb.nl/rdf-data/termbases/solvency2/risk+mitigation-en#component1> a decomp:Component ;
        decomp:correspondsTo <https://dnb.nl/rdf-data/termbases/solvency2/risk-en> .

    <https://dnb.nl/rdf-data/termbases/solvency2/risk+mitigation-en#component2> a decomp:Component ;
        decomp:correspondsTo <https://dnb.nl/rdf-data/termbases/solvency2/mitigation-en> .

The sense:

::

    <https://dnb.nl/rdf-data/termbases/solvency2/risk+mitigation-en#Sense> ontolex:reference <https://dnb.nl/rdf-data/termbases/solvency2/iate_2149365> .

And the other two LexicalEntries for *mitigation* and *risk*:

::

    <https://dnb.nl/rdf-data/termbases/solvency2/risk-en> a ontolex:LexicalEntry,
            ontolex:Word ;
        rdfs:label "risk"@en ;
        lexinfo:partOfSpeech "noun" ;
        ontolex:language "en" .


::

    <https://dnb.nl/rdf-data/termbases/solvency2/mitigation-en> a ontolex:LexicalEntry,
            ontolex:Word ;
        rdfs:label "mitigation"@en ;
        lexinfo:partOfSpeech "noun" ;
        ontolex:language "en" .

The CanonicalForm (the lemmatized version of the term):

::

    <https://dnb.nl/rdf-data/termbases/solvency2/risk+mitigation-en#CanonicalForm> a ontolex:Form ;
        ontolex:writtenRep "risk mitigation"@en .
