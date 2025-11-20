"""
scan_vulnerabilities.py

Scans baseline_patches_2_2 and sementic_hinted_patches_2 directories for security vulnerabilities
using flawfinder and saves results to JSON.
"""

import subprocess
from pathlib import Path
import json
from datetime import datetime
import re

# Configuration
BASELINE_DIR = "results/baseline_patches_2"
CODEASTRA_DIR = "results/sementic_hinted_patches_2"
OUTPUT_JSON = "results/vulnerability_scan.json"


def parse_flawfinder_output(output_text):
    """Parse flawfinder output to extract vulnerabilities."""
    vulnerabilities = []
    lines = output_text.split('\n')
    
    # Pattern: "file.cpp:123:  [2] (buffer) strcpy:" or "file.cpp:123:  [2] (buffer) char:"
    # The description comes on the next line(s), indented
    # More flexible pattern that handles various formats
    pattern = r'^([^:]+):(\d+):\s+\[(\d+)\]\s+\(([^)]+)\)\s+([^:\n]+):\s*$'
    
    in_results = False
    i = 0
    
    while i < len(lines):
        line = lines[i]
        line_stripped = line.strip()
        line_rstripped = line.rstrip()  # Preserve leading spaces for indented descriptions
        
        # Check if we're entering the results section
        if 'FINAL RESULTS:' in line_stripped:
            in_results = True
            i += 1
            # Skip empty lines after FINAL RESULTS:
            while i < len(lines) and not lines[i].strip():
                i += 1
            continue
        
        # Stop at analysis summary or if no hits found
        if line_stripped.startswith('ANALYSIS SUMMARY:') or 'No hits found' in line_stripped:
            break
        
        if in_results and line_stripped:
            # Try to match the vulnerability header line
            match = re.match(pattern, line_rstripped)
            if match:
                file_path, line_num, risk_level, category, function = match.groups()
                
                # Collect multi-line description from following indented lines
                description_parts = []
                i += 1
                
                # Read description lines (they are indented with spaces)
                while i < len(lines):
                    next_line = lines[i]
                    next_stripped = next_line.strip()
                    next_rstripped = next_line.rstrip()
                    
                    # Stop if we hit another vulnerability header
                    if re.match(pattern, next_rstripped):
                        break
                    
                    # Stop at summary sections
                    if (next_stripped.startswith('ANALYSIS SUMMARY:') or
                        next_stripped.startswith('FINAL RESULTS:') or
                        next_stripped.startswith('Hits =') or
                        next_stripped.startswith('Lines analyzed') or
                        next_stripped.startswith('Physical Source Lines')):
                        break
                    
                    # Description lines are typically indented (start with spaces/tabs)
                    # or continuation lines
                    if next_stripped:
                        # If it starts with whitespace, it's part of the description
                        if next_line.startswith((' ', '\t')):
                            description_parts.append(next_stripped)
                        # If it doesn't match our pattern and has content, include it
                        elif not re.match(pattern, next_rstripped):
                            description_parts.append(next_stripped)
                    elif description_parts:
                        # Empty line after description - might be separator, but continue
                        # in case there's more description after
                        pass
                    
                    i += 1
                
                description = ' '.join(description_parts).strip()
                
                vulnerabilities.append({
                    'line': int(line_num),
                    'level': int(risk_level),
                    'function': function.strip(),
                    'category': category.strip(),
                    'description': description
                })
                continue
        
        i += 1
    
    return vulnerabilities


def scan_file(file_path):
    """Scan a single file using flawfinder command-line tool."""
    try:
        # Run flawfinder with minimum level 1 to catch all vulnerabilities
        result = subprocess.run(
            ['flawfinder', '--minlevel', '1', str(file_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Combine stdout and stderr for parsing
        output = result.stdout + result.stderr
        
        # Parse output
        vulnerabilities = parse_flawfinder_output(output)
        
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
    codeastra_results = scan_directory(CODEASTRA_DIR, "sementic_hinted_patches_2")
    
    # Compile results
    output_data = {
        'timestamp': datetime.now().isoformat(),
        'scan_summary': {
            'baseline_patches_2': {
                'total_files': len(baseline_results),
                'files_with_vulnerabilities': sum(1 for r in baseline_results if r['vulnerability_count'] > 0),
                'total_vulnerabilities': sum(r['vulnerability_count'] for r in baseline_results)
            },
            'sementic_hinted_patches_2': {
                'total_files': len(codeastra_results),
                'files_with_vulnerabilities': sum(1 for r in codeastra_results if r['vulnerability_count'] > 0),
                'total_vulnerabilities': sum(r['vulnerability_count'] for r in codeastra_results)
            }
        },
        'results': {
            'baseline_patches_2': baseline_results,
            'sementic_hinted_patches_2': codeastra_results
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
    
    print(f"\nsementic_hinted_patches_2:")
    print(f"  Total files: {output_data['scan_summary']['sementic_hinted_patches_2']['total_files']}")
    print(f"  Files with vulnerabilities: {output_data['scan_summary']['sementic_hinted_patches_2']['files_with_vulnerabilities']}")
    print(f"  Total vulnerabilities: {output_data['scan_summary']['sementic_hinted_patches_2']['total_vulnerabilities']}")
    
    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()
