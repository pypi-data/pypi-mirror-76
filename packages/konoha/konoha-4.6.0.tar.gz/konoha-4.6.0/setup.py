# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['konoha',
 'konoha.api',
 'konoha.data',
 'konoha.integrations',
 'konoha.word_tokenizers']

package_data = \
{'': ['*']}

install_requires = \
['overrides==3.0.0']

extras_require = \
{'all': ['janome>=0.3.10,<0.4.0',
         'natto-py>=0.9.0,<0.10.0',
         'kytea>=0.1.4,<0.2.0',
         'sentencepiece>=0.1.85,<0.2.0',
         'sudachipy==0.4.5',
         'boto3>=1.11.0,<2.0.0',
         'fastapi>=0.54.1,<0.55.0',
         'uvicorn>=0.11.5,<0.12.0',
         'sudachidict-core>=20200330,<20200331',
         'nagisa>=0.2.7,<0.3.0'],
 'all_with_integrations': ['janome>=0.3.10,<0.4.0',
                           'natto-py>=0.9.0,<0.10.0',
                           'kytea>=0.1.4,<0.2.0',
                           'sentencepiece>=0.1.85,<0.2.0',
                           'sudachipy==0.4.5',
                           'boto3>=1.11.0,<2.0.0',
                           'allennlp>=1.0.0,<2.0.0',
                           'fastapi>=0.54.1,<0.55.0',
                           'uvicorn>=0.11.5,<0.12.0',
                           'sudachidict-core>=20200330,<20200331',
                           'nagisa>=0.2.7,<0.3.0'],
 'allennlp': ['allennlp>=1.0.0,<2.0.0'],
 'docs': ['sphinx>=3.1.1,<4.0.0', 'sphinx_rtd_theme>=0.4.3,<0.5.0'],
 'janome': ['janome>=0.3.10,<0.4.0'],
 'kytea': ['kytea>=0.1.4,<0.2.0'],
 'mecab': ['natto-py>=0.9.0,<0.10.0'],
 'nagisa': ['nagisa>=0.2.7,<0.3.0'],
 'remote': ['boto3>=1.11.0,<2.0.0'],
 'sentencepiece': ['sentencepiece>=0.1.85,<0.2.0'],
 'server': ['fastapi>=0.54.1,<0.55.0', 'uvicorn>=0.11.5,<0.12.0'],
 'sudachi': ['sudachipy==0.4.5', 'sudachidict-core>=20200330,<20200331']}

setup_kwargs = {
    'name': 'konoha',
    'version': '4.6.0',
    'description': 'A tiny sentence/word tokenizer for Japanese text written in Python',
    'long_description': None,
    'author': 'himkt',
    'author_email': 'himkt@klis.tsukuba.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
