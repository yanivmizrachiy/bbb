# -*- coding: utf-8 -*-
"""Builds the grade-8 algebra booklet.

Content is fully separated into topics/*.py — each topic is added here in the
order of the source curriculum. To add/edit a topic, edit its file (or this
ordered list); nothing else needs to change.
"""
import os
import wsengine as W
from topics import ORDER  # ordered list of topic modules

OUT = os.path.dirname(os.path.abspath(__file__))

for mod in ORDER:
    mod.build()          # each appends its SECTION + questions

W.render(
    OUT,
    h1="אלגברה לכיתה ח'",
    subtitle="פונקציות, גרפים, משוואות ואי-שוויונות",
    meta_line="פונקציה וגרף · קצב שינוי ושיפוע · משוואת הישר · אי-שוויונות · מערכות משוואות",
    pdf_name="אלגברה-ח-שאלות.pdf",
    meta={"key": "algebra8", "title": "אלגברה לכיתה ח'", "subtitle": "פונקציות, גרפים ומשוואות",
          "color": "#7c3aed", "icon": "ƒ"},
)
