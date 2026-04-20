#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    if not rows:
        raise ValueError(f"No rows found in {path}")
    return rows


def _ema(values: np.ndarray, alpha: float) -> np.ndarray:
    out = np.empty_like(values)
    out[0] = values[0]
    for i in range(1, len(values)):
        out[i] = alpha * values[i] + (1.0 - alpha) * out[i - 1]
    return out


def _finite(v: Any) -> bool:
    if not isinstance(v, (int, float)):
        return False
    return not (isinstance(v, float) and math.isnan(v))


def main() -> None:
    parser = argparse.ArgumentParser(description="Build clean presentation charts from run metrics JSONL.")
    parser.add_argument(
        "--metrics-jsonl",
        default="milestones_preview/charts/run_555m/train_metrics_555m.jsonl",
        help="Path to train_metrics.jsonl copy",
    )
    parser.add_argument(
        "--out-dir",
        default="milestones_preview/charts/run_555m",
        help="Directory for generated charts",
    )
    parser.add_argument("--ema-alpha", type=float, default=0.08, help="EMA alpha for train loss smoothing")
    args = parser.parse_args()

    metrics_path = Path(args.metrics_jsonl).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = _load_jsonl(metrics_path)

    # Base axes
    steps = np.array([int(r["step"]) for r in rows], dtype=np.int64)
    samples = np.array([int(r["processed_samples"]) for r in rows], dtype=np.int64)
    samples_m = samples.astype(np.float64) / 1e6

    # Train loss (all rows are finite)
    train_loss = np.array([float(r["train_loss"]) for r in rows], dtype=np.float64)
    train_loss_ema = _ema(train_loss, alpha=float(args.ema_alpha))

    # Finite-only eval rows
    val_idx = [i for i, r in enumerate(rows) if _finite(r.get("val_loss"))]
    val_samples_m = samples_m[val_idx] if val_idx else np.array([], dtype=np.float64)
    val_loss = np.array([float(rows[i]["val_loss"]) for i in val_idx], dtype=np.float64) if val_idx else np.array([])

    # Throughput
    sps = np.array([float(r["samples_per_sec"]) for r in rows], dtype=np.float64)
    sps_ema = _ema(sps, alpha=0.10)

    # Style
    plt.style.use("seaborn-v0_8-whitegrid")

    # 1) Train loss raw + EMA
    fig = plt.figure(figsize=(10, 5.2), dpi=180)
    ax = fig.add_subplot(111)
    ax.plot(samples_m, train_loss, color="#c77dff", alpha=0.28, linewidth=1.0, label="train_loss (raw)")
    ax.plot(samples_m, train_loss_ema, color="#7209b7", linewidth=2.2, label=f"train_loss EMA (alpha={args.ema_alpha:.2f})")
    ax.set_title("Run 555M: Train Loss (Raw vs Smoothed)")
    ax.set_xlabel("Processed Samples (Millions)")
    ax.set_ylabel("Loss")
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(out_dir / "run555_train_loss_raw_vs_ema.png")
    plt.close(fig)

    # 2) Val loss finite-only points
    fig = plt.figure(figsize=(10, 5.2), dpi=180)
    ax = fig.add_subplot(111)
    if len(val_loss) > 0:
        ax.plot(val_samples_m, val_loss, color="#3a0ca3", linewidth=1.8, marker="o", markersize=3.8, label="val_loss (eval steps only)")
    ax.set_title(f"Run 555M: Validation Loss (Finite-Only, n={len(val_loss)})")
    ax.set_xlabel("Processed Samples (Millions)")
    ax.set_ylabel("Val Loss")
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(out_dir / "run555_val_loss_eval_only.png")
    plt.close(fig)

    # 3) Throughput
    fig = plt.figure(figsize=(10, 5.2), dpi=180)
    ax = fig.add_subplot(111)
    ax.plot(samples_m, sps, color="#4cc9f0", alpha=0.25, linewidth=1.0, label="samples_per_sec (raw)")
    ax.plot(samples_m, sps_ema, color="#0077b6", linewidth=2.2, label="samples_per_sec EMA")
    ax.set_title("Run 555M: Throughput Stability")
    ax.set_xlabel("Processed Samples (Millions)")
    ax.set_ylabel("Samples / sec")
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(out_dir / "run555_throughput_raw_vs_ema.png")
    plt.close(fig)

    # 4) Single panel for slide
    fig, axs = plt.subplots(2, 2, figsize=(12, 8), dpi=180)

    axs[0, 0].plot(samples_m, train_loss, color="#c77dff", alpha=0.25, linewidth=0.9)
    axs[0, 0].plot(samples_m, train_loss_ema, color="#7209b7", linewidth=2.0)
    axs[0, 0].set_title("Train Loss")
    axs[0, 0].set_xlabel("Samples (M)")
    axs[0, 0].set_ylabel("Loss")

    if len(val_loss) > 0:
        axs[0, 1].plot(val_samples_m, val_loss, color="#3a0ca3", linewidth=1.7, marker="o", markersize=3)
    axs[0, 1].set_title("Val Loss (Eval-Only)")
    axs[0, 1].set_xlabel("Samples (M)")
    axs[0, 1].set_ylabel("Val Loss")

    axs[1, 0].plot(samples_m, sps, color="#4cc9f0", alpha=0.25, linewidth=0.9)
    axs[1, 0].plot(samples_m, sps_ema, color="#0077b6", linewidth=2.0)
    axs[1, 0].set_title("Samples / Sec")
    axs[1, 0].set_xlabel("Samples (M)")
    axs[1, 0].set_ylabel("sps")

    axs[1, 1].plot(samples_m, steps, color="#f72585", linewidth=1.8)
    axs[1, 1].set_title("Step vs Samples")
    axs[1, 1].set_xlabel("Samples (M)")
    axs[1, 1].set_ylabel("step")

    fig.suptitle(
        "dit_df_joint_v1v2v3_ctx8_2xh100_1521m_resume555m_20260303_045021_run01",
        fontsize=11,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(out_dir / "run555_clean_dashboard.png")
    plt.close(fig)

    summary = {
        "metrics_jsonl": str(metrics_path),
        "rows": int(len(rows)),
        "last_step": int(steps[-1]),
        "last_samples": int(samples[-1]),
        "finite_val_points": int(len(val_loss)),
        "nan_val_rows": int(len(rows) - len(val_loss)),
        "outputs": [
            "run555_train_loss_raw_vs_ema.png",
            "run555_val_loss_eval_only.png",
            "run555_throughput_raw_vs_ema.png",
            "run555_clean_dashboard.png",
        ],
    }
    (out_dir / "run555_chart_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

