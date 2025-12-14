#!/bin/bash
#SBATCH -p publicgpu 
#SBATCH --job-name=LLM_Triple_Extraction
#SBATCH --mail-user=slimane.arbaoui@insa-strasbourg.fr

echo "--- STARTING LLM EXTRACTION JOB ---"

# ================= ENVIRONMENT SETUP (Essential) =================
# 1. Clear modules
module purge
# 2. Load the system modules that match your virtual environment
module load python/python-3.11.4 
module load cuda/13.0
echo "Modules loaded: Python 3.11, CUDA 13.0"

# 3. Activate your PyTorch virtual environment
#source ~/Jobs/Job1/cudavenv/bin/activate
echo "Virtual environment activated."

# ================= PYTORCH/LLM EXECUTION =================
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

# Run your Python script that handles PDF parsing and LLM inference
echo "Starting PDF triple extraction script..."
PDF_FILE="p1.pdf"
ONTO_FILE="BatteryPhenomenon.owl"
CHUNK_SIZE=1500
MAX_NEW_TOKENS=1000


# List of models to run
MODELS=(
  "Qwen/Qwen2-7B-Instruct"
  "HuggingFaceH4/zephyr-7b-alpha"
  "mistralai/Mistral-7B-Instruct-v0.3"
  "meta-llama/Llama-3.1-8B-Instruct"
  "Qwen/Qwen3-8B"
  "openai/gpt-oss-20b"
)


for MODEL in "${MODELS[@]}"; do
    echo "Running model: $MODEL"
    OUTPUT_FILE="$(basename $MODEL)"
    python run_model.py "$MODEL" "$PDF_FILE" "$ONTO_FILE" $CHUNK_SIZE "$OUTPUT_FILE" $MAX_NEW_TOKENS
done

echo "--- JOB FINISHED ---"











