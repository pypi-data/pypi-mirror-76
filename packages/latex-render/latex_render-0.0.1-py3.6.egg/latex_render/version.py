# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: kebo0912@outlook.com
@version: 1.0

@file: version.py 
@time: 2020/8/5 上午12:03

这一行开始写关于本文件的说明与解释

"""
_MAJOR = "0"
_MINOR = "0"
# On master and in a nightly release the patch should be one ahead of the last
# released build.
_PATCH = "1"
# See https://semver.org/#is-v123-a-semantic-version for the semantics.

VERSION_SHORT = "{}.{}".format(_MAJOR, _MINOR)
VERSION = "{}.{}.{}".format(_MAJOR, _MINOR, _PATCH)
