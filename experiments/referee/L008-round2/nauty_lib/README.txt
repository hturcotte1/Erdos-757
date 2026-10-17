Referee round 2 (L008): the parts of nauty 2.8.8 (B. D. McKay and A. Piperno; Apache License 2.0, see COPYRIGHT and
LICENSE-2.0.txt) needed for the library routine densenauty, copied from the PyPI sdist pynauty-2.8.8.1 (src/nauty2_8_8).
nauty.h and naututil.h were generated from nauty-h.in / naututil-h.in by sed (64-bit words, MAXN = WORDSIZE; the exact sed
command is in the review's scratch history: every @...@ placeholder replaced by the usual Linux x86-64 value).  No configure
or make step was run.  Build: see ../reproduce.sh (gcc -O3 -c -DWORDSIZE=64 -DMAXN=WORDSIZE on nauty nautil naugraph
schreier naurng nautinv, then ar).  Only densenauty (canonical labelling, automorphism group size) is used, by
../src/bfs_enum.c and ../src/canon_list.c.
