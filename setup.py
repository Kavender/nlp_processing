from setuptools import setup, find_packages
import os

# Package Info
PACKAGE_NAME = "nlp_tookit"
AUTHOR = "Shisi Wang"
AUTHOR_EMAIL = "kavender.wang@gmail.com"
DESCRIPTION = "Out of box implementation of nlp utils to simply code development"
URL = "https://github.com/Kavender/nlp_toolkit"
KEYWORDS = ["NLP", "GenAI", "extraction", "transformation", "nlp_tookit"]
LICENSE = "Your License, e.g., MIT or Apache License 2.0"

# Version Info
_MAJOR = "0"
_MINOR = "0"
_PATCH = "1"
_SUFFIX = os.environ.get("PACKAGE_VERSION_SUFFIX", "-unreleased")

# Dependencies
BASIC_DEPENDENCIES = ["python-dotenv>=1.0.0", "pandas>=1.2.5", "overrides>=7.4.0"]

SIMILARITY_DEPENDENCIES = ["Metaphone==0.6"]

LANGUAGE_DEPENDENCIES = ["nltk>=3.3", "spacy>=3.0.0,<3.1.0"]

LLM_DEPENDENCIES = ["openai>=0.27.0", "tiktokens>=0.3.3", "tenacity>=8.2.3"]

DEV_DEPENDENCIES = ["pytest>=7.4.2"]

ALL_DEPENDENCIES = BASIC_DEPENDENCIES + SIMILARITY_DEPENDENCIES + LANGUAGE_DEPENDENCIES + LLM_DEPENDENCIES + DEV_DEPENDENCIES

# --- CUSTOMIZABLE SECTION ENDS HERE ---

VERSION_SHORT = "{0}.{1}".format(_MAJOR, _MINOR)
VERSION = "{0}.{1}.{2}{3}".format(_MAJOR, _MINOR, _PATCH, _SUFFIX)


# Reading the long description from README.md
try:
    with open("README.md", "r") as f:
        LONG_DESCRIPTION = f.read()
except:
    LONG_DESCRIPTION = DESCRIPTION

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    keywords=KEYWORDS,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(exclude=["*.pyc", "__pycache__", "tests*.*", "tests"]),
    zip_safe=False,
    license=LICENSE,
    install_requires=BASIC_DEPENDENCIES,
    extras_require={
        "language": LANGUAGE_DEPENDENCIES,
        "llm": LLM_DEPENDENCIES,
        "dev": DEV_DEPENDENCIES,
        "all": ALL_DEPENDENCIES,
    },
    include_package_data=True,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
)
