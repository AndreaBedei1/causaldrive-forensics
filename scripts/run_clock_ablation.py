"""Run evaluation-only clock A/B/C comparisons on an independent-clock recording."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from cdf.common.config import Config, load_run_config
from cdf.common.io import read_json
from cdf.common.layout import RunLayout
from cdf.evaluation.clock_ablation import run_clock_ablation


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    layout = RunLayout.from_run_dir(args.run_dir)
    manifest = read_json(layout.manifest)
    cfg = (
        Config(manifest["config"])
        if manifest.get("config")
        else load_run_config(scenario_id=manifest["scenario_id"])
    )
    report = run_clock_ablation(layout.root, cfg)
    for name, row in report["modes"].items():
        print(
            name,
            "association F1=",
            row["association"]["f1"],
            "merged event groups=",
            row["n_merged_groups"],
        )
    print(layout.evaluation_dir / "clock_ablation.json")


if __name__ == "__main__":
    main()
