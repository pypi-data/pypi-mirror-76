# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kass_flow']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'kass-flow',
    'version': '0.2.5',
    'description': 'Library to manage payments using the KASS API',
    'long_description': '\nKass Flow\n=========\n\nHelper for the `KASS <https://www.kass.is/>`_ payment gateway. Written for python 3.8.5 (probably works on versions >= 3.6).\n\nSee the `KASS API docs <https://kass.github.io/api/>`_ for more info.\n\nThis module is not affiliated with KASS.\n\nTODO\n----\n\n\n* [x] Create payment\n* [ ] Retreive payment info\n* [ ] Retreive payment status\n* [ ] Cancel payment\n* [ ] Add concurrency with RQ when dispatching multiple payments\n\nUsage\n-----\n\nHere is a short guide to get you started.\n\nThis will dispatch a payment to the KASS API.\n\n.. code-block:: sh\n\n   poetry add kass-flow\n   # or\n   pip install kass-flow\n\n.. code-block:: python\n\n   from kass_flow.kass import KassBilling\n   from kass_flow.interfaces import KassRequestPaymentDict\n\n   kass_token: str = "some-token"\n   kass_url: str = "https://api.kass.is/v1/payments"\n   instance = KassBilling(kass_token, kass_url)\n\n   payload: KassRequestPaymentDict = {\n       "amount": 2199,\n       "description": "Kass bolur",\n       "image_url": "https://photos.kassapi.is/kass/kass-bolur.jpg",\n       "order": "ABC123",\n       "recipient": "7798217",\n       "terminal": 1,\n       "expires_in": 90,\n       "notify_url": "https://example.com/callbacks/kass",\n   }\n\n   result, is_valid = instance.dispatch(payload)\n\nWhen the recipient cancels or pays the requested order KASS will send a callback to the ``notify_url``\\ , which you need to catch on your server and probably validate the signature that is included in the POST payload.\n\nAt some point in time the user will pay/reject the requested order. Here is an example on how to validate the payload.\n\n.. code-block:: python\n\n   from kass_flow.kass import KassBilling\n   from kass_flow.interfaces import KassRequestPaymentDict\n\n   def some_view_that_handles_kass_callback(request):\n       payload = request.data\n       kass_token: str = "some-token"\n       kass_url: str = "https://api.kass.is/v1/payments"\n       instance = KassBilling(kass_token, kass_url)\n\n       if instance.is_signature_valid(payload):\n           # process the payload.\n\nDevelopment\n-----------\n\n.. code-block:: sh\n\n   pip install poetry\n    # to manage envs yourself\n   poetry config virtualenvs.create false\n   poetry install\n   pytest tests\n\nIf you are using VSCode for development there is a ``.vscode/settings.example.json`` for sensible defaults. Since mypy is used you need to install the ``mypyls`` language server.\n\n.. code-block::\n\n   poetry install "https://github.com/matangover/mypyls/archive/master.zip#egg=mypyls[default-mypy]"\n   # or\n   pip install "https://github.com/matangover/mypyls/archive/master.zip#egg=mypyls[default-mypy]"\n',
    'author': 'Jón Levy',
    'author_email': 'nonni@nonni.cc',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/busla/kass-flow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<=3.8',
}


setup(**setup_kwargs)
