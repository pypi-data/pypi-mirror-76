# -*- coding: utf-8 -*-

import os
from ddhi_encoder.interview_generator import InterviewGenerator,InterviewGeneratorFactory


__author__ = "Clifford Wulfman"
__copyright__ = "Clifford Wulfman"
__license__ = "mit"


test_file = os.path.join(
    os.path.dirname(__file__),
    "transcript1.docx"
    )


def test_generator_factory():
    factory = InterviewGeneratorFactory()
    generator = factory.interview_for("DDHI", test_file)
    assert type(generator) is InterviewGenerator


def test_interview_generator():
    factory = InterviewGeneratorFactory()
    generator = factory.interview_for("DDHI", test_file)
    generator.update_tei()
