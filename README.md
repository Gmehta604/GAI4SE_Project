# Security Patch Generation with Semantic Hints

This project implements a pipeline for generating security patches using CodeLlama, with and without semantic hints from GPT-4.

## System Architecture

```
[ Juliet C/C++ Files ]
         |
         v
[ generate_hints_codeastra.py (CodeAstra) ]
Generate security hint for each vulnerable snippet
         |
         v
[ CodeLlama Scripts ]
run_baseline.py → fixes without hint
run_hinted.py → fixes with hints
         |
         v
results/baseline_patches/   results/semantic_hint_patches/
         |
         v
├── scan_vulnerabilities.py → flawfinder
├── check_functionality.py → gcc + run
└── compute_similarility.py → CodeBERT similarity
         |
         v
visualize_results.py → Generate graphs using Results
```

## Directory Structure

```
.
├── juliet_files/                    # Input: Juliet C/C++ test cases
├── benchmark/
│   ├── vulnerable_snippets/         # Extracted _bad() functions
│   ├── ground_truth_patches/        # Extracted _good() functions
│   └── security_hints.json          # GPT-4 generated hints
├── results/
│   ├── baseline_patches/            # CodeLlama patches (no hints)
│   ├── semantic_hint_patches/       # CodeLlama patches (with hints)
│   └── results.csv                  # Evaluation results
├── parse_juliet.py                  # Extract functions from Juliet files
├── generate_hints_codeastra.py      # Generate hints using Coeeastra
├── run_baseline.py                  # Generate patches without hints
├── run_hinted.py                    # Generate patches with hints
├── evaluate.py                      # Evaluate patches
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install system dependencies:**
   - GCC compiler (for functionality testing)
   - Flawfinder (for security analysis)
     ```bash
     pip install flawfinder
     # Or on Linux: sudo apt-get install flawfinder
     ```

3. **Set up OpenAI API key:**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   # Or on Windows:
   set OPENAI_API_KEY=your-api-key-here
   ```

## Usage

### Step 1: Parse Juliet Test Cases

Place your Juliet C/C++ test case files in the `juliet_files/` directory, then run:

```bash
python parse_juliet.py
```

This will:
- Extract `_bad()` functions → `benchmark/vulnerable_snippets/`
- Extract `_good()` functions → `benchmark/ground_truth_patches/`

### Step 2: Generate Security Hints

Generate security hints using GPT-4:

```bash
python generate_hints.py
```

Options:
- `--input`: Directory with vulnerable snippets (default: `benchmark/vulnerable_snippets`)
- `--output`: Output JSON file (default: `benchmark/security_hints.json`)
- `--api-key`: OpenAI API key (or set `OPENAI_API_KEY` env var)
- `--model`: Model to use (default: `gpt-4`)

### Step 3: Generate Patches

#### Baseline (without hints):
```bash
python run_baseline.py
```

#### With hints:
```bash
python run_hinted.py
```

Options:
- `--input`: Directory with vulnerable snippets
- `--output`: Output directory for patches
- `--model`: CodeLlama model name (default: `codellama/CodeLlama-7b-Instruct-hf`)
- `--max-length`: Maximum generation length

### Step 4: Evaluate Patches

Evaluate all generated patches:

```bash
python evaluate.py
```

This will:
- Check security using flawfinder
- Check functionality (compilation + execution)
- Compute quality (CodeBERT similarity to ground truth)
- Generate `results/results.csv` with all metrics

## Output Format

The `results.csv` file contains:
- `method`: "baseline" or "hinted"
- `file`: Relative path to the patch file
- `security_pass`: Boolean (True if no security issues)
- `func_pass`: Boolean (True if compiles and runs)
- `similarity_score`: Float (0-1, CodeBERT similarity to ground truth)

## Notes

- CodeLlama models are large and require significant GPU memory. Adjust model size or use CPU if needed.
- GPT-4 API calls incur costs. Monitor usage when processing large datasets.
- Flawfinder and GCC must be installed for full evaluation functionality.
- CodeBERT similarity computation requires the model to be downloaded on first run.

## Troubleshooting

- **Out of memory errors**: Use a smaller CodeLlama model or reduce batch size
- **Flawfinder not found**: Install via pip or system package manager
- **GCC not found**: Install GCC compiler for your platform
- **OpenAI API errors**: Check API key and rate limits






