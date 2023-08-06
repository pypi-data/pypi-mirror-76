# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['olliepy',
 'olliepy.utils',
 'reports-templates',
 'reports-templates.regression-error-analysis-report']

package_data = \
{'': ['*'],
 'reports-templates.regression-error-analysis-report': ['css/*',
                                                        'img/*',
                                                        'js/*']}

install_requires = \
['flask>=1.1.2,<2.0.0',
 'ipython>=7.17.0,<8.0.0',
 'numpy>=1.19.1,<2.0.0',
 'pandas>=1.1.0,<2.0.0',
 'pycrypto>=2.6.1,<3.0.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'scipy>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'olliepy',
    'version': '0.1.1',
    'description': 'An interactive reporting tool written in python for machine learning experiments that generates interactive reports written in VueJS.',
    'long_description': None,
    'author': 'ahmed.mohamed',
    'author_email': 'hanoush87@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
