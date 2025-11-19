"""
check_functionality.py

Checks compilation functionality using GCC/G++ directly.
No parsing, no rules - just compile and report GCC's result.
"""

import subprocess
from pathlib import Path
import json
from datetime import datetime
import re
import os

# Configuration
BASELINE_DIR = "results/baseline_patches"
CODEASTRA_DIR = "results/sementic_hint_patches"
OUTPUT_JSON = "results/functionality_check.json"


def extract_code_from_file(content):
    """Extract C/C++ code from markdown code blocks."""
    if not content:
        return ""
    
    # Find code in markdown blocks
    code_block_pattern = r'```(?:c|cpp|c\+\+|cxx)?\s*\n(.*?)```'
    matches = re.findall(code_block_pattern, content, re.DOTALL | re.IGNORECASE)
    if matches:
        return max(matches, key=len).strip()
    
    # If no markdown, return content as-is
    return content.strip()


def check_compilation(file_path):
    """Compile file using GCC/G++ - trust GCC's result."""
    file_path = Path(file_path)
    
    temp_cpp = file_path.parent / f"{file_path.stem}_test.cpp"
    temp_exe = file_path.parent / f"{file_path.stem}_test.exe"
    
    try:
        # Read file
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        if not content.strip():
            return False, "Empty file"
        
        # Extract code
        code = extract_code_from_file(content)
        if not code or len(code.strip()) < 20:
            return False, "No code found"
        
        # Simple test harness
        test_code = f"""#include <iostream>
#include <cstring>
#include <cstdio>
#include <cstdlib>

void printLine(const char* s) {{ std::cout << s << std::endl; }}
void printIntLine(int i) {{ std::cout << i << std::endl; }}
void printLongLine(long l) {{ std::cout << l << std::endl; }}
void printUnsignedLine(unsigned u) {{ std::cout << u << std::endl; }}

{code}

int main() {{ return 0; }}
"""
        
        # Write test file
        with open(temp_cpp, 'w', encoding='utf-8') as f:
            f.write(test_code)
        
        # Determine compiler
        is_cpp = file_path.suffix.lower() in ['.cpp', '.cxx', '.cc', '.c++']
        compiler = 'g++' if is_cpp else 'gcc'
        
        # Compile with GCC
        compile_cmd = [compiler, str(temp_cpp), '-o', str(temp_exe)]
        if is_cpp:
            compile_cmd.append('-std=c++11')
        
        # Run GCC
        result = subprocess.run(
            compile_cmd,
            capture_output=True,
            text=True,
            timeout=15
        )
        
        # GCC says success = success, GCC says fail = fail
        if result.returncode == 0 and temp_exe.exists():
            return True, None
        
        # GCC failed
        error_msg = result.stderr[:200] if result.stderr else result.stdout[:200] if result.stdout else "Compilation failed"
        return False, error_msg
        
    except FileNotFoundError:
        return None, f"GCC/G++ not found"
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)[:200]
    finally:
        # Cleanup
        for f in [temp_cpp, temp_exe]:
            if f.exists():
                try:
                    f.unlink()
                except:
                    pass


def check_directory(directory_path, directory_name):
    """Check all files in directory."""
    directory = Path(directory_path)
    if not directory.exists():
        print(f"Warning: Directory not found: {directory_path}")
        return []
    
    c_files = list(directory.rglob('*.c')) + list(directory.rglob('*.cpp')) + \
              list(directory.rglob('*.cc')) + list(directory.rglob('*.cxx'))
    
    results = []
    print(f"\nChecking {directory_name} ({len(c_files)} files)...")
    
    for i, file_path in enumerate(c_files, 1):
        print(f"  [{i}/{len(c_files)}] {file_path.name}...", end=" ", flush=True)
        
        compiles, error = check_compilation(file_path)
        
        result = {
            'file': str(file_path.relative_to(directory)),
            'full_path': str(file_path),
            'compiles': compiles,
        }
        
        if error:
            result['error'] = error
        
        results.append(result)
        
        if compiles is True:
            print("✓ Compiles")
        elif compiles is False:
            print(f"✗ Failed")
        else:
            print(f"⊘ Skipped")
    
    return results


def main():
    """Main function."""
    print("Starting functionality check using GCC/G++...")
    print("=" * 60)
    
    baseline_results = check_directory(BASELINE_DIR, "baseline_patches_2")
    codeastra_results = check_directory(CODEASTRA_DIR, "codeastra_2")
    
    output_data = {
        'timestamp': datetime.now().isoformat(),
        'functionality_summary': {
            'baseline_patches_2': {
                'total_files': len(baseline_results),
                'compiles_successfully': sum(1 for r in baseline_results if r['compiles'] is True),
                'compilation_failed': sum(1 for r in baseline_results if r['compiles'] is False),
                'skipped': sum(1 for r in baseline_results if r['compiles'] is None),
                'success_rate': 0.0
            },
            'codeastra_2': {
                'total_files': len(codeastra_results),
                'compiles_successfully': sum(1 for r in codeastra_results if r['compiles'] is True),
                'compilation_failed': sum(1 for r in codeastra_results if r['compiles'] is False),
                'skipped': sum(1 for r in codeastra_results if r['compiles'] is None),
                'success_rate': 0.0
            }
        },
        'results': {
            'baseline_patches_2': baseline_results,
            'codeastra_2': codeastra_results
        }
    }
    
    # Calculate success rates
    for dir_name in ['baseline_patches_2', 'codeastra_2']:
        summary = output_data['functionality_summary'][dir_name]
        if summary['total_files'] > 0:
            summary['success_rate'] = (summary['compiles_successfully'] / summary['total_files']) * 100
    
    # Save to JSON
    output_path = Path(OUTPUT_JSON)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("\n" + "=" * 60)
    print("FUNCTIONALITY CHECK SUMMARY")
    print("=" * 60)
    
    for dir_name in ['baseline_patches_2', 'codeastra_2']:
        summary = output_data['functionality_summary'][dir_name]
        print(f"\n{dir_name}:")
        print(f"  Total files: {summary['total_files']}")
        print(f"  Compiles successfully: {summary['compiles_successfully']}")
        print(f"  Compilation failed: {summary['compilation_failed']}")
        print(f"  Skipped: {summary['skipped']}")
        print(f"  Success rate: {summary['success_rate']:.1f}%")
    
    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()

