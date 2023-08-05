# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pysigtool']
install_requires = \
['lief>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['pysigtool = pysigtool:main']}

setup_kwargs = {
    'name': 'pysigtool',
    'version': '0.1.4',
    'description': 'Extract digital signatures contained in a PE file.',
    'long_description': 'pysigtool\n=======================================\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n\nExtract digital signatures contained in a PE file.\n\nInstall\n---------------------------------------\n\n```\n$ pip install pysigtool\n```\n\nUsage\n---------------------------------------\n\n```\n$ pysigtool msvcr120.dll\nsaving msvcr120_dll.der\n$ ls msvcr120_dll.der\nmsvcr120_dll.der\n$ openssl pkcs7 -in msvcr120_dll.der -inform der -print\nPKCS7: \n  type: pkcs7-signedData (1.2.840.113549.1.7.2)\n  d.sign: \n    version: 1\n    md_algs:\n        algorithm: sha1 (1.3.14.3.2.26)\n        parameter: NULL\n    contents: \n      type: undefined (1.3.6.1.4.1.311.2.1.4)\n      d.other: SEQUENCE:\n....\n```\n\n',
    'author': 'Koh M. Nakagawa',
    'author_email': 'tsunekou1019@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kohnakagawa/pysigtool',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
