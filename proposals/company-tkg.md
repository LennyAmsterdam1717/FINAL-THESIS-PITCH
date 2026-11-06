# Proposal 4: Next year's company relations
## Temporal knowledge-graph completion on a public 10-K company knowledge graph, and whether predicted new relations carry market information

*Feasibility dossier, 6 Nov 2026. Based on Card 1 + runner-up R3 (cold-start, I24) of `thesis-proposals`; the LLM look-ahead idea (Card 2 / D-3) is folded in as a robustness module.*
*Legend: [FT] full text opened · [ABS] abstract/record only · [SNIP] search-result excerpt only · [UNVERIFIED] not opened · [BG] pre-2025 background. "(1 Nov)"/"(2 Nov)" = opened in an earlier session, not re-opened today.*

Supervisor directions hit: **link prediction** (core) · **heterogeneous graphs** (typed relations, several entity types) · temporal graphs · **knowledge networks and text analysis** (her listed expertise) · optional time series + graph (economic test).

**Headline from today's data check:** the earlier card scored this 60/70, the highest of all. A sample of FinReflectKG (4 of 103 shards, 34 filers) shows that relations *between listed firms* are sparse (≈ 3.6 per filer-year) and that 39 % of later-year edges are "never seen before", which mixes true new relations with extraction noise. The topic stays strong but riskier than it looked; re-scored at **54/70** below.

---

## 1. The problem in plain language

Every year, each US-listed company files an annual report (the 10-K) with the SEC. In it, the company tells investors who it competes with, which suppliers it depends on, who its partners are, and which firms it holds stakes in. In 2025, a team released **FinReflectKG**, a free knowledge graph extracted with large language models from ten years of these reports for all S&P 500 companies: about 17.5 million facts such as *(Verizon, competes with, Comcast, 2014)*.

Such a graph is a map of the corporate world that changes every year. New partnerships are announced, suppliers are replaced, competitors appear when a firm enters a new market. Can a model **predict next year's map from the previous years**? For example: *given everything Nvidia and its neighbours disclosed up to 2022, will Nvidia's 2023 10-K name a new partner or competitor, and which one?* And a second, more financial question: **if a model predicts that two firms are about to become linked, do their stock prices already start moving together before the link is disclosed?** If yes, the predicted link carries information that investors have not yet fully priced.

Why it matters:
- **Analysts and consultants** (competitive intelligence, M&A screening, supply-chain risk) want early signals of who is about to become a partner, supplier or competitor.
- **Risk managers** want to know which hidden dependencies are likely to appear before they are disclosed.
- **AI research**: temporal knowledge-graph (TKG) forecasting is an active field, but its benchmarks are political-event graphs (ICEWS, GDELT) and Wikipedia; there is no public company-relation benchmark with honest year-ahead evaluation.

The honest catch: the "ground truth" is itself produced by an LLM. If a relation appears in 2023 but not in 2022, it may be a real new relation, or the extraction may simply have missed it in 2022. Part of the thesis is measuring how much of the "future" is real and how much is extraction noise.

### 1.1 Technical formulation

- **Data.** Quadruples (s, r, o, y) from FinReflectKG: subject s = filing company (normalised ticker), relation r from the normalised schema (e.g. competes_with, partners_with, depends_on, supply, has_stake_in), object o = an organisation entity (listed firm, private firm, subsidiary, regulator), year y = filing year (2014–2024). Object entities are resolved to canonical IDs (listed: ticker/CIK; unlisted: normalised name clusters).
- **Task (TKG forecasting, year-ahead).** Given all quadruples with y ≤ t, rank objects o for queries (s, r, ?, t+1), and score (s, r, o, t+1) existence. Report separately for **repeated** edges (seen at some y ≤ t) and **new** edges (never seen before), because repeated edges are trivially predictable by recurrence.
- **Economic test.** For listed pairs (i, j) with high predicted probability of a *new* relation at t+1, compare residual co-movement and lead-lag strength in the 12 months *before* the t+1 filing date against matched pairs with low probability (difference-in-differences, matched on industry, size, prior correlation).
- **Inductive variant.** Firms entering the S&P 500 (index additions) have no history: predict their relations from their first filing's text (cold start).
- **Noise audit.** For a stratified sample of predicted and observed new edges, check against the source chunk text (`chunk_text` is in the dataset) and against the previous year's filing to estimate the share of real vs spurious "new" relations.

---

## 2. Where the problem comes from

### 2.1 Papers that name the gap

| Paper (status, venue) | Section | Short quote (< 15 words) | What exactly is missing, in my words |
|---|---|---|---|
| **Arun, Dimino, Agarwal, Sarmah & Pasquali (2025)**, *FinReflectKG: Agentic Construction and Evaluation of Financial KGs*, ACM ICAIF 2025 (peer-reviewed), arXiv 2508.17906 (v1 25 Aug 2025, v2 7 Oct 2025) · [FT, PDF re-read 6 Nov] <https://arxiv.org/abs/2508.17906> | 7 Conclusion and Future Work; 6 Discussion | "Temporal KGs can enhance explainability for signal generation for market movements" (7); "our evaluation methodology depends on LLM-voting surrogate ground truth" (6) | The authors plan to "enrich our dataset with time-aware features" and see temporal KGs as useful for market signals, but the paper does **not** mention link prediction or KG completion. Its own limitations confirm the risks of this proposal: quality is judged by LLM voting, not gold labels, and cross-document co-reference is "only partially addressed" (i.e. entity resolution across years is open). Reported quality is moderate (schema compliance 84 %, CheckRules 65 % for the best mode). |
| **FinReflectKG dataset card (Domyn, Hugging Face)** · [read today] <https://huggingface.co/datasets/domyn/FinReflectKG> | Temporal Information | (paraphrase) | Start/end dates are often defaults: if no date is extractable, start = filing year and end = "default_end_timestamp". In the sample, 72 % of rows are `default` vs 28 % `extracted` (my count on shard 0). Year-ahead forecasting must therefore use filing year, not the extracted dates. |
| **Naik (2026)**, *FinKGR: Neuro-Symbolic Reasoning on Financial Knowledge Graphs via Rule Mining and Transformers*, SJSU MSc project (Spring 2026) · [ABS today] <https://doi.org/10.31979/etd.qn2h-ge6b> | Abstract | "The neuro-symbolic union achieves higher coverage than the neural model" | Predicts future quadruples on a financial TKG. **Dataset not named; PDF embargoed until 22 May 2027.** This is the main unverifiable overlap risk; it is an MSc project, not a peer-reviewed paper, and reports no numbers in the abstract. |
| **Xiang, Hu, Zhang, Lan & Liu (2025)**, *Graph Neural Poisson Models for Supply Chain Relationship Forecasting* (GDES), arXiv 2508.12044 · [ABS today] <https://arxiv.org/abs/2508.12044> | Abstract | (paraphrase) | Dynamic supply-link prediction on 87,969 firms (AUC 93.84 %); data source and split not described on the abstract page. Shows the task is meaningful but not on a public, multi-relation, filing-based KG with a disclosed protocol. |
| **Sun et al. (2025)**, *InterCorpRel-LLM*, arXiv 2510.09735 · [FT/ABS (1 Nov)] | Data / evaluation | (paraphrase) | Supplier-link prediction with GNN + LLM on proprietary FactSet data, a single year and a random split. Public data and temporal splits are missing. |
| **Ding et al. (2026)**, *TRACE*, arXiv 2603.12500 · [ABS today] <https://arxiv.org/abs/2603.12500> | Abstract / intro | (paraphrase) | Rule mining and multi-hop paths over a financial TKG of S&P 500 stocks, but used for **UP/DOWN movement prediction**; KG completion is not the task. Confirms the tooling, not the gap. |
| **Dukkipati et al. (2025, v2 Feb 2026)**, *Predictive AI with External Knowledge Infusion*, arXiv 2504.20058 · [ABS (1 Nov); snippet today] | Contributions | (paraphrase) | Builds stock-market TKGs (Wikidata relations, events) to improve *return forecasting* via Hawkes processes; relation forecasting is not evaluated. |

**Gap statement (partly named).** FinReflectKG's authors name temporal KGs for market signals as future work but use the KG only for QA/extraction tasks and never for link prediction; company-relation link prediction exists only on proprietary data (InterCorpRel, GDES) or for return prediction (TRACE, Dukkipati). Year-ahead TKG completion on a public company KG, with repeated vs new edges scored separately and an economic test of predicted edges, is not done in any paper I could open. FinKGR may overlap and cannot be checked until May 2027.

### 2.2 Lineage (timeline)

| Year | Work | Status | Step |
|---|---|---|---|
| 2013–2016 | Static KG embeddings (TransE, ComplEx) | [BG] | Link prediction on knowledge graphs |
| 2016 | Hoberg & Phillips text-based network industries | [BG] | Company relations from 10-K text |
| 2019 | Feng et al., *Temporal Relational Ranking for Stock Prediction* (Wikidata company relations) | [BG, SNIP today] | Company KGs as inputs to stock models |
| 2021–2022 | RE-GCN (Li et al.), TLogic (Liu et al.) | [BG; TLogic repo cloned today] | Temporal KG forecasting with recurrent GNNs and temporal rules |
| 2024 | Gastinger et al., TGB 2.0 (TKG + heterogeneous temporal benchmarks); FinDKG (Li et al.) | [BG] | Benchmarks; first financial TKG link-prediction study, built from news |
| 2025 | FinReflectKG (ICAIF'25); InterCorpRel-LLM; GDES | [FT]/[FT/ABS]/[ABS] | Public 10-K KG; proprietary link prediction |
| 2026 | HalluBench (arXiv 2603.20252) on FinReflectKG; TRACE; FinKGR (MSc, embargoed); TKG methods (SKER, *Pattern Recognition* 2026; TRTL, *Neural Networks* 2026; TransFIR, emerging entities) | [ABS (2 Nov)]/[ABS]/[ABS]/[SNIP] | KG used for QA/hallucination, movement prediction; TKG methods mature on ICEWS/GDELT |
| **Now** | — | — | No year-ahead completion benchmark on a public company KG; no test of whether predicted new relations are priced |

### 2.3 Related gaps in neighbouring fields that transfer

- **TKG forecasting evaluation**: recurrency baselines ("history repeats itself", Gastinger et al. 2024 [BG]) often rival learned models on ICEWS/GDELT; the 2026 temporal-link-prediction critiques (Qarkaxhija & Scholtes 2026 [ABS]; Yu & Ha 2026 [ABS]) say the same for unsigned graphs. *Transfer:* recurrence/EdgeBank and frequency baselines are mandatory, and new-edge scores are the headline.
- **Inductive TKG reasoning for emerging entities** (TransFIR 2026 [SNIP]): directly applies to firms entering the index.
- **LLM look-ahead bias** (Look-Ahead-Bench 2026; *All Leaks Count* 2026; Yang 2026 *LLM latent edges* [FT (1 Nov)]): an LLM baseline that "knows" 2023 relations from pre-training would inflate results. *Transfer:* LLM baselines only on years after the model's training cutoff; this brings in the strongest part of the rejected Card 2 as a module.
- **Hallucination in KG-augmented finance QA** (HalluBench 2026 [ABS (2 Nov)]): shows the KG's own errors are a research topic; the noise audit here quantifies them for the temporal dimension.

### 2.4 Who is working on it (kill-test evidence)

- **Groups:** Domyn (FinReflectKG authors; Italian/US AI company) — the most likely to add a temporal-completion benchmark; SJSU (FinKGR); TKG-method groups in China and Singapore (A*STAR, SKER); Mila/McGill (TGB 2.0).
- **Is anyone close?** Domyn's own roadmap (temporal KGs) and FinKGR. Neither has a public result on year-ahead company-relation completion with an economic test.
- **Searches run today:** `FinReflectKG temporal knowledge graph completion link prediction company relations` → dataset card, abstract page, MultiHop benchmark summary, secondary articles: **no link-prediction use**; `temporal knowledge graph forecasting company relationships SEC filings supplier competitor prediction 2026` (extended) → TRTL (*Neural Networks* 2026, ICEWS), Feng 2019, NIST-GNN (*Quant. Finance* 2025, news co-occurrence for returns), Dukkipati 2025/26, Chen et al. (*IJDSA* 2026, LLM enterprise relations for forecasting): **none forecasts relations**; `FinKGR San Jose State University …` → SJSU record (embargo to May 2027), TRACE (2603.12500), SKER (2026), TransFIR (2026). Earlier: `thesis-proposals/sweep/kill_K2.md` (I7, I24; OpenReview API "financial temporal knowledge graph completion"). **Verdict: survives, with one unverifiable overlap (FinKGR).**

---

## 3. Literature background

### 3.1 What you need to understand the problem
- **Knowledge graphs and link prediction**: triples, embeddings (TransE, ComplEx, RotatE), R-GCN; filtered MRR/Hits@k.
- **Temporal KG forecasting** (extrapolation setting): recurrent models (RE-GCN, TiRGN), rule-based (TLogic), and their evaluation pitfalls (recurrency baseline, time-aware filtering).
- **LLM-based information extraction** and its error modes (entity resolution, hallucinated relations, default timestamps); how FinReflectKG's extract–critique–correct loop works.
- **Entity resolution** for company names (CIK/ticker mapping, subsidiaries, name changes).
- **Event-study / difference-in-differences** basics for the economic test; residual co-movement (shared with Proposals 1–2).

### 3.2 State of the art closest to the solution, and the difference

| Paper | What it does | How this thesis differs |
|---|---|---|
| FinReflectKG 2025 [FT] + HalluBench 2026 [ABS] | Builds the KG; QA and hallucination benchmarks | Uses it for **year-ahead TKG completion**; adds a temporal noise audit |
| InterCorpRel-LLM 2025 [FT/ABS (1 Nov)] | Supplier-link prediction on FactSet, random split | Public data; multi-relation; chronological, new-vs-repeated scoring |
| GDES 2025 [ABS] | Poisson-GNN forecasting of supply edges on 88 k firms | Filing-based KG with several relation types; economic test of predicted edges |
| TRACE 2026 [ABS] | Rule-anchored KG paths for stock UP/DOWN | Predicts the relations themselves; rules as explanations of predicted relations |
| FinKGR 2026 (MSc) [ABS] | Neuro-symbolic TKG link prediction, dataset unknown | Must be compared once the PDF is public (May 2027) or the author is contacted |
| TLogic / RE-GCN [BG; code cloned] | Generic TKG forecasting | Used as baselines on a new domain |

---

## 4. Data and access

| Dataset | What it is | Existing / formable | Size | Licence / terms | Cost | Access test (6 Nov 2026) | Rating |
|---|---|---|---|---|---|---|---|
| **FinReflectKG** (`domyn/FinReflectKG`, Hugging Face) | 10-K triples, 743 S&P 500 firms, 2014–2024, with chunk text, ticker, year | Existing | 103 parquet shards (~16 MB each, ≈ 1.7 GB), 17.51 M triples | **CC-BY-NC-4.0** (non-commercial: thesis OK; keep separate from Accenture client work) | Free | **API reachable from the shell (HTTP 200); 4 shards downloaded** (680,131 rows, 34 filers). Run `tools/finreflectkg_sample_stats.py`: after crude name matching to *current* S&P 500 firms, **789 yearly listed–listed edges (344 distinct)**: compete 323, partner 272, depends 129, stake 43, supply 22; **3.57 per filer-year**; **46 % of yearly edges also appear the year before; 283 of 728 later-year edges are never seen before**. Many ORG targets are generic ("wholly-owned subsidiary", "key labor union") | Easy access; **medium–hard quality** |
| Point-in-time S&P 500 membership (`fja05680/sp500`) | Ticker/CIK mapping, index additions for the cold-start variant | Existing | 14 MB | MIT | Free | **Cloned OK** (≈ 775 additions since 1996) | Easy |
| SEC EDGAR 10-K full text + filing dates | Filing dates (point-in-time), text for cold-start and noise audit | Formable | large | Public domain | Free | Shell 403; via laptop/`edgartools` | Medium |
| Prices + FF5 factors | Economic test | Formable / existing | as Proposal 1 | as Proposal 1 | Free | FF5 downloaded; prices on laptop | Medium |
| Optional validation layers | Hoberg–Phillips TNIC (gvkey-keyed; UU finance data hub lists it per deep dive) ; Compustat segments via UU WRDS (Compustat listed, CRSP not) | Existing (licensed) | — | UU licence | Free for UU | Not tested today | Medium |

**Minimum viable dataset:** FinReflectKG restricted to the four cleanest relation families (competes, partners, depends/supply, has_stake_in) with objects resolved to (a) listed firms via name + ticker matching and (b) high-frequency unlisted ORG clusters; filing years 2014–2024 (train ≤ 2020, validate 2021–2022, test 2023–2024). **Fallback:** if listed–listed edges are too sparse for the economic test, keep the TKG-completion benchmark over all ORG objects (much denser) and turn the economic test into a case study; or switch the economic part to 13F co-ownership edges (Proposal 5 data).

---

## 5. Approach and 30-week plan

**Research question.** *To what extent can company relations disclosed in next year's 10-K filings be predicted from the past temporal company knowledge graph, and do predicted new relations between listed firms anticipate their co-movement before disclosure?*
- **SQ1 (benchmark).** Do temporal KG models (rules, recurrent GNNs, LLM re-rankers on post-cutoff years) beat recurrence and frequency baselines on year-ahead completion, especially on **new** edges?
- **SQ2 (noise).** What share of observed and predicted "new" edges are real new relations rather than extraction artefacts, and how does correcting for this change SQ1?
- **SQ3 (economics).** Do listed pairs with high predicted probability of a new relation show higher residual co-movement or lead-lag before the filing date than matched pairs?
- *(Optional SQ4, cold start)* How well can relations of newly added index members be predicted from their first filing?

**Pipeline.** HF shards → company subgraph per year → entity resolution (ticker/CIK, name clustering) → relation normalisation (map ~70 raw labels to families) → chronological splits → baselines and TKG models → new/repeated scoring → noise audit (chunk text + previous filing; LLM judge + 200-edge manual check) → economic test → relation radar.

**Existing code to build on (checked today):** `liu-yushan/TLogic` (Apache-2.0; last commit 2024-11-23); `shenyangHuang/TGB` (MIT; TGB 2.0 TKG loaders/evaluators); RE-GCN / TiRGN repos (named in earlier notes, not re-cloned); PyTorch Geometric (R-GCN, RotatE via KGE module); Hugging Face `datasets`. To build: entity resolution, relation normalisation, year-ahead evaluator with new/repeated split, noise-audit protocol, economic test (shared residual-return code with Proposal 1), dashboard.

**Baselines.** Recurrence (predict last year's edges); frequency/recency; popularity of object; "same-industry neighbour has the relation" heuristic; static R-GCN/ComplEx trained on ≤ t; LLM zero-shot re-ranking restricted to post-cutoff test years.

**Metrics.** Time-aware filtered MRR, Hits@1/10, AUPRC for existence; all separately for repeated and new edges, per relation family; for SQ2 precision of "new" edges after audit; for SQ3 difference-in-differences estimates with matched-pair bootstrap CIs.

**Splits.** Train ≤ 2020 filing year, validate 2021–2022, test 2023–2024; features only from filings dated before the prediction date; LLM baselines only on years after their documented training cutoff.

**Week-by-week plan**

| Weeks | Phase | Work | Output |
|---|---|---|---|
| 1–4 | Phase 1 | Literature (TKG forecasting, financial KGs, LLM extraction quality, look-ahead); contact FinKGR author about the dataset | `lit_review.md` |
| 5–6 | Phase 1 | Full FinReflectKG download; entity resolution prototype; edge statistics by relation family and year (extends today's sample) | Data report |
| 7–8 | Phase 1 | Proposal; licence confirmed; decide relation families | **Go/no-go** |
| 9–12 | Phase 2 | Resolution + normalisation finished; baselines | SQ1 baselines |
| 13–17 | Phase 2 | TLogic, RE-GCN/TiRGN, R-GCN; LLM re-ranker on 2024 | SQ1 results |
| 18–20 | Phase 2 | Noise audit (SQ2) | SQ2 results |
| 21–23 | Phase 2 | Economic test (SQ3); optional cold start | SQ3 results |
| 24–25 | Phase 2 | Relation radar | Artefact |
| 26–30 | Writing | Thesis | Thesis |

**Usable artefact.** *Relation radar:* for a chosen company, its current KG neighbourhood, predicted new relations for next year with rule-path explanations ("A partners with B, B competes with C → A will compete with C"), the source sentence for each existing relation, and the co-movement history of predicted pairs.

---

## 6. Feasibility verdict

**Top 3 risks and mitigations**
1. **Ground truth is LLM-extracted and noisy (evaluation).** Today's sample: 39 % of later-year listed–listed edges are never seen before; many targets are generic names. *Mitigation:* SQ2 turns this into a measured result; restrict headline metrics to the cleaner relation families; manual audit of ≥ 200 edges; report results with and without audited edges.
2. **Sparse listed–listed edges and only 11 yearly snapshots (data/scope).** ≈ 3.6 per filer-year → perhaps 25–30 k yearly edges in total (extrapolated, unverified). *Mitigation:* the completion benchmark uses all ORG objects (denser); the economic test uses only listed pairs and is framed as a test, not the headline; 13F edges (Proposal 5) as a backup economic layer.
3. **Overlap with FinKGR (novelty).** Unverifiable until May 2027. *Mitigation:* email the author/advisor in week 1; this thesis's distinguishing parts (new-vs-repeated scoring, noise audit, economic test) are unlikely to be in an MSc project focused on a neuro-symbolic model.

**Minimum thesis (fallback).** Year-ahead completion benchmark on FinReflectKG (recurrence vs TLogic vs one recurrent GNN), with the noise audit. Clear RQ, public data, no dependence on prices.

**Ethics / GDPR.** FinReflectKG contains PERSON entities (2,124 rows in shard 0, e.g. executives): **drop all PERSON nodes** and any relation that names a person. Respect CC-BY-NC (non-commercial; do not reuse in Accenture client work). Disclose generative-AI use, including any LLM used as a baseline or judge, with model versions and cutoffs.

**Scores (briefing §9)**

| Criterion (weight) | Score | Weighted | Reason |
|---|---|---|---|
| Novelty (×3) | 4 | 12 | Empty niche in opened literature, but FinKGR unverifiable and GDES/InterCorpRel close in task (earlier: 5) |
| Supervisor fit (×2) | 5 | 10 | Knowledge networks + text + link prediction: her core expertise |
| Data (×2) | 3 | 6 | Free and reachable, but sparse, noisy listed–listed edges (earlier: 4) |
| Feasibility (×2) | 4 | 8 | TKG libraries exist; entity resolution is the main work |
| Evaluation clarity (×1) | 3 | 3 | LLM ground truth; mitigated by the audit (earlier: 4) |
| AI relevance (×1) | 5 | 5 | TKG reasoning, LLM extraction quality, look-ahead |
| Artefact (×1) | 3 | 3 | Relation radar |
| Industry (×1) | 4 | 4 | Competitive intelligence, supply-chain risk |
| Frank's interests (×1) | 3 | 3 | Less market-focused; LLM-validation angle helps |
| **Total** | | **54 / 70** | (earlier: 60; lowered after the sample check) |

---

## 7. Questions for the supervisor

1. Is an LLM-extracted KG acceptable as (noisy) ground truth if the thesis measures the noise (SQ2)?
2. Would you rather see the emphasis on KG reasoning (rules, explainable paths) or on the economic test of predicted relations?
3. Do you know the SJSU FinKGR project or its dataset? Is it worth contacting the author?
4. From your venture-capital (Crunchbase) graph projects: any code or lessons for temporal investor/company link prediction?
5. Is there GPU/LLM budget at UU for an LLM re-ranking baseline (open-weight models)?
