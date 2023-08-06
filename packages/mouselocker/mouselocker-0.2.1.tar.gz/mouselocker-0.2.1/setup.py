#!/usr/bin/env python3
# -*- coding: utf-8 -*- 


"""
Инструкции:

python3 setup.py sdist bdist_wheel - Сборка пакета
sudo python3 setup.py develop - Установка пакета для разработки
sudo python3 setup.py develop -u - Uninstall
sudo pip3 install dist/mouselocker-0.2.1.tar.gz - Установка пакета
sudo pip3 uninstall mouselocker - Удаление пакета
python3 -m twine upload --repository pypi dist/* - Залить на сервер
twine upload dist/* - Новая команда залить в pypi

Список классификации:
https://pypi.python.org/pypi?%3Aaction=list_classifiers
"""


from setuptools import setup, find_packages
from os.path import abspath, dirname, join

setup(
	name="mouselocker",
	version="0.2.1",
	description="Mouse Locker Program",
	long_description=open(join(abspath(dirname(__file__)), 'README.md'), encoding='utf-8').read(),
	long_description_content_type='text/markdown',
	author="Ildar Bikmamatov",
	author_email="vistoyn@gmail.com",
	license="GNU General Public License v3",
	url = "https://github.com/vistoyn/mouselocker2",
	packages=find_packages(),
	include_package_data = True,
	scripts=[
		'scripts/mouselocker'
	],
	install_requires=[
		'PyQt5',
		'python-xlib',
	],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Environment :: X11 Applications',
		'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
		'Operating System :: POSIX :: Linux',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Topic :: Utilities',
	],
)