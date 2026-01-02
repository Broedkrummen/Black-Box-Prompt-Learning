# Black-Box Prompt Learning (BDPL) - AI Agent Instructions

## Project Overview
This codebase implements Black-Box Discrete Prompt Learning (BDPL) for pre-trained language models, optimizing discrete prompts without access to model parameters or gradients. It uses variance-reduced policy gradient for gradient estimation in a black-box setting, enabling efficient prompt tuning via API calls.

## Architecture
- **Core Components**: `run_glue_discrete_LM.py` (RoBERTa experiments), `run_glue_discrete_GPT.py` (GPT-3 experiments), `loss.py` (custom losses like MarginLoss), `pmi_ngram.py` (PMI-based prompt vocabulary construction)
- **Data Flow**: Input text → Discrete prompt tokens → PLM API call → Logits → Policy gradient update
- **Key Design**: Black-box constraint ensures security; discrete prompts reduce parameters; policy gradient handles categorical optimization

## Developer Workflows
- **Setup**: Run `source install.sh` to create conda env `bdpl` with PyTorch 1.7.1, Transformers 4.6.0, and OpenAI API
- **RoBERTa Experiments**: `bash run.sh` (uses `run_glue_discrete_LM.py`)
- **GPT-3 Experiments**: `bash run.sh` with `--api_key` (uses `run_glue_discrete_GPT.py`)
- **Dataset Prep**: Download from https://github.com/allenai/dont-stop-pretraining, convert to TSV via external script, place in `./dataset/`
- **Prompt Vocab**: Run `python pmi_ngram.py --dataset <train_file> --output_dir <output_dir>` to generate PMI-based candidates
- **Tracing**: Tracing is enabled using OpenTelemetry; run `ai-mlstudio.tracing.open` in VS Code to start collector before running experiments

## Conventions & Patterns
- **Task Names**: GLUE tasks (`mrpc`, `qnli`, `cola`, `rte`) use `task_to_keys`; domain tasks (`CI`, `SE`, `RCT`, `HP`) use custom label mappings
- **Verbalizers**: Labels mapped to strings (e.g., `LABEL2ID_CONFIG["mrpc"] = {" no": 0, " yes": 1}`); see `LABEL_CONVERT` for conversions
- **Templates**: Task-specific prompts (e.g., `TEMPLATE_CONFIG["mrpc"] = " equivalent?"`)
- **Loss Functions**: Use `MarginLoss` for hinge loss (`--ce_loss False`); CrossEntropyLoss for CE loss
- **Logging**: WandB integration (`--use_wandb True`); checkpoints in `./ckpts/`
- **Hyperparams**: `--prompt_length` (default 6-20), `--k_shot` (few-shot examples), `--sample_size` (policy gradient samples)

## Integration Points
- **External APIs**: OpenAI GPT-3 (requires API key); HuggingFace models (RoBERTa-large)
- **Datasets**: GLUE benchmark + domain-specific (CitationIntent, SciERC, RCT, HyperPartisan)
- **Dependencies**: Fixed versions (PyTorch 1.7.1, Transformers 4.6.0) for reproducibility
- **Tracing**: OpenTelemetry with OTLP exporter to localhost:4318; OpenAI API calls are instrumented
- **Database**: MongoDB local instance at mongodb://localhost:27017/; database 'bdpl_db' with collections for experiments, results, datasets

## Key Files
- `run_glue_discrete_GPT.py`: GPT-3 black-box prompt learning with policy gradient
- `run_glue_discrete_LM.py`: RoBERTa white-box prompt learning (for comparison)
- `loss.py`: MarginLoss and other custom losses
- `pmi_ngram.py`: PMI n-gram extraction for prompt vocabulary
- `run.sh`: Example command lines for experiments