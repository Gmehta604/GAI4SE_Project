"""
parse_juliet.py

Extracts _bad() and _good() functions from Juliet C/C++ test cases.
Outputs vulnerable snippets and ground truth patches.
"""

import os
import re
from pathlib import Path


def extract_functions(file_path):
    """
    Extract _bad() and _good() functions from a Juliet test case file.
    
    Args:
        file_path: Path to the Juliet C/C++ source file
        
    Returns:
        tuple: (bad_function, good_function) or (None, None) if not found
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None, None
    
    # Pattern to match function definitions
    # Matches: return_type function_name_bad(...) { ... }
    bad_pattern = r'(\w+\s+\w+_bad\s*\([^)]*\)\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})'
    good_pattern = r'(\w+\s+\w+_good\s*\([^)]*\)\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})'
    
    # More robust pattern using balanced braces
    def extract_function(content, func_name):
        """Extract function with balanced braces."""
        pattern = rf'\w+\s+{func_name}\s*\([^)]*\)\s*\{{'
        match = re.search(pattern, content)
        if not match:
            return None
        
        start = match.start()
        brace_count = 0
        in_function = False
        
        for i in range(start, len(content)):
            if content[i] == '{':
                brace_count += 1
                in_function = True
            elif content[i] == '}':
                brace_count -= 1
                if in_function and brace_count == 0:
                    return content[start:i+1]
        
        return None
    
    bad_func = extract_function(content, '_bad')
    good_func = extract_function(content, '_good')
    
    return bad_func, good_func


def process_juliet_directory(input_dir, output_vulnerable_dir, output_patches_dir):
    """
    Process all C/C++ files in the Juliet directory.
    
    Args:
        input_dir: Directory containing Juliet test cases
        output_vulnerable_dir: Directory to save vulnerable snippets
        output_patches_dir: Directory to save ground truth patches
    """
    input_path = Path(input_dir)
    vulnerable_path = Path(output_vulnerable_dir)
    patches_path = Path(output_patches_dir)
    
    # Create output directories if they don't exist
    vulnerable_path.mkdir(parents=True, exist_ok=True)
    patches_path.mkdir(parents=True, exist_ok=True)
    
    # Find all C/C++ files
    c_files = list(input_path.rglob('*.c')) + list(input_path.rglob('*.cpp')) + \
              list(input_path.rglob('*.cc')) + list(input_path.rglob('*.cxx'))
    
    processed_count = 0
    skipped_count = 0
    
    for file_path in c_files:
        bad_func, good_func = extract_functions(file_path)
        
        if bad_func is None or good_func is None:
            skipped_count += 1
            continue
        
        # Generate output filename based on source file
        relative_path = file_path.relative_to(input_path)
        base_name = relative_path.stem
        parent_dirs = relative_path.parent.parts
        
        # Create corresponding directory structure in output
        if parent_dirs:
            (vulnerable_path / Path(*parent_dirs)).mkdir(parents=True, exist_ok=True)
            (patches_path / Path(*parent_dirs)).mkdir(parents=True, exist_ok=True)
            vulnerable_file = vulnerable_path / Path(*parent_dirs) / f"{base_name}_bad.c"
            patch_file = patches_path / Path(*parent_dirs) / f"{base_name}_good.c"
        else:
            vulnerable_file = vulnerable_path / f"{base_name}_bad.c"
            patch_file = patches_path / f"{base_name}_good.c"
        
        # Write vulnerable snippet
        with open(vulnerable_file, 'w', encoding='utf-8') as f:
            f.write(bad_func)
        
        # Write ground truth patch
        with open(patch_file, 'w', encoding='utf-8') as f:
            f.write(good_func)
        
        processed_count += 1
        print(f"Processed: {file_path.name}")
    
    print(f"\nProcessing complete!")
    print(f"Processed: {processed_count} files")
    print(f"Skipped: {skipped_count} files")


if __name__ == "__main__":
    # Configuration
    JULIET_DIR = "juliet_files"
    VULNERABLE_DIR = "benchmark/vulnerable_snippets"
    PATCHES_DIR = "benchmark/ground_truth_patches"
    
    print("Starting Juliet test case parsing...")
    print(f"Input directory: {JULIET_DIR}")
    print(f"Output vulnerable snippets: {VULNERABLE_DIR}")
    print(f"Output ground truth patches: {PATCHES_DIR}")
    print("-" * 60)
    
    process_juliet_directory(JULIET_DIR, VULNERABLE_DIR, PATCHES_DIR)




