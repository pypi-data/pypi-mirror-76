# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asloguru', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.1,<0.6.0']

extras_require = \
{':python_version < "3.7"': ['aiocontextvars>=0.2.0'],
 ':python_version ~= "2.7" and sys_platform == "win32"': ['pathlib2'],
 ':sys_platform == "win32"': ['colorama>=0.4.3,<0.5.0',
                              'win32-setctime>=1.0.0']}

setup_kwargs = {
    'name': 'autosysloguru',
    'version': '0.4.0',
    'description': 'Fancy defaults for the awesome loguru logs!',
    'long_description': '# Auto-Loguru\n\n> Fancy defaults for the awesome loguru logs!\n\nSimple!\n\n### Install:\n\n`pip install as_loguru`\n\n---\n\n### Use in Python script:\n\n`from as_loguru import logger`\n\n---\n\n> This is a wrapper for the marvlous `loguru` logging package. Below is the information from the original project repo.\n\n<p align="center">\n    <a href="#readme">\n        <img alt="Loguru logo" src="https://raw.githubusercontent.com/Delgan/loguru/master/docs/_static/img/logo.png">\n        <!-- Logo credits: Sambeet from Pixaday -->\n        <!-- Logo fonts: Comfortaa + Raleway -->\n    </a>\n</p>\n<p align="center">\n    <a href="https://pypi.python.org/pypi/loguru"><img alt="Pypi version" src="https://img.shields.io/pypi/v/loguru.svg"></a>\n    <a href="https://pypi.python.org/pypi/loguru"><img alt="Python versions" src="https://img.shields.io/badge/python-3.5%2B%20%7C%20PyPy-blue.svg"></a>\n    <a href="https://loguru.readthedocs.io/en/stable/index.html"><img alt="Documentation" src="https://img.shields.io/readthedocs/loguru.svg"></a>\n    <a href="https://travis-ci.com/Delgan/loguru"><img alt="Build status" src="https://img.shields.io/travis/Delgan/loguru/master.svg"></a>\n    <a href="https://codecov.io/gh/delgan/loguru/branch/master"><img alt="Coverage" src="https://img.shields.io/codecov/c/github/delgan/loguru/master.svg"></a>\n    <a href="https://www.codacy.com/app/delgan-py/loguru/dashboard"><img alt="Code quality" src="https://img.shields.io/codacy/grade/4d97edb1bb734a0d9a684a700a84f555.svg"></a>\n    <a href="https://github.com/Delgan/loguru/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/github/license/delgan/loguru.svg"></a>\n</p>\n<p align="center">\n    <a href="#readme">\n        <img alt="Loguru logo" src="https://raw.githubusercontent.com/Delgan/loguru/master/docs/_static/img/demo.gif">\n    </a>\n</p>\n\n---\n\n**Loguru** is a library which aims to bring enjoyable logging in Python.\n\nDid you ever feel lazy about configuring a logger and used `print()`\ninstead?... I did, yet logging is fundamental to every application and\neases the process of debugging. Using **Loguru** you have no excuse not\nto use logging from the start, this is as simple as\n\n```py\nfrom loguru import logger\n\nlogger.info("I\'m logging now!")\n```\n\nAlso, this library is intended to make Python logging less painful by\nadding a bunch of useful functionalities that solve caveats of the\nstandard loggers. Using logs in your application should be an\nautomatism, **Loguru** tries to make it both pleasant and powerful.\n\n# Installation\n\n    pip install loguru\n\n# Features\n\n-   Ready to use out of the box without boilerplate\n-   [No Handler, no Formatter, no Filter: one function to rule them\n    all][ready to use out of the box without boilerplate]\n-   [Easier file logging with rotation / retention /\n    compression][ready to use out of the box without boilerplate]\n-   [Modern string formatting using braces\n    style][ready to use out of the box without boilerplate]\n-   [Exceptions catching within threads or\n    main][ready to use out of the box without boilerplate]\n-   [Pretty logging with\n    colors][ready to use out of the box without boilerplate]\n-   [Asynchronous, Thread-safe,\n    Multiprocess-safe][ready to use out of the box without boilerplate]\n-   [Fully descriptive\n    exceptions][ready to use out of the box without boilerplate]\n-   [Structured logging as\n    needed][ready to use out of the box without boilerplate]\n-   [Lazy evaluation of expensive\n    functions][ready to use out of the box without boilerplate]\n-   [Customizable\n    levels][ready to use out of the box without boilerplate]\n-   [Better datetime\n    handling][ready to use out of the box without boilerplate]\n-   [Suitable for scripts and\n    libraries][ready to use out of the box without boilerplate]\n-   \\`Entirely compatible with standard loggin\n\n[Ready to use out of the box without boilerplate]:\n',
    'author': 'skeptycal',
    'author_email': 'skeptycal@gmail.com',
    'maintainer': 'skeptycal',
    'maintainer_email': 'skeptycal@gmail.com ',
    'url': 'https://skeptycal.github.io/auto_loguru',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
