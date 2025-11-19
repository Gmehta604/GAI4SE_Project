"""
run_hinted.py

Runs CodeLlama to generate patches for vulnerable snippets WITH security hints.
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
        tuple: (tokenizer, model, device)
    """
    print(f"Loading model: {model_name}...")
    
    # Check CUDA availability
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print(f"CUDA available! Using GPU: {torch.cuda.get_device_name(0)}")
        print(f"CUDA memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
    else:
        device = torch.device("cpu")
        print("CUDA not available. Using CPU (this will be slow!)")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    # Set pad_token if not already set
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.pad_token_id = tokenizer.eos_token_id
    
    # Load model with proper device configuration
    if torch.cuda.is_available():
        # Try to use 8-bit quantization to fit in 8GB GPU memory
        try:
            from transformers import BitsAndBytesConfig
            
            # Configure 8-bit quantization
            quantization_config = BitsAndBytesConfig(
                load_in_8bit=True,
                llm_int8_threshold=6.0
            )
            
            print("Using 8-bit quantization to optimize GPU memory usage...")
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                quantization_config=quantization_config,
                device_map="auto",
                low_cpu_mem_usage=True,
                trust_remote_code=True
            )
        except ImportError:
            print("bitsandbytes not available, using float16 (may require more GPU memory)...")
            print("Install with: pip install bitsandbytes")
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                dtype=torch.float16,  # Use dtype instead of torch_dtype
                device_map="auto",
                low_cpu_mem_usage=True,
                trust_remote_code=True
            )
        except Exception as e:
            print(f"Quantization failed ({e}), falling back to float16...")
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                dtype=torch.float16,
                device_map="auto",
                low_cpu_mem_usage=True,
                trust_remote_code=True
            )
        
        # Verify model is on GPU
        if hasattr(model, 'device'):
            print(f"Model device: {model.device}")
        else:
            # Check first parameter's device
            first_param_device = next(model.parameters()).device
            print(f"Model device (first param): {first_param_device}")
        
        # Check GPU memory usage
        if torch.cuda.is_available():
            memory_allocated = torch.cuda.memory_allocated(0) / 1024**3
            memory_reserved = torch.cuda.memory_reserved(0) / 1024**3
            print(f"GPU memory - Allocated: {memory_allocated:.2f} GB, Reserved: {memory_reserved:.2f} GB")
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            dtype=torch.float32,
            device_map=None
        )
        model = model.to(device)
    
    model.eval()  # Set to evaluation mode
    print("Model loaded successfully!")
    return tokenizer, model, device


def load_security_hints(hints_file="benchmark/security_hints_codeastra.json"):
    """
    Load security hints from JSON file.
    
    Args:
        hints_file: Path to JSON file containing hints
        
    Returns:
        dict: Mapping of file paths to hints
    """
    hints_path = Path(hints_file)
    if not hints_path.exists():
        print(f"Warning: Hints file not found: {hints_file}")
        return {}
    
    with open(hints_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_patch_with_hint(code_snippet, hint, tokenizer, model, device, max_length=1028):
    """
    Generate a patch for vulnerable code using CodeLlama with a security hint.
    
    Args:
        code_snippet: The vulnerable code to fix
        hint: Security hint describing the vulnerability
        tokenizer: CodeLlama tokenizer
        model: CodeLlama model
        device: torch device (cuda or cpu)
        max_length: Maximum generation length
        
    Returns:
        str: Generated patch
    """
    # Use CodeLlama-Instruct format with proper instruction tags
    prompt = f"""<s>[INST] Fix the following C/C++ code to remove security vulnerabilities.

            Security Hint: {hint}

            Vulnerable code:
            ```c
            {code_snippet}
            ```

            Output ONLY the fixed code. Do not include any explanations, comments, or descriptions. Provide only the corrected code snippet: [/INST]"""
    
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
    
    # Move inputs to the same device as the model
    if hasattr(model, 'device'):
        model_device = model.device
    else:
        model_device = next(model.parameters()).device
    
    inputs = {k: v.to(model_device) for k, v in inputs.items()}
    
    # Store input length to extract only newly generated tokens
    input_length = inputs['input_ids'].shape[1]
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_length,
            temperature=0.2,
            do_sample=True,
            top_p=0.95,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.1,
            use_cache=True  # Enable KV cache for faster generation
        )
    
    # Decode only the newly generated tokens (exclude the input prompt)
    generated_tokens = outputs[0][input_length:]
    generated_text = tokenizer.decode(generated_tokens, skip_special_tokens=True)
    
    # Clean up the generated code
    generated_code = generated_text.strip()
    
    # Extract code from code block if present
    if "```" in generated_code:
        # Find the first code block
        start_idx = generated_code.find("```")
        if start_idx != -1:
            # Skip the opening marker and language identifier
            start_idx = generated_code.find('\n', start_idx) + 1
            # Find the closing marker
            end_idx = generated_code.find("```", start_idx)
            if end_idx != -1:
                generated_code = generated_code[start_idx:end_idx].strip()
            else:
                # No closing marker, take everything after opening
                generated_code = generated_code[start_idx:].strip()
    
    # Remove any leading explanatory text (common patterns)
    lines = generated_code.split('\n')
    code_start = 0
    code_indicators = ['{', '}', ';', '#include', '#define', 'int ', 'void ', 'char ', 'return', 'if ', 'for ', 'while ']
    
    for i, line in enumerate(lines):
        # Skip lines that look like explanations (not code-like)
        line_stripped = line.strip()
        if not line_stripped:
            continue
        
        line_lower = line_stripped.lower()
        is_explanation = (
            line_lower.startswith(('here', 'the fixed', 'here is', 'here\'s', 'below', 'following')) or
            line_lower.endswith((':', 'is:', 'code:'))
        )
        
        has_code_indicator = any(indicator in line for indicator in code_indicators)
        
        if is_explanation and not has_code_indicator:
            continue
        else:
            code_start = i
            break
    
    generated_code = '\n'.join(lines[code_start:]).strip()
    
    return generated_code


def process_vulnerable_snippets(input_dir, output_dir, hints_file, tokenizer, model, device):
    """
    Process all vulnerable snippets and generate patches with hints.
    
    Args:
        input_dir: Directory containing vulnerable code snippets
        output_dir: Directory to save generated patches
        hints_file: Path to JSON file containing security hints
        tokenizer: CodeLlama tokenizer
        model: CodeLlama model
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Load security hints
    hints = load_security_hints(hints_file)
    print(f"Loaded {len(hints)} security hints")
    
    # Find all C/C++ files
    c_files = list(input_path.rglob('*.c')) + list(input_path.rglob('*.cpp')) + \
              list(input_path.rglob('*.cc')) + list(input_path.rglob('*.cxx'))
    
    processed = 0
    failed = 0
    no_hint = 0
    
    print(f"Processing {len(c_files)} files...")
    
    for file_path in c_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Get hint for this file
            relative_path = str(file_path.relative_to(input_path))
            hint = hints.get(relative_path, None)
            
            if not hint:
                no_hint += 1
                print(f"Warning: No hint found for {file_path.name}, skipping...")
                continue
            
            print(f"Generating patch for: {file_path.name}...", end=" ", flush=True)
            patch = generate_patch_with_hint(code, hint, tokenizer, model, device)
            print("✓", flush=True)
            
            if patch:
                # Maintain directory structure
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
    
    print(f"\nHinted patch generation complete!")
    print(f"Processed: {processed} files")
    print(f"Failed: {failed} files")
    print(f"No hint available: {no_hint} files")
    print(f"Patches saved to: {output_path}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate patches using CodeLlama with security hints")
    parser.add_argument("--input", default="benchmark/vulnerable_snippets",
                       help="Directory containing vulnerable snippets")
    parser.add_argument("--output", default="results/sementic_hint_patches",
                       help="Output directory for generated patches")
    parser.add_argument("--hints", default="benchmark/security_hints.json",
                       help="JSON file containing security hints")
    parser.add_argument("--model", default="codellama/CodeLlama-7b-Instruct-hf",
                       help="CodeLlama model name")
    parser.add_argument("--max-length", type=int, default=1024,
                       help="Maximum generation length")
    
    args = parser.parse_args()
    
    print("Starting hinted patch generation...")
    print(f"Input directory: {args.input}")
    print(f"Output directory: {args.output}")
    print(f"Hints file: {args.hints}")
    print(f"Model: {args.model}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"CUDA version: {torch.version.cuda}")
    else:
        print("Running on CPU (this will be slower)")
    print("-" * 60)
    
    tokenizer, model, device = load_codellama_model(args.model)
    process_vulnerable_snippets(args.input, args.output, args.hints, tokenizer, model, device)



