#!/usr/bin/env bash
# Try to download the key papers into kb/literature/papers/ (needs network access to these hosts).
# Missing files are reported; ask the scout subagent to fetch them via WebFetch instead.
cd "$(dirname "$0")/.." && mkdir -p kb/literature/papers && cd kb/literature/papers
get() {  # name url
  if [ -s "$1" ]; then echo "have $1"; return; fi
  if curl -sfL --max-time 60 -o "$1" "$2"; then echo "got  $1"; else rm -f "$1"; echo "FAIL $1 <- $2"; fi
}
get ma_tang_2026.pdf              https://arxiv.org/pdf/2602.23282v2
get henning_yeo_1802.01825.pdf    https://arxiv.org/pdf/1802.01825
get henning_yeo_ejc_2017.pdf      https://www.combinatorics.org/ojs/index.php/eljc/article/download/v24i2p50/pdf
get gyarfas_lehel_1995.pdf        https://users.renyi.hu/~gyarfas/Cikkek/69_linset5.pdf
get tao_2409.01343.pdf            https://arxiv.org/pdf/2409.01343
get bennett_et_al_2207.02920.pdf  https://arxiv.org/pdf/2207.02920
get patternboost_2411.00566.pdf   https://arxiv.org/pdf/2411.00566
get alphaevolve_2511.02864.pdf    https://arxiv.org/pdf/2511.02864
echo "Paywalled (get via a library and add by hand): Henning-Yeo, Graphs Combin. 37 (2021) 867-890, doi:10.1007/s00373-021-02285-x"
