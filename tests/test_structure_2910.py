"""Re-run the structural census (experiments/20261016-0150-structure-2910/stats.py) on three of the 2,910
saturated extremal 14-point classes and compare with the stored rows (K47)."""
import gzip, json, os, sys, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP = os.path.join(ROOT, "experiments", "20261016-0150-structure-2910")


def _load_stats():
    spec = importlib.util.spec_from_file_location("stats2910", os.path.join(EXP, "stats.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, ROOT)
    spec.loader.exec_module(mod)
    return mod


def test_three_classes_match_stored_rows():
    mod = _load_stats()
    stored = json.load(open(os.path.join(EXP, "results.json")))
    recs = [json.loads(s) for s in gzip.open(os.path.join(ROOT, "data", "census_n14_m12_classes.jsonl.gz"), "rt")]
    assert len(recs) == 2910 and stored["summary"]["n_classes"] == 2910
    for idx in (0, 1000, 2440):
        row = mod.analyse(recs[idx])
        for key in ("deg_seq", "max_deg", "n_max_sidon", "n_min_transversals", "universal_vertices",
                    "n_pairs_h12_eq7", "GL_sizes", "GR_sizes", "symmetric", "alpha", "tau"):
            assert row[key] == stored["rows"][idx][key], (idx, key)
        assert row["alpha"] == 8 and row["tau"] == 6 and row["universal_vertices"] == 0
        assert row["n_pairs_h12_eq7"] == 0 and sorted(row["GL_sizes"]) == [6, 7]
    # A_base (index 2440): degree sequence 4,3^6,2^7 and 143 maximum Sidon subsets (START_HERE section 6)
    r = stored["rows"][2440]
    assert r["deg_seq"] == [4, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2] and r["n_max_sidon"] == 143


def test_summary_distributions():
    S = json.load(open(os.path.join(EXP, "results.json")))["summary"]
    assert S["max_deg"] == {"3": 700, "4": 2210}
    assert S["symmetric"] == {"false": 2910}
    assert S["classes_with_h12_eq7_subset"] == 0
    assert S["universal_vertices"] == {"0": 2910}
    assert sum(S["n_max_sidon"].values()) == 2910 and S["n_max_sidon_min"] == 137 and S["n_max_sidon_max"] == 150
