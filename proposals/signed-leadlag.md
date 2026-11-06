# Proposal 1: When do influence links between stocks switch on, off or flip?
## Forecasting the state of signed, directed lead-lag edges, with a re-evaluation of the 2026 state of the art

*Feasibility dossier, 6 Nov 2026. Merges earlier cards C-1 + D-1 (`thesis-attempt-2`) and Card 3 + I2/I25 (`thesis-proposals`, incl. `deep_dive_idea3.md`).*
*Legend: [FT] full text opened · [ABS] abstract/record only · [SNIP] seen only as a search-result excerpt · [UNVERIFIED] not opened · [BG] pre-2025 background. "(2 Nov)" = opened in an earlier session, not re-opened today. Numbers must be re-checked in the PDFs before thesis use.*

Supervisor directions hit: **signed, time-activated influence edges + time series** (her capitalised point) · **link prediction** · temporal graphs · (optional) anomaly detection via sign-flip surprise.

---

## 1. The problem in plain language

Stocks do not move independently. Sometimes one stock moves first and another follows a day or a few days later. If Shell jumps because oil got more expensive, an oil-services supplier may rise two days later: a **positive (+)** link. The same oil move may push airline stocks *down* two days later, because their fuel bill goes up: a **negative (−)** link. Analysts call these **lead-lag relationships**. You can draw the whole market as a map of arrows: "A → B, +, two days".

The catch is that this map is not fixed. A link that worked last quarter can disappear this quarter, a new one can appear, and occasionally a link flips sign (two firms that used to move together start moving against each other, for example after one buys the other's competitor). Finance research has shown that lead-lag effects exist and that they change over time. What nobody has done is treat the *change itself* as the thing to predict: **"next month, will the link from A to B still be there, will it vanish, will a new one appear, and will its sign flip?"**

Why it matters:
- **Investors and quant teams** use lead-lag links for trading and hedging. A hedge built on a link that is about to switch off, or flip sign, does the opposite of what it should.
- **Risk managers and regulators** care about how shocks travel through the market. A map that knows which channels are about to open is a better early-warning tool than one that just copies last month.
- **Machine-learning research** has new models (2026) built precisely for networks with + and − links that change over time, but they have only been tested on Bitcoin trust ratings and Wikipedia votes. Stock markets are a harder, real test.

A concrete example: *when NVIDIA drops sharply, does AMD follow two days later, and can we predict the month in which that link stops working, or turns negative?*

There is an honest twist. The simplest forecast, "next month looks like this month" (**persistence**), is often very hard to beat. Recent work on other networks found that this lazy rule sometimes beats every deep model. Part of this thesis is therefore checking whether the 2026 state of the art for lead-lag link prediction actually learns lead-lag, or mostly learns *which stocks are volatile*.

### 1.1 Technical formulation

- **Universe.** Point-in-time S&P 500 constituents (daily membership list), daily total returns 2000–2026. Residual returns e_i(t) after removing Fama–French 5 factors (or market + sector-ETF returns), estimated on a trailing window only.
- **Edge construction (per formation date t).** On the trailing window [t−W, t] (W ≈ 120 trading days) compute, for every ordered pair (i, j) and lag ℓ ∈ {1,…,L} (L = 5), the lagged correlation ρ_ij(ℓ) = corr(e_i(s), e_j(s+ℓ)). Test H0: ρ_ij(ℓ) = 0 for all pairs and lags with a block-bootstrap or Fisher-z test and control the false discovery rate at q (Benjamini–Hochberg over all N(N−1)L tests). The edge state is s_ij(t) ∈ {+, −, 0}: the sign of the most significant lag if any lag survives FDR, else 0; ℓ*_ij(t) is stored as an edge attribute. Alternatives compared, not assumed: Granger tests, Lévy-area lead-lag, the anchor's thresholded co-exceedance.
- **Prediction target (no overlap).** The label for formation date t is the state computed on the **next, non-overlapping** block (t, t+H] with H = W, so labels never share data with features. Test origins step by H.
- **Task.** Given the signed directed snapshot sequence G(t_1),…,G(t) (plus node features from data ≤ t), predict P(s_ij(t+H) = c), c ∈ {+, −, 0}, for all ordered pairs. This is **3-class dynamic signed link prediction** (as in IDP-DSN), evaluated *conditionally on the current state*: persist (s→s), birth (0→±), death (±→0), flip (+↔−).
- **Re-evaluation sub-task (WP1).** On the anchor's public 37-asset dataset (Krstev et al. 2026), re-score its binary temporal link prediction under EdgeBank, time-decay PPR, smoothed-count, degree and volatility-only baselines, historical/inductive negatives and all-entity ranking.

---

## 2. Where the problem comes from

### 2.1 Papers that name the gap

| Paper (status, venue) | Section | Short quote (< 15 words) | What exactly is missing, in my words |
|---|---|---|---|
| **Regier, Polyak, Dadlani & Salmani (2026)**, *Dynamic Link Prediction with Temporally Enhanced Signed GNNs* (HCIM), arXiv 2605.26290, preprint · [FT today] <https://arxiv.org/abs/2605.26290> | VI.B Future Research Directions | "Existing real-world datasets are largely restricted to cryptocurrency and social network domains" | Temporal signed-network learning has no benchmark outside trust/social data; the authors explicitly list "market dynamics in financial networks" as a signal to add and call for "standardized benchmark datasets". Their own evaluation excludes non-edges (sign only), so joint existence + sign on real data is open. |
| **Hou, Huang, Ran & Jia (2026)**, *IDP-DSN*, SIGIR 2026 (peer-reviewed), arXiv 2604.18213 · [FT today] <https://arxiv.org/abs/2604.18213> | 6 Conclusion and Future Work | "scaled to larger real-world datasets and extended to heterogeneous signed interactions" | The 3-class {+, −, none} model has only been run on BitcoinAlpha/OTC, Wiki-RfA and Epinions; 13 baselines, **no persistence or EdgeBank baseline**. A market graph is a larger, real, non-social test. |
| **Krstev, Rigoni, Mishkovski & Pasa (2026)**, *A Temporal Graph Learning Framework for Lead-Lag Detection in Financial Markets*, *Machine Learning* 115(7):173 (peer-reviewed; received 15 Jan, accepted 29 Jun, online 8 Jul 2026, CC BY 4.0, per Crossref checked today; first public Oct 2025 on OpenReview) · [FT (2 Nov); Springer and OpenReview blocked today] <https://doi.org/10.1007/s10994-026-07113-y> | Conclusion / future work | (no verbatim quote available today; read on 2 Nov) | Authors name **larger datasets**, other domains and **interpretability** as future work, and warn that results may reflect the volatility of specific stocks. Gap I infer from the paper: 37 assets, edges = both moves > 5 % one day apart (no significance test), opposite-direction influence not modelled, one random negative per positive, no memorisation/persistence baseline. |
| **Zhou, Wang, Cucuringu et al. (2025)**, *DeltaLag*, ICAIF 2025 (peer-reviewed), arXiv 2511.00390 · [FT partial today: conclusion truncated] <https://arxiv.org/abs/2511.00390> | 1 Introduction | "assume temporal stability in lead-lag relationships" | Prior lead-lag models treat links as stable although they are "often transient and regime-dependent". DeltaLag learns dynamic leader–lag pairs but only to **predict returns**; it never evaluates the edges or their stability, and edges carry no sign. |
| **Qarkaxhija & Scholtes (2026)**, *Do Temporal Link Predictors Need Learned Memory?*, arXiv 2609.35364, preprint · [ABS today] <https://arxiv.org/abs/2609.35364> | Abstract | "With only 9--13 learned parameters" | A count-based predictor beats EdgeBank on all 16 TGB/TGB-Seq datasets and wins MRR on 7: learned memory is often not needed. No financial dataset is in TGB, so whether this holds for market graphs is unknown. |
| **Yu & Ha (2026)**, *Back to All-Entity Ranking*, arXiv 2607.27861, preprint · [ABS today] <https://arxiv.org/abs/2607.27861> | Abstract | (paraphrase only) | Model orderings flip between sampled-negative and full-catalogue evaluation; they recommend all-entity ranking when the catalogue is small and fixed. A stock universe is exactly that, and the anchor used one random negative. |
| **Roy & Dasgupta (2026)**, *SiST-GNN*, arXiv 2605.25548 · [FT (2 Nov)] | Results / discussion | (paraphrase only) | Copying the last snapshot beat every learned model on UCI-Message; authors recommend always reporting persistence. |
| **Izadifar & Rahmati (2026)**, 13F holdings benchmark, arXiv 2607.12067 · [FT (2 Nov)] | Results | (paraphrase only) | On a financial temporal graph, persistence (≈ 0.889 NDCG@10) is within 0.03 of the best model and beats every other learned model: finance graphs are persistence-dominated, so change-specific scoring is needed. |

**No paper names the exact gap** "forecast the state (+/−/0) of statistically validated, directed lead-lag edges, scored on births/deaths/flips against persistence". It is inferred by joining (a) the signed-temporal GNN papers that ask for real, non-social benchmarks (HCIM, IDP-DSN), (b) the lead-lag ML papers that assume or ignore edge stability (DeltaLag, Krstev), and (c) the 2026 temporal-link-prediction critiques that show simple baselines often win (Qarkaxhija & Scholtes, Yu & Ha, SiST-GNN).

### 2.2 Lineage (timeline)

| Year | Work | Status | Step |
|---|---|---|---|
| 1990 | Lo & MacKinlay: large stocks lead small ones | [BG, UNVERIFIED: classic, not opened] | Lead-lag between stocks as an economic fact |
| 2015 | Curme et al., statistically validated intraday lead-lag networks, *Quant. Finance* | [BG, SNIP] | Per-pair significance test + multiple-testing correction → **validated** edges; most links vanish beyond ~1 hour intraday |
| 2018 | Souza & Aste, predicting future stock-network structure (arXiv 1812.01103) | [BG, SNIP] | Edge insertion/removal in correlation networks is predictable; ~40 % of edges change within 20 weeks (unsigned, undirected) |
| 2021 | Castilho et al., forecasting co-movement edges vs persistence (arXiv 2110.11751) | [BG, FT (1 Nov)] | Link prediction of future co-movement edges with persistence baseline; unsigned, undirected |
| 2022 | Bennett, Cucuringu & Reinert, lead-lag clustering, *Machine Learning* 111 | [BG, ABS via search today] | Directed lead-lag networks of US stocks; low year-to-year cluster similarity |
| 2022 | He et al., MSGNN + FiLL signed directed lead-lag graphs (LoG 2022) | [BG, SNIP] | **Static yearly** signed directed lead-lag graphs used for link/sign prediction |
| 2022 | Raghavendra et al., SEMBA, dynamic signed networks (arXiv 2207.03408) | [BG, ABS via search today] | Defines dynamic signed link *existence + sign* prediction; notes no prior work on it |
| 2023 → 2026 | Cartea, Cucuringu & Jin, *Detecting lead–lag relationships in stock returns and portfolio strategies* (SSRN 4599565, 2023; *J. Empirical Finance* 89:101775, Nov 2026) | [Crossref record opened 6 Nov; full text not reachable (SSRN, ScienceDirect blocked); finding via SNIP] | Leader/follower roles change several times over 1963–2022; now peer-reviewed, statistical (no edge forecasting) |
| Oct 2025 | Krstev et al. (ICLR'26 submission → *Machine Learning* Jul 2026) | [FT (2 Nov)] | Lead-lag as **temporal link prediction** with TGNNs (37 assets, unsigned) |
| Nov 2025 | DeltaLag (ICAIF'25) | [FT partial] | Dynamic, pair-specific lags learned end-to-end; edges as means, not targets |
| 2026 | IDP-DSN (SIGIR'26), HCIM (May 2026) | [FT] | Modern 3-class dynamic signed link prediction, social/trust data only |
| 2026 | Qarkaxhija & Scholtes; Yu & Ha; Fei et al. (PPR); SiST-GNN | [ABS]/[FT (2 Nov)] | "Simple baselines often win" evaluation wave in temporal link prediction |
| **Now** | — | — | Nobody forecasts signed lead-lag edge *states* on a realistic equity universe; no signed temporal stock benchmark exists |

### 2.3 Related gaps in neighbouring fields that transfer

- **Temporal-graph benchmarks without finance.** TGB / TGB 2.0 / TGB-Seq contain no equity dataset (checked in the cloned `shenyangHuang/TGB` repo, `tgb/utils/info.py`: tgbl-coin, -comment, -enron, -flight, -lastfm, -review, -subreddit, -uci, -wiki; tgbn-genre, -reddit, -token, -trade, i.e. social, e-mail, music, review, flight, trade and crypto-token data). *Transfer:* the signed lead-lag stream is a ready new benchmark, and the "beat counts first" protocol (Qarkaxhija & Scholtes 2026; Ahmed & Shafi 2026, SimpleCount [ABS (2 Nov)]) carries over directly.
- **Evaluation critiques of temporal link prediction** (Yu & Ha 2026; Fei et al. 2026, time-decay PPR [ABS (2 Nov)]). *Transfer:* all-entity ranking is cheap for 500 stocks; PPR and EdgeBank become mandatory baselines.
- **Structural balance in signed market networks** (Dahake & Chakraborty 2026, S&P 500 balance drops in crises [ABS (2 Nov)]; Qing & Xu 2025/ESWA 2026, statistically validated signed stock networks [ABS (2 Nov)]). These are descriptive and contemporaneous. *Transfer:* triad-balance and lag-cycle consistency become features and a rule baseline for *forecasting* directed lagged signs.
- **Causal discovery on time series** (PCMCI, neural Granger; see `thesis-proposals` T6). *Transfer:* Granger/PCMCI edges are an alternative edge definition; FDR-controlled Granger networks are a 2025 statistics topic (Uematsu & Yamagata, *JASA* 2025 [SNIP]).

### 2.4 Who is working on it (kill-test evidence)

- **Groups:** Oxford-Man / UCLA (Cucuringu: lead-lag clustering, DeltaLag, Cartea et al.); Padova / Skopje (Krstev, Pasa: TGNN lead-lag, from an MSc thesis at Padova, `thesis.unipd.it` record seen today); signed-GNN groups in China (IDP-DSN) and Canada (HCIM); TGB group (McGill/Mila) for benchmarks.
- **Venues:** *Machine Learning*, ICAIF, SIGIR, LoG, arXiv q-fin.ST / cs.LG.
- **Is anyone close?** Krstev et al. are closest (same task family) and could extend to signs and more assets; their paper does not announce it. Cucuringu's line could add learning-based forecasting of edges. No preprint found that does it.
- **Searches run today (6 Nov 2026):** `forecasting signed lead-lag network edges stocks sign flip prediction 2026` (extended) → nothing on edge-state forecasting; returned CGLR (ESWA 2025, return prediction), Cross-stock LLM semantic networks (arXiv 2604.19476), robust lead-lag detection (Applied Math. Finance 2025, statistical); `dynamic signed graph neural network stock market dataset positive negative edges temporal link prediction` → only HCIM, IDP-DSN, SEMBA, DynamiSE (*MLJ* 2024), all non-financial; `Cartea Cucuringu Jin … Journal of Empirical Finance 2026` → SSRN 2023 version and Jin's Oxford DPhil thesis; the **JEF 2026 version is confirmed via Crossref** (vol. 89, article 101775, Nov 2026) but its text could not be opened; it is a statistical detection/portfolio paper, so it does not forecast edge states. Earlier kill tests (`thesis-proposals/sweep/kill_K1.md`: 13 searches + 2 OpenReview queries; `thesis-attempt-2/NOTES.md` Phase 3 queries 1 and 5) found the same. **Verdict: survives.**

---

## 3. Literature background

### 3.1 What you need to understand the problem
- **Lead-lag and slow information diffusion** (Lo & MacKinlay 1990 [BG]; Cartea et al. 2023 [BG]): why followers exist (attention, size, analyst coverage) and why links fade once exploited.
- **Residual returns and factor models** (Fama–French 5 factors; free data library, access test below). Without residualising, every edge is "the market moved".
- **Statistically validated networks** (Curme et al. 2015 [BG]): one test per pair and lag, then FDR control (Benjamini–Hochberg 1995 [BG]).
- **Signed networks and structural balance** (Heider/Cartwright–Harary [BG]): "the friend of my enemy is my enemy" as a triangle rule.
- **Temporal graph learning**: continuous-time models (TGN, TGAT, GraphMixer, DyGFormer) and their benchmarks (TGB [BG]); memorisation baseline EdgeBank (Poursafaei et al. 2022 [BG]).
- **Dynamic signed link prediction**: SEMBA (2022 [BG]) defines existence + sign; IDP-DSN (2026) is the current 3-class model.

### 3.2 State of the art closest to the solution, and the difference

| Paper | What it does | How this thesis differs |
|---|---|---|
| Krstev et al. 2026 (*MLJ*) [FT (2 Nov)] | TGNN binary lead-lag LP, 37 assets, threshold edges, one random negative, GraphMixer AP ≈ 0.79 | Signed 3-class **state** target; FDR-validated residual edges; ~500 point-in-time stocks; births/deaths/flips scored separately; persistence, EdgeBank, PPR, count and volatility baselines; WP1 re-tests their claim on their own data |
| IDP-DSN 2026 (SIGIR) [FT] | 3-class dynamic signed edge prediction with sign-selective memories | First application to market data; adds persistence baselines; uses it as one model among several, not as the contribution |
| HCIM 2026 [FT] | Temporal memory on a signed graph transformer; sign-only evaluation | Joint existence + sign; real data; answers their call for non-social benchmarks |
| DeltaLag 2025 (ICAIF) [FT partial] | Learns dynamic lead-lag pairs to predict returns | Edges are the *target*, with sign and validation; returns only in an optional economic check |
| Fanshawe et al. 2026 [FT (2 Nov)] | Forecasts signed pairwise correlations (S&P 500, WRDS) | Directed and lagged rather than contemporaneous; discrete state changes rather than a number; free data |
| Qarkaxhija & Scholtes 2026 [ABS] | Smoothed-count TLP baseline beats EdgeBank everywhere | Used as a mandatory baseline; tests whether "counts win" also holds on market graphs |

---

## 4. Data and access

| Dataset | What it is | Existing / formable | Size | Licence / terms | Cost | Access test (run 6 Nov 2026) | Rating |
|---|---|---|---|---|---|---|---|
| Krstev et al. lead-lag data (`ivankrstev7/Temporal_Graphs_Lead_Lag_Data`) | Daily prices, indicators and CityFalcon sentiment for 29 stocks + 8 commodities, Jun 2019–Jun 2024 | Existing | 13 MB | **No licence file** in repo (paper itself is CC BY 4.0) → ask authors before redistributing | Free | **Cloned OK** (last commit 2026-07-12). Found: `stocks.csv` lists 29 stocks but the price files hold only **23**: the five oil majors (XOM, CVX, COP, EOG, SLB) and FMG are missing (indicator files have 28, sentiment 29). Prices for these six are easy to re-source from free data, but the authors should confirm which data the paper used | Easy |
| Anchor code (`ivankrstev7/temporal_graph_lead_lag_detection`) | TGL + GraphMixer notebooks | Existing | 23 MB | No licence file | Free | **Cloned OK** (last commit 2026-01-14) | Easy |
| Point-in-time S&P 500 membership (`fja05680/sp500`) | Daily constituent lists since 1996, change log since 2019, CIK per current member | Existing | 14 MB | MIT | Free | **Cloned OK** (last commit 2026-09-07); daily rows from 1996-01-02, delisted tickers carry suffixes (e.g. `AAMRQ-201312`) | Easy |
| Fama–French 5 factors, daily | Factor returns for residualising | Existing | 0.15 MB | Free academic data library | Free | **Downloaded from the shell** (HTTP 200): 1963-07-01 → **2026-09-30** | Easy |
| Daily prices of current + delisted constituents | Returns for ~1,100 tickers that were ever in the S&P 500 since 2000 | Formable | ~1,100 × 6,500 days ≈ 7 M rows | Stooq: free; yfinance: unofficial API, terms unclear; LSEG Workspace / FactSet via UU financedata@uu.nl | Free (Stooq/yfinance); UU licence | From this cloud session: Yahoo API **HTTP 429**, Stooq **blocked** (shell), web fetch to Stooq needed an approval nobody answered → **not testable here; test on Frank's laptop**. UU WRDS has **no CRSP** (deep dive, 2 Nov) | Medium (delisted coverage is the risk) |
| Sector-ETF prices (SPDR XL*) | Sector factor for residuals | Formable (same sources) | 11 series | as above | Free | as above | Easy |
| Signed temporal benchmarks (BitcoinAlpha/OTC, Wiki-RfA, Epinions) | Sanity check for IDP-DSN | Existing (shipped via IDP-DSN / PyG Signed Directed) | small | research use | Free | `codewhisperer-rs/IDP-DSN` and `SherylHYX/pytorch_geometric_signed_directed` **cloned OK** | Easy |

**Minimum viable dataset:** S&P 100 point-in-time members, 2005–2026, daily prices from Stooq/yfinance, FF5 factors → about 100 × 99 × 5 tests per window, ~40 non-overlapping 6-month blocks. **Fallback:** current S&P 500 members only (survivor-biased), with the bias measured on the subset where delisted prices are available; or weekly returns, or same-day signed residual-correlation edges (denser).

---

## 5. Approach and 30-week plan

**Research question.** *Can the future state (positive, negative, absent) of statistically validated, directed lead-lag edges between stocks be predicted better than persistence, in particular births, deaths and sign flips, and which signals carry that predictability?*
- **SQ1 (WP1, re-evaluation).** On the anchor's public data, does GraphMixer's advantage survive EdgeBank, time-decay PPR, smoothed counts, a volatility-only score, historical/inductive negatives and all-entity ranking?
- **SQ2 (forecasting).** On a point-in-time S&P 500 universe, do dynamic signed GNNs (IDP-DSN) and temporal GNNs beat persistence, activation-frequency, triad-balance and gradient-boosting baselines on births, deaths and flips?
- **SQ3 (structure and meaning).** Do edge history, triad balance, lag-cycle consistency and sector/size features explain which edges persist; are predicted flips concentrated in particular regimes (2008, 2020, the 2025 tariff windows)?

**Pipeline.** prices → residual returns (trailing-window factor betas) → per-block lagged correlations for all ordered pairs and lags → FDR → signed directed snapshot with lag attribute → labels on the next non-overlapping block → models → change-specific evaluation → explorer dashboard.

**Existing code to build on (all checked by cloning today):**
- `ivankrstev7/temporal_graph_lead_lag_detection` (anchor; TGL + GraphMixer) for WP1.
- `tgm-team/tgm` (MIT, commit 2026-09-21; ICLR 2026) and `yule-BUAA/DyGLib` (MIT, last commit 2023-09) for TGN/TGAT/GraphMixer/DyGFormer and EdgeBank.
- `codewhisperer-rs/IDP-DSN` (no licence file; commit 2026-04-26) for the 3-class dynamic signed model.
- `SherylHYX/pytorch_geometric_signed_directed` (MIT, commit 2026-09-03) for static signed/directed GNNs (SGCN, SDGNN, MSGNN) and signed datasets.
- `shenyangHuang/TGB` (MIT) for evaluators.
- To build: residual-return and FDR edge pipeline (statsmodels/scipy), point-in-time universe handling, persistence/balance/count/PPR baselines (small), change-specific evaluator, dashboard (Streamlit or Dash).

**Baselines.** Persistence; activation frequency (share of past blocks with the same state); EdgeBank (∞ and time-window); smoothed counts (Qarkaxhija & Scholtes style); time-decay PPR; volatility-only (rank by recent |residual return| of leader × follower); triad-balance sign rule; logistic regression / LightGBM on pair features.

**Metrics.** Per-transition AUPRC and macro-F1 (persist / birth / death / flip), all-entity MRR for "who will follow A next block", calibration (Brier, reliability), all with bootstrap confidence intervals over blocks and 5 seeds; Friedman + post-hoc tests across models. Report the share of edges in each transition class (base rates) next to every number.

**Splits.** Walk-forward: train 2005–2016, validate 2017–2019, test 2020–2026 (covers COVID, 2022 rate shock, 2025 tariffs). Factor betas, FDR thresholds and scalers fitted on trailing data only; non-overlapping label blocks; an embargo gap of one block between train and test.

**Week-by-week plan** (assumes start in late Nov 2026 and part-time during the Accenture internship from 2 Jan 2027)

| Weeks | Phase | Work | Output |
|---|---|---|---|
| 1–4 | Phase 1 | Literature review (signed/dynamic GNNs, lead-lag finance, TLP evaluation); open the [UNVERIFIED] items (Cartea JEF 2026, MSGNN/FiLL) | `lit_review.md` |
| 5–6 | Phase 1 | **WP1 pilot** on anchor data: reproduce GraphMixer AP; run EdgeBank / volatility / all-entity ranking | Pilot table (strong go/no-go evidence) |
| 7–8 | Phase 1 | Research proposal; data access confirmed (prices incl. delisted) | **Go/no-go** |
| 9–12 | Phase 2 | Edge pipeline on S&P 100 then S&P 500; transition statistics (how often do edges flip?) | Descriptive chapter |
| 13–16 | Phase 2 | Baselines + gradient boosting; change-specific evaluator | Baseline results |
| 17–21 | Phase 2 | TGNNs (TGM) and IDP-DSN; signed heads; seeds | Main results |
| 22–23 | Phase 2 | SQ3: balance/lag-cycle analysis, regime tests (2020, 2022, 2025 tariffs); robustness (weekly returns, edge definitions) | Analysis chapter |
| 24–25 | Phase 2 | "Influence-edge monitor" dashboard | Artefact |
| 26–30 | Writing | Thesis text, figures, reproducibility package | Thesis |

**Usable artefact.** *Influence-edge monitor:* an interactive signed, directed market map (edge colour = sign, hover = lag and strength), with next-block probabilities of switching off or flipping, a history strip per edge, and the baselines' forecasts side by side so an analyst sees where the model disagrees with "nothing changes".

---

## 6. Feasibility verdict

**Top 3 risks and mitigations**
1. **Weak signal at daily frequency (evaluation/novelty).** Lead-lag between large US stocks may be mostly noise at daily horizons (Curme 2015 [BG]; a 2025 A-share study reports effects dissipate at daily level, arXiv 2506.19255 [SNIP]). *Mitigation:* FDR-validated residual edges, weekly returns as a robustness arm, S&P 1500 small caps (where lead-lag is classically stronger), and a clear framing: "can anything beat persistence on changes?" is a valid result either way, and the benchmark itself is a contribution.
2. **Survivorship / data (data).** Free sources miss delisted firms. *Mitigation:* point-in-time membership list (verified), ask UU about LSEG/FactSet, measure the bias on the subset with full data; S&P 100 minimum version is far less affected.
3. **Scope creep across edge definitions and models (scope).** *Mitigation:* fix one primary edge definition at the go/no-go (residual lagged correlation + FDR); others only as a robustness table; at most three learned models.

**Minimum thesis (fallback).** WP1 re-evaluation of the anchor + signed 3-class forecasting on S&P 100 with persistence, counts, balance and LightGBM vs one TGNN and IDP-DSN. This alone answers a clear RQ and is publishable as a short paper.

**Ethics / GDPR.** Company-level price data only; no natural persons. Not investment advice. Disclose generative-AI use (coding) under UU rules. Respect data-source terms (yfinance terms unclear → prefer Stooq or UU-licensed data for the final runs). Ask Krstev et al. before redistributing their unlicensed data.

**Scores (briefing §9)**

| Criterion (weight) | Score | Weighted | Reason |
|---|---|---|---|
| Novelty (×3) | 4 | 12 | No edge-state forecasting found; Krstev is close in task family |
| Supervisor fit (×2) | 5 | 10 | Her capitalised point + link prediction |
| Data (×2) | 4 | 8 | All free; delisted prices the only gap |
| Feasibility (×2) | 4 | 8 | Libraries + anchor code exist; pipeline is standard statistics |
| Evaluation clarity (×1) | 5 | 5 | Clean labels, chronological, persistence bar |
| AI relevance (×1) | 4 | 4 | Temporal/signed GNNs, benchmark rigour |
| Artefact (×1) | 4 | 4 | Influence-edge monitor |
| Industry (×1) | 3 | 3 | Quant/risk relevance; less Accenture-typical |
| Frank's interests (×1) | 4 | 4 | Markets; XAI via explanations of flips; politics via tariff regime test |
| **Total** | | **58 / 70** | |

---

## 7. Questions for the supervisor

1. Is "forecasting edge states" what you meant by signed, time-activated edges, or did you mean a model that *learns* signed edges inside return forecasting (more crowded)?
2. Is a thesis whose first result may be "the 2026 state of the art mostly learns persistence/volatility" welcome, as long as the forecasting part follows?
3. Which edge definition do you find most meaningful: residual lagged correlation + FDR, Granger, or the anchor's threshold rule?
4. Daily or weekly frequency; S&P 500 or S&P 1500? Is a European (AEX/Euronext) robustness check worth the weaker data?
5. Can UU provide delisted US prices (LSEG Workspace / FactSet via financedata@uu.nl)?
6. Would your group's temporal-motif code (LAS-GNN, TAML) be useful here, e.g. for lead-lag triangle motifs?
