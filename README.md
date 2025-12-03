# Automated Security Patch Generation with Semantic Hints

This project implements a comprehensive pipeline for generating security patches using Large Language Models (LLMs), with and without semantic hints from specialized code analysis models. The system evaluates the effectiveness of hint-enhanced patch generation compared to baseline approaches.

## Overview

The project demonstrates a two-stage approach to automated security vulnerability remediation:
1. **Hint Generation**: Using specialized models (CodeAstra-7B or GPT-4) to generate semantic hints describing vulnerabilities
2. **Patch Generation**: Using CodeLlama-7B-Instruct to generate security patches with and without hints

## Key Features

- 🔍 **Dual Hint Generation**: Support for both CodeAstra-7B (specialized cybersecurity model) and GPT-4
- 🛡️ **Security Analysis**: Automated vulnerability scanning using flawfinder
- ✅ **Functionality Testing**: Automated compilation and execution testing
- 📊 **Quality Assessment**: CodeBERT-based similarity scoring to ground-truth patches
- 📈 **Visualization**: Automated generation of comprehensive result graphs
- 📋 **Comprehensive Evaluation**: Multi-dimensional analysis across security, functionality, and quality metrics

## System Architecture

```
[ Juliet C/C++ Files ]
         |
         v
[ parse_juliet.py ]
Extract _bad() and _good() functions
         |
         +--> benchmark/vulnerable_snippets/
         +--> benchmark/ground_truth_2/
         |
         v
[ Hint Generation ]
└── generate_hints_codeastra.py (CodeAstra-7B)
         |
         v
[ Patch Generation ]
├── run_baseline.py → fixes without hints
└── run_hinted.py → fixes with hints
         |
         v
results/baseline_patches_2/   results/sementic_hinted_patches_2/
         |
         v
[ Evaluation Pipeline ]
├── scan_vulnerabilities.py → flawfinder security analysis
├── check_functionality.py → compilation & execution tests
├── compute_similarity.py → CodeBERT similarity scoring
└── visualize_results.py → generate graphs
         |
         v
[ Results ]
├── results/vulnerability_scan.json
├── results/functionality_check.json
├── results/codebert_similarity.json
└── results/graphs/*.png
```

## Directory Structure

```
.
├── juliet_files/                          # Input: Juliet C/C++ test cases
├── benchmark/
│   ├── vulnerable_snippets_2/            # Extended dataset (92 files)
│   ├── ground_truth_2/                   # Extended ground truth (116 files)
│   └── security_hints_codeastra.json     # CodeAstra-7B generated hints
├── results/
│   ├── baseline_patches_2/               # CodeLlama patches (no hints)
│   ├── sementic_hinted_patches_2/        # CodeLlama patches (with hints)
│   ├── graphs/                           # Visualization graphs
│   │   ├── flawfinder_summary.png
│   │   ├── flawfinder_vulnerability_levels.png
│   │   ├── functionality_comparison.png
│   │   ├── functionality_breakdown.png
│   │   └── combined_summary.png
│   ├── vulnerability_scan.json           # Flawfinder analysis results
│   ├── functionality_check.json          # Compilation/execution results
│   └── codebert_similarity.json          # CodeBERT similarity scores
├── parse_juliet.py                       # Extract functions from Juliet files
├── generate_hints_codeastra.py           # Generate hints using CodeAstra-7B
├── run_baseline.py                       # Generate patches without hints
├── run_hinted.py                         # Generate patches with hints
├── scan_vulnerabilities.py               # Security vulnerability scanning
├── check_functionality.py                # Functionality testing
├── compute_similarity.py                 # CodeBERT similarity computation
├── visualize_results.py                  # Generate visualization graphs
├── requirements.txt                      # Python dependencies
└── README.md                             # This file
```

## Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- `transformers>=4.30.0` - For CodeLlama and CodeAstra models
- `torch>=2.6.0` - PyTorch for model inference
- `openai>=1.0.0` - For GPT-4 API access (optional, if using GPT-4)
- `bitsandbytes>=0.41.0` - For 8-bit quantization
- `scipy>=1.10.0`, `numpy>=1.24.0` - For similarity computation

### 2. Install System Dependencies

- **GCC Compiler**: Required for functionality testing
  - Linux: `sudo apt-get install gcc g++`
  - macOS: `xcode-select --install`
  - Windows: Install MinGW or Visual Studio Build Tools

- **Flawfinder**: For security vulnerability scanning
  ```bash
  pip install flawfinder
  # Or on Linux:
  sudo apt-get install flawfinder
  ```

**Note**: CodeAstra-7B runs locally and doesn't require API keys.

### 4. GPU Setup (Recommended)

For best performance, use a GPU with CUDA support:
- **Minimum**: 8GB GPU memory (with 8-bit quantization)
- **Recommended**: 16GB+ GPU memory
- Models will automatically use CPU if GPU is unavailable (slower)

## Usage

### Step 1: Parse Juliet Test Cases

Extract vulnerable and secure functions from Juliet test suite files:

```bash
python parse_juliet.py
```

**Options:**
- `--input`: Directory containing Juliet files (default: `juliet_files/`)
- `--output-bad`: Output directory for vulnerable snippets (default: `benchmark/vulnerable_snippets_2/`)
- `--output-good`: Output directory for ground truth (default: `benchmark/ground_truth_2/`)

This will:
- Extract `_bad()` functions → `benchmark/vulnerable_snippets_2/`
- Extract `_good()` functions → `benchmark/ground_truth_2/`

### Step 2: Generate Security Hints

Choose one of two methods:

#### Option A: Using CodeAstra-7B (Recommended, Local)

```bash
python generate_hints_codeastra.py
```

**Options:**
- `--input`: Directory with vulnerable snippets (default: `benchmark/vulnerable_snippets_2`)
- `--output`: Output JSON file (default: `benchmark/security_hints_codeastra.json`)
- `--model`: Model name (default: `rootxhacker/CodeAstra-7B`)
- `--max-new-tokens`: Max tokens for hint generation (default: 256)
- `--temperature`: Generation temperature (default: 0.2)
- `--use-filenames`: Use only filename as JSON key

#### Option B: Using GPT-4 (Requires API Key)

```bash
python generate_hints.py
```

**Options:**
- `--input`: Directory with vulnerable snippets (default: `benchmark/vulnerable_snippets`)
- `--output`: Output JSON file (default: `benchmark/security_hints.json`)
- `--api-key`: OpenAI API key (or set `OPENAI_API_KEY` env var)
- `--model`: Model to use (default: `gpt-4`)

### Step 3: Generate Patches

#### Baseline (Without Hints)

Generate patches without semantic hints:

```bash
python run_baseline.py
```

**Options:**
- `--input`: Directory with vulnerable snippets (default: `benchmark/vulnerable_snippets_2`)
- `--output`: Output directory (default: `results/baseline_patches_2`)
- `--model`: CodeLlama model name (default: `codellama/CodeLlama-7b-Instruct-hf`)
- `--max-length`: Maximum generation length (default: 512)

#### Hint-Enhanced (With Semantic Hints)

Generate patches with semantic hints:

```bash
python run_hinted.py
```

**Options:**
- `--input`: Directory with vulnerable snippets (default: `benchmark/vulnerable_snippets_2`)
- `--output`: Output directory (default: `results/sementic_hinted_patches_2`)
- `--hints`: Hints JSON file (default: `benchmark/security_hints_codeastra.json`)
- `--model`: CodeLlama model name (default: `codellama/CodeLlama-7b-Instruct-hf`)
- `--max-length`: Maximum generation length (default: 1024)

### Step 4: Evaluate Patches

#### 4a. Security Vulnerability Analysis

Scan generated patches for vulnerabilities:

```bash
python scan_vulnerabilities.py
```

This generates `results/vulnerability_scan.json` with flawfinder analysis results.

#### 4b. Functionality Testing

Test compilation and execution:

```bash
python check_functionality.py
```

This generates `results/functionality_check.json` with compilation and execution results.

#### 4c. Quality Assessment

Compute CodeBERT similarity scores:

```bash
python compute_similarity.py
```

This generates `results/codebert_similarity.json` with similarity scores compared to ground-truth patches.

#### 4d. Visualization

Generate comprehensive result graphs:

```bash
python visualize_results.py
```

This generates visualization graphs in `results/graphs/`:
- `flawfinder_summary.png` - Security analysis overview
- `flawfinder_vulnerability_levels.png` - Vulnerability severity distribution
- `functionality_comparison.png` - Compilation/execution comparison
- `functionality_breakdown.png` - Detailed functionality results
- `combined_summary.png` - Integrated dashboard view

## Output Formats

### Vulnerability Scan Results (`vulnerability_scan.json`)

```json
{
  "scan_summary": {
    "baseline_patches_2": {
      "total_files": 92,
      "files_with_vulnerabilities": 35,
      "total_vulnerabilities": 115
    },
    "sementic_hinted_patches_2": {
      "total_files": 92,
      "files_with_vulnerabilities": 18,
      "total_vulnerabilities": 42
    }
  }
}
```

### Functionality Check Results (`functionality_check.json`)

```json
{
  "functionality_summary": {
    "baseline_patches_2": {
      "total_files": 92,
      "compiles_successfully": 81,
      "compilation_failed": 11,
      "success_rate": 88.04
    }
  }
}
```

### CodeBERT Similarity Results (`codebert_similarity.json`)

```json
{
  "summary": {
    "average_similarity": 0.7823,
    "min_similarity": 0.4521,
    "max_similarity": 0.9634
  }
}
```

## Key Results

Based on evaluation of 92 C/C++ vulnerability test cases:

- **Security Improvement**: Hint-enhanced patches reduce vulnerabilities by **40-50%** overall, **60-70%** for high-severity issues
- **Functionality Preservation**: Both approaches maintain **>85%** compilation success rates
- **Quality Enhancement**: Hint-enhanced patches show **15-20%** improvement in CodeBERT similarity to expert-written patches
- **Category Effectiveness**: Particularly effective for input validation (CWE-78, CWE-134) and memory safety (CWE-401, CWE-415) vulnerabilities

## Models Used

### CodeAstra-7B
- **Purpose**: Hint generation for vulnerability analysis
- **Model**: `rootxhacker/CodeAstra-7B`
- **Architecture**: LoRA fine-tuned transformer model specialized for cybersecurity
- **Usage**: Local inference (no API required)

### CodeLlama-7B-Instruct
- **Purpose**: Patch generation
- **Model**: `codellama/CodeLlama-7b-Instruct-hf`
- **Architecture**: Instruction-tuned code generation model
- **Usage**: Local inference with optional 8-bit quantization

### GPT-4 (Optional)
- **Purpose**: Alternative hint generation method
- **Usage**: OpenAI API (requires API key)

## Notes

- **GPU Memory**: CodeLlama requires significant GPU memory. The scripts automatically use 8-bit quantization when available to reduce memory usage from ~14GB to ~8GB.
- **Processing Time**: Average hint generation: 2-5 seconds/snippet; patch generation: 5-15 seconds/snippet
- **API Costs**: GPT-4 API calls incur costs. Monitor usage when processing large datasets. CodeAstra-7B runs locally at no cost.
- **Model Downloads**: Models are downloaded automatically from Hugging Face on first use (~15GB total).

## Troubleshooting

### Out of Memory Errors

- Use 8-bit quantization (automatically enabled if `bitsandbytes` is available)
- Reduce `--max-length` parameter
- Use CPU mode (slower but works on any machine)

### Flawfinder Not Found

```bash
pip install flawfinder
# Or on Linux:
sudo apt-get install flawfinder
```

### GCC Not Found

- **Linux**: `sudo apt-get install gcc g++`
- **macOS**: Install Xcode Command Line Tools
- **Windows**: Install MinGW or Visual Studio Build Tools

### Model Download Issues

- Ensure stable internet connection for initial model download
- Models are cached locally after first download
- Check Hugging Face access permissions

### CUDA Errors

- Verify CUDA installation: `nvidia-smi`
- Check PyTorch CUDA compatibility
- Models will fall back to CPU if CUDA unavailable

## Citation

If you use this work in your research, please cite:

```bibtex
@article{security-patch-generation-2024,
  title={Automated Security Patch Generation Using Large Language Models with Semantic Hints},
  author={Abhishek Potdar, Gaurav Mehta, Sharwari Akre, Yash Shah},
  year={2025}
}
```

## Acknowledgments

- Juliet Test Suite by NIST for vulnerability test cases
- CodeAstra-7B by rootxhacker for cybersecurity code analysis
- CodeLlama by Meta AI for code generation capabilities
- Hugging Face for model hosting and transformers library
