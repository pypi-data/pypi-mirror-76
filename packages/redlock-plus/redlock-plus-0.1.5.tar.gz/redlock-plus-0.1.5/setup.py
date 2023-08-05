# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['redlock_plus']
install_requires = \
['redis>=3.5.3,<4.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0'],
 'docs': ['sphinx>=3.1.2,<4.0.0'],
 'docs:platform_python_implementation == "CPython"': ['sphinx-autodoc-typehints>=1.11.0,<2.0.0']}

setup_kwargs = {
    'name': 'redlock-plus',
    'version': '0.1.5',
    'description': 'Distributed locks with Redis',
    'long_description': '.. _Redlock Algorithm: https://redis.io/topics/distlock#the-redlock-algorithm\n\n========\nRedlock+\n========\n\n.. image:: https://img.shields.io/pypi/implementation/redlock-plus?style=flat-square\n  :target: https://pypi.org/project/redlock-plus/\n.. image:: https://img.shields.io/pypi/pyversions/redlock-plus?style=flat-square\n  :target: https://pypi.org/project/redlock-plus/\n.. image:: https://github.com/provinzkraut/redlock-plus/workflows/Tests/badge.svg\n  :target: https://github.com/provinzkraut/redlock-plus/actions?query=workflow%3ATests\n\nRedlock+ is an up to date, feature complete implementation of the `Redlock Algorithm`_\nIt\'s a spiritual successor to `glasslion/redlock <https://github.com/glasslion/redlock>`_, which is no longer maintained.\n\n\nFeatures\n=========\n\n- Compliant with the standard library `Lock <https://docs.python.org/3/library/threading.html#threading.Lock>`_\n  and `RLock <https://docs.python.org/3/library/threading.html#threading.RLock>`_ so it can be used as a drop-in replacement\n- Complete implementation of the `Redlock Algorithm`_\n- Autoextend functionality to make redlock safer and easier to use\n- Well tested (Python 3.6+, PyPy3)\n- Type hinted\n\n\nDocumentation\n=============\n\nhttps://redlock-plus.readthedocs.io/en/latest/\n\n\nInstallation\n============\n\nRedlock+ is available on `PyPi <https://pypi.org/project/redlock-plus/>`_:\n\n.. code-block:: bash\n\n  pip install redlock-plus\n\n\nBasic usage\n===========\n\n.. code-block:: python\n\n    from redlock_plus import Lock\n\n    redis_instance_configs = [\n        {"url": "redis://localhost/0"},\n        {"url": "redis://example.com:1234/1"},\n        {"url": "redis://other.host:5678/2"},\n    ]\n\n    with Lock("my_resource", redis_instance_configs):\n        # do work\n\nor speed up things for repeated use using the factory\n\n.. code-block:: python\n\n    from redlock_plus import LockFactory\n\n    redlock_factory = LockFactory(\n        [\n            {"url": "redis://localhost/0"},\n            {"url": "redis://localhost/1"},\n            {"url": "redis://localhost/2"},\n        ]\n    )\n\n    with redlock_factory("my_resource"):\n        # do work\n',
    'author': 'Janek Nouvertné',
    'author_email': 'provinzkraut@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/provinzkraut/redlock-plus',
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
