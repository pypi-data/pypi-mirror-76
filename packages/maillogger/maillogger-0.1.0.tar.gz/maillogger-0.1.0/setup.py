# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maillogger', 'maillogger.file']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['maillogger = maillogger.main:main']}

setup_kwargs = {
    'name': 'maillogger',
    'version': '0.1.0',
    'description': 'Analysis tool for Postfix log in /var/log/maillog',
    'long_description': '# maillogger\n\n![PyPI](https://img.shields.io/pypi/v/maillogger)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/maillogger)\n![PyPI - License](https://img.shields.io/pypi/l/maillogger)\n\nAnalysis tool for Postfix log in /var/log/maillog\n\n<!-- TOC depthFrom:2 -->\n\n- [Feature](#feature)\n- [Installation](#installation)\n- [Usage](#usage)\n- [Examples](#examples)\n  - [Output a CSV file](#output-a-csv-file)\n  - [Output a JSON file](#output-a-json-file)\n  - [Output a TSV file](#output-a-tsv-file)\n  - [Output a compressed CSV file](#output-a-compressed-csv-file)\n\n<!-- /TOC -->\n\n## Feature\n\n- Load maillog file\n  - Identify text or gzip automatically\n- Parse maillog\n  - Use regex\n  - Convert to Python dictionary\n- Output the parsed maillog to files\n  - Supported data format is CSV, TSV and JSON\n  - Compression (gzip) is possible\n\n## Installation\n\n```bash\npip install maillogger\n```\n\n## Usage\n\n```\nusage: maillogger [-h] [-f {csv,tsv,json}] [-c] [-V] source_file target_file\n\nAnalysis tool for Postfix log in /var/log/maillog\n\npositional arguments:\n  source_file           Specify Postfix maillog file\n  target_file           Specify the filename to write parsed maillog. The file\n                        extension is automatically added to the end of\n                        filename.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -f {csv,tsv,json}, --format {csv,tsv,json}\n                        File data format to write the parsed maillog (Default:\n                        csv)\n  -c, --compress        Compress the output file with gzip\n  -V, --version         Show maillogger command version\n```\n\n## Examples\n\n### Output a CSV file\n\n```bash\nmaillogger /var/log/maillog result\n```\n\nor\n\n```bash\nmaillogger /var/log/maillog result -f csv\n```\n\nThen, `result.csv` is generated in current working directory.\n\n### Output a JSON file\n\n```bash\nmaillogger /var/log/maillog result -f json\n```\n\n### Output a TSV file\n\n```bash\nmaillogger /var/log/maillog result -f tsv\n```\n\n### Output a compressed CSV file\n\n```bash\nmaillogger /var/log/maillog result -f csv -c\n```\n\nThen, `result.csv.gz` is generated in current working directory.\n',
    'author': 'homoluctus',
    'author_email': 'w.slife18sy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/homoluctus/maillogger',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
