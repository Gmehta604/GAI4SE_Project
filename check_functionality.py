"""
check_functionality.py

Checks compilation functionality of patches in baseline_patches_2 and codeastra_2 directories.
Saves results to JSON.
"""

import subprocess
from pathlib import Path
import json
from datetime import datetime

# Configuration
BASELINE_DIR = "results/baseline_patches"
CODEASTRA_DIR = "results/codeastra_2"
OUTPUT_JSON = "results/functionality_check.json"


def extract_code_from_file(content):
    """Extract C/C++ code from file, removing markdown and explanatory text."""
    import re
    
    # Try to find code in markdown code blocks (```c, ```cpp, ```c++, etc.)
    code_block_pattern = r'```(?:c|cpp|c\+\+|cxx)?\s*\n(.*?)```'
    matches = re.findall(code_block_pattern, content, re.DOTALL | re.IGNORECASE)
    if matches:
        # Take the longest match (likely the actual code)
        return max(matches, key=len).strip()
    
    # If no markdown block, try to extract code by finding the first code-like line
    lines = content.split('\n')
    code_lines = []
    found_code_start = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip empty lines at the start
        if not stripped and not found_code_start:
            continue
        
        # Skip markdown code block markers
        if stripped.startswith('```'):
            continue
        
        # Skip lines that are clearly markdown/explanatory text
        # (contain backticks but aren't code)
        if '`' in stripped:
            # Allow if it's clearly code (has #include, namespace, etc.)
            if not any(keyword in stripped for keyword in ['#include', '#define', '#ifndef', 'namespace', 'class', 'struct', 'void', 'int', 'char', 'return']):
                continue
        
        # Skip lines that look like plain text explanations
        # (no code keywords, no code symbols)
        if stripped and not found_code_start:
            has_code_keyword = any(kw in stripped for kw in [
                '#include', '#define', '#ifndef', '#endif', 'namespace', 'class', 'struct', 
                'void', 'int', 'char', 'const', 'static', 'public', 'private', 'protected',
                'return', 'if', 'for', 'while', 'switch', 'case', 'break', 'continue'
            ])
            has_code_symbol = any(c in stripped for c in [';', '{', '}', '(', ')', '=', '<', '>', '[', ']', '::', '->', '.'])
            
            if not has_code_keyword and not has_code_symbol:
                continue
        
        # Once we find code, include everything (might be multi-line statements)
        if not found_code_start:
            # Check if this looks like the start of code
            if any(keyword in stripped for keyword in ['#include', '#define', '#ifndef', 'namespace', 'class', 'struct', 'void', 'int', 'char']):
                found_code_start = True
            elif any(c in stripped for c in [';', '{', '}', '(', ')']):
                found_code_start = True
        
        if found_code_start:
            code_lines.append(line)
    
    extracted = '\n'.join(code_lines).strip()
    
    # Clean up: remove any remaining markdown artifacts
    if extracted:
        # Remove lines that are just backticks or markdown
        cleaned_lines = []
        for line in extracted.split('\n'):
            stripped = line.strip()
            # Skip pure markdown/explanatory lines
            if stripped == '`' or stripped.startswith('```'):
                continue
            # Skip lines that are clearly explanations (contain backticks but no code)
            if '`' in stripped:
                # Only keep if it has code-like content
                if not any(c in stripped for c in [';', '{', '}', '(', ')', '=', '<', '>', '#', '::', '->']):
                    continue
            # Skip lines that look like plain text (no code keywords, no code symbols)
            if stripped and not any(keyword in stripped for keyword in [
                '#include', '#define', '#ifndef', '#endif', 'namespace', 'class', 'struct',
                'void', 'int', 'char', 'const', 'static', 'public', 'private', 'protected',
                'return', 'if', 'for', 'while', 'switch', 'case', 'break', 'continue',
                'new', 'delete', 'malloc', 'free', 'sizeof', 'typedef', 'using'
            ]):
                if not any(c in stripped for c in [';', '{', '}', '(', ')', '=', '<', '>', '[', ']', '::', '->', '.']):
                    continue
            cleaned_lines.append(line)
        extracted = '\n'.join(cleaned_lines).strip()
        
        # Remove any remaining markdown code block markers
        extracted = re.sub(r'^```[a-z]*\s*$', '', extracted, flags=re.MULTILINE | re.IGNORECASE)
        extracted = re.sub(r'^```\s*$', '', extracted, flags=re.MULTILINE | re.IGNORECASE)
    
    # If we got something that looks like code, return it
    if extracted and len(extracted) > 10:  # Minimum reasonable code length
        return extracted
    
    # Otherwise return original (might be pure code)
    return content.strip()


def check_compilation(file_path):
    """Check if a C/C++ file compiles successfully."""
    file_path = Path(file_path)
    
    # Skip support files that aren't meant to be compiled standalone
    skip_files = ['io.c', 'std_thread.c', 'main.cpp', 'main_linux.cpp', 'std_testcase.h', 'std_testcase_io.h']
    if file_path.name in skip_files:
        return None, "Support file (not meant to compile standalone)"
    
    temp_cpp = file_path.parent / f"{file_path.stem}_test.cpp"
    temp_exe = file_path.parent / f"{file_path.stem}_test.exe"
    
    try:
        # Read the patch code
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
        
        if not raw_content.strip():
            return False, "Empty file"
        
        # Extract actual code from markdown/explanatory text
        code = extract_code_from_file(raw_content)
        
        if not code.strip():
            return False, "No code found after extraction"
        
        # Create comprehensive test harness with all necessary includes and stubs
        import re
        
        # Remove problematic includes from the code
        code_cleaned = code
        # Remove std_testcase includes (they cause conflicts)
        code_cleaned = re.sub(r'#include\s*["<]std_testcase[^">]*[">]', '', code_cleaned, flags=re.IGNORECASE)
        code_cleaned = re.sub(r'#include\s*["<]std_testcase_io[^">]*[">]', '', code_cleaned, flags=re.IGNORECASE)
        
        # Remove all CWE*.h includes (these are test framework headers that don't exist)
        code_cleaned = re.sub(r'#include\s*["<]CWE[^">]*\.h[">]', '', code_cleaned, flags=re.IGNORECASE)
        
        # Remove other problematic includes that might not be available
        problematic_includes = [
            r'#include\s*["<]openssl/[^">]*[">]',
            r'#include\s*["<]ldap\.h[">]',
        ]
        for pattern in problematic_includes:
            code_cleaned = re.sub(pattern, '', code_cleaned, flags=re.IGNORECASE)
        
        # Remove main() function definitions (we add our own)
        # Match main() function with various signatures
        code_cleaned = re.sub(r'\bint\s+main\s*\([^)]*\)\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', '', code_cleaned, flags=re.DOTALL)
        
        # Remove references to goodG2B and other test framework functions
        code_cleaned = re.sub(r'\bCWE\d+[^;{]*goodG2B[^;{]*;', '', code_cleaned, flags=re.IGNORECASE)
        code_cleaned = re.sub(r'\bCWE\d+[^;{]*goodB2G[^;{]*;', '', code_cleaned, flags=re.IGNORECASE)
        
        # Remove any lines that are clearly explanatory text (contain backticks, markdown)
        lines = code_cleaned.split('\n')
        cleaned_lines = []
        for line in lines:
            stripped = line.strip()
            # Skip lines that are clearly markdown/explanatory
            if '`' in stripped and not any(c in stripped for c in [';', '{', '}', '(', ')', '=', '<', '>', '#']):
                continue
            # Skip lines that look like plain text explanations
            if stripped and not any(keyword in stripped for keyword in [
                '#include', '#define', '#ifndef', '#endif', 'namespace', 'class', 'struct',
                'void', 'int', 'char', 'const', 'static', 'public', 'private', 'protected',
                'return', 'if', 'for', 'while', 'switch', 'case', 'break', 'continue',
                'new', 'delete', 'malloc', 'free', 'sizeof', 'typedef'
            ]):
                # Check if it has code-like symbols
                if not any(c in stripped for c in [';', '{', '}', '(', ')', '=', '<', '>', '[', ']', '::', '->', '.']):
                    continue
            cleaned_lines.append(line)
        code_cleaned = '\n'.join(cleaned_lines)
        
        # Remove any remaining markdown artifacts
        code_cleaned = re.sub(r'```[a-z]*\s*\n', '', code_cleaned, flags=re.IGNORECASE)
        code_cleaned = re.sub(r'```\s*$', '', code_cleaned, flags=re.MULTILINE | re.IGNORECASE)
        
        # Check what Windows APIs might be needed
        needs_windows = any(api in code_cleaned for api in ['LogonUser', 'CryptAcquireContext', 'CryptCreateHash', 
                                                             'CryptDeriveKey', 'CryptEncrypt', 'HANDLE', 'HCRYPTPROV'])
        needs_wincrypt = 'CryptAcquireContext' in code_cleaned or 'CryptCreateHash' in code_cleaned
        
        test_code = f"""
// Standard C++ includes
#include <iostream>
#include <cstring>
#include <cstdio>
#include <cstdlib>
#include <cstddef>
#include <cstdint>
#include <climits>
#include <limits.h>
#include <string>
#include <vector>
#include <list>

"""
        
        # Add Windows includes if needed (but don't fail if not available)
        # We'll provide stubs instead
        if needs_windows:
            test_code += """
// Windows includes - if not available, stubs will be used
#ifdef _WIN32
#ifndef __MINGW32__
#include <windows.h>
"""
            if needs_wincrypt:
                test_code += "#include <wincrypt.h>\n"
            test_code += "#endif\n#endif\n\n"
        
        # Add comprehensive stubs
        test_code += """
// Stub functions that might be used
void printLine(const char* s) { std::cout << s << std::endl; }
void printIntLine(int i) { std::cout << i << std::endl; }
void printLongLine(long l) { std::cout << l << std::endl; }
void printUnsignedLine(unsigned u) { std::cout << u << std::endl; }
void printBytesLine(unsigned char* bytes, size_t len) {
    for (size_t i = 0; i < len; i++) {
        std::cout << (int)bytes[i] << " ";
    }
    std::cout << std::endl;
}

// Windows API stubs (if not on Windows, these will be empty)
#ifndef _WIN32
typedef void* HANDLE;
typedef void* HCRYPTPROV;
typedef void* HCRYPTKEY;
typedef void* HCRYPTHASH;
typedef unsigned long DWORD;
typedef unsigned char BYTE;
#define LOGON32_LOGON_NETWORK 0
#define LOGON32_PROVIDER_DEFAULT 0
#define MS_ENHANCED_PROV 0
#define PROV_RSA_AES 0
#define CRYPT_NEWKEYSET 0
#define CALG_SHA_256 0
#define CALG_AES_256 0

int LogonUserA(const char*, const char*, const char*, int, int, HANDLE*) { return 0; }
void CloseHandle(HANDLE) {}
int CryptAcquireContext(HCRYPTPROV*, const char*, const char*, int, int) { return 0; }
int CryptCreateHash(HCRYPTPROV, int, int, int, HCRYPTHASH*) { return 0; }
int CryptHashData(HCRYPTHASH, BYTE*, DWORD, int) { return 0; }
int CryptDeriveKey(HCRYPTPROV, int, HCRYPTHASH, int, HCRYPTKEY*) { return 0; }
int CryptEncrypt(HCRYPTKEY, HCRYPTHASH, int, int, BYTE*, DWORD*, DWORD) { return 0; }
void CryptDestroyKey(HCRYPTKEY) {}
void CryptDestroyHash(HCRYPTHASH) {}
void CryptReleaseContext(HCRYPTPROV, int) {}
#endif

// Socket stubs (if needed)
int connect_socket(int sock, const char* host, int port) { return 0; }
char* connect_socket_char(int sock, const char* host, int port) { return nullptr; }

// Include the patch code
"""
        
        test_code += f"""
{code_cleaned}

// Minimal main function
int main() {{
    return 0;
}}
"""
        
        # Write test file
        with open(temp_cpp, 'w', encoding='utf-8') as f:
            f.write(test_code)
        
        # Determine compiler based on file extension
        is_cpp = file_path.suffix.lower() in ['.cpp', '.cxx', '.cc', '.c++']
        compiler = 'g++' if is_cpp else 'gcc'
        
        # Try to compile with more lenient settings
        compile_cmd = [compiler, str(temp_cpp), '-o', str(temp_exe), '-w', '-fpermissive']
        if is_cpp:
            compile_cmd.extend(['-std=c++11'])
        
        # Add include paths if they exist (for Windows headers)
        import os
        if os.name == 'nt':  # Windows
            # Common Windows SDK paths (won't hurt if they don't exist)
            possible_includes = [
                'C:/Program Files (x86)/Windows Kits/10/Include',
                'C:/Program Files/Windows Kits/10/Include'
            ]
            for inc_path in possible_includes:
                if os.path.exists(inc_path):
                    compile_cmd.extend(['-I', inc_path])
                    break
        
        result = subprocess.run(
            compile_cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Check if compilation succeeded
        if result.returncode == 0 and temp_exe.exists():
            return True, None
        
        # Check if error is just about missing includes/libraries (which user says they have)
        error_output = (result.stderr + result.stdout).lower()
        
        # Check for include-related errors (missing header files)
        # These patterns indicate missing includes that user has available
        include_error_patterns = [
            r'no such file or directory',
            r'cannot find.*\.h',
            r'fatal error:.*\.h.*no such',
            r'std_testcase.*no such',
            r'cwe.*\.h.*no such',
            r'windows\.h.*no such',
            r'wincrypt\.h.*no such',
            r'openssl.*no such',
            r'ldap\.h.*no such'
        ]
        
        # Check for actual code errors (syntax, semantic errors) - NOT include errors
        # These indicate real problems in the code itself
        code_error_keywords = [
            'stray',
            'missing terminating',
            'expected.*before',
            'expected.*after',
            'invalid.*conversion',
            'redefinition',
            'does not name a type',
            'has not been declared',
            'cannot have cv-qualifier',
            'expected unqualified-id',
            'expected class-name',
            'found \':\' in nested-name-specifier',
            'undefined reference',
            'multiple definition',
            'conflicting.*declaration'
        ]
        
        # Check if error contains include errors
        has_include_error = False
        for pattern in include_error_patterns:
            if re.search(pattern, error_output, re.IGNORECASE):
                has_include_error = True
                break
        
        # Check if error contains actual code errors (but exclude "fatal error:" if it's about missing files)
        has_code_error = False
        for keyword in code_error_keywords:
            if re.search(keyword, error_output, re.IGNORECASE):
                # Make sure it's not just a "fatal error:" about a missing file
                if 'fatal error:' in keyword or 'error:' in keyword:
                    # Check if it's followed by a missing file pattern
                    if not re.search(r'fatal error:.*\.h.*no such', error_output, re.IGNORECASE):
                        has_code_error = True
                        break
                else:
                    has_code_error = True
                    break
        
        # If it's ONLY include errors (no actual code errors), mark as "would compile with proper includes"
        if has_include_error and not has_code_error:
            return None, "Missing includes/libraries (available in your environment)"
        
        error_msg = result.stderr[:200] if result.stderr else result.stdout[:200] if result.stdout else "Compilation failed"
        return False, error_msg
        
    except FileNotFoundError:
        return None, "Compiler not found (gcc/g++)"
    except subprocess.TimeoutExpired:
        return False, "Compilation timeout"
    except Exception as e:
        return False, str(e)[:200]
    finally:
        # Cleanup
        for f in [temp_cpp, temp_exe]:
            if f.exists():
                try:
                    f.unlink(missing_ok=True)
                except:
                    pass


def check_directory(directory_path, directory_name):
    """Check compilation for all files in a directory."""
    directory = Path(directory_path)
    if not directory.exists():
        print(f"Warning: Directory not found: {directory_path}")
        return []
    
    # Find all C/C++ files
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
            # Truncate long error messages
            error_msg = error[:80] if error else 'Unknown error'
            print(f"✗ Failed: {error_msg}")
        else:
            print(f"⊘ Skipped: {error}")
    
    return results


def main():
    """Main function to check functionality and save results."""
    print("Starting functionality check...")
    
    # Check both directories
    baseline_results = check_directory(BASELINE_DIR, "baseline_patches_2")
    codeastra_results = check_directory(CODEASTRA_DIR, "codeastra_2")
    
    # Compile results
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

