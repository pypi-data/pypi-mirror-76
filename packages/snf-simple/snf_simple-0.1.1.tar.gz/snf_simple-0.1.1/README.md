# Similarity Network Fusion (SNF)
SNF python implementation with intention to be 1-2 with MatlabV 2.1

Reference:

> B Wang, A Mezlini, F Demir, M Fiume, T Zu, M Brudno, B Haibe-Kains, A Goldenberg (2014) Similarity Network Fusion: a fast and effective method to aggregate multiple data types on a genome wide scale. Nature Methods. Online. Jan 26, 2014

## Usage
Install from pypi:
```shell script
pip install snf_simple
```



## Using the module
You can see an example usage under [demo](./examples/demo.py)

## Development
The project is using [poetry](https://python-poetry.org/) for reliable development.

See poetry documentation on how to install the latest version for your system:

> https://python-poetry.org/docs

### Setup
After installing poetry, start an environment:

```shell script
poetry install
```

If you are using PyCharm you can use [this plugin](https://plugins.jetbrains.com/plugin/14307-poetry) for setting up interpreter.

### Testing
Tests are using standard `pytest` format. You can run them after the setup with:

```shell script
pytest
```
