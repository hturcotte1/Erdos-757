s=open('i11.c').read()
a=s.index("    G h; int tau, sl; BUILD(h, tau, sl); int best = sl;")
b=s.index('    printf("SUBSA base')
new='''    G h; int tau, sl; BUILD(h, tau, sl); int best = 9999; long evals = 0; static long hist[HSZ];
    #define PEN(hh) ({ int iso_; int nc_ = components(&(hh), &iso_); (REQCONN && (nc_ != 1 || iso_)) ? 40 : 0; })
    int pen = PEN(h); int obj = sl + pen; if (!pen) best = sl;
    for (long it = 0; it < iters; it++) {
        double T = T0 * pow(T1 / T0, (double)it / iters);
        nin = nout = 0; for (int v = 0; v < N; v++) { if (inset[v]) in[nin++] = v; else out[nout++] = v; }
        int a = in[rndint(nin)], b = out[rndint(nout)]; inset[a] = 0; inset[b] = 1;
        G h2; int t2, s2; BUILD(h2, t2, s2); evals++; int p2 = PEN(h2); int o2 = s2 + p2;
        if (o2 <= obj || rnd01() < exp((double)(obj - o2) / T)) { obj = o2; sl = s2; tau = t2; h = h2; pen = p2; if (!pen) { if (sl + HOFF >= 0 && sl + HOFF < HSZ) hist[sl + HOFF]++; if (sl < best) best = sl; report_low(&h, tau, sl, "sub"); } }
        else { inset[a] = 1; inset[b] = 0; }
    }
'''
s=s[:a]+new+s[b:]
open('i11.c','w').write(s)
