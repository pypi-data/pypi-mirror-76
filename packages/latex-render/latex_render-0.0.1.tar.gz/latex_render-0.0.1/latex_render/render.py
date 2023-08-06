# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: kebo0912@outlook.com
@version: 1.0

@file: render.py
@time: 2020/7/31 下午9:19

这一行开始写关于本文件的说明与解释

refer: https://www.zhihu.com/question/26887527
"""

import re
from urllib.parse import quote

CODECOGS_RENDER_URL = 'https://latex.codecogs.com/svg.latex?'
GITHUB_RENDER_URL_BASE = 'https://render.githubusercontent.com/render/math?'


class LatexRender:
    """

    """

    def __init__(self, input_file: str, output_file: str = None, render_type: int = 1):
        """

        :param input_file:
        :param output_file:
        :param render_type: 1: use codecogs.com  2: use render.githubusercontent.com default: 1
        """
        self.input_file = input_file
        self.output_file = output_file or input_file
        self.render_type = render_type

    def render(self):
        """
        render the latex element of input_file
        :return:
        """
        text = open(self.input_file, encoding="utf-8").read()
        parts = text.split("$$")
        for i, part in enumerate(parts):
            if i & 1:
                parts[i] = self._latex_part(part=part.strip(), inline=False)
        text_out = "\n".join(parts)

        lines = text_out.split('\n')
        for lid, line in enumerate(lines):
            parts = re.split(r"\$(.*?)\$", line)
            for i, part in enumerate(parts):
                if i & 1:
                    parts[i] = self._latex_part(part=part.strip())
            lines[lid] = ' '.join(parts)
        text_out = "\n".join(lines)

        with open(self.output_file, "w", encoding='utf-8') as f:
            f.write(text_out)

    def _latex_part(self, part, inline=True):
        """

        :param part:
        :param inline:
        :return:
        """
        if str(self.render_type) == '1':
            if inline:
                part = f'![math]({CODECOGS_RENDER_URL}{quote(part)})'
            else:
                part = f'<p align="center"> <img src="{CODECOGS_RENDER_URL}{quote(part)}" alt="{part}"/> </p>'
        elif str(self.render_type) == '2':
            if inline:
                part = f'![math]({GITHUB_RENDER_URL_BASE}math={quote(part)})'
            else:
                part = f'<p align="center"> <img src="{GITHUB_RENDER_URL_BASE}math={quote(part)}" alt="{part}"/> </p>'
        else:
            raise ValueError("type mast be one of `1` and `2`, but got {}".format(self.render_type))
        return part
