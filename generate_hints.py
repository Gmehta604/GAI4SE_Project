"""
generate_hints.py

Generates security hints for vulnerable code snippets using GPT-4.
"""

import os
import json
from pathlib import Path
from openai import OpenAI


def generate_security_hint(code_snippet, api_key=None, model="gpt-4"):
    """
    Generate a security hint for a vulnerable code snippet using GPT-4.
    
    Args:
        code_snippet: The vulnerable code to analyze
        api_key: OpenAI API key (or set OPENAI_API_KEY env var)
        model: Model to use (default: gpt-4)
        
    Returns:
        str: Security hint describing the vulnerability and fix guidance
    """
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable.")
    
    client = OpenAI(api_key=api_key)
    
    prompt = f"""Analyze the following C/C++ code snippet and provide a security hint that:
1. Identifies the type of vulnerability
2. Explains why it's vulnerable
3. Provides guidance on how to fix it (without giving the complete solution)

Code snippet:
```c
{code_snippet}
```

Provide a concise security hint:"""
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a security expert specializing in C/C++ code vulnerabilities."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        
        hint = response.choices[0].message.content.strip()
        return hint
    except Exception as e:
        print(f"Error generating hint: {e}")
        return None


def process_vulnerable_snippets(input_dir, output_file="benchmark/security_hints.json", api_key=None):
    """
    Process all vulnerable snippets and generate security hints.
    
    Args:
        input_dir: Directory containing vulnerable code snippets
        output_file: JSON file to save hints (maps file path -> hint)
        api_key: OpenAI API key
    """
    input_path = Path(input_dir)
    output_path = Path(output_file)
    
    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Find all C/C++ files
    c_files = list(input_path.rglob('*.c')) + list(input_path.rglob('*.cpp')) + \
              list(input_path.rglob('*.cc')) + list(input_path.rglob('*.cxx'))
    
    hints = {}
    processed = 0
    failed = 0
    
    print(f"Processing {len(c_files)} files...")
    
    for file_path in c_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            print(f"Generating hint for: {file_path.name}...")
            hint = generate_security_hint(code, api_key)
            
            if hint:
                # Store relative path as key
                relative_path = str(file_path.relative_to(input_path))
                hints[relative_path] = hint
                processed += 1
                print(f"  ✓ Generated hint")
            else:
                failed += 1
                print(f"  ✗ Failed to generate hint")
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            failed += 1
    
    # Save hints to JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(hints, f, indent=2)
    
    print(f"\nHint generation complete!")
    print(f"Processed: {processed} files")
    print(f"Failed: {failed} files")
    print(f"Hints saved to: {output_path}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate security hints for vulnerable code snippets")
    parser.add_argument("--input", default="benchmark/vulnerable_snippets",
                       help="Directory containing vulnerable snippets")
    parser.add_argument("--output", default="benchmark/security_hints.json",
                       help="Output JSON file for hints")
    parser.add_argument("--api-key", default=None,
                       help="OpenAI API key (or set OPENAI_API_KEY env var)")
    parser.add_argument("--model", default="gpt-4",
                       help="OpenAI model to use")
    
    args = parser.parse_args()
    
    print("Starting security hint generation...")
    print(f"Input directory: {args.input}")
    print(f"Output file: {args.output}")
    print("-" * 60)
    
    process_vulnerable_snippets(args.input, args.output, args.api_key)

