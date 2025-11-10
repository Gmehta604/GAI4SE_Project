"""
run_baseline.py

Runs CodeLlama to generate patches for vulnerable snippets WITHOUT hints.
"""

import os
import json
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


def load_codellama_model(model_name="codellama/CodeLlama-7b-Instruct-hf"):
    """
    Load CodeLlama model and tokenizer.
    
    Args:
        model_name: HuggingFace model identifier
        
    Returns:
        tuple: (tokenizer, model)
    """
    print(f"Loading model: {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None
    )
    print("Model loaded successfully!")
    return tokenizer, model


def generate_patch(code_snippet, tokenizer, model, max_length=512):
    """
    Generate a patch for vulnerable code using CodeLlama.
    
    Args:
        code_snippet: The vulnerable code to fix
        tokenizer: CodeLlama tokenizer
        model: CodeLlama model
        max_length: Maximum generation length
        
    Returns:
        str: Generated patch
    """
    prompt = f"""Fix the following C/C++ code to remove security vulnerabilities:

```c
{code_snippet}
```

Fixed code:
```c
"""
    
    inputs = tokenizer(prompt, return_tensors="pt")
    if torch.cuda.is_available():
        inputs = {k: v.cuda() for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_length,
            temperature=0.2,
            do_sample=True,
            top_p=0.95,
            pad_token_id=tokenizer.eos_token_id
        )
    
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract the generated code (after "Fixed code:")
    if "Fixed code:" in generated_text:
        generated_code = generated_text.split("Fixed code:")[-1].strip()
        # Remove code block markers if present
        generated_code = generated_code.replace("```c", "").replace("```", "").strip()
        return generated_code
    
    return generated_text


def process_vulnerable_snippets(input_dir, output_dir, tokenizer, model):
    """
    Process all vulnerable snippets and generate patches.
    
    Args:
        input_dir: Directory containing vulnerable code snippets
        output_dir: Directory to save generated patches
        tokenizer: CodeLlama tokenizer
        model: CodeLlama model
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all C/C++ files
    c_files = list(input_path.rglob('*.c')) + list(input_path.rglob('*.cpp')) + \
              list(input_path.rglob('*.cc')) + list(input_path.rglob('*.cxx'))
    
    processed = 0
    failed = 0
    
    print(f"Processing {len(c_files)} files...")
    
    for file_path in c_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            print(f"Generating patch for: {file_path.name}...")
            patch = generate_patch(code, tokenizer, model)
            
            if patch:
                # Maintain directory structure
                relative_path = file_path.relative_to(input_path)
                output_file = output_path / relative_path
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(patch)
                
                processed += 1
                print(f"  ✓ Patch saved")
            else:
                failed += 1
                print(f"  ✗ Failed to generate patch")
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            failed += 1
    
    print(f"\nBaseline patch generation complete!")
    print(f"Processed: {processed} files")
    print(f"Failed: {failed} files")
    print(f"Patches saved to: {output_path}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate patches using CodeLlama (baseline, no hints)")
    parser.add_argument("--input", default="benchmark/vulnerable_snippets",
                       help="Directory containing vulnerable snippets")
    parser.add_argument("--output", default="results/baseline_patches",
                       help="Output directory for generated patches")
    parser.add_argument("--model", default="codellama/CodeLlama-7b-Instruct-hf",
                       help="CodeLlama model name")
    parser.add_argument("--max-length", type=int, default=512,
                       help="Maximum generation length")
    
    args = parser.parse_args()
    
    print("Starting baseline patch generation (no hints)...")
    print(f"Input directory: {args.input}")
    print(f"Output directory: {args.output}")
    print(f"Model: {args.model}")
    print("-" * 60)
    
    tokenizer, model = load_codellama_model(args.model)
    process_vulnerable_snippets(args.input, args.output, tokenizer, model)



