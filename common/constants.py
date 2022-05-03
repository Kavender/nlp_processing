# -*- coding: utf-8 -*-

BRACKET_ESCAPES = {'-lrb-': '(', '-rrb-': ')',
                   '-lcb-': '{', '-rcb-': '}',
                   '-lsb-': '[', '-rsb-': ']'}
TOKEN_MAPPING = {"``": '"', "''": '"',
                 "<s>": "", "</s>": "",
                 **BRACKET_ESCAPES}

ARABIC_PUNCTUATIONS = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
