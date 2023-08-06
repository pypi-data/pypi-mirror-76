# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: kebo0912@outlook.com
@version: 1.0

@file: __init__.py 
@time: 2020/8/5 上午12:01

这一行开始写关于本文件的说明与解释

"""
# Make sure that latex_render is running on Python 3.6.1 or later
# (to avoid running into this bug: https://bugs.python.org/issue29246)
import sys

if sys.version_info < (3, 6, 1):
    raise RuntimeError("latex_render requires Python 3.6.1 or later")

from latex_render.version import VERSION as __version__  # noqa
