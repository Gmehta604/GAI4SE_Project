"""
evaluate.py

Evaluates generated patches on three dimensions:
1. Security: Using flawfinder
2. Functionality: Compilation and execution
3. Quality: CodeBERT similarity to ground truth
"""

import os
import subprocess
import json
import csv
from pathlib import Path
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from scipy.spatial.distance import cosine


def check_security(patch_file):
    """
    Check if patch passes security analysis using flawfinder.
    
    Args:
        patch_file: Path to the generated patch file
        
    Returns:
        bool: True if no security issues found, False otherwise
    """
    try:
        result = subprocess.run(
            ['flawfinder', str(patch_file)],
            capture_output=True,
            text=True,
            timeout=30
        )
        # Flawfinder returns 0 if no issues found, non-zero otherwise
        # Also check if output contains "No hits found"
        return result.returncode == 0 or "No hits found" in result.stdout
    except FileNotFoundError:
        print("Warning: flawfinder not found. Install with: pip install flawfinder")
        return None
    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
        print(f"Error running flawfinder on {patch_file}: {e}")
        return False


def check_functionality(patch_file, test_input=None):
    """
    Check if patch compiles and runs correctly.
    
    Args:
        patch_file: Path to the generated patch file
        test_input: Optional test input for the program
        
    Returns:
        bool: True if compiles and runs successfully, False otherwise
    """
    patch_path = Path(patch_file)
    compile_output = patch_path.parent / f"{patch_path.stem}_compiled"
    
    try:
        # Try to compile
        compile_result = subprocess.run(
            ['gcc', str(patch_file), '-o', str(compile_output), '-w'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if compile_result.returncode != 0:
            return False
        
        # Try to run (if executable was created)
        if compile_output.exists():
            run_result = subprocess.run(
                [str(compile_output)],
                capture_output=True,
                text=True,
                timeout=10,
                input=test_input if test_input else None
            )
            # Clean up
            compile_output.unlink(missing_ok=True)
            return run_result.returncode == 0
        
        return False
        
    except FileNotFoundError:
        print("Warning: gcc not found. Skipping functionality check.")
        return None
    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
        print(f"Error checking functionality of {patch_file}: {e}")
        return False
    finally:
        # Clean up
        compile_output.unlink(missing_ok=True)


def load_codebert_model():
    """
    Load CodeBERT model for similarity computation.
    
    Returns:
        tuple: (tokenizer, model)
    """
    try:
        tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
        model = AutoModel.from_pretrained(
            "microsoft/codebert-base",
            dtype=torch.float32
        )
        model.eval()
        return tokenizer, model
    except Exception as e:
        print(f"Error loading CodeBERT: {e}")
        return None, None


def compute_codebert_similarity(code1, code2, tokenizer, model):
    """
    Compute CodeBERT similarity between two code snippets.
    
    Args:
        code1: First code snippet
        code2: Second code snippet
        tokenizer: CodeBERT tokenizer
        model: CodeBERT model
        
    Returns:
        float: Similarity score (0-1, higher is more similar)
    """
    if tokenizer is None or model is None:
        return None
    
    try:
        # Tokenize and encode
        tokens1 = tokenizer(code1, return_tensors="pt", truncation=True, max_length=512, padding=True)
        tokens2 = tokenizer(code2, return_tensors="pt", truncation=True, max_length=512, padding=True)
        
        with torch.no_grad():
            # Get embeddings (use CLS token)
            emb1 = model(**tokens1).last_hidden_state[:, 0, :].numpy()
            emb2 = model(**tokens2).last_hidden_state[:, 0, :].numpy()
        
        # Compute cosine similarity
        similarity = 1 - cosine(emb1[0], emb2[0])
        return max(0, min(1, similarity))  # Clamp to [0, 1]
    except Exception as e:
        print(f"Error computing similarity: {e}")
        return None


def check_quality(patch_file, ground_truth_file, tokenizer, model):
    """
    Check quality by comparing patch to ground truth using CodeBERT.
    
    Args:
        patch_file: Path to generated patch
        ground_truth_file: Path to ground truth patch
        tokenizer: CodeBERT tokenizer
        model: CodeBERT model
        
    Returns:
        float: Similarity score (0-1)
    """
    try:
        with open(patch_file, 'r', encoding='utf-8') as f:
            patch_code = f.read()
        
        with open(ground_truth_file, 'r', encoding='utf-8') as f:
            ground_truth_code = f.read()
        
        return compute_codebert_similarity(patch_code, ground_truth_code, tokenizer, model)
    except Exception as e:
        print(f"Error checking quality: {e}")
        return None


def get_ground_truth_filename(patch_filename):
    """
    Convert patch filename to ground truth filename.
    Patches are named *_bad.cpp, ground truth is named *_goodB2G.cpp
    
    Args:
        patch_filename: Filename of the patch (e.g., "file_bad.cpp")
        
    Returns:
        str: Ground truth filename (e.g., "file_goodB2G.cpp")
    """
    if isinstance(patch_filename, Path):
        patch_filename = patch_filename.name
    
    # Replace _bad.cpp or _bad.c with _goodB2G.cpp or _goodB2G.c
    if patch_filename.endswith('_bad.cpp'):
        return patch_filename.replace('_bad.cpp', '_goodB2G.cpp')
    elif patch_filename.endswith('_bad.c'):
        return patch_filename.replace('_bad.c', '_goodB2G.c')
    else:
        # If no _bad suffix, try to find matching ground truth
        # This handles other naming conventions
        return patch_filename


def evaluate_patches(baseline_dir, hinted_dir, vulnerable_dir, ground_truth_dir, output_csv="results/results.csv"):
    """
    Evaluate all generated patches.
    
    Args:
        baseline_dir: Directory containing baseline patches
        hinted_dir: Directory containing hinted patches
        vulnerable_dir: Directory containing vulnerable snippets
        ground_truth_dir: Directory containing ground truth patches
        output_csv: Output CSV file path
    """
    baseline_path = Path(baseline_dir)
    hinted_path = Path(hinted_dir)
    vulnerable_path = Path(vulnerable_dir)
    ground_truth_path = Path(ground_truth_dir)
    
    # Load CodeBERT model
    print("Loading CodeBERT model for quality evaluation...")
    tokenizer, model = load_codebert_model()
    
    # Find all patch files
    baseline_files = list(baseline_path.rglob('*.c')) + list(baseline_path.rglob('*.cpp'))
    hinted_files = list(hinted_path.rglob('*.c')) + list(hinted_path.rglob('*.cpp'))
    
    results = []
    
    # Evaluate baseline patches
    print("\nEvaluating baseline patches...")
    for patch_file in baseline_files:
        relative_path = patch_file.relative_to(baseline_path)
        vulnerable_file = vulnerable_path / relative_path
        # Convert patch filename to ground truth filename
        ground_truth_filename = get_ground_truth_filename(relative_path.name)
        ground_truth_file = ground_truth_path / ground_truth_filename
        
        if not vulnerable_file.exists():
            print(f"Skipping {relative_path}: vulnerable file not found at {vulnerable_file}")
            continue
        if not ground_truth_file.exists():
            print(f"Skipping {relative_path}: ground truth file not found at {ground_truth_file}")
            continue
        
        print(f"Evaluating: {relative_path}")
        
        security_pass = check_security(patch_file)
        func_pass = check_functionality(patch_file)
        similarity = check_quality(patch_file, ground_truth_file, tokenizer, model)
        
        results.append({
            'method': 'baseline',
            'file': str(relative_path),
            'security_pass': security_pass,
            'func_pass': func_pass,
            'similarity_score': similarity
        })
    
    # Evaluate hinted patches
    print("\nEvaluating hinted patches...")
    for patch_file in hinted_files:
        relative_path = patch_file.relative_to(hinted_path)
        vulnerable_file = vulnerable_path / relative_path
        # Convert patch filename to ground truth filename
        ground_truth_filename = get_ground_truth_filename(relative_path.name)
        ground_truth_file = ground_truth_path / ground_truth_filename
        
        if not vulnerable_file.exists():
            print(f"Skipping {relative_path}: vulnerable file not found at {vulnerable_file}")
            continue
        if not ground_truth_file.exists():
            print(f"Skipping {relative_path}: ground truth file not found at {ground_truth_file}")
            continue
        
        print(f"Evaluating: {relative_path}")
        
        security_pass = check_security(patch_file)
        func_pass = check_functionality(patch_file)
        similarity = check_quality(patch_file, ground_truth_file, tokenizer, model)
        
        results.append({
            'method': 'hinted',
            'file': str(relative_path),
            'security_pass': security_pass,
            'func_pass': func_pass,
            'similarity_score': similarity
        })
    
    # Write results to CSV
    output_path = Path(output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        if results:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
    
    print(f"\nEvaluation complete!")
    print(f"Results saved to: {output_path}")
    print(f"Total evaluations: {len(results)}")
    
    # Print summary statistics
    if results:
        baseline_results = [r for r in results if r['method'] == 'baseline']
        hinted_results = [r for r in results if r['method'] == 'hinted']
        
        def print_stats(method_name, method_results):
            if not method_results:
                return
            security_passes = sum(1 for r in method_results if r['security_pass'] is True)
            func_passes = sum(1 for r in method_results if r['func_pass'] is True)
            similarities = [r['similarity_score'] for r in method_results if r['similarity_score'] is not None]
            avg_similarity = np.mean(similarities) if similarities else None
            
            print(f"\n{method_name} Statistics:")
            print(f"  Security pass rate: {security_passes}/{len(method_results)} ({100*security_passes/len(method_results):.1f}%)")
            print(f"  Functionality pass rate: {func_passes}/{len(method_results)} ({100*func_passes/len(method_results):.1f}%)")
            if avg_similarity:
                print(f"  Average similarity: {avg_similarity:.3f}")
        
        print_stats("Baseline", baseline_results)
        print_stats("Hinted", hinted_results)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Evaluate generated patches")
    parser.add_argument("--baseline", default="results/baseline_patches",
                       help="Directory containing baseline patches")
    parser.add_argument("--hinted", default="results/semantic_hint_patches",
                       help="Directory containing hinted patches")
    parser.add_argument("--vulnerable", default="benchmark/vulnerable_snippets",
                       help="Directory containing vulnerable snippets")
    parser.add_argument("--ground-truth", default="benchmark/ground_truth",
                       help="Directory containing ground truth patches")
    parser.add_argument("--output", default="results/results.csv",
                       help="Output CSV file")
    
    args = parser.parse_args()
    
    print("Starting patch evaluation...")
    print(f"Baseline patches: {args.baseline}")
    print(f"Hinted patches: {args.hinted}")
    print(f"Vulnerable snippets: {args.vulnerable}")
    print(f"Ground truth patches: {args.ground_truth}")
    print(f"Output: {args.output}")
    print("-" * 60)
    
    evaluate_patches(
        args.baseline,
        args.hinted,
        args.vulnerable,
        args.ground_truth,
        args.output
    )

