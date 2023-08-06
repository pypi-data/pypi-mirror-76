#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: XSS
@Email: 18212010042@fudan.edu.cn
@Created: 2020/06/28
------------------------------------------
@Modify: 2020/06/28
------------------------------------------
@Description:
"""
from unittest import TestCase

from sekg.text.extractor.domain_entity.entity_extractor_for_text import EntityExtractorForText


class TestEntityExtractorForText(TestCase):
    def test_extract(self):
        sent = """Specifically, workspaces are designed for cyclical workloads - such as training neural networks - as
            they allow for off-heap memory reuse (instead of continually allocating and deallocating memory on each iteration
            of the loop). 
"""

        extractor = EntityExtractorForText()
        terms = extractor.extract(sent)
        print(terms)
