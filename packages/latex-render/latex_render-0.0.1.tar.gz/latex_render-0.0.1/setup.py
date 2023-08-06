
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VERSION = {}  # type: ignore
with open("latex_render/version.py", "r", encoding="utf-8") as version_file:
    exec(version_file.read(), VERSION)

setup(
    name='latex_render',
    version=VERSION["VERSION"],
    author='kebo',
    author_email='kebo0912@outlook.com',
    url='https://github.com/bo-ke/latex_render',
    description='latex_render for markdown',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'typing~=3.6.4',
        'overrides~=2.8.0'
    ],
    entry_points={"console_scripts": ["latex_render=latex_render.__main__:run"]},
    python_requires='>=3.6.1',
)
