@echo off
rem Manual review menu of the 23 canonical runs. Run from an activated environment: conda activate carla
cd /d "%~dp0.."
python scripts\review_canonical_runs.py %*
