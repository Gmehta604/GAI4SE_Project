"""
visualize_results.py

Creates visualizations for functionality and flawfinder results.
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import numpy as np

# Configuration
FLAWFINDER_JSON = "results/vulnerability_scan.json"
FUNCTIONALITY_JSON = "results/functionality_check.json"
OUTPUT_DIR = "results/graphs"

def load_json(file_path):
    """Load JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_output_dir():
    """Create output directory for graphs."""
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

def plot_flawfinder_summary(flawfinder_data):
    """Create summary graphs for flawfinder results."""
    # Handle both old and new format
    summary = flawfinder_data.get('summary') or flawfinder_data.get('scan_summary', {})
    
    # If scan_summary format, aggregate across directories
    if 'scan_summary' in flawfinder_data:
        scan_summary = flawfinder_data['scan_summary']
        total_files = sum(s.get('total_files', 0) for s in scan_summary.values())
        files_with_vulns = sum(s.get('files_with_vulnerabilities', 0) for s in scan_summary.values())
        total_vulns = sum(s.get('total_vulnerabilities', 0) for s in scan_summary.values())
        files_without_vulns = total_files - files_with_vulns
        successful = total_files  # Assume all successful if in scan_summary format
        failed = 0
    else:
        # Old format
        total_files = summary.get('total_files', 0)
        successful = summary.get('successful', 0)
        failed = summary.get('failed', 0)
        files_with_vulns = summary.get('files_with_vulns', 0)
        files_without_vulns = summary.get('files_without_vulns', 0)
        total_vulns = summary.get('total_vulnerabilities', 0)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Graph 1: Files Analysis
    ax1 = axes[0]
    categories = ['Total Files', 'Successful', 'Failed', 'With Vulns', 'Without Vulns']
    values = [
        total_files,
        successful,
        failed,
        files_with_vulns,
        files_without_vulns
    ]
    colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#95a5a6']
    bars = ax1.bar(categories, values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Number of Files', fontsize=12, fontweight='bold')
    ax1.set_title('Flawfinder: Files Analysis', fontsize=14, fontweight='bold', pad=15)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Rotate x-axis labels
    ax1.set_xticks(range(len(categories)))
    ax1.set_xticklabels(categories, rotation=15, ha='right')
    
    # Graph 2: Vulnerability Distribution
    ax2 = axes[1]
    
    # Pie chart for files with/without vulnerabilities
    if files_with_vulns + files_without_vulns > 0:
        sizes = [files_with_vulns, files_without_vulns]
        labels = [f'With Vulnerabilities\n({files_with_vulns})', 
                 f'Without Vulnerabilities\n({files_without_vulns})']
        colors_pie = ['#e74c3c', '#2ecc71']
        explode = (0.05, 0)  # explode the first slice
        
        wedges, texts, autotexts = ax2.pie(sizes, explode=explode, labels=labels, colors=colors_pie,
                                           autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
        ax2.set_title(f'Flawfinder: Vulnerability Distribution\n(Total: {total_vulns} vulnerabilities)', 
                     fontsize=14, fontweight='bold', pad=15)
    else:
        ax2.text(0.5, 0.5, 'No data available', ha='center', va='center', 
                transform=ax2.transAxes, fontsize=12)
        ax2.set_title('Flawfinder: Vulnerability Distribution', fontsize=14, fontweight='bold', pad=15)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/flawfinder_summary.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {OUTPUT_DIR}/flawfinder_summary.png")
    plt.close()

def plot_flawfinder_vulnerability_levels(flawfinder_data):
    """Create graph showing vulnerability levels distribution."""
    results = flawfinder_data.get('results', {})
    
    # Count vulnerabilities by level
    level_counts = {}
    
    # Handle both old format (list) and new format (dict with directory keys)
    if isinstance(results, dict):
        # New format: results is a dict with directory names as keys
        for dir_name, file_results in results.items():
            for file_result in file_results:
                vulnerabilities = file_result.get('vulnerabilities', [])
                for vuln in vulnerabilities:
                    level = str(vuln.get('level', 0))
                    level_counts[level] = level_counts.get(level, 0) + 1
    else:
        # Old format: results is a list
        for result in results:
            hits = result.get('parsed', {}).get('hits', [])
            for hit in hits:
                level = str(hit.get('level', '0'))
                level_counts[level] = level_counts.get(level, 0) + 1
    
    if not level_counts:
        print("  No vulnerability level data available")
        return
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    levels = sorted(level_counts.keys(), key=int)
    counts = [level_counts[level] for level in levels]
    
    # Color gradient from low to high risk
    colors = plt.cm.RdYlGn_r(np.linspace(0.3, 0.9, len(levels)))
    
    bars = ax.bar(levels, counts, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_xlabel('Risk Level', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Vulnerabilities', fontsize=12, fontweight='bold')
    ax.set_title('Flawfinder: Vulnerability Distribution by Risk Level', 
                fontsize=14, fontweight='bold', pad=15)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/flawfinder_vulnerability_levels.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {OUTPUT_DIR}/flawfinder_vulnerability_levels.png")
    plt.close()

def plot_functionality_comparison(functionality_data):
    """Create comparison graphs for functionality results."""
    summary = functionality_data.get('functionality_summary', {})
    
    if not summary:
        print("  No functionality summary data available")
        return
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Graph 1: Compilation Success Comparison
    ax1 = axes[0]
    directories = list(summary.keys())
    compiles_success = [summary[dir_name].get('compiles_successfully', 0) for dir_name in directories]
    compilation_failed = [summary[dir_name].get('compilation_failed', 0) for dir_name in directories]
    skipped = [summary[dir_name].get('skipped', 0) for dir_name in directories]
    
    x = np.arange(len(directories))
    width = 0.25
    
    bars1 = ax1.bar(x - width, compiles_success, width, label='Compiles Successfully', 
                   color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=1.5)
    bars2 = ax1.bar(x, compilation_failed, width, label='Compilation Failed', 
                   color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
    bars3 = ax1.bar(x + width, skipped, width, label='Skipped', 
                   color='#95a5a6', alpha=0.8, edgecolor='black', linewidth=1.5)
    
    ax1.set_ylabel('Number of Files', fontsize=12, fontweight='bold')
    ax1.set_title('Functionality: Compilation Results Comparison', fontsize=14, fontweight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels([d.replace('_', ' ').title() for d in directories], rotation=15, ha='right')
    ax1.legend(loc='upper right', fontsize=10)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Graph 2: Success Rate Comparison
    ax2 = axes[1]
    success_rates = [summary[dir_name].get('success_rate', 0) for dir_name in directories]
    colors = ['#3498db', '#9b59b6']
    
    bars = ax2.bar(range(len(directories)), success_rates, color=colors[:len(directories)], 
                   alpha=0.8, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Success Rate (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Functionality: Compilation Success Rate', fontsize=14, fontweight='bold', pad=15)
    ax2.set_xticks(range(len(directories)))
    ax2.set_xticklabels([d.replace('_', ' ').title() for d in directories], rotation=15, ha='right')
    ax2.set_ylim(0, max(success_rates) * 1.2 if success_rates else 100)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels
    for i, (bar, rate) in enumerate(zip(bars, success_rates)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{rate:.2f}%',
                ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/functionality_comparison.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {OUTPUT_DIR}/functionality_comparison.png")
    plt.close()

def plot_functionality_breakdown(functionality_data):
    """Create detailed breakdown of functionality results."""
    summary = functionality_data.get('functionality_summary', {})
    
    if not summary:
        return
    
    fig, axes = plt.subplots(1, len(summary), figsize=(7*len(summary), 6))
    
    if len(summary) == 1:
        axes = [axes]
    
    for idx, (dir_name, data) in enumerate(summary.items()):
        ax = axes[idx]
        
        total = data.get('total_files', 0)
        compiles = data.get('compiles_successfully', 0)
        failed = data.get('compilation_failed', 0)
        skipped = data.get('skipped', 0)
        
        # Pie chart
        sizes = [compiles, failed, skipped]
        labels = [f'Compiles\n({compiles})', f'Failed\n({failed})', f'Skipped\n({skipped})']
        colors = ['#2ecc71', '#e74c3c', '#95a5a6']
        
        # Remove zero values
        filtered_data = [(s, l, c) for s, l, c in zip(sizes, labels, colors) if s > 0]
        if filtered_data:
            sizes, labels, colors = zip(*filtered_data)
            # Create explode tuple matching the length of filtered sizes
            # Explode the first slice (compiles) if it exists
            explode = tuple(0.05 if i == 0 and sizes[0] > 0 else 0 for i in range(len(sizes)))
            
            wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                            autopct='%1.1f%%', startangle=90,
                                            textprops={'fontsize': 10, 'fontweight': 'bold'})
            ax.set_title(f'{dir_name.replace("_", " ").title()}\n(Total: {total} files)', 
                        fontsize=13, fontweight='bold', pad=15)
        else:
            ax.text(0.5, 0.5, 'No data', ha='center', va='center', 
                   transform=ax.transAxes, fontsize=12)
            ax.set_title(f'{dir_name.replace("_", " ").title()}', 
                        fontsize=13, fontweight='bold', pad=15)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/functionality_breakdown.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {OUTPUT_DIR}/functionality_breakdown.png")
    plt.close()

def plot_combined_summary(flawfinder_data, functionality_data):
    """Create a combined summary visualization."""
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    # 1. Flawfinder Summary (Top Left)
    ax1 = fig.add_subplot(gs[0, 0])
    # Handle both old and new format
    flaw_summary = flawfinder_data.get('summary') or flawfinder_data.get('scan_summary', {})
    
    if 'scan_summary' in flawfinder_data:
        # New format: aggregate across directories
        scan_summary = flawfinder_data['scan_summary']
        total_files = sum(s.get('total_files', 0) for s in scan_summary.values())
        files_with_vulns = sum(s.get('files_with_vulnerabilities', 0) for s in scan_summary.values())
        files_without_vulns = total_files - files_with_vulns
    else:
        # Old format
        total_files = flaw_summary.get('total_files', 0)
        files_with_vulns = flaw_summary.get('files_with_vulns', 0)
        files_without_vulns = flaw_summary.get('files_without_vulns', 0)
    
    categories = ['Total Files', 'With Vulns', 'Without Vulns']
    values = [
        total_files,
        files_with_vulns,
        files_without_vulns
    ]
    colors = ['#3498db', '#e74c3c', '#2ecc71']
    bars = ax1.bar(categories, values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Count', fontsize=11, fontweight='bold')
    ax1.set_title('Flawfinder: Vulnerability Overview', fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # 2. Functionality Comparison (Top Right)
    ax2 = fig.add_subplot(gs[0, 1])
    func_summary = functionality_data.get('functionality_summary', {})
    if func_summary:
        directories = list(func_summary.keys())
        success_rates = [func_summary[d].get('success_rate', 0) for d in directories]
        colors_bar = ['#3498db', '#9b59b6']
        bars = ax2.bar(range(len(directories)), success_rates, 
                      color=colors_bar[:len(directories)], alpha=0.8, 
                      edgecolor='black', linewidth=1.5)
        ax2.set_ylabel('Success Rate (%)', fontsize=11, fontweight='bold')
        ax2.set_title('Functionality: Success Rate Comparison', fontsize=12, fontweight='bold')
        ax2.set_xticks(range(len(directories)))
        ax2.set_xticklabels([d.replace('_', ' ').title() for d in directories], 
                           rotation=15, ha='right')
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        for bar, rate in zip(bars, success_rates):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height, f'{rate:.2f}%',
                    ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # 3. Flawfinder Vulnerability Levels (Bottom Left)
    ax3 = fig.add_subplot(gs[1, 0])
    results = flawfinder_data.get('results', {})
    level_counts = {}
    
    # Handle both old format (list) and new format (dict with directory keys)
    if isinstance(results, dict):
        # New format: results is a dict with directory names as keys
        for dir_name, file_results in results.items():
            for file_result in file_results:
                vulnerabilities = file_result.get('vulnerabilities', [])
                for vuln in vulnerabilities:
                    level = str(vuln.get('level', 0))
                    level_counts[level] = level_counts.get(level, 0) + 1
    else:
        # Old format: results is a list
        for result in results:
            hits = result.get('parsed', {}).get('hits', [])
            for hit in hits:
                level = str(hit.get('level', '0'))
                level_counts[level] = level_counts.get(level, 0) + 1
    
    if level_counts:
        levels = sorted(level_counts.keys(), key=int)
        counts = [level_counts[level] for level in levels]
        colors_grad = plt.cm.RdYlGn_r(np.linspace(0.3, 0.9, len(levels)))
        bars = ax3.bar(levels, counts, color=colors_grad, alpha=0.8, 
                       edgecolor='black', linewidth=1.5)
        ax3.set_xlabel('Risk Level', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Count', fontsize=11, fontweight='bold')
        ax3.set_title('Flawfinder: Vulnerabilities by Risk Level', fontsize=12, fontweight='bold')
        ax3.grid(axis='y', alpha=0.3, linestyle='--')
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax3.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}',
                        ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # 4. Functionality Status (Bottom Right)
    ax4 = fig.add_subplot(gs[1, 1])
    if func_summary:
        directories = list(func_summary.keys())
        compiles = [func_summary[d].get('compiles_successfully', 0) for d in directories]
        failed = [func_summary[d].get('compilation_failed', 0) for d in directories]
        skipped = [func_summary[d].get('skipped', 0) for d in directories]
        
        x = np.arange(len(directories))
        width = 0.25
        bars1 = ax4.bar(x - width, compiles, width, label='Compiles', color='#2ecc71', 
                       alpha=0.8, edgecolor='black', linewidth=1.5)
        bars2 = ax4.bar(x, failed, width, label='Failed', color='#e74c3c', 
                       alpha=0.8, edgecolor='black', linewidth=1.5)
        bars3 = ax4.bar(x + width, skipped, width, label='Skipped', color='#95a5a6', 
                       alpha=0.8, edgecolor='black', linewidth=1.5)
        ax4.set_ylabel('Number of Files', fontsize=11, fontweight='bold')
        ax4.set_title('Functionality: Compilation Status', fontsize=12, fontweight='bold')
        ax4.set_xticks(x)
        ax4.set_xticklabels([d.replace('_', ' ').title() for d in directories], 
                           rotation=15, ha='right')
        ax4.legend(fontsize=9)
        ax4.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.suptitle('Results Summary Dashboard', fontsize=16, fontweight='bold', y=0.98)
    plt.savefig(f'{OUTPUT_DIR}/combined_summary.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {OUTPUT_DIR}/combined_summary.png")
    plt.close()

def main():
    """Main function to generate all visualizations."""
    print("=" * 60)
    print("Generating Visualizations for Results")
    print("=" * 60)
    
    create_output_dir()
    
    # Load data
    print("\nLoading data...")
    try:
        flawfinder_data = load_json(FLAWFINDER_JSON)
        print(f"✓ Loaded flawfinder data from {FLAWFINDER_JSON}")
    except FileNotFoundError:
        print(f"✗ Error: {FLAWFINDER_JSON} not found")
        flawfinder_data = None
    
    try:
        functionality_data = load_json(FUNCTIONALITY_JSON)
        print(f"✓ Loaded functionality data from {FUNCTIONALITY_JSON}")
    except FileNotFoundError:
        print(f"✗ Error: {FUNCTIONALITY_JSON} not found")
        functionality_data = None
    
    # Generate flawfinder visualizations
    if flawfinder_data:
        print("\nGenerating Flawfinder visualizations...")
        plot_flawfinder_summary(flawfinder_data)
        plot_flawfinder_vulnerability_levels(flawfinder_data)
    
    # Generate functionality visualizations
    if functionality_data:
        print("\nGenerating Functionality visualizations...")
        plot_functionality_comparison(functionality_data)
        plot_functionality_breakdown(functionality_data)
    
    # Generate combined summary
    if flawfinder_data and functionality_data:
        print("\nGenerating Combined Summary...")
        plot_combined_summary(flawfinder_data, functionality_data)
    
    print("\n" + "=" * 60)
    print("Visualization Complete!")
    print(f"All graphs saved to: {OUTPUT_DIR}/")
    print("=" * 60)

if __name__ == "__main__":
    main()

