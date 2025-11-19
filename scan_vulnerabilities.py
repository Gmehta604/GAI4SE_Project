"""
scan_vulnerabilities.py

Scans baseline_patches_2 and codeastra_2 directories for security vulnerabilities
using flawfinder and saves results to JSON.
"""

import subprocess
from pathlib import Path
import json
from datetime import datetime
import re

# Configuration
BASELINE_DIR = "results/sementic_hinted_patches_2"
CODEASTRA_DIR = "results/baseline_patches_2"
OUTPUT_JSON = "results/vulnerability_scan.json"


def parse_flawfinder_output(output_text):
    """Parse flawfinder output to extract vulnerabilities."""
    vulnerabilities = []
    lines = output_text.split('\n')
    
    # Pattern: "file.cpp:123:  [2] (buffer) strcpy: description"
    pattern = r'^([^:]+):(\d+):\s+\[(\d+)\]\s+\(([^)]+)\)\s+([^:]+):\s*(.*)$'
    
    in_results = False
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('FINAL RESULTS:'):
            in_results = True
            i += 1
            continue
        
        if line.startswith('ANALYSIS SUMMARY:') or 'No hits found' in line:
            break
        
        if in_results:
            match = re.match(pattern, line)
            if match:
                file_path, line_num, risk_level, category, function, description_start = match.groups()
                
                # Collect multi-line description
                description = description_start
                i += 1
                while i < len(lines):
                    next_line = lines[i].strip()
                    if (re.match(pattern, next_line) or 
                        next_line.startswith('ANALYSIS SUMMARY:') or
                        next_line.startswith('FINAL RESULTS:')):
                        break
                    if next_line and not next_line.startswith('[') and not next_line.startswith('Hits'):
                        description += " " + next_line
                    i += 1
                
                vulnerabilities.append({
                    'line': int(line_num),
                    'level': int(risk_level),
                    'function': function,
                    'category': category,
                    'description': description.strip()
                })
                continue
        
        i += 1
    
    return vulnerabilities


def scan_file(file_path):
    """Scan a single file using flawfinder command-line tool."""
    try:
        result = subprocess.run(
            ['flawfinder', '--minlevel', '1', str(file_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Parse output
        vulnerabilities = parse_flawfinder_output(result.stdout + result.stderr)
        
        return vulnerabilities, None
        
    except FileNotFoundError:
        return [], "flawfinder not found"
    except subprocess.TimeoutExpired:
        return [], "timeout"
    except Exception as e:
        return [], str(e)


def scan_directory(directory_path, directory_name):
    """Scan a directory for vulnerabilities."""
    directory = Path(directory_path)
    if not directory.exists():
        print(f"Warning: Directory not found: {directory_path}")
        return []
    
    # Find all C/C++ files
    c_files = list(directory.rglob('*.c')) + list(directory.rglob('*.cpp')) + \
              list(directory.rglob('*.cc')) + list(directory.rglob('*.cxx'))
    
    results = []
    
    print(f"\nScanning {directory_name} ({len(c_files)} files)...")
    
    for i, file_path in enumerate(c_files, 1):
        print(f"  [{i}/{len(c_files)}] {file_path.name}...", end=" ", flush=True)
        
        vulnerabilities, error = scan_file(file_path)
        
        result = {
            'file': str(file_path.relative_to(directory)),
            'full_path': str(file_path),
            'vulnerability_count': len(vulnerabilities),
            'vulnerabilities': vulnerabilities
        }
        
        if error:
            result['error'] = error
        
        results.append(result)
        
        if len(vulnerabilities) > 0:
            print(f"✓ Found {len(vulnerabilities)} vulnerability(ies)")
        else:
            print("✓ No vulnerabilities")
    
    return results


def main():
    """Main function to scan directories and save results."""
    print("Starting vulnerability scan...")
    
    # Scan both directories
    baseline_results = scan_directory(BASELINE_DIR, "baseline_patches_2")
    codeastra_results = scan_directory(CODEASTRA_DIR, "codeastra_2")
    
    # Compile results
    output_data = {
        'timestamp': datetime.now().isoformat(),
        'scan_summary': {
            'baseline_patches_2': {
                'total_files': len(baseline_results),
                'files_with_vulnerabilities': sum(1 for r in baseline_results if r['vulnerability_count'] > 0),
                'total_vulnerabilities': sum(r['vulnerability_count'] for r in baseline_results)
            },
            'codeastra_2': {
                'total_files': len(codeastra_results),
                'files_with_vulnerabilities': sum(1 for r in codeastra_results if r['vulnerability_count'] > 0),
                'total_vulnerabilities': sum(r['vulnerability_count'] for r in codeastra_results)
            }
        },
        'results': {
            'baseline_patches_2': baseline_results,
            'codeastra_2': codeastra_results
        }
    }
    
    # Save to JSON
    output_path = Path(OUTPUT_JSON)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("\n" + "=" * 60)
    print("SCAN SUMMARY")
    print("=" * 60)
    print(f"\nbaseline_patches_2:")
    print(f"  Total files: {output_data['scan_summary']['baseline_patches_2']['total_files']}")
    print(f"  Files with vulnerabilities: {output_data['scan_summary']['baseline_patches_2']['files_with_vulnerabilities']}")
    print(f"  Total vulnerabilities: {output_data['scan_summary']['baseline_patches_2']['total_vulnerabilities']}")
    
    print(f"\ncodeastra_2:")
    print(f"  Total files: {output_data['scan_summary']['codeastra_2']['total_files']}")
    print(f"  Files with vulnerabilities: {output_data['scan_summary']['codeastra_2']['files_with_vulnerabilities']}")
    print(f"  Total vulnerabilities: {output_data['scan_summary']['codeastra_2']['total_vulnerabilities']}")
    
    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()
