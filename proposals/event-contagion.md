# Proposal 3: Which peers move when a firm surprises or defaults?
## Event-conditioned, signed contagion on a public heterogeneous company graph, with explanations of the channel

*Feasibility dossier, 6 Nov 2026. Merges earlier cards A-2 "contagion exposure after credit events, explained counterfactually" (`thesis-attempt-2`) and Card 4 "event-conditioned signed edge activation" + ideas I4, I26, I29 (`thesis-proposals`).*
*Legend: [FT] full text opened · [ABS] abstract/record only · [SNIP] search-result excerpt only · [UNVERIFIED] not opened · [BG] pre-2025 background. "(2 Nov)"/"(1 Nov)" = opened in an earlier session, not re-opened today.*

Supervisor directions hit: **credit default → stock market** (her separate problem) · **heterogeneous graphs** (used for an edge task, not node classification) · **signed, time-activated edges** (an edge "activates" with a sign after an event) · link prediction · time series + graph. Fits Frank's XAI background through relation-level and counterfactual explanations.

---

## 1. The problem in plain language

When a listed company goes bankrupt, has its credit rating cut, or shocks the market with terrible quarterly results, the damage rarely stays inside that one company. Its **suppliers** may lose a big customer. Its **customers** may lose a supplier. Its **competitors** may suffer because investors fear the whole industry is in trouble, or they may *gain* because they can take over market share. Funds that **own both** may sell other holdings to cover losses. Some of these neighbours fall, some rise, most do not react at all.

Finance research has measured these effects **on average**: for example, suppliers of bankrupt firms lose value on average. What a risk manager actually needs is different: *for this event, which specific listed firms will react, in which direction, and through which relationship?* A bank's credit desk, an asset manager with a concentrated portfolio, or a supervisor watching contagion would all like a ranked list, not an average.

The obstacle is data and rarity. Bankruptcies of listed firms are rare (hundreds per decade), and the relationship data that banks use (Compustat customer segments, FactSet supply chains, credit-default-swap prices) is expensive. This thesis turns the problem around: it **learns from frequent events** (every quarter thousands of firms announce earnings, some of them with big surprises) on a graph built from **free public filings**, and then tests whether the learned "who reacts to whom" model transfers to the rare credit events.

Concrete example: *A large retailer files for Chapter 11. Which of its listed suppliers fall over the next five days, which competitor rises, and is the supplier's drop explained by "the retailer was 15 % of its revenue" or by "the same five funds own both"?*

Why it matters:
- **Credit and counterparty risk** teams (and consultancies building risk tools) need event-time exposure lists.
- **Supervisors** (ECB, Fed, ESMA) monitor contagion channels; knowing *which* channel carries the shock is a policy question.
- **AI research**: event-conditioned prediction on heterogeneous graphs with explanations that can be checked against an economic ground truth is rare; 2026 counterfactual explainers for temporal graphs have not been tried on financial data.

### 1.1 Technical formulation

- **Graph.** A heterogeneous, slowly time-varying company graph G(t) = (V, {E_r(t)}) with node type firm (optionally fund, sector) and relation types r ∈ {same SIC/GICS industry, common 13F ownership (overlap of top holders), 10-K-disclosed customer/supplier/competitor/partner (FinReflectKG or LLM extraction), 10-K text similarity, past price lead-lag (from Proposal 1)}. Every edge carries the date it became public (filing date).
- **Events.** Focal event (f, τ, type) with type ∈ {earnings surprise, bankruptcy filing, rating downgrade, severe price shock}; event-level features x_f,τ (event type, surprise size and sign, focal firm size, sector).
- **Candidates.** For each event, candidate peers j ∈ N_k(f) (k-hop neighbours in G(τ⁻), the graph strictly before τ) plus a matched set of unlinked controls.
- **Label.** y_fj,τ ∈ {+, −, 0}: sign of peer j's cumulative abnormal return CAR_j[0, +h] (h ∈ {1, 5}; Fama–French 5-factor model estimated on [−250, −30]) if significant after FDR within event, else 0.
- **Task.** Learn p(y_fj,τ | G(τ⁻), x_f,τ, x_j) → *event-conditioned signed edge activation*. Rank peers per event.
- **Transfer.** Train on earnings events; test zero-shot and fine-tuned on credit events.
- **Explanation.** For each predicted reaction, attribute it to relation types/paths (relation ablation, GNNExplainer/PGExplainer, counterfactual edge deletion); compare with an economic ground truth where it exists (e.g. disclosed major customers).

---

## 2. Where the problem comes from

### 2.1 Papers that name the gap

| Paper (status, venue) | Section | Short quote (< 15 words) | What exactly is missing, in my words |
|---|---|---|---|
| **Xu, Hao, Tang, Chen, Liu, Liu & Zhang (2025)**, *FinRipple*, Findings of ACL 2025 (peer-reviewed), arXiv 2505.23826 · [FT today] <https://arxiv.org/abs/2505.23826> | Limitations | "it relies heavily on highquality, explicit KGs for effective performance" | The closest work: an LLM predicts signed impact on each KG-connected S&P 500 firm after a news item. Its KG is built from commercial sources (Compustat-Capital IQ supply chains, BoardEx, Thomson holdings, USPTO patents); code and benchmark "will" be released later; evaluated on residual alignment and portfolios. A public-graph, credit-event, per-edge-labelled version is open. |
| **Avramov, Ge, Li & Linton (2026)**, *Dual peer effects and cross-stock predictability*, *J. Financial Economics* 180:104274 (peer-reviewed, online 6 Mar 2026) · [FT today, author PDF] <https://doi.org/10.1016/j.jfineco.2026.104274> | 3.5 Dynamic response to PI shocks | "What these tests do not reveal is the time path of price adjustment" | Peer information moves prices across economically linked firms only gradually, but the authors have "not yet established" what news is being transmitted and how prices adjust after a peer surprise. Event-level, link-specific reactions are exactly that question. Uses CRSP/Compustat/IBES (paid). |
| **Kim et al. (2026)**, *DefaultGNN*, ACM venue (DOI 10.1145/3799682.3840153; CIKM 2026 per earlier notes), arXiv 2609.25542 · [ABS today; code repo cloned] <https://arxiv.org/abs/2609.25542> | Abstract | (paraphrase) | Predicts *default itself* from private Korean tax-invoice networks; listed firms and equity reactions are not studied. The equity side of default contagion on public data is open. |
| **Karanjai, Madhavarao, Xu & Shi (2026)**, *CausalGraphX*, AAAI'26 workshop, arXiv 2607.14416 · [ABS today] <https://arxiv.org/abs/2607.14416> | Abstract | "large-scale synthetic financial networks" | Counterfactual GNN explanations for cascading defaults exist only on **synthetic** networks; no real public data, no equity outcome. |
| **Brogaard & Chen (2026)**, production-network GNN for CDS spreads, working paper · [FT (1 Nov)] | Data / conclusion | (paraphrase) | Credit endpoint (CDS, Markit) with industry-level edges; firm-level public graph and equity endpoint open. |
| **Zelvyte et al. (2026)**, multiplex Hawkes credit contagion, arXiv 2606.15755 · [FT/ABS (1 Nov)] | Model scope | (paraphrase) | 99 firms' credit spreads only; no equity layer. |
| **Frankel, Godigbe & Rabier (2025)**, *Information Spillovers at Earnings Announcements*, *J. Accounting Research* 63(1):319–362 (peer-reviewed) · [ABS today] <https://doi.org/10.1111/1475-679X.12562> | Abstract | (paraphrase) | Signed and absolute focal–peer co-movement is significantly *lower* on earnings-announcement dates, also for large surprises and industry leaders. A substantive risk for the earnings-first design that must be tested in the pilot, not assumed away. Note: this is an *average* result; per-edge predictability can still exist. |

**No paper names the exact gap.** It is inferred from: FinRipple's own limitation (dependence on a high-quality KG) plus its commercial data; Avramov et al.'s statement that the time path and content of peer-information transmission are not established; and the fact that every 2026 default-network GNN found uses private data and predicts default rather than equity contagion (DefaultGNN; earlier Chinese guarantee-network papers, `thesis-proposals/sweep/T7.md`).

### 2.2 Lineage (timeline)

| Year | Work | Status | Step |
|---|---|---|---|
| 1992 | Lang & Stulz: bankruptcy contagion vs competitive effects within industries | [BG, UNVERIFIED: classic, not opened] | Rivals can fall (contagion) or rise (competition): the **sign** question |
| 2008 | Cohen & Frazzini, *Economic links and predictable returns* | [BG, SNIP via a 2026 literature-review page] | Customer–supplier links transmit news slowly |
| 2008 | Hertzel, Li, Officer & Rodgers, *Inter-firm linkages and the wealth effects of financial distress*, *JFE* | [BG, ABS via Penn State record today] | Suppliers of filing firms have significantly negative abnormal returns; contagion extends beyond industry |
| 2019 | Arata, bankruptcy propagation on a Japanese customer–supplier network (RIETI) | [BG, ABS via search today] | Firm-level contagion is significant but aggregate reach is limited (private data) |
| 2022 | Alldredge et al., *Rev. Accounting Studies* | [BG, ABS (1 Nov)] | Peer information transfer around events |
| 2025 | FinRipple (ACL Findings) | [FT] | LLM + commercial KG predicts signed ripples per connected firm after news |
| 2025 | Frankel, Godigbe & Rabier (*JAR*) | [ABS today] | Earnings-day peer co-movement is lower than expected |
| 2026 | Avramov et al. (*JFE*); Brogaard & Chen; Zelvyte et al.; DefaultGNN; CausalGraphX | [FT]/[FT]/[FT]/[ABS]/[ABS] | Peer predictability, credit-spread networks, private-data default GNNs, synthetic counterfactuals |
| **Now** | — | — | No public-data, event-level, signed, per-edge prediction of equity contagion with explained channels |

### 2.3 Related gaps in neighbouring fields that transfer

- **Temporal-GNN explainers** (TemGX, ICLR 2026, code cloned today; MemExplainer, ICML 2026, code cloned today; CoDy-style counterfactual explainers) are evaluated on Wikipedia/Reddit/MOOC only ([ABS (2 Nov)]). *Transfer:* financial contagion offers something those benchmarks lack: a partial **economic ground truth** for explanations (a disclosed major customer should be the explanation for a supplier's drop).
- **Event-based / few-shot transfer on graphs**: learning on frequent event types and transferring to rare ones mirrors few-shot link prediction; the earnings → credit design is a domain-transfer test.
- **Event-study econometrics** (abnormal returns, FDR across many peers): standard tools turn into per-edge labels, which ML evaluation can use.
- **Smurfing lessons** (`smurfing-thesis`): chronological splits, alert budgets (precision@K per event), placebo/matched controls.

### 2.4 Who is working on it (kill-test evidence)

- **Groups / venues:** HKUST-GZ + USTC (FinRipple; ACL), finance economists (Avramov, Linton: JFE; Hertzel line), Korean and Chinese groups on private default networks (CIKM, ESWA), credit-network econometrics (Zelvyte; Brogaard).
- **Is anyone close?** FinRipple is closest; a follow-up could swap news for credit events, but they rely on commercial KGs and an LLM-RL pipeline. The finance line (Avramov et al.) works at the portfolio level, not per edge.
- **Searches run today:** `peer firms stock price reaction earnings announcement prediction graph neural network supply chain information transfer 2026` (extended) → news co-occurrence TGNN for price prediction (Chen & Kawashima, SSRN 2026; return prediction, crowded type), earnings-day direction prediction without graph (arXiv 2605.25894), Avramov et al. 2026 (JFE), supply-chain return-prediction GNNs (Iowa PhD thesis; FS-GCLSTM arXiv 2303.09406; IJIRT 2026): **none predicts per-peer event reactions**; `bankruptcy filing contagion customers suppliers rivals abnormal returns machine learning network 2025 2026` → classic event studies (Hertzel 2008; Lang–Stulz line), trade-credit default networks on private bank data (PLOS ONE 2021; Italian bank data), RIETI Japan: **no public-data ML on equity contagion**. Earlier: `thesis-proposals/sweep/kill_K3.md` (~15 searches for I4/I29/I26) and `thesis-attempt-2` Phase 3 query 6. **Verdict: survives** (FinRipple and Avramov et al. are the position points).

---

## 3. Literature background

### 3.1 What you need to understand the problem
- **Event studies**: abnormal returns, CAR windows, estimation windows, factor models; cross-sectional dependence when many peers react to one event (needs FDR or clustered tests).
- **Contagion vs competition effects** (Lang & Stulz 1992 [BG]; Hertzel et al. 2008 [BG]): why reactions are signed.
- **Economic links** (Cohen & Frazzini 2008 [BG]): customer momentum and slow diffusion; why some links transmit and others do not.
- **Heterogeneous GNNs** (R-GCN, HGT) and **edge-level classification** conditioned on context.
- **Explainability on graphs**: GNNExplainer/PGExplainer (factual), CF-GNNExplainer (counterfactual), temporal explainers (TemGX, MemExplainer); fidelity, sparsity and stability metrics.
- **Credit events**: what counts as a default (Chapter 7/11 filings, missed payments), rating actions and their public disclosure (SEC Rule 17g-7(b) histories, 12-month delay).

### 3.2 State of the art closest to the solution, and the difference

| Paper | What it does | How this thesis differs |
|---|---|---|
| FinRipple 2025 (ACL Findings) [FT] | LLM + RL predicts signed −10…+10 impact on KG-connected S&P 500 firms after news; KG from Compustat-Capital IQ, BoardEx, Thomson, USPTO; test 2020–mid-2022; no code yet | Public graph (EDGAR, 13F, FinReflectKG); earnings and credit events; per-edge labels from significant realised reactions; F1/AUPRC per sign and precision@K per event; credit-transfer test; relation-level explanations checked against disclosures |
| Avramov et al. 2026 (*JFE*) [FT] | Peer Index from SIC/customer/co-coverage peers predicts returns; portfolio evidence | Event-time, per-link prediction instead of a stock-level predictor; free data |
| DefaultGNN 2026 [ABS] | Default prediction on private buyer–seller networks | Predicts equity reactions *to* a default, not default itself; public data |
| CausalGraphX 2026 [ABS] | Counterfactual explanations of cascading defaults on synthetic networks | Real data; explanations evaluated against economic ground truth |
| TemGX / MemExplainer 2026 [ABS (2 Nov); code cloned] | Temporal-GNN explainers on social benchmarks | First financial use; economic plausibility as an extra evaluation |

---

## 4. Data and access

| Dataset | What it is | Existing / formable | Size | Licence / terms | Cost | Access test (6 Nov 2026) | Rating |
|---|---|---|---|---|---|---|---|
| Earnings dates (8-K Item 2.02) | Event timestamps for all filers | Formable from EDGAR via `edgartools` (MIT; 8-K item parsing incl. "Item 1.03 – Bankruptcy or Receivership" found in `edgar/documents/form_schema.py`) | ~25–30 k 8-K 2.02 per year (all filers; my estimate, check) | Public domain; SEC fair-access policy (declare a User-Agent, ≤ 10 req/s) | Free | `edgartools` wheel **downloaded** (v5.62.1) and inspected; EDGAR itself **403 from the shell** → run on laptop | Medium |
| Bankruptcies, 1979–2022 | Florida-UCLA-LoPucki BRD cases table (large public companies, ~200 fields) | Existing | > 1,000 cases | Free for research; **no longer updated after Dec 2022** | Free | Site **reached via search** (`lopucki.law.ufl.edu`): "The Cases table is now available free" | Easy |
| Bankruptcies, 2023–2026 | 8-K Item 1.03 filings | Formable (`edgartools`) | tens–low hundreds of listed firms per year (estimate) | Public domain | Free | as above | Medium |
| Rating actions | NRSRO XBRL histories under Rule 17g-7(b) (S&P, Moody's, Fitch, KBRA …) | Formable | large | Agency terms (attribution, no redistribution); 12-month delay | Free | Not re-tested today (pages found on 1 Nov; ratingshistory.info mirror unverified) | Medium–hard |
| Prices | Daily returns of focal firms and peers | Formable | as Proposal 1 | Stooq / yfinance / UU (LSEG, FactSet) | Free | Not testable here (Yahoo 429, Stooq blocked) | Medium |
| Fama–French 5 factors | Abnormal returns | Existing | small | free | Free | **Downloaded** (to 2026-09-30) | Easy |
| Industry codes | SIC in SEC Financial Statement Data Sets (quarterly ZIPs 2009 → 2026, 40–120 MB each) | Existing | ~5 GB total | Public domain | Free | SEC pages **reached via search** (data.gov catalogue lists 2026 Q1; sec.gov lists 2025 Q4) | Easy |
| Common ownership | SEC 13F data sets (2013 Q2 → 2026) | Formable | quarterly ZIPs ≤ 100 MB | Public domain | Free | 99-manager sample in `e-izdfr/portfolio-holdings-prediction` **cloned OK**; full sets via laptop | Easy–medium |
| Customer / supplier / competitor links | FinReflectKG 10-K triples (S&P 500, 2014–2024) | Existing | 17.5 M triples | **CC-BY-NC-4.0** | Free | **Reached and sampled**: 8 tickers → 439 mentions of other current S&P 500 firms (partners_with 135, competes_with 78, depends_on 72, has_stake_in 49, supply 10). Supply links are rare; competitor links are common | Easy access / medium quality |
| Major-customer disclosures (ground truth for explanations) | 10-K text "customer X accounted for N % of revenue" | Formable (LLM extraction from 10-K) | — | Public domain | Free (LLM compute) | Not tested today | Medium–hard |

**Minimum viable dataset:** S&P 1500 focal firms, earnings events 2010–2026 with a price-based surprise (|CAR[−1,+1]| in the top decile), candidate peers = same-SIC + top-holder overlap + FinReflectKG competitor/partner links; credit events = LoPucki BRD (to 2022) + 8-K 1.03 (2023–2026) restricted to listed filers with at least one listed peer. **Fallback:** widen "credit event" to severe negative shocks (≥ 30 % one-day drop or Item 2.02 with extreme negative surprise), which gives thousands of events while keeping the same graph, labels and explanations.

---

## 5. Approach and 30-week plan

**Research question.** *Can a public heterogeneous company graph predict which linked listed firms react to a focal firm's event, and with which sign, and does a model learned from earnings surprises transfer to credit events?*
- **SQ1 (earnings).** Which relation types (industry, common ownership, disclosed customer/supplier/competitor, text similarity, past lead-lag) predict signed peer reactions to earnings surprises, and does a heterogeneous GNN beat event-study heuristics and gradient boosting?
- **SQ2 (credit transfer).** Does the earnings-trained model rank the peers that react to bankruptcies and downgrades better than a credit-only model and simple heuristics?
- **SQ3 (explanations).** Are relation-level and counterfactual explanations faithful (fidelity, sparsity, stability across seeds) and economically plausible (do they point to the disclosed customer when one exists)?

**Pipeline.** EDGAR (8-K items, 10-K text, 13F, SIC) + FinReflectKG → point-in-time heterogeneous graph snapshots (yearly/quarterly; edges dated by filing) → event set (earnings, credit) → per-(event, peer) CARs and FDR labels → models → evaluation per event type → explainers → contagion explorer.

**Existing code to build on (checked today):** `dgunning/edgartools` (MIT; 8-K item parsing); `e-izdfr/portfolio-holdings-prediction` (MIT; 13F graph construction and CUSIP matching); PyTorch Geometric heterogeneous modules (HeteroConv, HGT, RGCN; library not cloned today); `nicej1899/TemGX` (no licence file; commit 2025-11-20) and `yazhengliu/MemExplainer` (no licence file; commit 2026-07-14) for temporal explanations; `jhkim611/DefaultGNN` (commit 2026-10-07) as a reference implementation of dual-view firm networks. To build: event-study labeller (statsmodels), point-in-time graph builder, matched-control sampler, evaluation harness, explorer.

**Baselines.** Same-SIC peers; "named major customer/supplier" flag; top-k past return correlation; past reaction of the same pair (persistence of reactions); logistic regression and LightGBM on relation indicators + pair features; optional FinRipple-style LLM scoring of a sample of events.

**Metrics.** Per-sign AUPRC and macro-F1 over (event, peer) pairs; precision@K and NDCG per event; calibration; for transfer, the same on credit events with bootstrap CIs over events; for explanations, fidelity+/−, sparsity, rank agreement across explainers and seeds, and hit rate on disclosed customer links.

**Splits.** Chronological by event date (train 2010–2018, validate 2019–2020, test 2021–2026); graph snapshots strictly before each event (filing dates, not fiscal-year ends); factor betas from the pre-event window; placebo = matched unlinked firms of similar size, sector and beta.

**Week-by-week plan**

| Weeks | Phase | Work | Output |
|---|---|---|---|
| 1–4 | Phase 1 | Literature review (event studies, contagion, heterogeneous GNNs, GNN explainers); FinRipple and Avramov et al. in depth | `lit_review.md` |
| 5–6 | Phase 1 | Pilot: 1 year of earnings events on S&P 500 with SIC peers; check that significant signed peer reactions exist (the Frankel 2025 risk) | Pilot base rates |
| 7–8 | Phase 1 | Proposal; event counts for credit events confirmed | **Go/no-go** |
| 9–13 | Phase 2 | Graph builder (SIC, 13F, FinReflectKG, text); event sets; labeller | Data chapter |
| 14–17 | Phase 2 | SQ1: baselines, LightGBM, RGCN/HGT | SQ1 results |
| 18–20 | Phase 2 | SQ2: credit transfer (zero-shot, fine-tuned), severe-shock fallback | SQ2 results |
| 21–23 | Phase 2 | SQ3: explainers, economic plausibility test | SQ3 results |
| 24–25 | Phase 2 | Contagion explorer | Artefact |
| 26–30 | Writing | Thesis | Thesis |

**Usable artefact.** *Contagion explorer:* pick a firm and an event type ("Chapter 11", "earnings miss") and get the ranked list of listed peers expected to react, each with sign, probability, the relation path that explains it ("competitor in the 10-K; 6 shared top-10 holders") and the most similar historical events. A natural risk-management demo for Accenture.

---

## 6. Feasibility verdict

**Top 3 risks and mitigations**
1. **Weak earnings-day spillovers (evaluation/novelty).** Frankel, Godigbe & Rabier (2025) report lower peer co-movement on earnings days, even for large surprises. *Mitigation:* the week-5 pilot measures base rates before go/no-go; restrict to large surprises; use [0, +5] windows; if spillovers are too rare, switch the frequent-event source to severe price shocks.
2. **Rare credit events (data).** Listed bankruptcies with listed peers may number only in the low hundreds. *Mitigation:* LoPucki BRD (1979–2022) + 8-K 1.03 for coverage; rating downgrades as a more frequent credit event; severe-shock fallback; report credit results as a transfer test with confidence intervals, not as the headline.
3. **Relation coverage and graph leakage (data/evaluation).** Supply links in public data are sparse (sample check: supply 10 of 439 links); relations must be dated by filing to avoid look-ahead. *Mitigation:* rely on SIC + 13F + competitor links first; FinReflectKG `year` field and EDGAR filing dates for point-in-time edges; supply links as a bonus layer.

**Minimum thesis (fallback).** Earnings-event signed peer-reaction prediction on S&P 500 with SIC + 13F + FinReflectKG relations, LightGBM vs one heterogeneous GNN, relation ablation as explanation, and a qualitative credit-event case study (e.g. 10–20 bankruptcies).

**Ethics / GDPR.** Firm-level nodes only; do **not** use BoardEx-style shared-director links or Form 4 insider data (named natural persons). Rating data used under agency terms, no redistribution. Present outputs as risk analysis, not trading or credit advice. Disclose generative-AI use (coding, possible LLM extraction).

**Scores (briefing §9)**

| Criterion (weight) | Score | Weighted | Reason |
|---|---|---|---|
| Novelty (×3) | 4 | 12 | No public-data per-edge equity-contagion model; FinRipple close |
| Supervisor fit (×2) | 5 | 10 | Her credit-default problem + heterogeneous graph + signed activation |
| Data (×2) | 3 | 6 | Free but must be assembled; credit events rare |
| Feasibility (×2) | 3 | 6 | Most engineering of the five (event study + graph builder) |
| Evaluation clarity (×1) | 4 | 4 | Clean per-edge labels; placebo controls |
| AI relevance (×1) | 4 | 4 | Heterogeneous GNNs, transfer, explainability |
| Artefact (×1) | 5 | 5 | Contagion explorer |
| Industry (×1) | 5 | 5 | Credit/risk; very Accenture-relevant |
| Frank's interests (×1) | 5 | 5 | Markets, XAI, regulation/supervision |
| **Total** | | **57 / 70** | (earlier: A-2 55, Card 4 54; the earnings-first design raises data and feasibility vs A-2) |

---

## 7. Questions for the supervisor

1. Is the earnings-first, credit-transfer design an acceptable answer to "credit default into stock markets", or do you want credit events at the centre even if they are few?
2. Are event-study labels (significant abnormal returns) acceptable as ground truth for an ML thesis?
3. Is the XAI part (explanations checked against disclosed relations) enough of an AI contribution, or should the model itself be new?
4. Is FinReflectKG (LLM-extracted, CC-BY-NC) acceptable as a relation source? Can UU provide Compustat customer segments (UU's WRDS list shows Compustat) for a cleaner supply-chain layer?
5. How should the thesis position itself against FinRipple (an LLM approach) — compare against it on a sample, or treat it as related work only?
