# Primary-source files (copied 2026-10-13)

| File | Origin | License / note |
|---|---|---|
| `ma_tang_verify_base_block.py`, `ma_tang_verify_README.md` | github.com/QuanyuTang/ep757-45set-base-block-verification | Authors' verification code for $A_{\rm base}$ (Ma–Tang Lemma 5.1); run with `python3 kb/literature/sources/ma_tang_verify_base_block.py` |
| `formal_conjectures_757.lean` | google-deepmind/formal-conjectures, `FormalConjectures/ErdosProblems/757.lean` | Apache-2.0. States the problem; its "solved" variants still use the 1995 bounds (1/2, 3/5) |
| `tao_constants_5b.md` | github.com/teorth/optimizationproblems, `constants/5b.md` | Tao's constants database entry "C_5b"; lists exactly 9/17 and 4/7 as of 2026-09-26 |
| `aday_757_reader_5_9/` (`README.md`, `day_757_reader_five_ninths_refereed.txt`, `problem_757.txt`, `submission_7bkzb8.md`) | Erdős Problem a Day (erdosproblemaday.com) pages on an anonymous reader's self-similar construction claiming c* <= 5/9 for #757 (submission 7bkzb8 of 17 Oct 2026; write-up of 19 Oct 2026), fetched 2026-10-20 (17:24Z and 20:20Z) through the agent proxy and converted to plain text | UNTRUSTED third-party text, [community]; never executed. The site marks the claim 'unreviewed by humans' and the submitter declares that AI tools found and refereed it; the construction is NOT this project's (verified here, not discovered here). Exact verification and proof here: K59, K60 (kb/known_results.md), `experiments/20261020-1730-reader-5-9/`, `results/proofs/L015-reader-family-c-le-5-9.md` |

The paper PDFs are not included (no network access from the build sandbox). Run
`bash scripts/fetch_papers.sh` in a session with network access, or ask the `scout` to fetch them.
The digests in kb/notes/ capture what matters from each paper.
