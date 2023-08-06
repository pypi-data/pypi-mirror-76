# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bananopy']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'bananopy',
    'version': '0.3.2',
    'description': 'Python library for interaction with Banano',
    'long_description': '===============================\n🍌\U0001f967: Banano Python Library\n===============================\n\n.. image:: https://img.shields.io/pypi/l/bananopy.svg\n    :target: https://github.com/milkyklim/bananopy/blob/master/LICENSE\n    :alt: License\n\n.. image:: https://github.com/milkyklim/bananopy/workflows/CI/badge.svg\n    :target: https://github.com/milkyklim/bananopy/actions\n    :alt: Build Status\n\n.. image:: https://img.shields.io/github/workflow/status/milkyklim/bananopy/CI?label=docs\n    :target: https://milkyklim.github.io/bananopy\n    :alt: Documentation Status\n\n.. image:: https://img.shields.io/pypi/pyversions/bananopy.svg\n    :target: https://pypi.python.org/pypi/\n    :alt: Supported Python Versions\n\n.. image:: https://img.shields.io/pypi/v/bananopy.svg\n    :target: https://pypi.python.org/pypi/bananopy\n    :alt: Package Version\n\n.. image:: https://img.shields.io/badge/Banano%20Node-v20.0-yellow\n    :alt: Banano Node Version\n\n🍌\U0001f967 is a python wrapper for Banano node communication.\nIt takes care of RPC responses (type conversions) and exposes a pythonic API for making RPC calls.\n\nFull list of RPC calls is coming from `docs <https://docs.nano.org/commands/rpc-protocol/>`_.\n\n**Setup**\n\n.. code-block:: bash\n\n    pip install bananopy\n\nBananopy checks if ``BANANO_HTTP_PROVIDER_URI`` environment variable is set.\n\nTo set it run:\n\n.. code-block:: bash\n\n    export BANANO_HTTP_PROVIDER_URI=<ip_address>\n\n\nOtherwise, bananopy will fallback and use public node (``https://api-beta.banano.cc``) for API calls.\n\n**Note:** Public node is running Banano Node v18, meaning some requests might fail.\n\n**Development**\n\nRepository uses `poetry <https://python-poetry.org/>`_ to keep track of dependances. Once you have poetry installed make sure\nyou are on Python 3.7+ and run these commands:\n\n.. code-block:: bash\n\n    git clone https://github.com/milkyklim/bananopy.git\n    poetry install\n\nTo run the tests:\n\n.. code-block:: bash\n\n    poetry run pytest -v\n\n**Note:** Only public requests are actually tested. Dangerous RPC calls controlled by ``enable_control`` are checked for error response only.\n\n**Conversion**\n\n``float`` type is not supported in conversion, e.g. ``ban_to_banoshi`` cause it might lead to unexpected precision loss.\nUse ``str``, ``int`` or ``Decimal`` types instead.\n\n**Example**\n\n.. code-block:: python\n\n    >>> import bananopy.banano as ban\n    Using https://api-beta.banano.cc as API provider on port 7072\n\n    >>> account = "ban_1bananobh5rat99qfgt1ptpieie5swmoth87thi74qgbfrij7dcgjiij94xr"\n    >>> ban.account_balance(account)\n    {\'balance\': 1626688000000000000017763568393401, \'pending\': 0}\n\n**Support**\n\nBenis to ``ban_1dsarukqn5y8oqho43praocn97wjs17t8eppzgfb78nzzxmjapkidxrcgsqc``\n',
    'author': 'milkyklim',
    'author_email': '10698619+milkyklim@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/milkyklim/bananopy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
