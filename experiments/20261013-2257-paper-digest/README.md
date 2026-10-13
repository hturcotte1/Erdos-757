# Paper digest (2026-10-13)
Question: digest Gyarfas-Lehel 1995 and Henning-Yeo (2017 EJC, 2018 arXiv) for the lower-bound track; try to obtain Henning-Yeo 2021.
Method: `pdftotext -layout` for the two Henning-Yeo PDFs (text files here). The Gyarfas-Lehel PDF is a scan without text layer; pages rendered with `pdftoppm -r 130 -png` and read visually (PNGs deleted afterwards, regenerate with that command).
Scripts: chk_fibonacci_F7_AG.py (Fibonacci sets are (4,5), tau=floor(2(n-1)/5), F7/F8/AG(2,3) tau and HY slack), chk_L13_L8.py (L(8)=F8, L(13) linear F7-free tau=6), hy_tight_search.py (random search for small HY slack, heuristic). Run with `python3 <script>` from repo root.
Results: see kb/notes/gyarfas_lehel_1995.md, kb/notes/henning_yeo_2021_affine.md. HY 2021 full text NOT obtainable (closed access).
