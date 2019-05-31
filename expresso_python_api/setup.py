"""
Copyright 2012  IO Rodeo Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from setuptools import setup, find_packages

setup(
    name='Expresso',
    version='0.1.0',
    author='Francisco Zabala',
    author_email='cisco@iorodeo.com',
    packages=[
        'expresso/',
        'expresso/gui/',
        'expresso/gui/mcwidget_ui/',
        'expresso/libs/',
        'expresso/libs/',
        'expresso/libs/expresso_serial/',
        'expresso/libs/serial_device/',
        ],

    package_data = { },
    scripts=[
        'expresso/bin/expresso-gui',
        ],
    license='../LICENSE.txt',
    description="Serial interface and control software for IO Rodeo's Expresso.",
    long_description=open('README.txt').read(),
    install_requires= [],
)
