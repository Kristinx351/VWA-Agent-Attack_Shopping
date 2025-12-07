# VWA Agent Attack - Shopping

This repository contains the code and experiments for adversarial attacks on multimodal language model agents, specifically focused on shopping scenarios in the VisualWebArena environment.

## Overview

This project combines two main components:

- **agent-attack/**: Implementation of adversarial attacks on multimodal LM agents
- **visualwebarena/**: Modified VisualWebArena environment for evaluating multimodal agents on realistic visual web tasks

The research focuses on dissecting the adversarial robustness of multimodal agents when performing shopping-related tasks in web environments.

## Repository Structure

```
.
├── agent-attack/          # Adversarial attack implementation
│   ├── agent_attack/      # Core attack modules
│   ├── scripts/           # Evaluation and attack scripts
│   ├── episode_scripts/   # Episode-wise evaluation scripts
│   └── step_scripts/     # Step-wise evaluation scripts
│
└── visualwebarena/        # VisualWebArena evaluation environment
    ├── agent/            # Agent implementations
    ├── browser_env/      # Browser environment
    ├── llms/             # LLM providers
    └── evaluation_harness/ # Evaluation tools
```

## Installation

### Prerequisites

- Python 3.10 or 3.11 (Python 3.12 is not supported due to deprecated distutils)
- CUDA-capable GPU (recommended for attacks and captioning)
- Docker (required for VisualWebArena environments)
- At least 200GB disk space (for VisualWebArena)

### Step 1: Clone the Repository

```bash
git clone git@github.com:Kristinx351/VWA-Agent-Attack_Shopping.git
cd VWA-Agent-Attack_Shopping
```

### Step 2: Install VisualWebArena

```bash
cd visualwebarena/
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install
pip install -e .
pytest -x  # Verify installation
```

### Step 3: Install Agent Attack

```bash
cd ../agent-attack/
pip install -e .
```

You may need to install PyTorch according to your CUDA version.

## Setup

### API Keys

Set up the required API keys as environment variables:

**OpenAI:**
```bash
export OPENAI_API_KEY=<your-openai-api-key>
```

**Anthropic (for Claude):**
```bash
export ANTHROPIC_API_KEY=<your-anthropic-api-key>
```

**Google (for Gemini):**
```bash
gcloud auth login
gcloud config set project <your-google-cloud-project-id>
export VERTEX_PROJECT=<your-google-cloud-project-id>
export AISTUDIO_API_KEY=<your-aistudio-api-key>
```

### Environment URLs

Configure the URLs for each website environment:

```bash
export CLASSIFIEDS="http://127.0.0.1:9980"
export CLASSIFIEDS_RESET_TOKEN="4b61655535e7ed388f0d40a93600254c"
export SHOPPING="http://127.0.0.1:7770"
export REDDIT="http://127.0.0.1:9999"
export WIKIPEDIA="http://127.0.0.1:8888"
export HOMEPAGE="http://127.0.0.1:4399"
```

Replace `http://127.0.0.1` with your actual IP address if needed.

### VisualWebArena Environment Setup

1. **Setup Docker environments**: Follow the instructions in `visualwebarena/environment_docker/README.md`

2. **Generate test config files**:
```bash
cd visualwebarena/
python scripts/generate_test_data.py
```

3. **Obtain auto-login cookies**:
```bash
bash prepare.sh
```

## Usage

### Running Attacks

Generate adversarial examples for shopping scenarios:

**Captioner Attack:**
```bash
cd agent-attack/
python scripts/run_cap_attack.py
```

**CLIP Attack:**
```bash
python scripts/run_clip_attack.py --model gpt-4-vision-preview
python scripts/run_clip_attack.py --model gemini-1.5-pro-latest
python scripts/run_clip_attack.py --model claude-3-opus-20240229
python scripts/run_clip_attack.py --model gpt-4o-2024-05-13
```

> **Note**: Each attack on an image takes approximately 1 hour on a single GPU. We used NVIDIA A100 (80G) for captioner attacks and NVIDIA A6000 for CLIP attacks.

### Evaluation

#### Episode-wise Evaluation

Run full episode evaluations for different models:

**GPT-4V:**
```bash
bash agent-attack/episode_scripts/gpt4v_benign.sh
bash agent-attack/episode_scripts/gpt4v_bim_caption_attack.sh
bash agent-attack/episode_scripts/gpt4v_clip_attack_self_cap.sh
```

**GPT-4o:**
```bash
bash agent-attack/episode_scripts/gpt4o_benign.sh
bash agent-attack/episode_scripts/gpt4o_bim_caption_attack.sh
bash agent-attack/episode_scripts/gpt4o_clip_attack_self_cap.sh
```

**Gemini 1.5 Pro:**
```bash
bash agent-attack/episode_scripts/gemini1.5pro_benign.sh
bash agent-attack/episode_scripts/gemini1.5pro_bim_caption_attack.sh
bash agent-attack/episode_scripts/gemini1.5pro_clip_attack_self_cap.sh
```

**Claude 3 Opus:**
```bash
bash agent-attack/episode_scripts/claude3opus_benign.sh
bash agent-attack/episode_scripts/claude3opus_bim_caption_attack.sh
bash agent-attack/episode_scripts/claude3opus_clip_attack_self_cap.sh
```

#### Step-wise Evaluation

For faster development and testing, use step-wise evaluation:

```bash
bash agent-attack/step_scripts/gpt4v_benign.sh
bash agent-attack/step_scripts/gpt4v_bim_caption_attack.sh
bash agent-attack/step_scripts/gpt4v_clip_attack_self_cap.sh
```

### Running VisualWebArena Agents

Run the GPT-4V + SoM agent on shopping tasks:

```bash
cd visualwebarena/
python run.py \
  --instruction_path agent/prompts/jsons/p_som_cot_id_actree_3s.json \
  --test_start_idx 0 \
  --test_end_idx 1 \
  --result_dir gpt4_som_shopping \
  --test_config_base_dir=config_files/test_shopping \
  --model gpt-4-vision-preview \
  --action_set_tag som \
  --observation_type image_som
```

## Project Details

### Supported Models

- **OpenAI**: GPT-4V, GPT-4o, GPT-3.5
- **Anthropic**: Claude 3 Opus
- **Google**: Gemini 1.5 Pro

### Attack Methods

1. **Captioner Attack (BIM)**: Attacks the image captioning component
2. **CLIP Attack**: Attacks the vision-language understanding

### Evaluation Metrics

- Success rate on shopping tasks
- Attack effectiveness
- Agent robustness analysis

## Data

Large data directories are excluded from this repository (see `.gitignore`):
- `agent-attack/data/`
- `agent-attack/exp_data/`
- `agent-attack/exp_result/`
- `visualwebarena/environment_docker/`

## Citation

If you use this code, please cite the original papers:

```bibtex
@article{wu2024agentattack,
  title={Dissecting Adversarial Robustness of Multimodal LM Agents},
  author={Wu, Chen Henry and Shah, Rishi and Koh, Jing Yu and Salakhutdinov, Ruslan and Fried, Daniel and Raghunathan, Aditi},
  journal={arXiv preprint arXiv:2406.12814},
  year={2024}
}

@article{koh2024visualwebarena,
  title={VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks},
  author={Koh, Jing Yu and Lo, Robert and Jang, Lawrence and Duvvur, Vikram and Lim, Ming Chong and Huang, Po-Yu and Neubig, Graham and Zhou, Shuyan and Salakhutdinov, Ruslan and Fried, Daniel},
  journal={arXiv preprint arXiv:2401.13649},
  year={2024}
}
```

## Related Work

- [VisualWebArena](https://github.com/web-arena-x/visualwebarena) - Original VisualWebArena repository
- [Agent Attack](https://github.com/ChenWu98/agent-attack) - Original agent attack repository
- [WebArena](https://webarena.dev/) - Web-based agent evaluation benchmark

## License

See individual LICENSE files in `agent-attack/` and `visualwebarena/` directories.

## Notes

- This repository focuses specifically on shopping scenarios
- Large data files are excluded from git (see `.gitignore`)
- Make sure to set up all required environment variables before running experiments
- GPU is recommended for running attacks and captioning models

