# NOTES: decision log

Running log of decisions, search queries, access tests and open questions for the MSc AI thesis
(Utrecht University; supervisor Dr. Ioana Karnstedt-Hulpuș). Newest entries at the top of each day.

Verification legend used in this repo: **[FT]** full text opened (via web fetch, which extracts/summarises; re-check
numbers in the PDF) · **[ABS]** abstract or record page only · **[UNVERIFIED]** not opened, lead only ·
**[BG]** pre-2025 background work (never used as evidence that a niche is open or closed).

---

## 2026-11-06 (afternoon): feasibility study of the 5 best proposals

**Reading of the task (worked unattended, no questions asked):** consolidate all earlier scouting repos, pick exactly
five proposals, and write one feasibility dossier per proposal with gap evidence from papers actually opened in this
session or in earlier sessions (earlier-session [FT]/[ABS] tags are carried over and marked as such where I did not
re-open the paper). Implementation effort is *not* a reason to reject a proposal (Frank codes with generative AI).

### Step 1: earlier work read

| Repo | Files read | What it contains |
| --- | --- | --- |
| `thesis-attempt-2` (2 Nov 2026) | `README.md`, `topic_options_2026.md` (full), `lit_review_2026.md` (full), `NOTES.md` (full); `references.bib` grepped per key as needed | 2026-only scouting run around the anchor paper Krstev et al. 2026 (*Machine Learning* 115:173). 13 raw ideas with kill tests; 6 worked cards (A-1 13F events, A-2 credit-event contagion + counterfactual XAI, B-1 surprise edges, B-2 13F crowding anomalies, C-1 signed temporal lead-lag LP with WP1 re-evaluation, C-2 economic links → lead-lag); 3 runner-ups (D-1 audit, D-2 tariff stress tests, D-3 point-in-time LLM graphs). Recommendation: C-1 + B-1 combined. |
| `thesis-subject-attempt-3` | `README.md` | **Empty**: only a one-line README. Nothing to reuse. |
| `thesis-proposals` (1–2 Nov 2026) | `README.md`, `topic_shortlist.md` (full), `deep_dive_idea3.md` (full), `NOTES.md` (full), `lit_review.md` (how-made, counts, crowding map, comparison table; per-theme entries grepped by key as needed), `sweep/*` (headers + grep by key; raw provenance files, uncorrected) | 2025–2026 scouting run with 8 theme sweeps (158 opened entries, 227 bib keys), 30 raw ideas, 4 kill-test reports, an independent citation check (61 citations), 6 full cards (1 TKG completion on FinReflectKG, 2 LLM-graph look-ahead, 3 signed lead-lag edge-state forecasting, 4 event-conditioned signed edge activation, 5 audit of learned graphs, 6 unexplained co-movement anomalies), 5 runner-ups (R1–R5), and a deep dive on Card 3 (Krstev et al. now published; UU WRDS has no CRSP). |
| `smurfing-thesis` (Oct 2026, dropped topic) | `README.md`, `NOTES.md` (full), `lit_review.md` (headings) | AML smurfing review around GARG-AML. Reusable lessons only: (1) shell reaches GitHub only, read papers via web fetch; (2) evaluation protocol: chronological split, point-in-time features, PR-AUC + recall@K alert budget, PU-robustness test, injected patterns with known ground truth; (3) LAS-GNN code (MIT) exists from the supervisor's group; (4) do not copy random splits from prior work. |

Note on "read fully": the curated deliverables were read in full. The raw sweep files (~800 KB) and the 277 KB
`lit_review.md` of `thesis-proposals` were read through their structure and grepped per paper when a dossier needed
an entry, because their corrected content is already in `topic_shortlist.md`, `NOTES.md` and `references.bib`.

**Inconsistency found and resolved:** `thesis-proposals` lists Krstev et al. as a *withdrawn ICLR 2026 submission*
(key `krstev2025temporal`); `thesis-attempt-2` and the deep dive show it was published in *Machine Learning* 115:173
(online 8 Jul 2026). This repo uses the journal version (key `krstev2025temporal`, kept from the earlier repo because the paper was first public in Oct 2025 on OpenReview; the bib entry points to the journal version).

### Step 2: all proposals found, deduplicated, and the 5 picks

Earlier scores are out of 70 (briefing §9). "AT2" = `thesis-attempt-2`, "TP" = `thesis-proposals`.

| # | Proposal (merged sources) | Earlier score(s) | Kill-test outcome (earlier) | Decision |
|---|---|---|---|---|
| 1 | **Signed lead-lag edge-state forecasting + re-evaluation of the anchor** (AT2 C-1 + D-1; TP Card 3 + I2 + I25; deep dive) | 58 (C-1), 56 (D-1), 58 (Card 3) | Weakened → survives (MSGNN static; anchor unsigned) | **PICK → `proposals/signed-leadlag.md`.** Most direct hit on her capitalised point; low-risk WP1 first result. |
| 2 | **Unexpected edges: edge-level anomaly detection in signed stock networks** (AT2 B-1; TP Card 6 + I19/I20; TP R1 = I3 + I21) | 58 (B-1), 52 (Card 6), ≈50 (R1) | Survives (B-1, I20); I19 narrowly; I3/I21 weakened (early warning crowded) | **PICK → `proposals/unexpected-edges.md`.** Anomaly direction. Merged around one question: *expected relative to what?* (learned dynamics vs known company relations). Early warning only as a secondary test. |
| 3 | **Which peers move when a firm surprises or defaults? Event-conditioned signed contagion with explanations** (AT2 A-2; TP Card 4 + I4/I26/I29) | 55 (A-2), 54 (Card 4) | Survives (FinRipple closest) | **PICK → `proposals/event-contagion.md`.** Her separate credit-default problem; earnings-first design fixes the rare-event risk of A-2; counterfactual XAI fits Frank. |
| 4 | **Temporal KG completion on a public 10-K company KG (FinReflectKG)** (TP Card 1 + R3/I24) | 60 | Survives (FinKGR unverifiable) | **PICK → `proposals/company-tkg.md`.** Highest earlier score; knowledge networks = her expertise; link prediction. Today's sample check shows a serious data-quality risk (see dossier). |
| 5 | **Who enters, who exits? Edge events on the temporal 13F ownership graph** (AT2 A-1; TP R2 = I5 + I6; AT2 B-2 as a module) | 55 (A-1), ≈49 (R2), 50 (B-2) | Weakened → survives | **PICK → `proposals/ownership-events.md`.** Heterogeneous + temporal + link prediction (edge birth/death) on the cleanest free data; a 2026 benchmark (with code) to extend. |
| 6 | Look-ahead contamination and construction robustness of LLM-built company graphs (TP Card 2 + I8/I9; AT2 D-3) | 59 (Card 2), 48 (D-3) | Survives (strengthened) | **Reject as standalone.** Strong for Frank (LLM validation, AI Act) but weakest on her graph directions (fit 3/5). Kept as a robustness module inside Proposal 4 and listed under "Other directions". |
| 7 | Do economic links explain price lead-lag? (AT2 C-2) | 55 | Survives | **Reject as standalone; folded into Proposal 1 SQ3 / Proposal 2 (relation layers).** Overlaps 1 and 4; supply-chain coverage risk. |
| 8 | Audit of learned / causally discovered stock graphs vs real links (TP Card 5 + I10–I12) | 54 | I10 weakened (guo2026nystrom); I11, I12 survive | **Reject.** Evaluation-only, depends on third-party code running; less creative fit with her "find a niche" advice. Listed under "Other directions". |
| 9 | 13F crowding anomalies (AT2 B-2) | 50 | Weakened | **Merged into Proposal 5** as an optional anomaly chapter. |
| 10 | Tariff / sanction shocks through firm networks (AT2 D-2; TP R4 = I17) | 52, ≈46 | Weakened; thin alone | **Reject as standalone** (one shock = case study). Used as a regime test in Proposals 1–3. |
| 11 | Text-derived hyperedges vs clique projection (TP R5 = I23) | ≈46 | Survives | **Reject.** Crowded hypergraph-architecture zone; costly extraction. |
| 12 | Cold-start relations for IPOs (TP R3 = I24) | ≈47 | Survives | **Merged into Proposal 4** as an inductive sub-question. |
| 13 | Temporal-GNN explainers on financial graphs (TP I16; AT2 idea 10) | — | Survives / weakened | **Merged** as the XAI component of Proposals 3 (and 1, 4). |
| 14 | Regime signed causal graphs; KG priors for causal discovery; credit–equity Hawkes; decoupling; distress-text diffusion; US→Europe lead-lag (TP I13, I15, I27, I28, I30, I18) | not scored | Weakened | **Reject** (reasons in TP NOTES §3: incremental, sparse public data, or no European point-in-time data). |
| 15 | Insider / shadow trading (TP I22) | — | Dropped | **Reject** (named natural persons, tiny labels). |
| 16 | Plain heterogeneous distress classification; new TGNN for return prediction; crypto pump-and-dump (AT2 ideas 11–13) | — | Killed | **Reject** (crowded / outside gates / scope). |

Directions covered by the five picks: signed time-activated edges (1, 2), link prediction (1, 4, 5), anomaly detection (2), credit default (3), heterogeneous graphs (3, 4, 5), temporal graphs (all), time series + graph (1, 2, 3). That is more than three distinct directions, so Frank has a real choice. **No new proposals were needed**: the repos contain more than five strong candidates.

### Access tests (6 Nov 2026)

| Resource | Route | Result |
| --- | --- | --- |
| Google Scholar | web fetch `scholar.google.com/scholar?q=signed+lead-lag…&as_ylo=2026` | **Blocked** (`robots_disallowed`). Tried once, not retried. "Cited by" checks left to Frank. |
| Springer article + PDF (Krstev et al.) | web fetch | **Blocked** today (`client_error`; worked on 2 Nov). Earlier [FT] reading reused. |
| OpenReview API | web fetch `api2.openreview.net/notes?forum=KsWRLyIAKP` | **Blocked** (`client_error`). |
| arXiv abs/html | web fetch | Works; one rate limit on 2610.33171 after three parallel fetches. |
| Web fetch of URLs not surfaced by a search | e.g. `stooq.com/db/h/` | Needed a permission approval that nobody answered (the user said visiting websites is allowed, but the tool still asks). Decision: fetch only URLs surfaced by searches or earlier pages; no retries. |
| GitHub (shell clone) | 13 repos | All OK (list per dossier). |
| Hugging Face (shell) | `huggingface.co/api/datasets/domyn/FinReflectKG` + one 16 MB parquet shard | **Works** (HTTP 200). |
| Kenneth French data library (shell) | FF5 daily zip | **Works** (HTTP 200; data to 2026-09-30). |
| SEC (shell) | `sec.gov/files/...13f...`, `data.sec.gov/submissions` | **403** (proxy). Test via web fetch instead. |
| Yahoo Finance API (shell) | `query1.finance.yahoo.com` | **429**. |
| Stooq (shell) | `stooq.com/db/h/` | No connection. |

### Dossier 1 (signed lead-lag) decisions and searches
- Searches (WebSearch): `forecasting signed lead-lag network edges stocks sign flip prediction 2026` (extended); `dynamic signed graph neural network stock market dataset positive negative edges temporal link prediction`; `Cartea Cucuringu Jin "Detecting lead-lag relationships in stock returns" Journal of Empirical Finance 2026`; `Krstev Rigoni Mishkovski Pasa temporal graph learning lead-lag detection financial markets`. Outcome: no kill. Cartea et al. JEF 2026 still [UNVERIFIED].
- Opened today: HCIM 2605.26290 [FT]; IDP-DSN 2604.18213 [FT]; DeltaLag 2511.00390 [FT partial]; Qarkaxhija & Scholtes 2609.35364 [ABS]; Yu & Ha 2607.27861 [ABS]. 2610.33171 rate-limited (still [UNVERIFIED]).
- Data finding: the anchor's data repo lists 29 stocks but its price files contain 23; must be resolved before WP1.
- Decision: labels on the **next non-overlapping block** (earlier cards used rolling windows with step 20 and window 120, which would let labels share 100 of 120 days with features and inflate persistence).

### Dossier 2 (unexpected edges) decisions and searches
- Searches: `edge-level anomaly detection stock correlation network unexplained co-movement company relations 2026` (extended); `temporal link prediction surprise score anomaly detection financial market network event validation 2026 arXiv`; `Graph neural networks for anomaly detection: a systematic review of dynamic temporal approaches Artificial Intelligence Review 2026`; `SEC litigation releases 2026 list sec.gov`.
- Opened today: Caputi & Meadows 2604.02549 [FT]; Ahmed & Shafi 2608.15965 [ABS]; Ren et al. 2605.08726 [ABS]; Li et al. 2026 *Discover Computing* [FT, new closest work]; Li & Fan 2510.17088v2 [FT, new]; AIR 2026 review record [metadata only].
- New closest work found: **Li et al. 2026 (*Discover Computing* 29:493)**: inconsistency-based stock/interval anomalies. Does not kill the idea (no edge-level, no relation-based expectation, pseudo-labels from prices), but must be cited as the position point.
- Data finding: `fja05680/sp500` gives ≈ 775 S&P 500 additions since 1996 → index inclusion is a clean, frequent positive control for co-movement anomalies (Barberis et al. 2005 effect).
- Decision: merged B-1 and Card 6 around the question "expected relative to what?"; early warning (R1) kept as a secondary SQ only, because 2026 early-warning work is crowded and has few events.
- Decision: SEC litigation releases name natural persons → only a sparse secondary label, firm/ticker level only.
