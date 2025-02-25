#!/bin/bash

echo "========== Start dbt with Luigi Orchestration Process =========="

# Accessing Env Variables
source .venv

# Activate Virtual Environment
source ".venv/bin/activate"

# Set Python script
PYTHON_SCRIPT="$ROOT_DIR/source_to_staging/pipeline_main.py"

# Get Current Date
current_datetime=$(date '+%d-%m-%Y_%H-%M')


echo "========== End of dbt with Luigi Orchestration Process =========="