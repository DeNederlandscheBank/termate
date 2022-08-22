The TBX format
--------------

TBX, or TermBase eXchange, is an international standard for representing and exchanging information from termbases. TBX version 3 is published as ISO 30042:2019. A TBX Resource represents a collection of terminological concepts and is expressed as an XML file. It contains a header and a body of text with the terminological concepts. The main elements are described below.

* Header (tbxHeader): represents the metadata of the TBX Resource and contains the file description (fileDesc). The file description (fileDesc) contains (optional) title statement (titleStmt), publication statement (publicationStmt) and source description (sourceDesc).

* Terminological concept (conceptEntry): represents a language-independent concept. Each terminological concept has a unique IS, is described by a set of properties, such as the subject field it belongs to, and is associated to language sections, which are sets of language-specific terms that express the terminological concept.

* Language section (langSec): a language section is a language-specific container for all terms that represent a terminological concept in a given language. The language section contains simple terms.

* Term section (termSec): represents a language-specific term. A term section always contains a term with the text of the term and zero or more term notes (with term properties and linguistical properties) and descriptions (such as the reliability code of the term in relation to the concept). Related term notes are grouped in a term note group (termNoteGrp).

Version 3 of TBX provides dialect-specific schema to constrain TBX files. The TBX Resource contains the dialect name associated with a corresponding external schema. In this package a provisional private dialect TBX-DNB is used that extends the public dialect TBX-Basic with additional linguistic annotations.

* `Introduction to TermBase eXchange (TBX) Version 3 <https://www.tbxinfo.net/>`_

* `The Lexicon Model for Ontologies <https://lemon-model.net/>`_
