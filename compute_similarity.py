"""
compute_similarity.py

Computes CodeBERT-based similarity scores between ground-truth Juliet fixes and
two sets of generated patches (baseline_patches_2 and codeastra_2).

Outputs a JSON report with per-file cosine similarities and summary statistics.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import torch
from packaging import version
from transformers import AutoModel, AutoTokenizer


# ---------------------------------------------------------------------------
# Configuration (edit these paths if needed)
# ---------------------------------------------------------------------------
GROUND_TRUTH_DIR = "benchmark/ground_truth"
BASELINE_DIR = "results/baseline_patches_2"
CODEASTRA_DIR = "results/codeastra_2"
OUTPUT_JSON = "results/codebert_similarity.json"
MODEL_NAME = "microsoft/codebert-base"
MAX_LENGTH = 512  # CodeBERT token limit
MIN_TORCH_VERSION = "2.6.0"


# ---------------------------------------------------------------------------
# Helper dataclasses
# ---------------------------------------------------------------------------
@dataclass
class SimilarityResult:
    file: str
    ground_truth_file: Optional[str]
    similarity: Optional[float]
    status: str
    notes: Optional[str] = None


# ---------------------------------------------------------------------------
# Text / Code utilities
# ---------------------------------------------------------------------------
def extract_code_from_patch(content: str) -> str:
    """
    Extract C/C++ code from a patch file that might include markdown fences.
    Falls back to the raw content if no fenced block is found.
    """
    if not content:
        return ""

    fence_pattern = re.compile(r"```(?:c|cpp|c\+\+)?\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)
    matches = fence_pattern.findall(content)
    if matches:
        # Take the longest fenced block (usually the actual code)
        return max(matches, key=len).strip()

    # Remove stray markdown artifacts/backticks
    cleaned_lines = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("```") or stripped == "`":
            continue
        if "`" in stripped and not any(sym in stripped for sym in (";", "{", "}", "(", ")", "#", "=")):
            continue
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()


def read_code(path: Path, is_patch: bool) -> Optional[str]:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        print(f"[WARN] Failed to read {path}: {exc}")
        return None

    return extract_code_from_patch(text) if is_patch else text.strip()


def find_ground_truth_file(patch_file: Path, ground_truth_dir: Path) -> Optional[Path]:
    """
    Map a *_bad.cpp patch to the corresponding *_good?.cpp ground-truth file.
    """
    stem = patch_file.stem  # e.g., CWE121_..._bad
    base = re.sub(r"_bad$", "", stem)
    if base == stem:
        return None

    patterns = [
        f"{base}_good*.cpp",
        f"{base}_good*.c",
    ]

    for pattern in patterns:
        matches = list(ground_truth_dir.glob(pattern))
        if matches:
            return matches[0]

    # Fallback: some files use suffixes like good1/goodB2G1
    loose_pattern = f"{base}_good*.cpp*"
    matches = list(ground_truth_dir.glob(loose_pattern))
    return matches[0] if matches else None


# ---------------------------------------------------------------------------
# Environment / version guards
# ---------------------------------------------------------------------------
def ensure_supported_torch_version() -> None:
    """
    Hugging Face now hard-requires torch>=2.6 when model weights are stored
    in .bin format (see CVE-2025-32434). Provide a clear message if the local
    environment is outdated so the user can upgrade before we attempt to load
    CodeBERT.
    """
    current = version.parse(torch.__version__)
    required = version.parse(MIN_TORCH_VERSION)
    if current < required:
        raise RuntimeError(
            f"PyTorch {MIN_TORCH_VERSION}+ is required but found {torch.__version__}. "
            "Please upgrade your environment, e.g.:\n"
            f"  pip install --upgrade 'torch>={MIN_TORCH_VERSION}'\n"
            "and rerun the script."
        )


# ---------------------------------------------------------------------------
# CodeBERT embedding utilities
# ---------------------------------------------------------------------------
class CodeBERTEncoder:
    def __init__(self, model_name: str = MODEL_NAME, max_length: int = MAX_LENGTH):
        ensure_supported_torch_version()
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()
        self.max_length = max_length

    @torch.no_grad()
    def encode(self, code: str) -> Optional[torch.Tensor]:
        if not code:
            return None

        inputs = self.tokenizer(
            code,
            return_tensors="pt",
            truncation=True,
            max_length=self.max_length,
        )
        outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state
        mask = inputs.attention_mask.unsqueeze(-1)
        summed = (embeddings * mask).sum(dim=1)
        counts = mask.sum(dim=1).clamp(min=1)
        mean_pooled = summed / counts
        return mean_pooled.squeeze(0)


def cosine_similarity(vec1: torch.Tensor, vec2: torch.Tensor) -> float:
    vec1_norm = torch.nn.functional.normalize(vec1, dim=0)
    vec2_norm = torch.nn.functional.normalize(vec2, dim=0)
    return torch.dot(vec1_norm, vec2_norm).item()


# ---------------------------------------------------------------------------
# Core processing logic
# ---------------------------------------------------------------------------
def process_directory(
    label: str,
    patches_dir: Path,
    ground_truth_dir: Path,
    encoder: CodeBERTEncoder,
) -> Dict[str, Iterable]:
    results: List[SimilarityResult] = []

    patch_files = sorted(
        list(patches_dir.glob("*.cpp")) + list(patches_dir.glob("*.c"))
    )

    for patch_file in patch_files:
        gt_file = find_ground_truth_file(patch_file, ground_truth_dir)
        if not gt_file or not gt_file.exists():
            results.append(
                SimilarityResult(
                    file=patch_file.name,
                    ground_truth_file=None,
                    similarity=None,
                    status="missing_ground_truth",
                    notes="No matching ground truth file found",
                )
            )
            continue

        gt_code = read_code(gt_file, is_patch=False)
        patch_code = read_code(patch_file, is_patch=True)

        if not gt_code:
            results.append(
                SimilarityResult(
                    file=patch_file.name,
                    ground_truth_file=str(gt_file),
                    similarity=None,
                    status="empty_ground_truth",
                )
            )
            continue

        if not patch_code:
            results.append(
                SimilarityResult(
                    file=patch_file.name,
                    ground_truth_file=str(gt_file),
                    similarity=None,
                    status="empty_patch",
                )
            )
            continue

        gt_vec = encoder.encode(gt_code)
        patch_vec = encoder.encode(patch_code)

        if gt_vec is None or patch_vec is None:
            results.append(
                SimilarityResult(
                    file=patch_file.name,
                    ground_truth_file=str(gt_file),
                    similarity=None,
                    status="embedding_failed",
                    notes="Model returned empty embedding",
                )
            )
            continue

        sim = cosine_similarity(gt_vec, patch_vec)

        # Map cosine (-1..1) to 0..1 for readability
        normalized_sim = (sim + 1) / 2

        results.append(
            SimilarityResult(
                file=patch_file.name,
                ground_truth_file=str(gt_file),
                similarity=round(normalized_sim, 4),
                status="ok",
            )
        )

    similarities = [r.similarity for r in results if r.similarity is not None]
    summary = {
        "total_files": len(results),
        "matched_files": sum(1 for r in results if r.status == "ok"),
        "missing_ground_truth": sum(1 for r in results if r.status == "missing_ground_truth"),
        "empty_ground_truth": sum(1 for r in results if r.status == "empty_ground_truth"),
        "empty_patch": sum(1 for r in results if r.status == "empty_patch"),
        "embedding_failed": sum(1 for r in results if r.status == "embedding_failed"),
        "average_similarity": round(sum(similarities) / len(similarities), 4) if similarities else None,
        "min_similarity": min(similarities) if similarities else None,
        "max_similarity": max(similarities) if similarities else None,
    }

    return {
        "label": label,
        "summary": summary,
        "results": [r.__dict__ for r in results],
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    ground_truth_path = Path(GROUND_TRUTH_DIR)
    baseline_path = Path(BASELINE_DIR)
    codeastra_path = Path(CODEASTRA_DIR)

    for path, name in [
        (ground_truth_path, "ground truth"),
        (baseline_path, "baseline patches"),
        (codeastra_path, "codeastra patches"),
    ]:
        if not path.exists():
            raise FileNotFoundError(f"{name} directory not found: {path}")

    print("Loading CodeBERT model (this may take a moment)...")
    encoder = CodeBERTEncoder()
    print("Model loaded.\n")

    baseline_report = process_directory(
        "baseline_patches_2", baseline_path, ground_truth_path, encoder
    )
    codeastra_report = process_directory(
        "codeastra_2", codeastra_path, ground_truth_path, encoder
    )

    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "model": MODEL_NAME,
        "ground_truth_dir": str(ground_truth_path),
        "baseline_dir": str(baseline_path),
        "codeastra_dir": str(codeastra_path),
        "summary": {
            "baseline_patches_2": baseline_report["summary"],
            "codeastra_2": codeastra_report["summary"],
        },
        "results": {
            "baseline_patches_2": baseline_report["results"],
            "codeastra_2": codeastra_report["results"],
        },
    }

    output_path = Path(OUTPUT_JSON)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("Similarity computation complete.")
    print(f"Baseline avg similarity: {baseline_report['summary']['average_similarity']}")
    print(f"Codeastra avg similarity: {codeastra_report['summary']['average_similarity']}")
    print(f"Report saved to {output_path}")


if __name__ == "__main__":
    main()

