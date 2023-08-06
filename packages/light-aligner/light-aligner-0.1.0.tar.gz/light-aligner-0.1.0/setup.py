# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['light_aligner']

package_data = \
{'': ['*'],
 'light_aligner': ['stopwords/*',
                   'stopwords/.git/*',
                   'stopwords/.git/hooks/*',
                   'stopwords/.git/info/*',
                   'stopwords/.git/logs/*',
                   'stopwords/.git/logs/refs/heads/*',
                   'stopwords/.git/logs/refs/remotes/origin/*',
                   'stopwords/.git/objects/09/*',
                   'stopwords/.git/objects/14/*',
                   'stopwords/.git/objects/1d/*',
                   'stopwords/.git/objects/22/*',
                   'stopwords/.git/objects/2e/*',
                   'stopwords/.git/objects/35/*',
                   'stopwords/.git/objects/3d/*',
                   'stopwords/.git/objects/42/*',
                   'stopwords/.git/objects/4c/*',
                   'stopwords/.git/objects/55/*',
                   'stopwords/.git/objects/58/*',
                   'stopwords/.git/objects/72/*',
                   'stopwords/.git/objects/7b/*',
                   'stopwords/.git/objects/7e/*',
                   'stopwords/.git/objects/86/*',
                   'stopwords/.git/objects/8d/*',
                   'stopwords/.git/objects/ad/*',
                   'stopwords/.git/objects/b3/*',
                   'stopwords/.git/objects/bc/*',
                   'stopwords/.git/objects/d1/*',
                   'stopwords/.git/objects/ec/*',
                   'stopwords/.git/objects/ee/*',
                   'stopwords/.git/refs/heads/*',
                   'stopwords/.git/refs/remotes/origin/*']}

install_requires = \
['absl-py>=0.9.0,<0.10.0',
 'blinker>=1.4,<2.0',
 'cchardet>=2.1.6,<3.0.0',
 'chardet>=3.0.4,<4.0.0',
 'diskcache>=4.1.0,<5.0.0',
 'flake8>=3.8.3,<4.0.0',
 'jinja2>=2.11.2,<3.0.0',
 'langid>=1.1.6,<2.0.0',
 'linetimer>=0.1.4,<0.2.0',
 'logzero>=1.5.0,<2.0.0',
 'matplotlib>=3.3.0,<4.0.0',
 'msgpack>=1.0.0,<2.0.0',
 'openpyxl>=3.0.4,<4.0.0',
 'orjson>=3.3.0,<4.0.0',
 'pandas>=1.1.0,<2.0.0',
 'polyglot>=16.7.4,<17.0.0',
 'rank_bm25>=0.2.1,<0.3.0',
 'seaborn>=0.10.1,<0.11.0',
 'sentence-splitter>=1.4,<2.0',
 'textblob>=0.15.3,<0.16.0',
 'ujson>=3.1.0,<4.0.0',
 'xlrd>=1.2.0,<2.0.0',
 'yaspin>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'light-aligner',
    'version': '0.1.0',
    'description': 'a light-weight aligner.',
    'long_description': '# Light-Aligner ![build](https://github.com/ffreemt/light-aligner/workflows/build/badge.svg)\nA light-weight aligner for dual-texts (currently just English-Chinese) based on similariy scores using word for word "translation"\n\n## Features\n* Fast\n* Low resources demand\n* No internet required\n\n## Special Dependencies\nLight-Aligner depends on polyglot that depends on `libicu`\n\nTo install `libicu`\n###### For Linux/OSX\n\nE.g.\n* Ubuntu: `sudo apt install libicu-dev`\n* Centos: `yum install libicu`\n* OSX: `brew install icu4c`\n\nThen use `poetry` or `pip` to install ` PyICU pycld2 Morfessor`, e.g.\n```\npoetry add PyICU pycld2 Morfessor\n```\nor\n```\npip install PyICU pycld2 Morfessor\n```\n###### For Windows\n\nDownload and install the `pyicu` and `pycld2` (possibly also `Morfessor`) whl packages for your OS/Python version from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu and https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycld2 (possibly also Morfessor https://www.lfd.uci.edu/~gohlke/pythonlibs/)\n\n### Installation\n```pip install light-aligner``` (Not yet ready)\nor\nClone the repo and install necessary packages using `pip`:\n```\ngit clone git@github.com:ffreemt/light-aligner.git\ncd light-aigner\npip install -r requirements.txt\n```\nor\nClone the repo and install necessary packages using `poetry`\n```\ngit clone git@github.com:ffreemt/light-aligner.git\ncd light-aigner\npoetry install -v\n```\nThis also works in `Linux/OSX`. In fact, the build process in github (pertaining to that github workflow badge ![build](https://github.com/ffreemt/light-aligner/workflows/build/badge.svg)) is carried out in Linux.\n\n\n### Usage\n\n```\ncd light-aligner\npython -m light-aligner\n```\n\nYou may wish to use powershell (e.g., right click the powershell script`run-python-m.ps1` and select `Run with Powershell`) or conemu or cmder for better visual terminal experience.\n\nJoin qq-group 316287378 if you have any questions. The group chat is normally in Chinese but can be switched to English i fso desired.\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/light-aligner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
