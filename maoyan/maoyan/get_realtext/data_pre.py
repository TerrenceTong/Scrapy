# -*- coding: utf-8 -*-

from fontTools.ttLib import TTFont


font = TTFont("72a82e70f92e717337c58ceef6272be42080.woff")
font.saveXML('template.xml')