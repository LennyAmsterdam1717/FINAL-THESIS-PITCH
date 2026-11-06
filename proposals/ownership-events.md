# Proposal 5: Who enters, who exits?
## Predicting edge births and deaths on the temporal heterogeneous ownership graph of institutional investors (SEC 13F)

*Feasibility dossier, 6 Nov 2026. Based on card A-1 "Who buys next?" (`thesis-attempt-2`), runner-up R2 (ideas I5 + I6) of `thesis-proposals`, with card B-2 (13F crowding anomalies) as an optional chapter.*
*Legend: [FT] full text opened · [ABS] abstract/record only · [SNIP] search-result excerpt only · [UNVERIFIED] not opened · [BG] pre-2025 background. "(1 Nov)"/"(2 Nov)" = opened in an earlier session, not re-opened today.*

Supervisor directions hit: **link prediction** (edge birth = entry, edge death = exit) · **heterogeneous graphs** (manager and stock nodes; holding, co-movement and portfolio-overlap edges) used for an edge task, not node classification · temporal graphs · time series + graph · optional anomaly detection (coordinated entries). Close to her earlier venture-capital investor–company graph projects (Crunchbase) mentioned on her UU staff page.

---

## 1. The problem in plain language

Every quarter, each US investment manager with more than $100 million in US stocks must publish its holdings on SEC Form 13F. About 8,000–9,000 managers file, from BlackRock to small hedge funds. Together these filings form a large network: managers on one side, stocks on the other, and a link whenever a manager holds a stock. The network changes every quarter: a fund **enters** a new stock (a new link appears), **exits** one (a link disappears), or sharply increases or cuts a position.

A July 2026 benchmark showed that predicting the *size* of each position next quarter is almost trivial: "copy last quarter's portfolio" is nearly as good as the best deep model, because portfolios change slowly. The interesting part is exactly what that benchmark does not score: **the changes**. Which manager will buy into which stock next quarter? Which managers are about to leave a stock at the same time? Those are the moves that matter for prices, liquidity and crowding risk.

Concrete example: *Given the holdings of the 1,000 largest managers up to Q2 2025, plus how stocks moved together and how similar managers' portfolios are, can we rank, for each manager, the stocks it is most likely to enter in Q3 2025, and does a stock that many managers are predicted to enter perform differently afterwards?*

Why it matters:
- **Asset managers and brokers** want to anticipate institutional demand (who might buy what) for investor relations, liquidity planning and capital-markets advice.
- **Risk managers and regulators** care about crowded trades: many funds entering or exiting the same stock at once can amplify price moves.
- **AI research**: this is a clean, public temporal *heterogeneous* link-prediction problem where the 2026 benchmark found learned models barely beat persistence; scoring births and deaths instead of levels is the natural next test.

### 1.1 Technical formulation

- **Graph.** Quarterly discrete-time heterogeneous graph G_q = (M ∪ S, E_hold(q) ∪ E_ss(q) ∪ E_mm(q)): managers M (top-N by reported value), stocks S (point-in-time S&P 500 or S&P 1500), holding edges (m, s) with weight w_ms(q) = portfolio weight; stock–stock edges from rolling residual co-movement or sector (shared with Proposal 1); manager–manager edges from portfolio-overlap (cosine of weight vectors).
- **Events.** For each (m, s, q→q+1): entry (w = 0 → > 0), exit (> 0 → 0), large increase (> +25 %), large decrease (< −25 %), no change. Entries are further split into **first-time entries** and **re-entries** (held at some earlier quarter).
- **Tasks.** (T1) *Entry ranking:* for each manager m, rank all stocks s not held at q by P(entry at q+1); evaluated with all-entity ranking. (T2) *Exit classification:* for each held (m, s), P(exit at q+1). (T3) *Event classification* over the five classes (macro-AUPRC).
- **Information timing.** A 13F for quarter q is filed up to 45 days after quarter end. Features may only use filings with filing date < prediction date; prices only up to the prediction date.
- **Economic check (secondary).** Aggregate predicted net entries per stock vs next-quarter abnormal return, turnover and volatility (portfolio sorts, Fama–MacBeth), strictly out of sample.

---

## 2. Where the problem comes from

### 2.1 Papers that name the gap

| Paper (status, venue) | Section | Short quote (< 15 words) | What exactly is missing, in my words |
|---|---|---|---|
| **Izadifar & Rahmati (2026)**, *Institutional Equity Holdings Prediction Using Node Affinities of Dynamic Graphs*, arXiv 2607.12067 (preprint, marked for an Elsevier journal; v1 13 Jul 2026) · [FT today] <https://arxiv.org/abs/2607.12067> | Conclusion; Limitations; Future Work | "a promising direction for more challenging and less persistent prediction problems" (Conclusion); "randomly sampled subset of institutional investment managers" (Limitations) | First TGB-style 13F benchmark: predicts next-quarter **weights** (NDCG@10) for 99 sampled managers × 503 S&P 500 stocks. Persistence 0.8891 and EMA 0.8882 vs best model (NAVIS) 0.9127. Entries/exits are not evaluated; manager sample is small "due to computational resource constraints"; future work lists harder, less persistent settings, multi-step forecasting and hypergraphs. |
| **Thomaz & Mauá (2024)**, *A Case Study of Next Portfolio Prediction for Mutual Funds*, arXiv 2410.18098 · [BG, FT (1 Nov)] | Task | (paraphrase) | Predicts new positions for mutual funds from N-PORT holdings as a recommendation problem, without a graph of stock–stock or manager–manager relations. Shows the entry task is meaningful; graph structure is untested. |
| **Frontiers in AI (2026)**, *LLM-driven time-series forecasting of financial network indicators*, doi:10.3389/frai.2026.1722121 · [ABS via search extract (2 Nov)] | Abstract | (paraphrase) | Forecasts **aggregate** indicators of Chinese fund–stock bipartite networks; no manager–stock link events. |
| **GeomHerd (Yang et al., 2026)**, arXiv 2605.11645 · [ABS today] <https://arxiv.org/abs/2605.11645> | Abstract | (paraphrase) | Herding measured by Ricci curvature on *simulated* LLM-agent interaction graphs. **Correction:** the abstract does not mention a 13F graph; the earlier note that its appendix uses 13F overlap is from a PDF search extract and stays [UNVERIFIED]. |

**Gap statement (inferred, partly named).** Izadifar & Rahmati explicitly point to "less persistent prediction problems" and a larger manager universe as next steps; entry/exit (edge birth/death) prediction on the full 13F graph with heterogeneous context is that harder problem. No 2025–2026 paper found evaluates it.

### 2.2 Lineage (timeline)

| Year | Work | Status | Step |
|---|---|---|---|
| 1975 | SEC Form 13F introduced (Section 13(f), Securities Exchange Act) | [BG, public record] | Quarterly public holdings |
| 2008–2014 | Herding and common-ownership finance (e.g. Antón & Polk 2014: common ownership predicts co-movement) | [BG, ABS (1 Nov)] | Ownership links explain return co-movement |
| 2013 | 13F XML filings start (SEC data sets from 2013 Q2) | [SEC page reached today] | Machine-readable holdings |
| 2022 | Poursafaei et al., EdgeBank / DGB | [BG] | Memorisation baselines for temporal edges |
| 2023 | Crowding signals from holdings networks (arXiv 2306.08105) | [BG, SNIP (2 Nov)] | Graph-based crowding measures |
| 2024 | Thomaz & Mauá, next-portfolio prediction (N-PORT) | [BG, FT (1 Nov)] | New-position prediction as recommendation |
| 2026 | Izadifar & Rahmati: TGB node-affinity benchmark on 13F | [FT today] | Levels are persistence-dominated |
| **Now** | — | — | Births/deaths on the full, heterogeneous 13F graph unevaluated |

### 2.3 Related gaps in neighbouring fields that transfer

- **Temporal link prediction under repeated edges.** In the 13F sample, 40 % of entries are re-entries (computed today, see §4): exactly the "repeated vs new edge" problem of TGB/TGB-Seq and the 2026 count-baseline papers (Qarkaxhija & Scholtes 2026 [ABS]; Yu & Ha 2026 [ABS]). *Transfer:* EdgeBank-style re-entry memory and smoothed counts are mandatory baselines; first-time entries are the headline metric.
- **Sequential recommendation** (next-item prediction): manager → stock entries are "next items"; collaborative filtering and session models are natural baselines that graph papers often omit.
- **Heterogeneous temporal graph benchmarks** (TGB 2.0 "thg" datasets [BG]): provide loaders/evaluators for multi-relation temporal graphs; none is financial.
- **Dynamic-graph anomaly detection** (BAG 2026 [ABS]): coordinated entries/exits of many managers in one stock are edge-burst anomalies (optional chapter from card B-2).

### 2.4 Who is working on it (kill-test evidence)

- **Groups / venues:** Amirkabir University (Izadifar & Rahmati; presented at the McGill/Mila Temporal Graph Learning Reading Group on 28 Oct 2026, per its page seen today); TGB team (benchmarks); finance groups on herding/crowding (journal-heavy, regression-based).
- **Is anyone close?** Izadifar & Rahmati are the obvious group to extend their benchmark to changes; the reading-group talk shows visibility. Not announced.
- **Searches run today:** `predicting institutional investor new positions 13F initiation exit machine learning graph 2026` (extended) → Izadifar & Rahmati (abs, HTML, Pith summary), TGL reading-group page, and practitioner tools (sec-api.io, VertData, FinzData: descriptive trackers and factor recipes, no ML prediction of entries); `SEC Form 13F data sets download quarterly sec.gov structured data` → SEC data-set pages (data access). Earlier: `thesis-attempt-2` Phase 3 query 3 and 7; `thesis-proposals/sweep/kill_K2.md` (I5, I6). **Verdict: survives (weakened only by the 2026 benchmark, which this extends).**

---

## 3. Literature background

### 3.1 What you need to understand the problem
- **Form 13F mechanics**: who files, what is reported (long positions in 13(f) securities, no shorts), 45-day lag, amendments (13F-HR/A), confidential treatment; CUSIP identifiers.
- **Institutional investor behaviour**: herding, momentum trading, style persistence, window dressing, common ownership (Antón & Polk 2014 [BG]).
- **Temporal heterogeneous graphs and link prediction**: discrete-time snapshots, HGT/R-GCN with GRU, TGN-style memory models; negative sampling vs all-entity ranking.
- **Recommendation baselines**: popularity, item-kNN, matrix factorisation.
- **Evaluation pitfalls**: persistence dominance, repeated vs new edges, look-ahead via filing dates, survivorship in the stock universe.

### 3.2 State of the art closest to the solution, and the difference

| Paper | What it does | How this thesis differs |
|---|---|---|
| Izadifar & Rahmati 2026 [FT] | Weight (affinity) forecasting, 99 managers, TGB models, persistence nearly wins | Births/deaths as targets; top-N managers (not a random 99); heterogeneous context (stock–stock co-movement, manager overlap); first-time vs re-entry scoring |
| Thomaz & Mauá 2024 [BG, FT (1 Nov)] | Next-portfolio prediction for mutual funds | Graph-based, heterogeneous, temporal; 13F managers; economic check |
| Frontiers in AI 2026 [ABS] | Aggregate network indicators (China) | Manager–stock level, US public data |
| TGB / TGM models (TGN, DyGFormer, GraphMixer) [BG; code cloned] | Generic temporal link prediction | Applied with all-entity ranking on a new domain |
| Qarkaxhija & Scholtes 2026 [ABS] | Smoothed-count baselines beat EdgeBank | Used as baselines; tests "counts win" on ownership graphs |

---

## 4. Data and access

| Dataset | What it is | Existing / formable | Size | Licence / terms | Cost | Access test (6 Nov 2026) | Rating |
|---|---|---|---|---|---|---|---|
| **SEC Form 13F data sets** | Flattened XML extracts of all 13F filings (SUBMISSION, COVERPAGE, INFOTABLE, SIGNATURE, …) | Existing | One ZIP per quarter, 35–95 MB (2013 Q2 → "2026 March April May", 94.81 MB) | US public domain | Free | SEC data-set page **reached via search** (`sec.gov/about/dera_form-13f`, last updated 31 May 2026; data.gov catalogue lists Dec 2025–Feb 2026). Shell download **403** → download on laptop | Easy |
| **13F benchmark sample** (`e-izdfr/portfolio-holdings-prediction`) | Preprocessed 99-manager × 503-stock edge list, CUSIP↔ticker matching tables, node features | Existing | 88 MB repo; 209,351 edges, 48 quarters 2013 Q2–2025 Q1 | MIT | Free | **Cloned OK** (commit 2026-07-04). Ran `tools/13f_sample_events.py`: per quarter on average **522 entries, 361 exits, 3,932 continuing positions, 540 increases > 25 %, 479 decreases > 25 %**; 11.7 % of next-quarter positions are entries; exit rate 8.4 %; **39.5 % of entries are re-entries** | Easy |
| CUSIP → ticker/CIK mapping | Needed to join holdings with prices | Formable (SEC "Official List of 13(f) Securities"; the sample repo's `matching.csv`, `figi_to_cusip.xlsx`) | — | public / MIT | Free | Sample mapping files present in the cloned repo | Medium |
| Point-in-time index membership (`fja05680/sp500`) | Stock universe | Existing | 14 MB | MIT | Free | **Cloned OK** | Easy |
| Prices + FF5 factors | Stock–stock edges, economic check | Formable / existing | as Proposal 1 | as Proposal 1 | Free | FF5 downloaded; prices on laptop | Medium |
| Optional: Thomson/Refinitiv s34 via WRDS | Cleaned 13F | Licensed | — | UU licence? | — | Not on UU's WRDS list as checked on 2 Nov (only Compustat, Fama–French, S&P DJI noted) → **assume unavailable** | Hard |

**Minimum viable dataset:** the 99-manager sample (already cloned) for the pilot; then top-500 managers by reported value × point-in-time S&P 500, 2013 Q2–2026 Q1 (~52 quarters) from the SEC data sets. **Fallback:** stay with the published sample (smaller, but directly comparable to the 2026 benchmark).

---

## 5. Approach and 30-week plan

**Research question.** *Can a temporal heterogeneous graph model of institutional ownership predict next-quarter position entries and exits better than persistence, re-entry memory, popularity and recommendation baselines, and does heterogeneous context (stock co-movement, manager overlap) help?*
- **SQ1.** How well can first-time entries, re-entries and exits be predicted, compared with count-based and recommendation baselines?
- **SQ2.** Does adding stock–stock co-movement edges and manager–manager overlap edges improve prediction (ablation), and for which manager types (size, turnover, style)?
- **SQ3 (secondary).** Do aggregate predicted entries/exits per stock carry information about next-quarter abnormal returns, turnover or volatility (out of sample)? *(Optional SQ4: are coordinated, unexpected entries/exits detectable as anomalies?)*

**Pipeline.** SEC 13F ZIPs → clean INFOTABLE (13F-HR + amendments; aggregate sub-managers; filter share class) → CUSIP mapping → quarterly holdings tensor → event labels (with first-time vs re-entry flag) → stock–stock and manager–manager edges (trailing data only) → models → all-entity ranking evaluation → economic check → manager radar dashboard.

**Existing code to build on (checked today):** `e-izdfr/portfolio-holdings-prediction` (MIT; 13F preprocessing, TGB node-affinity setup, NAVIS and baselines); `shenyangHuang/TGB` (MIT; evaluators, thg loaders); `tgm-team/tgm` (MIT; TGN, DyGFormer, GraphMixer); `yule-BUAA/DyGLib` (MIT); PyTorch Geometric heterogeneous modules (HGT, HeteroConv; not cloned today). To build: event labeller, all-entity evaluator, re-entry-aware baselines, ablation harness, economic test, dashboard.

**Baselines.** Persistence (no change); re-entry memory (EdgeBank-style: rank stocks previously held); smoothed counts; stock popularity (entries by all managers last quarter); manager-style kNN / matrix factorisation; LightGBM on manager, stock and pair features (momentum, size, past flows, overlap with similar managers).

**Metrics.** Entry ranking: all-entity MRR, Recall@10/50 per manager, reported separately for first-time entries and re-entries; exits: AUPRC, calibration; five-class macro-AUPRC; for SQ3, portfolio sorts and Fama–MacBeth t-statistics with Newey–West errors.

**Splits.** Walk-forward by quarter: train 2013 Q2–2020 Q4, validate 2021, test 2022 Q1–2026 Q1; inputs restricted to filings with filing date before the prediction date; stock universe point-in-time.

**Week-by-week plan**

| Weeks | Phase | Work | Output |
|---|---|---|---|
| 1–4 | Phase 1 | Literature (13F, herding, temporal heterogeneous LP, recommendation baselines) | `lit_review.md` |
| 5–6 | Phase 1 | Pilot on the cloned 99-manager sample: persistence, re-entry memory and LightGBM for entries/exits | Pilot table |
| 7–8 | Phase 1 | Proposal; decide manager universe | **Go/no-go** |
| 9–12 | Phase 2 | Full SEC 13F pipeline (top-500 managers), mapping, labels | Data chapter |
| 13–16 | Phase 2 | Baselines + recommendation models | SQ1 baselines |
| 17–21 | Phase 2 | Temporal / heterogeneous GNNs; ablations (SQ2) | SQ1–SQ2 results |
| 22–23 | Phase 2 | Economic check (SQ3); optional anomaly chapter | SQ3 results |
| 24–25 | Phase 2 | Manager radar | Artefact |
| 26–30 | Writing | Thesis | Thesis |

**Usable artefact.** *Manager radar:* per manager, the stocks it is most likely to enter or exit next quarter, with the evidence (similar managers who already entered, correlated stocks it holds, its past re-entries); per stock, predicted net institutional demand next quarter and which manager types drive it.

---

## 6. Feasibility verdict

**Top 3 risks and mitigations**
1. **Persistence and re-entry dominance (novelty/evaluation).** 40 % of entries are re-entries, which memory baselines catch easily. *Mitigation:* first-time entries as the headline metric; report everything against re-entry memory and counts; a finding that heterogeneous context does or does not help first-time entries is clear either way.
2. **Data cleaning (data/scope).** Amendments, sub-manager aggregation, CUSIP changes and confidential treatment complicate the raw SEC data. *Mitigation:* reuse the 2026 benchmark's mapping code; start with the top-500 managers and S&P 500 stocks; document every cleaning rule.
3. **Quarterly resolution: only ~52 time steps (evaluation).** *Mitigation:* many (manager, stock) events per quarter (≈ 500 entries per quarter already in the 99-manager sample, far more at 500 managers); walk-forward evaluation over 17 test quarters with bootstrap CIs.

**Minimum thesis (fallback).** Entry/exit prediction on the published 99-manager sample with re-entry-aware baselines, LightGBM, one temporal GNN and one heterogeneous ablation; directly comparable to the 2026 benchmark.

**Ethics / GDPR.** Most 13F filers are legal persons, but some are individuals or family offices, and the SIGNATURE table lists signatory names and phone numbers: **drop the SIGNATURE and other-manager name fields**, pseudonymise filers that are natural persons, report results in aggregate. Not investment advice. Disclose generative-AI use.

**Scores (briefing §9)**

| Criterion (weight) | Score | Weighted | Reason |
|---|---|---|---|
| Novelty (×3) | 4 | 12 | Named next step of a July-2026 benchmark; births/deaths unevaluated |
| Supervisor fit (×2) | 4 | 8 | Heterogeneous temporal LP; investor–company graphs like her Crunchbase work; less "stock-to-stock" than her notes |
| Data (×2) | 5 | 10 | Cleanest free data of the five; sample verified today (earlier: 4) |
| Feasibility (×2) | 4 | 8 | Benchmark code exists; cleaning work is known |
| Evaluation clarity (×1) | 5 | 5 | Exact labels, chronological, base rates known (earlier: 4) |
| AI relevance (×1) | 4 | 4 | Temporal heterogeneous LP, recommendation vs GNN |
| Artefact (×1) | 4 | 4 | Manager radar |
| Industry (×1) | 4 | 4 | Asset management, capital markets, IR |
| Frank's interests (×1) | 3 | 3 | Markets yes; less XAI/politics |
| **Total** | | **58 / 70** | (earlier A-1: 55; raised after the sample check) |

---

## 7. Questions for the supervisor

1. Is an ownership (manager–stock) graph acceptable as a "stock network" for this thesis, given that your notes emphasise stock-to-stock influence?
2. Is predicting edge births/deaths "non-standard" enough, or should the heterogeneous model itself be the contribution?
3. Would a recommendation-system framing (first-time entries as next items) be welcome, or should it stay within temporal graph learning?
4. Does UU have Thomson/Refinitiv 13F (s34) or another cleaned holdings source? (UU's WRDS list did not show it on 2 Nov.)
5. Any lessons or code from your venture-capital (Crunchbase) investor–company graph projects?
