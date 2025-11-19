"""
generate_report.py

Generates a comprehensive report comparing:
1. Vulnerable code -> Baseline patches (with BLEU score)
2. Baseline patches -> Hinted patches (with BLEU score)

Uses BLEU score as a metric to determine similarity between code snippets.
"""

import os
import csv
import re
from pathlib import Path
from collections import Counter
import math


def extract_code_from_patch(patch_content):
    """
    Extract C/C++ code from patch file, handling markdown code blocks.
    
    Args:
        patch_content: Content of the patch file (may contain markdown)
        
    Returns:
        str: Extracted code, or original content if no code block found
    """
    # Try to find code in markdown code blocks (```c, ```cpp, ```c++, etc.)
    code_block_pattern = r'```(?:c|cpp|c\+\+)?\s*\n(.*?)```'
    match = re.search(code_block_pattern, patch_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # If no markdown code block, return original content
    return patch_content.strip()


def tokenize_code(code):
    """
    Tokenize code into tokens for BLEU score calculation.
    Splits on whitespace, punctuation, and operators.
    
    Args:
        code: Code string to tokenize
        
    Returns:
        list: List of tokens
    """
    # Remove comments (single-line and multi-line)
    code = re.sub(r'//.*?$', '', code, flags=re.MULTILINE)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    
    # Tokenize: split on whitespace, but keep operators and punctuation as separate tokens
    # This is a simple tokenization - for better results, use a proper code tokenizer
    tokens = []
    current_token = []
    
    for char in code:
        if char.isspace():
            if current_token:
                tokens.append(''.join(current_token))
                current_token = []
        elif char in '()[]{},;:+-*/%=<>!&|^~':
            if current_token:
                tokens.append(''.join(current_token))
                current_token = []
            tokens.append(char)
        else:
            current_token.append(char)
    
    if current_token:
        tokens.append(''.join(current_token))
    
    # Filter out empty tokens
    tokens = [t for t in tokens if t.strip()]
    
    return tokens


def ngram_precision(candidate, reference, n):
    """
    Calculate n-gram precision for BLEU score.
    
    Args:
        candidate: Candidate tokens (list)
        reference: Reference tokens (list)
        n: n-gram size
        
    Returns:
        tuple: (matches, total_candidate_ngrams)
    """
    candidate_ngrams = []
    for i in range(len(candidate) - n + 1):
        candidate_ngrams.append(tuple(candidate[i:i+n]))
    
    reference_ngrams = []
    for i in range(len(reference) - n + 1):
        reference_ngrams.append(tuple(reference[i:i+n]))
    
    candidate_counts = Counter(candidate_ngrams)
    reference_counts = Counter(reference_ngrams)
    
    matches = 0
    for ngram, count in candidate_counts.items():
        matches += min(count, reference_counts.get(ngram, 0))
    
    total = len(candidate_ngrams)
    return matches, total


def brevity_penalty(candidate, reference):
    """
    Calculate brevity penalty for BLEU score.
    
    Args:
        candidate: Candidate tokens (list)
        reference: Reference tokens (list)
        
    Returns:
        float: Brevity penalty (0-1)
    """
    if len(candidate) > len(reference):
        return 1.0
    elif len(reference) == 0:
        return 0.0
    else:
        return math.exp(1 - len(reference) / len(candidate))


def bleu_score(candidate, reference, max_n=4):
    """
    Calculate BLEU score between candidate and reference code.
    
    BLEU (Bilingual Evaluation Understudy) score measures similarity between
    two code snippets based on n-gram precision. A score of 1.0 means perfect
    match, while 0.0 means no similarity. In the context of code comparison:
    - Higher BLEU score = more similar code (more tokens match)
    - Lower BLEU score = more different code (fewer tokens match)
    
    Note: BLEU is designed for natural language but can be adapted for code.
    It measures token-level similarity, not semantic correctness.
    
    Args:
        candidate: Candidate code string (the generated/modified code)
        reference: Reference code string (the original/target code)
        max_n: Maximum n-gram size (default 4, meaning 1-grams through 4-grams)
        
    Returns:
        float: BLEU score (0-1, higher is more similar)
    """
    candidate_tokens = tokenize_code(candidate)
    reference_tokens = tokenize_code(reference)
    
    if len(candidate_tokens) == 0:
        return 0.0
    
    if len(reference_tokens) == 0:
        return 0.0
    
    # Calculate precision for each n-gram
    precisions = []
    for n in range(1, max_n + 1):
        matches, total = ngram_precision(candidate_tokens, reference_tokens, n)
        if total == 0:
            precisions.append(0.0)
        else:
            precisions.append(matches / total)
    
    # Calculate geometric mean of precisions
    if any(p == 0 for p in precisions):
        return 0.0
    
    geometric_mean = math.exp(sum(math.log(p) for p in precisions) / len(precisions))
    
    # Apply brevity penalty
    bp = brevity_penalty(candidate_tokens, reference_tokens)
    
    bleu = bp * geometric_mean
    return min(1.0, max(0.0, bleu))


def normalize_code(code):
    """
    Normalize code by removing extra whitespace and standardizing formatting.
    
    Args:
        code: Code string
        
    Returns:
        str: Normalized code
    """
    # Remove leading/trailing whitespace
    code = code.strip()
    
    # Normalize whitespace (multiple spaces/tabs to single space)
    code = re.sub(r'\s+', ' ', code)
    
    # Normalize newlines
    code = re.sub(r'\n\s*\n', '\n', code)
    
    return code


def calculate_code_diff_stats(code1, code2):
    """
    Calculate basic statistics about code differences.
    
    Args:
        code1: First code string
        code2: Second code string
        
    Returns:
        dict: Statistics including line counts, token counts, etc.
    """
    tokens1 = tokenize_code(code1)
    tokens2 = tokenize_code(code2)
    
    lines1 = len([l for l in code1.split('\n') if l.strip()])
    lines2 = len([l for l in code2.split('\n') if l.strip()])
    
    return {
        'tokens1': len(tokens1),
        'tokens2': len(tokens2),
        'lines1': lines1,
        'lines2': lines2,
        'token_diff': len(tokens2) - len(tokens1),
        'line_diff': lines2 - lines1,
    }


def generate_comparison_report(
    vulnerable_dir,
    baseline_dir,
    hinted_dir,
    output_csv="results/comparison_report.csv"
):
    """
    Generate a comprehensive report comparing vulnerable code, baseline patches, and hinted patches.
    
    Args:
        vulnerable_dir: Directory containing vulnerable snippets
        baseline_dir: Directory containing baseline patches
        hinted_dir: Directory containing hinted patches
        output_csv: Output CSV file path
    """
    vulnerable_path = Path(vulnerable_dir)
    baseline_path = Path(baseline_dir)
    hinted_path = Path(hinted_dir)
    
    # Find all baseline patch files
    baseline_files = list(baseline_path.rglob('*.c')) + list(baseline_path.rglob('*.cpp'))
    
    results = []
    
    print("Generating comparison report...")
    print(f"Found {len(baseline_files)} baseline patches")
    print("-" * 80)
    
    for baseline_file in baseline_files:
        relative_path = baseline_file.relative_to(baseline_path)
        vulnerable_file = vulnerable_path / relative_path
        hinted_file = hinted_path / relative_path
        
        # Skip if vulnerable file doesn't exist
        if not vulnerable_file.exists():
            print(f"Skipping {relative_path}: vulnerable file not found")
            continue
        
        # Read vulnerable code
        try:
            with open(vulnerable_file, 'r', encoding='utf-8') as f:
                vulnerable_code = f.read()
        except Exception as e:
            print(f"Error reading {vulnerable_file}: {e}")
            continue
        
        # Read baseline patch
        try:
            with open(baseline_file, 'r', encoding='utf-8') as f:
                baseline_content = f.read()
            baseline_code = extract_code_from_patch(baseline_content)
        except Exception as e:
            print(f"Error reading {baseline_file}: {e}")
            continue
        
        # Read hinted patch (if exists)
        hinted_code = None
        if hinted_file.exists():
            try:
                with open(hinted_file, 'r', encoding='utf-8') as f:
                    hinted_content = f.read()
                hinted_code = extract_code_from_patch(hinted_content)
            except Exception as e:
                print(f"Error reading {hinted_file}: {e}")
        
        # Normalize codes for comparison
        vulnerable_norm = normalize_code(vulnerable_code)
        baseline_norm = normalize_code(baseline_code)
        
        # Calculate BLEU scores
        # 1. Vulnerable -> Baseline
        bleu_vulnerable_to_baseline = bleu_score(baseline_norm, vulnerable_norm)
        
        # 2. Baseline -> Hinted (if hinted exists)
        bleu_baseline_to_hinted = None
        if hinted_code:
            hinted_norm = normalize_code(hinted_code)
            bleu_baseline_to_hinted = bleu_score(hinted_norm, baseline_norm)
        
        # Calculate code length changes
        vulnerable_len = len(vulnerable_code)
        baseline_len = len(baseline_code)
        hinted_len = len(hinted_code) if hinted_code else None
        
        baseline_change = baseline_len - vulnerable_len
        hinted_change = (hinted_len - baseline_len) if hinted_len else None
        
        # Calculate additional statistics
        v_to_b_stats = calculate_code_diff_stats(vulnerable_code, baseline_code)
        b_to_h_stats = calculate_code_diff_stats(baseline_code, hinted_code) if hinted_code else None
        
        # Store results
        result = {
            'file': str(relative_path),
            'vulnerable_length': vulnerable_len,
            'baseline_length': baseline_len,
            'hinted_length': hinted_len if hinted_len else 'N/A',
            'vulnerable_lines': v_to_b_stats['lines1'],
            'baseline_lines': v_to_b_stats['lines2'],
            'hinted_lines': b_to_h_stats['lines2'] if b_to_h_stats else 'N/A',
            'vulnerable_tokens': v_to_b_stats['tokens1'],
            'baseline_tokens': v_to_b_stats['tokens2'],
            'hinted_tokens': b_to_h_stats['tokens2'] if b_to_h_stats else 'N/A',
            'baseline_length_change': baseline_change,
            'hinted_length_change': hinted_change if hinted_change is not None else 'N/A',
            'baseline_line_change': v_to_b_stats['line_diff'],
            'hinted_line_change': b_to_h_stats['line_diff'] if b_to_h_stats else 'N/A',
            'baseline_token_change': v_to_b_stats['token_diff'],
            'hinted_token_change': b_to_h_stats['token_diff'] if b_to_h_stats else 'N/A',
            'bleu_vulnerable_to_baseline': round(bleu_vulnerable_to_baseline, 4),
            'bleu_baseline_to_hinted': round(bleu_baseline_to_hinted, 4) if bleu_baseline_to_hinted is not None else 'N/A',
        }
        
        results.append(result)
        
        print(f"Processed: {relative_path}")
        print(f"  BLEU (Vulnerable->Baseline): {bleu_vulnerable_to_baseline:.4f}")
        if bleu_baseline_to_hinted is not None:
            print(f"  BLEU (Baseline->Hinted): {bleu_baseline_to_hinted:.4f}")
    
    # Write results to CSV
    output_path = Path(output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        if results:
            fieldnames = [
                'file',
                'vulnerable_length',
                'baseline_length',
                'hinted_length',
                'vulnerable_lines',
                'baseline_lines',
                'hinted_lines',
                'vulnerable_tokens',
                'baseline_tokens',
                'hinted_tokens',
                'baseline_length_change',
                'hinted_length_change',
                'baseline_line_change',
                'hinted_line_change',
                'baseline_token_change',
                'hinted_token_change',
                'bleu_vulnerable_to_baseline',
                'bleu_baseline_to_hinted'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
    
    print("\n" + "=" * 80)
    print("Report Generation Complete!")
    print(f"Results saved to: {output_path}")
    print(f"Total files processed: {len(results)}")
    
    # Print summary statistics
    if results:
        bleu_v_to_b_scores = [r['bleu_vulnerable_to_baseline'] for r in results]
        bleu_b_to_h_scores = [r['bleu_baseline_to_hinted'] for r in results if r['bleu_baseline_to_hinted'] != 'N/A']
        
        baseline_length_changes = [r['baseline_length_change'] for r in results]
        hinted_length_changes = [r['hinted_length_change'] for r in results if r['hinted_length_change'] != 'N/A']
        
        baseline_line_changes = [r['baseline_line_change'] for r in results]
        hinted_line_changes = [r['hinted_line_change'] for r in results if r['hinted_line_change'] != 'N/A']
        
        print("\n" + "=" * 80)
        print("Summary Statistics")
        print("=" * 80)
        
        print("\nBLEU Scores (Vulnerable -> Baseline):")
        print(f"  Average: {sum(bleu_v_to_b_scores) / len(bleu_v_to_b_scores):.4f}")
        print(f"  Min: {min(bleu_v_to_b_scores):.4f}")
        print(f"  Max: {max(bleu_v_to_b_scores):.4f}")
        
        if bleu_b_to_h_scores:
            print("\nBLEU Scores (Baseline -> Hinted):")
            print(f"  Average: {sum(bleu_b_to_h_scores) / len(bleu_b_to_h_scores):.4f}")
            print(f"  Min: {min(bleu_b_to_h_scores):.4f}")
            print(f"  Max: {max(bleu_b_to_h_scores):.4f}")
        
        print("\nCode Length Changes (Baseline vs Vulnerable):")
        print(f"  Average change: {sum(baseline_length_changes) / len(baseline_length_changes):.1f} characters")
        print(f"  Min change: {min(baseline_length_changes):.1f} characters")
        print(f"  Max change: {max(baseline_length_changes):.1f} characters")
        
        if hinted_length_changes:
            print("\nCode Length Changes (Hinted vs Baseline):")
            print(f"  Average change: {sum(hinted_length_changes) / len(hinted_length_changes):.1f} characters")
            print(f"  Min change: {min(hinted_length_changes):.1f} characters")
            print(f"  Max change: {max(hinted_length_changes):.1f} characters")
        
        print("\nLine Count Changes (Baseline vs Vulnerable):")
        print(f"  Average change: {sum(baseline_line_changes) / len(baseline_line_changes):.1f} lines")
        print(f"  Min change: {min(baseline_line_changes):.1f} lines")
        print(f"  Max change: {max(baseline_line_changes):.1f} lines")
        
        if hinted_line_changes:
            print("\nLine Count Changes (Hinted vs Baseline):")
            print(f"  Average change: {sum(hinted_line_changes) / len(hinted_line_changes):.1f} lines")
            print(f"  Min change: {min(hinted_line_changes):.1f} lines")
            print(f"  Max change: {max(hinted_line_changes):.1f} lines")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate comparison report with BLEU scores")
    parser.add_argument("--vulnerable", default="benchmark/vulnerable_snippets_2",
                       help="Directory containing vulnerable snippets")
    parser.add_argument("--baseline", default="results/baseline_patches_2",
                       help="Directory containing baseline patches")
    parser.add_argument("--hinted", default="results/codeastra_2",
                       help="Directory containing hinted patches")
    parser.add_argument("--output", default="results/comparison_report.csv",
                       help="Output CSV file")
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("Code Comparison Report Generator")
    print("=" * 80)
    print(f"Vulnerable snippets: {args.vulnerable}")
    print(f"Baseline patches: {args.baseline}")
    print(f"Hinted patches: {args.hinted}")
    print(f"Output: {args.output}")
    print("=" * 80)
    
    generate_comparison_report(
        args.vulnerable,
        args.baseline,
        args.hinted,
        args.output
    )

