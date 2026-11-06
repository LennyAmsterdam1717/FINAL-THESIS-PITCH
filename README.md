# final-thesis-pitch

MSc AI thesis, Utrecht University (supervisor: Dr. Ioana Karnstedt-Hulpuș). Topic area: network analysis of the stock market and between listed companies, using public data only. This repo holds the **feasibility study of the five best proposals** (6 Nov 2026), built on the earlier scouting repos `thesis-attempt-2` and `thesis-proposals`.

**Start with `feasibility_overview.md`.**

| File | What it is |
| --- | --- |
| `feasibility_overview.md` | One-page recommendation (which proposal to pitch and why), a side-by-side comparison of all 5, questions for the supervisor, and "Other interesting directions" |
| `proposals/signed-leadlag.md` | **Proposal 1**: forecasting the state (+/−/none) of signed, directed lead-lag edges, plus a re-evaluation of Krstev et al. 2026 (58/70) |
| `proposals/unexpected-edges.md` | **Proposal 2**: edge-level anomaly detection in signed stock networks; "expected" from learned dynamics vs from company relations (58/70) |
| `proposals/event-contagion.md` | **Proposal 3**: which linked firms react to earnings surprises and credit events, with which sign and through which relation (57/70) |
| `proposals/company-tkg.md` | **Proposal 4**: year-ahead temporal knowledge-graph completion on FinReflectKG, with a noise audit and an economic test (54/70) |
| `proposals/ownership-events.md` | **Proposal 5**: entry/exit (edge birth/death) prediction on the temporal heterogeneous 13F ownership graph (58/70) |
| `NOTES.md` | Decision log: files read in the earlier repos, the full table of earlier proposals with picks and rejections, access tests, every search query, data checks, corrections, open questions |
| `references.bib` | Every cited work; the `note` field gives the verification status ([FT]/[ABS]/[SNIP]/[UNVERIFIED]/[BG]) and the first-public date |
| `tools/bib_pull.py` | Copies BibTeX entries by key from the earlier repos |
| `tools/finreflectkg_sample_stats.py` | Company–company edge statistics on FinReflectKG parquet shards (used in Proposal 4) |
| `tools/13f_sample_events.py` | Entry/exit base rates on the 2026 13F benchmark sample (used in Proposal 5) |

**Verification legend:** [FT] full text opened · [ABS] abstract or record page only · [SNIP] search-result excerpt only · [UNVERIFIED] not opened · [BG] pre-2025 background. "(1 Nov)" or "(2 Nov)" means the paper was opened in an earlier session and not re-opened. Re-check every number against the PDF before it goes into the thesis.
