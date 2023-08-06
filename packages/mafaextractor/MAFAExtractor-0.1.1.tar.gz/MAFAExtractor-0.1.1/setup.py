# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mafaextractor']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.1,<2.0.0', 'pandas>=1.1.0,<2.0.0', 'scipy>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'mafaextractor',
    'version': '0.1.1',
    'description': 'Extract label data from the MAFA dataset into a Pandas DataFrame.',
    'long_description': '# MAFAExtractor\n\nThis is a tool for extracting data from the [MAFA Dataset](https://openaccess.thecvf.com/content_cvpr_2017/html/Ge_Detecting_Masked_Faces_CVPR_2017_paper.html). It succesfully extracts all labels and data from the dataset\'s provided MATLAB files into a Pandas DataFrame.\n\nThe primary function is `extract_mafa()` which is all you really need if you\'re just extracting the data into Pandas. If the filename isn\'t the original `LabelTrainAll.mat` or `LabelTestAll.mat`, then you have to provide the `dataset_type` which can be either *"train"* or *"test"*. You can also choose whether you want the dataframe to be cleaned to have more readable and processed values by the `clean` parameter (which by default is True), or can be set to False if you  require the dataset\'s original headings.\n\n## Installation\nInstall mafaextractor by either running pip install into your environment using:\n```shell\npip install mafaextractor\n```\nor by cloning the github repository into your working directory:\n```shell\ngit clone https://github.com/DhyeyLalseta/MAFAExtractor\n```\n\n## Usage:\n```python3\nfrom mafaextractor import extract_mafa\n\ndf = extract_mafa("path/to/LabelTrainAll.mat <or> LabelTestAll.mat")\n\n# differing file names\ndf = extract_mafa("path/to/IChangedTheTestingSetsFileName.mat", dataset_type="test")\n\n# no cleaning\ndf = extract_mafa("path/to/TestingSet.mat", dataset_type="test", clean=False)\n```\nIf you run into any bugs or have any concerns feel free to contact me via e-mail at dhyeyl1@outlook.com!\n\n## License\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Dhyey Lalseta',
    'author_email': 'dhyeylalseta@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DhyeyLalseta/MAFAExtractor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
