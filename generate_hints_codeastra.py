# =======================================================
# Automated Code Vulnerability Analysis using CodeAstra-7B
# =======================================================

from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel, PeftConfig
import torch
import argparse
import os
import json
from pathlib import Path
import time
import tempfile


# -------------------------------
# Load Model Function
# -------------------------------
def load_model(model_name="rootxhacker/CodeAstra-7B"):
    print(f"Loading model: {model_name}")

    # Load PEFT configuration
    config = PeftConfig.from_pretrained(model_name)
    base_model_name = config.base_model_name_or_path

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)

    # Load base model
    model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None,
        load_in_4bit=False
    )

    # Load LoRA adapter (CodeAstra fine-tuning)
    model = PeftModel.from_pretrained(model, model_name)
    model.eval()

    return model, tokenizer


# -------------------------------
# Code Analysis Function (Corrected)
# -------------------------------
def analyze_code(model, tokenizer, code, max_new_tokens=256, temperature=0.2):
    """
    Analyze a given code snippet using CodeAstra-7B model.
    Returns vulnerability assessment text.
    """
    prompt = f"""You are a cybersecurity code analysis assistant.
1. Identifies the type of vulnerability
2. Explains why it's vulnerable
3. Provides guidance on how to fix it (without giving the complete solution)

Code:
{code}

Analysis:
"""  # <-- I also added 'Analysis:' to better cue the model to start

    print(torch.cuda.is_available())

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    # move inputs to model device
    if torch.cuda.is_available():
        device = model.device if hasattr(model, 'device') else torch.device('cuda')
        inputs = {k: v.to(device) for k, v in inputs.items()}

    # Get the length of the input tokens
    input_length = inputs['input_ids'].shape[1]

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=True,
            top_p=0.95,
            eos_token_id=tokenizer.eos_token_id,
        )

    # ====================================================================
    # START: CORRECTED SECTION
    # ====================================================================
    
    # Get the full output sequence
    seq = outputs[0]

    # Get *only* the newly generated tokens (excluding the prompt)
    generated_tokens = seq[input_length:]
    
    # Decode only the new tokens to get the hint
    hint = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()

    # ====================================================================
    # END: CORRECTED SECTION
    # ====================================================================

    return hint

# -------------------------------
# Main Function
# -------------------------------
def main():
    parser = argparse.ArgumentParser(description="Generate security hints using CodeAstra-7B (PEFT)")
    parser.add_argument('--input', default='benchmark/vulnerable_snippets_2', help='Directory with vulnerable snippets')
    parser.add_argument('--output', default='benchmark/security_hints_codeastra.json', help='Output JSON file for hints')
    parser.add_argument('--model', default='rootxhacker/CodeAstra-7B', help='Model name or path')
    parser.add_argument('--max-new-tokens', type=int, default=256)
    parser.add_argument('--temperature', type=float, default=0.2)
    parser.add_argument('--debug-dir', default='benchmark/hints_codeastra_debug', help='Directory to save per-file debug hints')
    parser.add_argument('--merge', action='store_true', help='Merge with existing hints file instead of overwriting')
    parser.add_argument('--use-filenames', action='store_true', help='Use only filename (basename) as JSON key instead of relative path')
    args = parser.parse_args()

    input_path = Path(args.input)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    debug_dir = Path(args.debug_dir)
    debug_dir.mkdir(parents=True, exist_ok=True)

    model, tokenizer = load_model(args.model)

    # gather files
    c_files = list(input_path.rglob('*.c')) + list(input_path.rglob('*.cpp')) + list(input_path.rglob('*.cc')) + list(input_path.rglob('*.cxx'))
    print(f"Found {len(c_files)} files to analyze")

    # load existing hints if merging
    hints = {}
    if args.merge and out_path.exists():
        try:
            with open(out_path, 'r', encoding='utf-8') as ef:
                hints = json.load(ef)
            print(f"Loaded existing hints from {out_path}; {len(hints)} entries")
        except Exception:
            print(f"Warning: failed to load existing hints from {out_path}; starting fresh")
    for fp in c_files:
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                code = f.read()

            print(f"Generating hint for {fp.name}...")
            hint = analyze_code(model, tokenizer, code, max_new_tokens=args.max_new_tokens, temperature=args.temperature)
            # store relative path key
            rel = str(fp.relative_to(input_path))
            key = fp.name if args.use_filenames else rel
            hints[key] = hint

            # save per-file debug
            dbg_file = debug_dir / (fp.name + '.hint.txt')
            with open(dbg_file, 'w', encoding='utf-8') as df:
                df.write(hint)
            time.sleep(0.05)

            # atomic incremental write of JSON after each file
            try:
                with tempfile.NamedTemporaryFile('w', delete=False, dir=out_path.parent, encoding='utf-8') as tf:
                    json.dump(hints, tf, indent=2)
                    tmp_name = tf.name
                os.replace(tmp_name, out_path)  # atomic on Windows
            except Exception as e:
                print(f"Warning: failed to write incremental JSON: {e}")

        except Exception as e:
            print(f"Error processing {fp}: {e}")

    # write JSON
    with open(out_path, 'w', encoding='utf-8') as of:
        json.dump(hints, of, indent=2)
    print(f"Hints saved to {out_path}")


# -------------------------------
# Entry Point
# -------------------------------
if __name__ == "__main__":
    main()
