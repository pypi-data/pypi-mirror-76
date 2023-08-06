# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: kebo0912@outlook.com
@version: 1.0

@file: __main__.py 
@time: 2020/8/5 上午12:05

这一行开始写关于本文件的说明与解释

"""
import os
import sys
import logging
from typing import Any
from overrides import overrides
import argparse

from latex_render import __version__
from latex_render.render import LatexRender

LEVEL = logging.DEBUG
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", level=LEVEL)

logger = logging.getLogger(__name__)


class ArgumentParser(argparse.ArgumentParser):
    """
    Custom argument parser that will display the default value for an argument
    in the help message.
    """

    _action_defaults_to_ignore = {"help"}

    @staticmethod
    def _is_empty_default(default: Any) -> bool:
        if default is None:
            return True
        if isinstance(default, (str, list, tuple, set)):
            return not bool(default)
        return False

    @overrides
    def add_argument(self, *args, **kwargs):
        # Add default value to the help message when the default is meaningful.
        default = kwargs.get("default")
        if kwargs.get(
                "action"
        ) not in self._action_defaults_to_ignore and not self._is_empty_default(default):
            description = kwargs.get("help", "")
            kwargs["help"] = f"{description} (default = {default})"
        super().add_argument(*args, **kwargs)


def create_parser(program):
    """
        Creates the argument parser for the main program.
    """
    parser = ArgumentParser(description="Run Latex_render", prog=program)
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(program):
    """

    :param program:
    :return:
    """
    parser = create_parser(program=program)
    parser.add_argument("-i", "--i", required=True, dest="input_file_path", help="input file path")
    parser.add_argument("-o", "--o", required=False, dest="output_file_path",
                        help="output file path, if None use the input file path")
    parser.add_argument("-type", "--type", required=False, default=1,
                        help="type, 1: use codecogs.com  2: use render.githubusercontent.com")
    args = parser.parse_args()
    logger.info(msg=f'Use parameters: {str(args)}')
    try:
        if os.path.exists(args.input_file_path):
            if args.input_file_path.split(".")[-1] in ["md", "MD"]:
                logger.info(msg="Start rendering.....")
                latex_render = LatexRender(input_file=args.input_file_path, output_file=args.output_file_path,
                                           render_type=args.type)
                latex_render.render()
                logger.info(msg="Task complete")
            else:
                raise ValueError("input_file mast be end with `.md` or `.MD`")
        else:
            raise FileNotFoundError(f'there is no such file: `{args.input_file_path}`')
    except Exception as e:
        logger.error(msg=repr(e))


def run():
    main(program="latex_render")


if __name__ == "__main__":
    run()
