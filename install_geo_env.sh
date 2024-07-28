#!/bin/bash

# Define environment name
ENV_NAME="geo_env"

# Create a new virtual environment
python3 -m venv $ENV_NAME

# Activate the environment
source $ENV_NAME/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install geopy pandas jupyter folium ipykernel

# Create a new IPython kernel
python -m ipykernel install --user --name $ENV_NAME --display-name "Python ($ENV_NAME)"

echo "IPython kernel environment '$ENV_NAME' created successfully with geopy, pandas, jupyter, and folium."

# Deactivate the environment
deactivate

# Optional: To list the newly created kernel
jupyter kernelspec list
