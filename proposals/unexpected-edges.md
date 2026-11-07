# Proposal 2: Unexpected edges
## Edge-level anomaly detection in signed stock networks: "unexpected" relative to learned dynamics, or relative to known company relations?

*Feasibility dossier, 6 Nov 2026. Merges earlier cards B-1 "surprise edges" (`thesis-attempt-2`), Card 6 "unexplained co-movement" + ideas I19/I20 and runner-up R1 (I3 + I21) (`thesis-proposals`).*
*Legend: [FT] full text opened · [ABS] abstract/record only · [SNIP] search-result excerpt only · [UNVERIFIED] not opened · [BG] pre-2025 background. "(2 Nov)" = opened in an earlier session, not re-opened today.*

Supervisor directions hit: **anomaly detection** · **signed, time-activated edges** · temporal graphs · link prediction (as the expectation model) · heterogeneous / knowledge graph (as context) · time series + graph. It is close to her graph-based financial-crime work without being AML.

---

## 1. The problem in plain language

Most of the time, when two stocks suddenly start moving together, there is a boring reason: they are in the same industry, one supplies the other, the same big funds own both, or the whole market moved. Market-surveillance teams, risk managers and journalists care about the *other* cases: two stocks that start moving together (or against each other) **for no reason anyone can see**. Such links can be the first trace of news that has not been announced, of a merger rumour, of a crowded trade about to unwind, or occasionally of coordinated manipulation.

Today, anomaly detection on stock networks almost always works at the level of the **whole market**: "this week the network looks strange", checked against a handful of crisis dates. That is too coarse for an analyst, who wants to know **which pair of stocks** is behaving strangely and **why it is strange**. And "strange" needs a reference: strange compared with how this link usually behaves over time, or strange compared with what we know about the two companies? Those are two different notions of "expected", and nobody has compared them.

Why it matters:
- **Regulators and exchanges** (market abuse surveillance, the EU Market Abuse Regulation, SEC) need screening tools that point at specific instruments and explain the alert.
- **Risk managers** want to know when a hedge or a pairs trade is held together by a relationship that has no economic basis and may break.
- **Machine-learning research** has mature dynamic-graph anomaly detectors (2026 benchmarks with 25 models), but none of their benchmarks contains stock-market data, and a 2026 paper shows a one-feature counting rule often matches them.

A concrete example: *Two mid-cap stocks in unrelated industries, with no shared top-10 institutional owners and no mention of each other in their annual reports, suddenly show a strong same-direction lead-lag link for two weeks. A week later, one announces it will acquire the other. Could the link have been flagged as "unexplained" before the announcement, and how many false alarms would that cost?*

The honest difficulty: there is no list of "true" anomalous stock pairs. The thesis therefore uses three kinds of evidence: planted anomalies with known answers, public event calendars that should produce *explainable* anomalies (index additions, mergers, earnings), and careful controls so that "anomaly" does not just mean "very volatile stock".

### 1.1 Technical formulation

- **Edge stream.** Universe V (point-in-time S&P 500, optionally S&P 1500). For each window (weekly step, trailing W = 60 trading days), compute signed residual co-movement or lagged edges e_ij(t) ∈ {+, −, 0} with weights w_ij(t) (residual correlation or lagged correlation after FDR; shared pipeline with Proposal 1, but contemporaneous edges are the default here because they are denser).
- **Two expectation models.**
  - *Dynamics-based* E_dyn: a temporal link predictor trained on the edge history up to t gives p_dyn(e_ij(t+1) = c | history). Surprise S_dyn = −log p_dyn(observed state).
  - *Relation-based* E_rel: a model that predicts the co-movement state from slowly changing company relations only (same SIC/GICS, common 13F ownership overlap, 10-K text similarity, FinReflectKG relations, size/beta similarity) gives p_rel(c | relations). Surprise S_rel = −log p_rel(observed state).
  - *Combined* E_both: relations + history.
- **Anomaly types.** (a) unexpected birth (strong edge where none was expected), (b) unexpected sign (− where + expected, or vice versa), (c) unexpected death (expected strong edge vanishes). Node-level and graph-level scores are aggregates of edge scores.
- **Evaluation targets.** (i) injected anomalies with ground truth, (ii) enrichment of top-k alerts near public events against volatility- and degree-matched controls (positive-unlabelled setting), (iii) optional lead-vs-coincident test of aggregated surprise against a public stress index.
- **Research contribution.** An edge-level anomaly benchmark for stock networks and a comparison of what "expected" should mean.

---

## 2. Where the problem comes from

### 2.1 Papers that name the gap

| Paper (status, venue) | Section | Short quote (< 15 words) | What exactly is missing, in my words |
|---|---|---|---|
| **Caputi & Meadows (2026)**, *Financial Anomaly Detection for the Canadian Market*, arXiv 2604.02549, preprint · [FT today] <https://arxiv.org/abs/2604.02549> | 2.1 Data; 2.2 Networks; 3.6 Results and discussion | "replacing negative entries with 0" (2.2); "our emphasis on global graph anomalies over local node-level deviations" (3.6) | Ground truth is **seven** stress-index peaks; negative edges are dropped; only whole-graph anomalies are scored. They say the result "does depend on the networks at hand". Edge-level, signed scoring and a larger event set are open. (The paper has no explicit limitations section; gaps are from these passages.) |
| **Li, Yu, Kim, … & Jung (2026)**, *Dynamic relational network embedding-based anomaly detection for predicting financial risks*, *Discover Computing* 29:493 (peer-reviewed, online 3 Aug 2026) · [FT today] <https://doi.org/10.1007/s10791-026-10424-2> | 5 Conclusion | "may incorrectly identify certain highly volatile market periods as financial bubbles" | The closest 2026 paper: edges are added when co-movement is "inconsistent" with a Granger-type dependency, but the score is per **stock and interval**, labels are price-drop pseudo-labels (circular, as the authors admit), 100 random stocks. They plan larger datasets. Volatility confound and edge-level alerts are open. |
| **Li & Fan (2025, v2 2026)**, *Explainable Heterogeneous Anomaly Detection in Financial Networks via Adaptive Expert Routing*, arXiv 2510.17088, preprint · [FT today] <https://arxiv.org/abs/2510.17088> | Abstract; V-A | "static graph structures cannot adapt when correlations shift across regimes" | Uses sector/geography priors as structure, scores **stocks** and a market index; pairs are never output as anomalies; six test events; survivor universe from WRDS ("modestly optimistic bias"). Edge-level, public-data, relation-conditioned scoring is open. |
| **Ahmed & Shafi (2026)**, *Beat the Counter First*, arXiv 2608.15965, preprint · [ABS today] <https://arxiv.org/abs/2608.15965> | Abstract | "no parameter fitting" | A one-feature count/recency baseline matches the SLADE detector on 3 of 6 datasets; on planted structure detectors are near random. No financial data. Any stock-graph detector must beat this first. |
| **Hua et al. (2026)**, *BAG: Benchmarking Anomaly Detection on Dynamic Graphs*, AAAI 2026 (peer-reviewed) · [ABS (2 Nov); AAAI page blocks fetch; repo README read today] <https://github.com/frhuaaa/BAG> | Benchmark scope | (no quote; page blocked) | 25 detectors, 10 datasets (Wikipedia, Reddit, MOOC, …); **no equity dataset**. Code supports CTDG edge detectors incl. GraphMixer, DyGFormer, EdgeBank, so a stock edge stream can be plugged in. |
| **Ren, Yi, Chen & Gao (2026)**, *Investor-driven information diffusion and excess comovement*, *J. Int. Financ. Mark. Inst. Money* (DOI 10.1016/j.intfin.2025.102258), arXiv 2605.08726 · [FT (1 Nov); ABS today] | Abstract | "retail-driven information diffusion has a notably stronger effect on excess comovement" | Explains **average** factor-residual excess co-movement by investor channels (China vs US); does not flag individual pairs. The "explained vs unexplained" split per edge is open. |
| **Chen et al. (2026)**, velocity-based manipulation detection with enforcement-document labels, arXiv 2608.05373 · [FT (1 Nov)] | Method / data | (paraphrase only) | Uses positive-only labels from SEC/SEBI enforcement documents; not graph-based. Shows enforcement releases can act as sparse positive labels (PU setting). |

**No paper names the exact gap** "edge-level anomalies in signed stock networks, with 'expected' defined by dynamics vs by company relations". It is inferred from (a) finance anomaly papers that stop at graph or stock level and admit label and volatility problems (Caputi & Meadows; Li et al. 2026; Li & Fan), (b) generic detector benchmarks without finance data and with a strong counting baseline (BAG; Ahmed & Shafi), and (c) finance work that explains co-movement only on average (Ren et al.).

### 2.2 Lineage (timeline)

| Year | Work | Status | Step |
|---|---|---|---|
| 2005 | Barberis, Shleifer & Wurgler: S&P 500 inclusion raises co-movement with the index | [BG, UNVERIFIED: classic, not opened] | Co-movement can be "non-fundamental": a positive control for this thesis |
| 2014 | Antón & Polk: common ownership predicts co-movement | [BG, ABS (1 Nov)] | Ownership is a known explanation of co-movement |
| 2016 | Hoberg & Phillips: text-based industry networks | [BG, cited in Springer 2024 paper seen today] | Text similarity as an explanation layer |
| 2022 | Poursafaei et al., EdgeBank / DGB | [BG] | Memorisation baselines for temporal edges |
| 2024 | Poštuvan et al., *Learning-based link anomaly detection in CTDGs* (arXiv 2405.18050) | [BG, ABS via search today] | Link predictors adapted to typed link anomalies; direct application of link prediction is sub-optimal |
| 2025 | Li & Fan (arXiv 2510.17088 v1) | [FT] | Structural priors + stock-level anomaly scores |
| 2026 | BAG (AAAI), DynGraphAgentBench, SimpleCount | [ABS] | Mature generic detectors; counting baselines; no finance data |
| 2026 | Caputi & Meadows; Li et al. (*Discov. Comput.*); CF2TLP (IEEE SMC 2026, temporal LP before SVB) | [FT]/[FT]/[ABS] | Finance anomaly detection at graph/stock level with very few events |
| **Now** | — | — | No edge-level, signed, relation-conditioned detector with a public event-based evaluation |

### 2.3 Related gaps in neighbouring fields that transfer

- **Dynamic-graph anomaly benchmarks** (BAG, DynGraphAgentBench [ABS (2 Nov)]): injected-anomaly protocols and chronological deployment windows with delayed labels transfer directly; a market edge stream would be the first financial dataset.
- **Positive-unlabelled learning on company graphs** (Iwata 2026, "no record ≠ no risk", arXiv 2607.26859 [ABS (1 Nov)]): event calendars only mark *some* anomalies, so PU-aware metrics are needed.
- **AML lessons from the dropped smurfing topic** (`smurfing-thesis/NOTES.md`): planted patterns with known depth, alert-budget metrics (precision@K), PU robustness. These transfer as the evaluation design.
- **Systematic review of dynamic-graph anomaly detection** (Ares-Robledo, Rifà-Pous & Clarisó, *Artif. Intell. Rev.* 59(5), 2026, open access, doi:10.1007/s10462-026-11532-7) [FT, read 7 Nov in the browser pane]. It reviews 79 studies, **all in cybersecurity** (intrusion, botnets, industrial control); finance is absent. Its conclusion names the shortage of robust real-world graph datasets and the weak interpretability of flagged anomalies ("limited rationale for flagged anomalies") as main barriers. *Transfer:* an edge-level financial benchmark with explanations (which expectation was violated, which relations were checked) addresses both.

### 2.4 Who is working on it (kill-test evidence)

- **Groups / venues:** single-author or small-team q-fin preprints (Canada, Korea, US); AAAI/IJCAI/KDD for generic detectors (BAG group in China); RPI (Li & Fan); Cardiff (CF2TLP). No group owns "edge-level anomalies in stock networks".
- **Is anyone close?** Li et al. 2026 (*Discov. Comput.*) is closest in spirit (inconsistent co-movement) but scores stocks and intervals; extending to edges would be easy for them. Li & Fan could add pair-level outputs. Neither announces it.
- **Searches run today:** `edge-level anomaly detection stock correlation network unexplained co-movement company relations 2026` (extended) → Li et al. 2026 (*Discov. Comput.*), Li & Fan 2025/26, older ResearchGate items (2021–2023), Information networks of stock prices (arXiv 2606.07450, Indonesia, descriptive); `temporal link prediction surprise score anomaly detection financial market network event validation 2026 arXiv` → Ozimek 2026 (arXiv 2606.08586, stock-level topological anomaly scores, 10 stocks intraday), CF2TLP (SMC 2026), CTDG link anomaly paper (2024), a computer-network paper; `Graph neural networks for anomaly detection: a systematic review … 2026` → the AIR record. Earlier: `thesis-proposals/sweep/kill_K4.md` (I19, I20) and `thesis-attempt-2/NOTES.md` Phase 3 query 4. **Verdict: survives**, with Li et al. 2026 as the paper to position against.

---

## 3. Literature background

### 3.1 What you need to understand the problem
- **Co-movement and its explanations**: factor models (residual co-movement), industry, common ownership (Antón & Polk 2014 [BG]), index inclusion (Barberis et al. 2005 [BG]), text-based industries (Hoberg & Phillips 2016 [BG]).
- **Anomaly detection on dynamic graphs**: node/edge/subgraph/graph anomalies; CTDG vs DTDG detectors; reconstruction- and prediction-based scores (Ekle & Eberle 2024 survey, *TKDD* [BG, ABS via search]).
- **Evaluation without labels**: injected anomalies, positive-unlabelled metrics, precision@K under an alert budget, matched controls.
- **Calibration**: a surprise score is only meaningful if the predictor is calibrated (reliability diagrams, temperature scaling).

### 3.2 State of the art closest to the solution, and the difference

| Paper | What it does | How this thesis differs |
|---|---|---|
| Li et al. 2026, *Discov. Comput.* [FT] | Multi-layer stock network with an "inconsistency coefficient"; autoencoder flags anomalous stocks/intervals (bubbles); 100 random stocks; price-drop pseudo-labels | Scores **edges** with sign; two explicit notions of "expected"; labels from external events, not from prices; volatility-matched controls |
| Caputi & Meadows 2026 [FT] | Graph-level detection on 39 TSX stocks, 7 events, negatives dropped | Edge-level, signed, hundreds of events, S&P 500/1500 |
| Li & Fan 2025/26 [FT] | Stock-level scores with sector/geography priors, WRDS data | Pair-level output; relations as an *explicit* expectation model; free data |
| BAG 2026 (AAAI) [ABS + code] | Generic detector benchmark | Uses its detectors as baselines on a new financial dataset |
| Ahmed & Shafi 2026 [ABS] | SimpleCount baseline | Mandatory baseline |
| Krstev et al. 2026 (*MLJ*) [FT (2 Nov)] | Temporal link predictor for lead-lag | Its predictor becomes the dynamics-based expectation model E_dyn |

---

## 4. Data and access

| Dataset | What it is | Existing / formable | Size | Licence / terms | Cost | Access test (6 Nov 2026) | Rating |
|---|---|---|---|---|---|---|---|
| Daily prices (current + delisted S&P 500/1500) | Returns for edges | Formable | ~7 M rows (S&P 500) | Stooq free; yfinance unofficial | Free | Not testable from this cloud session (Yahoo 429, Stooq blocked); test on laptop | Medium |
| Point-in-time S&P 500 membership + changes (`fja05680/sp500`) | Universe + **index additions/deletions** as events | Existing | 14 MB | MIT | Free | **Cloned OK**: 2,720 change dates 1996-01-02 → 2026-08-18; ≈ 775 additions; change log with add/remove since 2019 (125 rows) | Easy |
| Fama–French 5 factors daily | Residualising | Existing | small | free | Free | **Downloaded** (to 2026-09-30) | Easy |
| FinReflectKG (Hugging Face `domyn/FinReflectKG`) | Company relations from 10-Ks (partners_with, competes_with, depends_on, has_stake_in, supply …) | Existing | 103 parquet shards, 17.5 M triples | **CC-BY-NC-4.0** | Free | **Reached** (API 200); one 16 MB shard downloaded and inspected: 170 k triples for 8 tickers, only **439 mentions of another current S&P 500 firm** (see Proposal 4 for details) | Easy access, medium quality |
| 13F institutional holdings | Common-ownership overlap per pair | Formable (SEC 13F data sets) or sample in `e-izdfr/portfolio-holdings-prediction` | quarterly ZIPs, ≤ 100 MB each | public domain (SEC) | Free | Sample repo **cloned OK** (MIT; 209,351 manager–stock edges 2013-Q2 onward for 99 managers × S&P 500); SEC from shell 403 → full data via laptop | Easy–medium |
| SIC codes / 10-K text | Industry + text-similarity layers | Formable (EDGAR) | — | public | Free | EDGAR from shell 403; via laptop or `edgartools` (MIT, clone OK, too big to keep) | Medium |
| Event calendars | S&P changes (above); 8-K filings by item (2.02 earnings, 1.01/2.01 deals, 1.03 bankruptcy); SEC litigation releases (≈ 11.8 k since 1996) | Formable | — | public domain | Free | SEC litigation-release index **reached via search** (`sec.gov/enforcement-litigation/litigation-releases`); releases mostly name **persons** and small caps → only a sparse secondary label | Medium |
| Stress index | Optional graph-level check (OFR FSI / STLFSI) | Existing | small | public | Free | Not tested today | Easy |

**Minimum viable dataset:** S&P 500 point-in-time members 2010–2026, weekly windows, relation layer = GICS/SIC + 13F overlap; events = S&P index additions/deletions + 8-K Item 1.01/2.01 deal dates. **Fallback:** current members only + injected anomalies + index-addition positive control.

---

## 5. Approach and 30-week plan

**Research question.** *Can edge-level anomalies in signed stock co-movement networks be detected reliably, and does defining "expected" by learned network dynamics, by known company relations, or by both, give alerts that better match public information events?*
- **SQ1.** On injected anomalies (births, sign flips, vanished edges) with known ground truth, how do dynamics-based, relation-based and combined surprise scores compare with SimpleCount, EdgeBank-style and BAG detectors?
- **SQ2.** Which public event types (index additions, deals, earnings, bankruptcies, enforcement releases) produce detectable edge anomalies beyond volatility- and degree-matched controls, and which surprise definition captures which event type?
- **SQ3 (secondary).** Does aggregated edge surprise lead or only coincide with market stress (pre-registered test on 2008, 2020, 2022, 2023, 2025)?

**Pipeline.** prices → residual returns → weekly signed edge snapshots (+ lag variant from Proposal 1) → relation layers (sector, 13F overlap, text, FinReflectKG) → E_dyn (temporal link predictor), E_rel (GBDT/R-GCN on relations), E_both → calibrated surprise per edge → alerts → evaluation (injection, event enrichment, PU metrics) → surprise feed dashboard.

**Existing code to build on (checked today):** `frhuaaa/BAG` (no licence file; commit 2026-04-21; CTDG/DTDG edge detectors incl. GraphMixer, DyGFormer, EdgeBank, FreeDyG, SAD); `tgm-team/tgm` (MIT); `njmead811/Financial-Anomaly-Detection-for-the-Canadian-Market` (MIT, commit 2026-07-26; Caputi & Meadows baselines incl. GlocalKD and TDA); `e-izdfr/portfolio-holdings-prediction` (MIT; 13F graph); PyGOD (named in earlier notes, not re-checked). To build: edge pipeline (shared with Proposal 1), relation layers, injection generator, event-enrichment evaluator with matched controls, calibration, dashboard.

**Baselines.** SimpleCount-style count/recency/first-occurrence; |Δ correlation|; Isolation Forest on edge features; EdgeBank; BAG CTDG detectors; graph-level GlocalKD (from Caputi & Meadows' repo) aggregated as a reference.

**Metrics.** Injection: AUROC/AUPRC per anomaly type. Events: precision@K and recall@K at fixed weekly alert budgets; lift over matched controls with bootstrap CIs; PU-adjusted AUPRC. Calibration of E_dyn/E_rel (Brier). Stress test: lead-time distributions vs a placebo.

**Splits.** Train expectation models on 2005–2016, validate 2017–2019, deploy weekly on 2020–2026 with models refit only on past data; event labels never used for training.

**Week-by-week plan**

| Weeks | Phase | Work | Output |
|---|---|---|---|
| 1–4 | Phase 1 | Literature review (financial co-movement explanations, dynamic-graph anomaly detection, PU evaluation); read the AIR 2026 review | `lit_review.md` |
| 5–6 | Phase 1 | Pilot: S&P 100 weekly edges; index-addition positive control with a simple |Δρ| score | Pilot figure |
| 7–8 | Phase 1 | Proposal; event calendars scoped | **Go/no-go** |
| 9–12 | Phase 2 | Edge pipeline S&P 500; relation layers (sector, 13F, text) | Data chapter |
| 13–15 | Phase 2 | Injection generator + baselines (SimpleCount, EdgeBank, BAG) | SQ1 baseline table |
| 16–19 | Phase 2 | E_dyn, E_rel, E_both; calibration | SQ1 results |
| 20–22 | Phase 2 | Event enrichment with matched controls (SQ2) | SQ2 results |
| 23 | Phase 2 | Stress lead/coincident test (SQ3) | Short section |
| 24–25 | Phase 2 | Surprise-feed dashboard | Artefact |
| 26–30 | Writing | Thesis | Thesis |

**Usable artefact.** *Surprise feed:* a weekly ranked list of the most unexpected stock pairs, each with its sign, which expectation model was surprised (dynamics, relations, or both), the relations that were checked (sector, shared holders, 10-K mentions), and the nearest public filing. Explicitly a screening tool, not an accusation.

---

## 6. Feasibility verdict

**Top 3 risks and mitigations**
1. **Weak labels (evaluation).** Most anomalies may be driven by unobserved news; enforcement releases are sparse and about persons. *Mitigation:* injected anomalies as the primary quantitative test; S&P index additions as a clean positive control with ≈ 775 events; deal and earnings dates as secondary; report results per event type; PU-aware metrics.
2. **"Anomaly = volatility" (evaluation/novelty).** The closest 2026 paper admits its detector confuses volatile periods with bubbles. *Mitigation:* volatility- and degree-matched controls built into every enrichment test; residual returns; report correlation of the score with |return|.
3. **Relation-layer quality (data/scope).** FinReflectKG company–company relations are sparse and noisy (sample check today). *Mitigation:* start with sector + 13F overlap (clean, structured); add text similarity; FinReflectKG only as an extra layer, with a manual check of 100 edges.

**Minimum thesis (fallback).** Injected-anomaly benchmark + index-addition positive control on S&P 500, comparing SimpleCount, EdgeBank, one BAG detector and the relation-based surprise. Clear RQ, clear metrics, no dependence on rare events.

**Ethics / GDPR.** Company-level nodes only. SEC litigation releases name natural persons → keep only firm/ticker-level labels, never store or display names. Present alerts as screening, never as evidence of wrongdoing; say so in the thesis and the dashboard. No investment advice. Disclose generative-AI use.

**Scores (briefing §9)**

| Criterion (weight) | Score | Weighted | Reason |
|---|---|---|---|
| Novelty (×3) | 4 | 12 | No edge-level signed detector with relation-based expectation found; Li et al. 2026 close |
| Supervisor fit (×2) | 5 | 10 | Anomaly detection + signed edges + knowledge context; near her financial-crime graph work |
| Data (×2) | 4 | 8 | Free; events need assembling |
| Feasibility (×2) | 4 | 8 | BAG and TGM code; pipeline shared with Proposal 1 |
| Evaluation clarity (×1) | 3 | 3 | Weak labels; mitigated by injection and positive control |
| AI relevance (×1) | 4 | 4 | Dynamic-graph anomaly detection, calibration |
| Artefact (×1) | 5 | 5 | Surprise feed is the most dashboard-ready of the five |
| Industry (×1) | 4 | 4 | Surveillance / risk; regulatory tech |
| Frank's interests (×1) | 4 | 4 | Markets, XAI (why is it surprising?), regulation |
| **Total** | | **58 / 70** | |

---

## 7. Questions for the supervisor

1. Is an evaluation based on injected anomalies + public event enrichment (no true per-edge labels) acceptable at MSc level?
2. Which notion of "expected" interests you more: learned dynamics (link prediction) or knowledge-based (company relations)? Is comparing both the right framing?
3. Would ING/SPIN contacts see market-abuse screening as a relevant use case, and could they comment on realistic alert budgets?
4. Should Proposals 1 and 2 be one thesis with two chapters (shared edge stream), or kept separate?
5. Is FinReflectKG (CC-BY-NC, LLM-extracted) acceptable as one relation layer?
