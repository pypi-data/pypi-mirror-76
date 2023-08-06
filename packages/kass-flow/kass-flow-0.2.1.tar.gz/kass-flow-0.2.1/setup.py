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
    'version': '0.2.1',
    'description': 'Library to manage payments using the KASS API',
    'long_description': '# Kass Flow\n\nHelper for the [KASS](https://www.kass.is/) payment gateway. Written for python 3.8.5 (probably works on versions >= 3.6).\n\nSee the [KASS API docs](https://kass.github.io/api/) for more info.\n\nThis module is not affiliated with KASS.\n\n## TODO\n\n- [x] Create payment\n- [ ] Retreive payment info\n- [ ] Retreive payment status\n- [ ] Cancel payment\n- [ ] Add concurrency with RQ when dispatching multiple payments\n\n## Usage\n\nHere is a short guide to get you started.\n\nThis will dispatch a payment to the KASS API.\n\n```python\nfrom kass_flow import kass\n\nkass_token: str = "some-token"\nkass_url: str = "https://api.kass.is/v1/payments"\ninstance = kass.KassBilling(kass_token, kass_url)\n\npayload: kass.KassRequestPaymentDict = {\n    "amount": 2199,\n    "description": "Kass bolur",\n    "image_url": "https://photos.kassapi.is/kass/kass-bolur.jpg",\n    "order": "ABC123",\n    "recipient": "7798217",\n    "terminal": 1,\n    "expires_in": 90,\n    "notify_url": "https://example.com/callbacks/kass",\n}\n\nresult, is_valid = instance.dispatch(payload)\n```\n\nWhen the recipient cancels or pays the requested order KASS will send a callback to the `notify_url`, which you need to catch on your server and validate the signature included in the POST payload.\n\n```python\nis_valid = instance.is_signature_valid(payload)\n```\n\nThe payload can now be processed.\n\n## Development\n\n```sh\npip install poetry\n # to manage envs yourself\npoetry config virtualenvs.create false\npoetry install\npytest tests\n```\n\nIf you are using VSCode for development there is a `.vscode/settings.example.json` for sensible defaults. Since mypy is used you need to install the `mypyls` language server.\n\n```\npoetry install "https://github.com/matangover/mypyls/archive/master.zip#egg=mypyls[default-mypy]"\n# or\npip install "https://github.com/matangover/mypyls/archive/master.zip#egg=mypyls[default-mypy]"\n```\n',
    'author': 'Jón Levy',
    'author_email': 'nonni@nonni.cc',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/busla/kass-flow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
