# -*- coding: utf-8 -*-

import os
from lxml import etree
from ddhi_encoder.interview import Interview
import spacy


__author__ = "Clifford Wulfman"
__copyright__ = "Clifford Wulfman"
__license__ = "mit"

test_file = os.path.join(
    os.path.dirname(__file__),
    "aninterview.xml"
    )


def test_io():
    interview = Interview()
    interview.read(test_file)
    assert b'TEI' in etree.tostring(interview.tei_doc)
    outfile = os.path.join('/tmp', 'test_interview_tmpfile.xml')
    try:
        os.remove(outfile)
    except OSError:
        pass
    interview.write(outfile)
    assert os.path.isfile(outfile)


def test_tagging():
    interview = Interview()
    interview.read(test_file)
    interview.nlp = spacy.load('en_core_web_sm')
    interview.tag()
    outfile = os.path.join('/tmp', 'test_interview_tmpfile_tagged.xml')
    interview.write(outfile)
    assert os.path.isfile(outfile)
