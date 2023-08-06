# Latex Render

Renders LaTeX for markdown file, include Github README
<p align="center">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/LaTeX_logo.svg/200px-LaTeX_logo.svg.png">
</p>

## Installation
Make sure that you have Python 3.6.1 or above and pip installed. To install `latex_render`, you'll just need to run:
```shell script
pip install latex_render
```

## Usage
Once you've installed `latex_render`, you can run the command-line interface either with the `latex_render` command
```shell script
$ latex_render -h
usage: latex_render [-h] [--version] -i INPUT_FILE_PATH [-o OUTPUT_FILE_PATH]
                    [-type TYPE]

Run Latex_render

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -i INPUT_FILE_PATH, --i INPUT_FILE_PATH
                        Input file path;
  -o OUTPUT_FILE_PATH, --o OUTPUT_FILE_PATH
                        Output file path, if not provided, use input file path instead;
  -type TYPE, --type TYPE
                        Render type, 1: use codecogs.com 2: use
                        render.githubusercontent.com (default = 1);
```

## Citing
cite this repo
```
@misc{latex_render,
  author = {kebo},
  title = {latex_render},
  year = {2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/bo-ke/latex_render}},
  commit = {master}
}
```