# -*- coding: utf-8 -*-

import pytest
import spacy
import re
from lxml import etree
from ddhi_encoder.utterance import Utterance

__author__ = "Clifford Wulfman"
__copyright__ = "Clifford Wulfman"
__license__ = "mit"


def test_utterance():
    speaker = "John"
    speech = "Jack gave the ball to Jane"
    utterance = Utterance(speaker, speech)
    utterance.nlp = spacy.load("en_core_web_sm")
    utterance.process()

    assert utterance.speaker == speaker
    assert utterance.speech == speech
    assert len(utterance) == len(speech)
    assert utterance._doc[0].text == "Jack"
    assert utterance._doc[0].pos_ == "PROPN"
    assert utterance._doc.ents[0].label_ == "PERSON"
    xml = utterance.xml()
    assert xml.tag == "{http://www.tei-c.org/ns/1.0}" + "u"
    assert xml.xpath("@who")[0] == "John"


def test_special_chars():
    speaker = "John"
    speech = "Jack gave the <ball> to Jane & Jim"
    utterance = Utterance(speaker, speech)
    utterance.nlp = spacy.load("en_core_web_sm")
    utterance.process()
    xml = utterance.xml()
    assert xml.text == "Jack gave the <ball> to Jane & Jim"
