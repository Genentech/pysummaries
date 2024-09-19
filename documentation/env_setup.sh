#/bin/bash

set -e

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# for ipywidgets to function correctly
#jupyter labextension install @jupyter-widgets/jupyterlab-manager@2.0.0
