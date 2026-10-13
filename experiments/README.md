# Experiments

One folder per experiment: `experiments/<YYYYMMDD-HHMM>-<slug>/` with:
- `README.md`: question, method, exact command, parameters and seeds, result, conclusion, tags;
- the scripts used (or a pointer to e757/ functions);
- outputs: small ones in the folder; large ones gzipped under data/.

Long runs: `bash scripts/start_job.sh experiments/<id> <max_hours> <command...>`, then
`bash scripts/jobs.sh` to monitor. `run.log` and `job.pid` are git-ignored, so summarize the
results in README.md.

Special folders:
- `experiments/referee/`: the referee's independent checks.
- `experiments/falsify/`: falsifier reports.
