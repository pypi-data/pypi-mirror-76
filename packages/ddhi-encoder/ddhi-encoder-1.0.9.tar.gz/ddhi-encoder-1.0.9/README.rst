A collection of command-line utilities to assist in the creation of
TEI-encoded oral history interviews. Part of the Dartmouth Digital
History Initiative.

.. _ddhi-encoder-1:

DDHI Encoder
============

The ddhi-encoder package is being developed to assist encoders in the
DDHI project in encoding oral history interview transcripts in TEI. At
present, it contains two command-line utilities:

#. ``ddhi_convert``: convert a Dartmouth DVP transcript from docx to
   tei.xml.
#. ``ddhi_tag``: perform named-entity tagging on a DDHI TEI
   transcription.

Installation
------------

You can use pip to install this package:

.. code:: bash

   pip install ddhi-encoder

To peform named-entity tagging with ``ddhi_tag``, you will need a Spacy
model. Before running ``ddhi_tag``, install Spacy's small English model:

.. code:: bash

   python -m spacy download en_core_web_sm

See `the Spacy documentation <https://spacy.io/models>`__ for more
information.

Use
---

Use ``ddhi_convert`` to transform a DOCX-encoded transcription into a
simply structured TEI document:

.. code:: bash

   ddhi_convert ~/Desktop/transcripts/zien_jimmy_transcript_final.docx -o tmp.tei.xml

Use ``ddhi_tag`` to add named-entity tags to a TEI-encoded
transcription:

.. code:: bash

   ddhi_tag -o zien.tei.xml tmp.tei.xml
