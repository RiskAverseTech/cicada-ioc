# results/

One file per lane or measurement, named by the section that reports it; each README section names its files. Three log files (`diff_score.log`, `hypotheses/run1_failed.log`, `hypotheses/run2_crashed.log`) carry absolute paths from the machine the runs were made on; they are historical artefacts and contain nothing sensitive.

Added 2026-11-25 (housekeeping): `ledger_snapshots.json` and its rendering `ledger_snapshots.md` pin what this record read of other labs and when (`src/ledger_watch.py`); `interchange_rows.json` is the lane list in another ledger's row format (`src/export_interchange.py`); `section_dates.json` is the first commit date of each README section.
