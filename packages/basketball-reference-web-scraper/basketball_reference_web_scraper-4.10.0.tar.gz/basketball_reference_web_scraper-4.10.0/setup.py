# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['basketball_reference_web_scraper', 'basketball_reference_web_scraper.output']

package_data = \
{'': ['*']}

install_requires = \
['certifi==2018.10.15',
 'chardet==3.0.4',
 'idna==2.7',
 'lxml==4.5.1',
 'pytz==2018.6',
 'requests==2.20.0',
 'urllib3==1.24.3']

setup_kwargs = {
    'name': 'basketball-reference-web-scraper',
    'version': '4.10.0',
    'description': 'A Basketball Reference client that generates data by scraping the website',
    'long_description': '<p align="center">\n    <a href="#" target="_blank" rel="noopener noreferrer">\n        <img width="550" src="https://imgur.com/dJL05Ud.png" alt="logo">\n    </a>\n</p>\n<p align="center">\n    <a href="https://pypi.org/project/basketball-reference-scraper/">\n        <img src="https://img.shields.io/pypi/v/basketball_reference_web_scraper" alt="pypi" />\n    </a>\n    <a href="https://pypi.org/project/basketball-reference-scraper/">\n        <img src="https://img.shields.io/pypi/pyversions/basketball_reference_web_scraper" alt="python version" />\n    </a>\n    <a href="https://pypi.org/project/basketball-reference-scraper/">\n        <img src="https://img.shields.io/pypi/l/basketball_reference_web_scraper" alt="license" />\n    </a>\n    <a href="https://codecov.io/gh/jaebradley/basketball_reference_web_scraper">\n        <img src="https://codecov.io/gh/jaebradley/basketball_reference_web_scraper/branch/v4/graph/badge.svg" alt="code coverage" />\n    </a>\n    <a href="https://github.com/jaebradley/basketball_reference_web_scraper/workflows/Basketball%20Reference%20Web%20Scraper/badge.svg">\n        <img src="https://github.com/jaebradley/basketball_reference_web_scraper/workflows/Basketball%20Reference%20Web%20Scraper/badge.svg" alt="continuous integration" />\n    </a>\n</p>\n\n[Basketball Reference](http://www.basketball-reference.com) is a great site (especially for a basketball stats nut like me), and hopefully they don\'t get too pissed off at me for creating this.\n\nI initially wrote this library as an exercise for creating my first `PyPi` package - hope you find it valuable!  \n\n## Documentation\n\nFor documentation about installing the package and API methods see [the documentation page](https://jaebradley.github.io/basketball_reference_web_scraper/).\n\n## Contributors\n\nThanks to [@DaiJunyan](https://github.com/DaiJunyan), [@ecallahan5](https://github.com/ecallahan5), \n[@Yotamho](https://github.com/Yotamho), and [@ntsirakis](https://github.com/ntsirakis) for their contributions!\n\n',
    'author': 'Jae Bradley',
    'author_email': 'jae.b.bradley@gmail.com',
    'maintainer': 'Jae Bradley',
    'maintainer_email': 'jae.b.bradley@gmail.com',
    'url': 'https://jaebradley.github.io/basketball_reference_web_scraper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
