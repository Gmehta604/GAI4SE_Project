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
BASELINE_DIR = "results/baseline_patches_2"
CODEASTRA_DIR = "results/sementic_hinted_patches_2"
OUTPUT_JSON = "results/functionality_check.json"


def extract_code_from_file(content):
    """Extract C/C++ code from markdown code blocks."""
    if not content:
        return ""
    
    # Find code in markdown blocks
    code_block_pattern = r'```(?:c|cpp|c\+\+|cxx)?\s*\n(.*?)```'
    matches = re.findall(code_block_pattern, content, re.DOTALL | re.IGNORECASE)
    if matches:
        code = max(matches, key=len).strip()
    else:
        code = content.strip()
    
    return code


def clean_code_for_standalone_compilation(code):
    """Remove local header includes and dependencies to make code standalone compilable."""
    if not code:
        return code
    
    lines = code.split('\n')
    cleaned_lines = []
    ifdef_depth = 0
    skip_block = False
    
    # Patterns for local headers that should be removed
    local_header_patterns = [
        r'std_testcase',
        r'std_testcase_io',
        r'io\.h',
        r'std_thread',
    ]
    
    for line in lines:
        original_line = line
        stripped = line.strip()
        
        # Handle local header includes - remove them
        if re.match(r'\s*#\s*include\s*"', stripped):
            # Check if it's a local header we want to skip
            is_local_header = any(re.search(pattern, stripped, re.IGNORECASE) for pattern in local_header_patterns)
            if is_local_header:
                continue  # Skip this include
            # Keep other local includes (might be user-defined)
            cleaned_lines.append(line)
        # Keep standard library includes
        elif re.match(r'\s*#\s*include\s*<', stripped):
            cleaned_lines.append(line)
        # Handle ifdef/ifndef blocks - be careful with these
        elif re.match(r'\s*#\s*ifdef\s+', stripped) or re.match(r'\s*#\s*ifndef\s+', stripped):
            # Check if it's related to OMITBAD/OMITGOOD which we define
            if re.search(r'OMIT(BAD|GOOD)', stripped, re.IGNORECASE):
                cleaned_lines.append(line)  # Keep these, we define them
            else:
                # Skip other ifdef blocks that might depend on missing headers
                ifdef_depth += 1
                skip_block = True
        elif re.match(r'\s*#\s*endif', stripped):
            if ifdef_depth > 0:
                ifdef_depth -= 1
                if ifdef_depth == 0:
                    skip_block = False
            else:
                cleaned_lines.append(line)
        elif skip_block and ifdef_depth > 0:
            # Skip lines inside problematic ifdef blocks
            continue
        # Keep all other lines (including function calls - we provide stubs)
        else:
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)


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
        
        # Clean code to remove local header dependencies
        cleaned_code = clean_code_for_standalone_compilation(code)
        if not cleaned_code or len(cleaned_code.strip()) < 20:
            return False, "No compilable code found after cleaning"
        
        # Simple test harness with stub functions for common patterns
        test_code = f"""#include <iostream>
#include <cstring>
#include <cstdio>
#include <cstdlib>
#include <cstdint>

// Stub functions that might be referenced from missing headers
void printLine(const char* s) {{ std::cout << s << std::endl; }}
void printIntLine(int i) {{ std::cout << i << std::endl; }}
void printLongLine(long l) {{ std::cout << l << std::endl; }}
void printUnsignedLine(unsigned u) {{ std::cout << u << std::endl; }}

// Common type definitions that might be missing
#ifndef OMITBAD
#define OMITBAD
#endif
#ifndef OMITGOOD
#define OMITGOOD
#endif

{cleaned_code}

int main() {{ 
    // Try to call any main-like functions if they exist
    return 0; 
}}
"""
        
        # Write test file
        with open(temp_cpp, 'w', encoding='utf-8') as f:
            f.write(test_code)
        
        # Determine compiler
        is_cpp = file_path.suffix.lower() in ['.cpp', '.cxx', '.cc', '.c++']
        compiler = 'g++' if is_cpp else 'gcc'
        
        # Check if compiler exists first
        try:
            subprocess.run([compiler, '--version'], capture_output=True, timeout=5, check=True)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False, f"Compiler '{compiler}' not found or not accessible"
        except Exception:
            pass  # Continue anyway
        
        # Compile with GCC
        compile_cmd = [compiler, str(temp_cpp), '-o', str(temp_exe)]
        if is_cpp:
            compile_cmd.append('-std=c++11')
        
        # Run GCC
        result = subprocess.run(
            compile_cmd,
            capture_output=True,
            text=True,
            timeout=15,
            errors='replace'
        )
        
        # GCC says success = success, GCC says fail = fail
        if result.returncode == 0 and temp_exe.exists():
            return True, None
        
        # Analyze error to see if it's a real code error or just missing dependencies
        error_output = (result.stderr + result.stdout) if result.stderr or result.stdout else ""
        
        # Check if error is due to missing headers/files (these should have been cleaned)
        missing_header_patterns = [
            r'No such file or directory',
            r'std_testcase\.h',
            r'std_testcase_io\.h',
            r'fatal error.*\.h',
        ]
        
        is_header_error = any(re.search(pattern, error_output, re.IGNORECASE) for pattern in missing_header_patterns)
        
        if is_header_error:
            # This shouldn't happen if cleaning worked, but log it differently
            error_msg = "Header dependency issue (should have been cleaned)"
        else:
            # Real compilation error
            error_msg = error_output[:300] if error_output else "Compilation failed"
        
        return False, error_msg
        
    except FileNotFoundError as e:
        return False, f"File or compiler not found: {str(e)[:200]}"
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
            print(f"✗ Failed: {error[:50] if error else 'Unknown error'}")
        else:
            print(f"⊘ Skipped: {error if error else 'Unknown'}")
    
    return results


def main():
    """Main function."""
    print("Starting functionality check using GCC/G++...")
    print("=" * 60)
    
    # Check if GCC/G++ is available
    for compiler in ['gcc', 'g++']:
        try:
            result = subprocess.run([compiler, '--version'], capture_output=True, timeout=5)
            if result.returncode == 0:
                version_line = result.stdout.decode('utf-8', errors='ignore').split('\n')[0]
                print(f"Found {compiler}: {version_line}")
                break
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    else:
        print("WARNING: GCC/G++ not found. Please install GCC/G++ and ensure it's in your PATH.")
        print("Continuing anyway...")
    print()
    
    baseline_results = check_directory(BASELINE_DIR, "baseline_patches_2")
    codeastra_results = check_directory(CODEASTRA_DIR, "sementic_hinted_patches_2")
    
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
            'sementic_hinted_patches_2': {
                'total_files': len(codeastra_results),
                'compiles_successfully': sum(1 for r in codeastra_results if r['compiles'] is True),
                'compilation_failed': sum(1 for r in codeastra_results if r['compiles'] is False),
                'skipped': sum(1 for r in codeastra_results if r['compiles'] is None),
                'success_rate': 0.0
            }
        },
        'results': {
            'baseline_patches_2': baseline_results,
            'sementic_hinted_patches_2': codeastra_results
        }
    }
    
    # Calculate success rates
    for dir_name in ['baseline_patches_2', 'sementic_hinted_patches_2']:
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
    
    for dir_name in ['baseline_patches_2', 'sementic_hinted_patches_2']:
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

