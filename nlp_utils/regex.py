# coding: utf-8
import re
import string

ARABIC_PUNCTUATIONS = """`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ"""
ENGLISH_PUNCTUATIONS = string.punctuation

REGEX_NEWLINE = re.compile(r"(\r\n|[\n\v])+", flags=re.UNICODE | re.IGNORECASE)
REGEX_NONBREAKING_SPACE = re.compile(r"[^\S\n\v]+", flags=re.UNICODE)
REGEX_OWNERSHIP = re.compile(r"(\w|\s)\'s$", flags=re.UNICODE | re.IGNORECASE)
REGEX_CONSECUTIVE_PUNCTUATION = re.compile(f"([{ENGLISH_PUNCTUATIONS}])[{ENGLISH_PUNCTUATIONS}]+")
REGEX_HYPHENATED_WORD = re.compile(r"(\w{2,}(?<!\d))\s+-\s+((?!\d)\w{2,})", flags=re.UNICODE | re.IGNORECASE)
REGEX_URL = re.compile(
    r"\b(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)\b"
)
REGEX_EMAIL = re.compile(
    r"(?:mailto:)?" r"(?:^|(?<=[^\w@.)]))([\w+-](\.(?!\.))?)*?[\w+-]@(?:\w-?)*?\w+(\.([a-z]{2,})){1,3}" r"(?:$|(?=\b))",
    flags=re.UNICODE | re.IGNORECASE,
)
REGEX_VALID_EMAIL = re.compile(r"\b[\w.!#$%&’*+\/=?^`{|}~-]+@[\w-]+(?:\.[\w-]+)*\b", flags=re.UNICODE | re.IGNORECASE)
REGEX_PASSWORD = re.compile(
    r"(?=^.{6,}$)((?=.*\w)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[|!$%&\/\(\)\?\^\'\\\+\-\*]))^.*"
)
REGEX_IPV4_ADDRESS = re.complie(
    r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b", flags=re.UNICODE | re.IGNORECASE
)
REGEX_SSN_SIMPLE = re.complie(r"^((?<area>[\d]{3})[-][\d]{2}[-][\d]{4})$", flags=re.UNICODE | re.IGNORECASE)
# from _regex.py
REGEX_DIV = re.compile(
    ".*[career|careers|jobs|job|description|responsibility|experience|skill|qualification]-.*", re.IGNORECASE
)
REGEX_JOB_KEYWORDS = re.compile(
    r"[career|careers|jobs|job|description|responsibility|experience|skill|qualification]", re.IGNORECASE
)


REGEX_DIGITA_AROUND_COMMON = re.compile(r"(\d)[?,:;!](\d)", flags=re.UNICODE | re.IGNORECASE)

REGEX_NON_ALPHA = re.compile("^[^a-zA-Z0-9].*$")
