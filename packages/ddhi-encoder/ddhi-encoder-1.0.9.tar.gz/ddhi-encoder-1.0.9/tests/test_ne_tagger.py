# -*- coding: utf-8 -*-

from lxml import etree
import spacy
from ddhi_encoder.ne_tagger import NamedEntity, DDHINETagger

__author__ = "Clifford Wulfman"
__copyright__ = "Clifford Wulfman"
__license__ = "mit"


nlp = spacy.load("en_core_web_sm")


def test_Named_Entity():
    comparandum = etree.Element("persName")
    subject = NamedEntity({"type": "PERSON"})
    assert subject.element.tag == comparandum.tag

    comparandum = etree.Element("name", type="event")
    subject = NamedEntity({"type": "EVENT"})
    assert subject.element.tag == comparandum.tag
    assert subject.element.attrib == comparandum.attrib


def test_tagger_start_state():
    utterance = etree.Element("u")
    utterance.text = "Jane ate yesterday and burped."
    tagger = DDHINETagger(nlp, utterance)
    assert tagger._root == utterance
    assert tagger._idx is None


def test_tagger_registry():
    utterance = etree.Element("u")
    utterance.text = "Jane ate yesterday and burped."
    tagger = DDHINETagger(nlp, utterance)
    tagger.register_named_entity("EVENT")
    assert tagger.is_registered("EVENT") is True
    assert tagger.is_registered("BOGUS") is False


def test_indexes():
    utterance = etree.Element("u")
    utterance.text = "Jane ate yesterday and burped."
    tagger = DDHINETagger(nlp, utterance)
    tagger.reset_root()
    assert tagger._root.text is None
    tagger._idx = 0
    assert bool(tagger.current_entity) is False


def test_process_token():
    utterance = etree.Element("u")
    utterance.text = "Jane ate yesterday and burped."
    tagger = DDHINETagger(nlp, utterance)
    tagger.reset_root()
    tagger.process_token(0)
    assert tagger._idx == 0
    assert tagger.in_registered_entity() is True
    assert tagger.current_entity['type'] == "PERSON"
    assert tagger.current_entity['start'] == 0
    assert tagger.curr_tail() is None
    assert tagger._root.text is None
    tagger.process_token(1)
    assert tagger._idx == 1
    assert tagger.in_registered_entity() is False
    assert tagger.curr_tok().text == "ate"
    assert tagger.curr_tail().text == "Jane"
    assert tagger.curr_tail().tail == " ate "
    assert tagger._latest_entity.element.tag == "persName"
    tagger.process_token(2)
    assert tagger.in_registered_entity() is True


def test_tag():
    utterance = etree.Element("u", who="CARBONE")
    utterance.text = r"So this is Riley Carbone, and I'm at Rauner [Special Collections] Library."
    tagger = DDHINETagger(nlp, utterance)
    tagger.tag()
    assert etree.tostring(tagger._root) == b'<u who="CARBONE">So this is <persName>Riley Carbone</persName>, and I\'m at <persName>Rauner</persName> [Special Collections] Library.</u>'

def test_tag_at_end_of_sentence():
    utterance = etree.Element("u", who="SOLOMON")
    utterance.text = r"In D.C."
    tagger = DDHINETagger(nlp, utterance)
    tagger.tag()
    assert etree.tostring(tagger._root) == b'<u who="SOLOMON">In <placeName>D.C.</placeName></u>'
