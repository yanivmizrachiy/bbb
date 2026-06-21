# -*- coding: utf-8 -*-
"""Builds the grade-8 geometry booklet (content separated into topics/*.py)."""
import os
import wsengine as W
from topics import ORDER

OUT = os.path.dirname(os.path.abspath(__file__))

for mod in ORDER:
    mod.build()

W.render(
    OUT,
    h1="גאומטריה לכיתה ח'",
    subtitle="מעגל וגופים · זוויות · חפיפת משולשים · דמיון",
    meta_line="מעגל, גליל וחרוט · גאומטריה קדם-היסקית · חפיפת משולשים · דמיון",
    pdf_name="גאומטריה-ח-שאלות.pdf",
    meta={"key": "geometry8", "title": "גאומטריה לכיתה ח'", "subtitle": "מעגל, גופים, חפיפה ודמיון",
          "color": "#0d9488", "icon": "△"},
)
