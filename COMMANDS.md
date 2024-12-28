

```bash
source ~/miniconda3/bin/activate && conda create --prefix ./env python=3.10

source ~/miniconda3/bin/activate ./env

conda install -c conda-forge tree-sitter

# Install poetry project
poetry install
```