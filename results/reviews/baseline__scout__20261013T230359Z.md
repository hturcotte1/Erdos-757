NOVELTY: CLEAR

# Baseline novelty scan for the bounds 9/17 <= c* <= 4/7 (Erdos #757)

Scan date: 2026-10-13 (UTC). Result: no source found that changes the bounds. The latest state
is still Ma-Tang arXiv:2602.23282v2 (6 Mar 2026): 9/17 <= c* <= 4/7. The review-README's allowed first lines
are CLEAR/PRIOR-WORK/UNSURE; CLEAR is used here to mean "bounds unchanged" (CHANGED does not apply).

## Sources checked
| Source | URL | What it showed (date) |
|---|---|---|
| erdosproblems.com/757 | https://www.erdosproblems.com/757 | Lists Erdos-Sos c>=1/2; Gyarfas-Lehel 1/2+1/(141*76) <= c <= 3/5; Ma-Tang 9/17 <= c <= 4/7. Last edited 10 Apr 2026. 7 comments. No proof claims. |
| page history | https://www.erdosproblems.com/history/757 | Only edits: 2026-04-10 fix of the GL lower bound typo and statement clean-up; Ma-Tang bounds unchanged. |
| forum thread | https://www.erdosproblems.com/forum/thread/757 | 7 comments, latest 27 Feb 2026 (Tang announces arXiv paper; Tao: constant 5b added to database; Sothanaphan checks). Nothing after March 2026. |
| arXiv abs page | https://arxiv.org/abs/2602.23282 | Only v1 (26 Feb 2026) and v2 (6 Mar 2026). No v3 as of 2026-10-13 (arXiv API shows updated 2026-03-06). |
| arXiv API searches (math.CO/NT) | https://export.arxiv.org/api/query | Queries: Sidon + "distinct differences"; "weak Sidon"; "(4,5)-set"; Erdos problem + Sidon; Sidon subset + arithmetic progressions; Gyarfas-Lehel + Sidon; Henning-Yeo + transversal. Only hit on topic: 2602.23282. Unrelated 2026 hits read and rejected: 2605.03274 (Lean Singer constructions), 2604.12623 (rainbow Cameron-Erdos), 2608.02667 (Sidon subsets of multinomial coefficient values), 2609.12546 (Kneser graph Smith group). Henning-Yeo arXiv hits are older (2013-2018). |
| Semantic Scholar citations | https://api.semanticscholar.org/graph/v1/paper/DOI:10.1006/jctb.1995.1028/citations | Citing Gyarfas-Lehel 1995: only Ma-Tang 2026 (plus unrelated older Sidon papers). |
| Semantic Scholar citations of Henning-Yeo 2021 | https://api.semanticscholar.org/graph/v1/paper/DOI:10.1007/s00373-021-02285-x/citations | Citing: Ma-Tang 2026 and a 2022 J. Oper. Res. China paper on transversals of connected k-uniform hypergraphs. |
| Semantic Scholar citations of Ma-Tang | https://api.semanticscholar.org/graph/v1/paper/arXiv:2602.23282/citations | Empty (as of scan). OpenAlex cites-query was rate limited (HTTP 429-style), so not checked. |
| Tao constants database, constant 5b | https://teorth.github.io/optimizationproblems/constants/5b.html | Upper 4/7 [MT26], lower 9/17 [MT26]. No later entry. |
| GitHub issue 9804 | https://github.com/the-omega-institute/trureturing/issues/9804 | Opened 24 Sep 2026, open, no visible comments. Says explicitly it improves neither endpoint; its displayed examples have ratio 7/12 > 4/7. Quote: it "does not improve either endpoint". (gh CLI API access was denied in this sandbox; read via web fetch.) |
| Erdos Problem a Day log | https://erdosproblemaday.com/progress | Entry 12 Aug 2026 (PARTIAL): "Exact finite table through 15, plus f(17)=10, f(24)=14, f(26)=15, f(28)=16 ... the asymptotic constant remains 9/17 <= c* <= 4/7." Matches kb/00_START_HERE.md section 5, so no new information. |
| General web searches | WebSearch (3 queries: "Erdos problem 757 ... improved bound 2026", "Erdos 757 github issue", mathoverflow query) | No improvement; no MathOverflow thread; no GitHub issue other than 9804. |
| Henning-Yeo 2021 availability | Springer, UJ pure, SDU portal, Unpaywall, OpenAlex, Crossref | Closed access; no repository copy (Unpaywall is_oa=false). zbMATH Open record 1470.05066: "contents unavailable due to conflicting licenses". |

## Not checked / limits
- GitHub code/issue search for "Erdos 757" via API was not available (access disabled); only the issue page above and web search.
- Google Scholar and MathOverflow search pages cannot be queried programmatically; web search snippets used instead.
- ResearchGate returned 403.

## Conclusion
Bounds unchanged since Ma-Tang v2 (6 Mar 2026). Ma-Tang's own statements: lower bound via Henning-Yeo [Thm 7] for linear F7-free 3-uniform hypergraphs; upper bound via the 14-point base block with h=8.
