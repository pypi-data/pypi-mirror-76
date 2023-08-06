# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_ulogin',
 'django_ulogin.migrations',
 'django_ulogin.templatetags',
 'django_ulogin.tests']

package_data = \
{'': ['*'],
 'django_ulogin': ['locale/ru/LC_MESSAGES/*', 'templates/django_ulogin/*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'django-ulogin',
    'version': '1.1.1',
    'description': 'User social authentication with ulogin.ru service',
    'long_description': 'django-ulogin\n=============\n\n\n.. image:: https://travis-ci.org/marazmiki/django-ulogin.svg?branch=master\n     :target: https://travis-ci.org/marazmiki/django-ulogin\n     :alt: Travis CI building status\n\n.. image:: https://coveralls.io/repos/github/marazmiki/django-ulogin/badge.svg?branch=master\n     :target: https://coveralls.io/github/marazmiki/django-ulogin?branch=master\n     :alt: Code coverage status\n\n.. image:: https://badge.fury.io/py/django-ulogin.svg\n     :target: http://badge.fury.io/py/django-ulogin\n     :alt: PyPI release\n\n.. image:: https://pypip.in/wheel/django-ulogin/badge.svg\n     :target: https://pypi.python.org/pypi/django-ulogin/\n     :alt: Wheel Status\n\n.. image:: https://img.shields.io/pypi/pyversions/django-ulogin.svg\n     :target: https://img.shields.io/pypi/pyversions/django-ulogin.svg\n     :alt: Supported Python versions\n\n.. image:: https://img.shields.io/pypi/djversions/django-ulogin.svg\n     :target: https://pypi.python.org/pypi/django-ulogin/\n     :alt: Supported Django versions\n\n.. image:: https://readthedocs.org/projects/django-ulogin/badge/?version=latest\n     :target: https://django-ulogin.readthedocs.io/ru/latest/?badge=latest\n     :alt: Documentation Status\n\n\nОписание\n--------\n\n**django-ulogin** — подключаемое универсальное django-приложение для социальной аутентификации пользователей с помощью внешнего интернет-сервиса `uLogin <https://ulogin.ru>`_\n\n\n.. attention::\n    Создатели приложения никак не связаны с интернет-сервисом `uLogin <https://ulogin.ru>`_, поэтому все вопросы, касающиеся непосредственно работы сервиса, а не этого приложения, просьба отправлять на `team@ulogin.ru <team@ulogin.ru>`_.\n\n\nПодробная документация проекта доступна на `Read the Docs <https://django-ulogin.readthedocs.org/>`_.\n',
    'author': 'Mikhail Porokhovnichenko',
    'author_email': 'marazmiki@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
