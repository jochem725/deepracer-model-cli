# AWS DeepRacer Model CLI
The DeepRacer Model CLI contains utility commands for working with AWS DeepRacer models. 

## Setup
Install the [Poetry](https://github.com/sdispater/poetry) dependency manager for Python and install the dependencies via `poetry install`. 
Then activate the virtual environment using `poetry shell`

## Usage
To run the toolset you need the complete model folder obtained from local training. 
This is the folder that contains `.coach_checkpoint`, `*.ckpt.*`, `model_metadata.json` and `model_*.pb`.

### Archive model for running on physical car
`deepracer-model-cli <PATH TO MODEL FOLDER> <PATH TO OUTPUT TARFILE> --[export_last|export_best]`