# Feasibility overview: five thesis proposals on stock-market and company networks

*6 Nov 2026 · MSc AI, Utrecht University · supervisor Dr. I. Karnstedt-Hulpuș · dossiers in `proposals/` · decision log in `NOTES.md`*

## Which one to pitch (summary)

**Pitch Proposal 1, "When do influence links between stocks switch on, off or flip?"**, and offer Proposal 2 as its second chapter.
It answers your supervisor's capitalised point (signed, time-activated influence edges with time series) and her "link prediction!!!!" directly. No paper I opened forecasts the *state* of signed lead-lag edges. The 2026 signed-network models built for this kind of task were tested only on Bitcoin and Wikipedia data, and their authors ask for financial benchmarks. The data are free; every component passed today's access test except bulk prices, which you download on your laptop. The first result is low-risk: a re-evaluation of the July-2026 *Machine Learning* paper on its own public data (cloned today). The main risk, a weak daily signal, becomes a measurable finding.

**Alternatives.** Choose Proposal 3 if she cares most about credit default (most Accenture-relevant, but the most data assembly). Choose Proposal 5 for the safest data and cleanest labels. Proposal 4 fits her expertise best, but today's sample of its knowledge graph was noisier than its earlier score assumed.

## Side-by-side comparison

| | **1 Signed lead-lag edge states** | **2 Unexpected edges** | **3 Event contagion** | **4 Company TKG** | **5 Ownership events** |
|---|---|---|---|---|---|
| Dossier | [signed-leadlag.md](proposals/signed-leadlag.md) | [unexpected-edges.md](proposals/unexpected-edges.md) | [event-contagion.md](proposals/event-contagion.md) | [company-tkg.md](proposals/company-tkg.md) | [ownership-events.md](proposals/ownership-events.md) |
| One-line question | Can the next state (+/−/none) of validated lead-lag edges be predicted beyond persistence, especially births and flips? | Which stock pairs co-move unexpectedly, and should "expected" mean learned dynamics or known company relations? | Which linked firms react to a firm's earnings surprise or default, with which sign, and through which relation? | Which company relations appear in next year's 10-Ks, and are predicted new links already priced? | Which managers will enter or exit which stocks next quarter? |
| Supervisor directions | **signed, time-activated** · link prediction · temporal · TS + graph | **anomaly** · signed · temporal · KG context | **credit default** · heterogeneous · signed activation | link prediction · heterogeneous · **knowledge networks** · temporal | link prediction · heterogeneous · temporal |
| Closest 2025–26 work | Krstev et al. 2026 (*MLJ*); IDP-DSN (SIGIR'26); HCIM 2026 | Li et al. 2026 (*Discov. Comput.*); Caputi & Meadows 2026; BAG (AAAI'26) | FinRipple (ACL Findings'25); Avramov et al. 2026 (*JFE*) | FinReflectKG (2025); FinKGR (MSc, embargoed); GDES 2025 | Izadifar & Rahmati 2026 |
| Gap named by a paper? | Partly: HCIM asks for non-crypto signed benchmarks and names finance | No, inferred (papers stop at graph or stock level) | Partly: Avramov et al. say the price path after peer surprises is not established | No, inferred (KG released "to catalyse research"; never used for link prediction) | **Yes**: the 13F benchmark names "less persistent prediction problems" as the next step |
| Kill-test outcome (today) | Survives | Survives (Li et al. 2026 new, not a kill) | Survives | Survives; FinKGR overlap unverifiable until May 2027 | Survives |
| Main data | Prices (Stooq/yfinance/UU) + point-in-time S&P 500 list + FF5 | Same + 13F + FinReflectKG + S&P index changes | EDGAR 8-K + LoPucki BRD + 13F + FinReflectKG + prices | FinReflectKG (CC-BY-NC) + EDGAR + prices | SEC 13F data sets + 2026 benchmark sample |
| Data access tested today | Anchor data, S&P list, FF5 OK; prices need a laptop | S&P changes (~775 additions), FinReflectKG, 13F sample OK | `edgartools` 8-K item parser, BRD page, SEC pages OK | FinReflectKG API + 4 shards OK, but sparse (3.6 listed–listed edges per filer-year) | 13F sample OK; base rates computed (522 entries per quarter; 40 % are re-entries) |
| Data rating | Medium (delisted prices) | Medium | Medium–hard | Easy access / noisy content | **Easy** |
| Biggest risk | Weak daily lead-lag signal | Weak labels; anomaly = volatility | Earnings spillovers lower than expected (Frankel et al. 2025); rare credit events | LLM-extracted ground truth; sparse edges | Persistence and re-entry dominance |
| Minimum thesis | WP1 re-evaluation + S&P 100 signed forecasting | Injected anomalies + index-addition control | Earnings-only signed peer reactions + credit case study | Year-ahead completion benchmark + noise audit | Entries/exits on the published 99-manager sample |
| Usable artefact | Influence-edge monitor | Surprise feed | Contagion explorer | Relation radar | Manager radar |
| Ethics / GDPR | None (prices only) | Litigation releases name persons → firm-level only | No director/insider links | Drop PERSON entities; CC-BY-NC | Drop the SIGNATURE table; pseudonymise natural-person filers |
| Novelty ×3 | 4 (12) | 4 (12) | 4 (12) | 4 (12) | 4 (12) |
| Supervisor fit ×2 | 5 (10) | 5 (10) | 5 (10) | 5 (10) | 4 (8) |
| Data ×2 | 4 (8) | 4 (8) | 3 (6) | 3 (6) | 5 (10) |
| Feasibility ×2 | 4 (8) | 4 (8) | 3 (6) | 4 (8) | 4 (8) |
| Evaluation ×1 | 5 | 3 | 4 | 3 | 5 |
| AI relevance ×1 | 4 | 4 | 4 | 5 | 4 |
| Artefact ×1 | 4 | 5 | 5 | 3 | 4 |
| Industry ×1 | 3 | 4 | 5 | 4 | 4 |
| Frank's interests ×1 | 4 | 4 | 5 | 3 | 3 |
| **Total / 70** | **58** | **58** | **57** | **54** | **58** |
| Earlier score(s) | 58 (C-1, Card 3) | 58 (B-1), 52 (Card 6) | 55 (A-2), 54 (Card 4) | 60 (Card 1) | 55 (A-1) |

Score differences of 3 points or less are within judgement noise (the earlier repos said the same). Choose by your supervisor's answer to "which direction matters most to you?" and by your own interest. Score arithmetic was checked by script.

**Combinations that work.** 1 + 2 (one edge stream; prediction, then surprise). 1 + 3 (lead-lag edges as one relation in the contagion graph). 4 + 3 (the knowledge graph as the relation layer for contagion). 5 + 2 (coordinated entries as anomalies).

## Questions for the supervisor (all proposals)
1. Which of your directions matters most to you: signed time-activated edges (1, 2), credit default (3), knowledge-graph link prediction (4), or heterogeneous ownership graphs (5)?
2. Do you prefer a method contribution or an evaluation/benchmark contribution with careful baselines? (All five can lean either way; 1, 2 and 4 are most naturally benchmark-first.)
3. Data: can UU provide delisted US prices (LSEG Workspace / FactSet via financedata@uu.nl)? UU's WRDS list shows Compustat but not CRSP.
4. Is LLM-extracted data (FinReflectKG, CC-BY-NC) acceptable as a relation layer or as ground truth?
5. Is US-only scope fine, or do you want a European robustness check (weaker free data)?

## Other interesting directions (not developed)

| Direction | Link | Why it is promising |
|---|---|---|
| Look-ahead contamination of LLM-built company graphs (earlier Card 2) | <https://arxiv.org/abs/2607.15640> (Yang 2026, [FT, 1 Nov]) | The paper frames parametric look-ahead in LLM economic graphs but does not measure it. Strong fit with your LLM-validation and AI Act background. Rejected only because it is weak on your supervisor's graph directions. |
| Auditing learned stock graphs against real links (earlier Card 5) | <https://arxiv.org/abs/2609.08106> (Guo 2026, [FT, 1 Nov]) | Learned attention in one 2026 stock model is near-uniform. A multi-model audit would be cheap and publishable. |
| LLM-filtered semantic firm networks for cross-stock prediction | <https://arxiv.org/abs/2604.19476> (Huang 2026, [FT, 1 Nov]; seen again today) | LLM-typed 10-K edges beat random graphs of the same density. Construction sensitivity has not been tested. |
| Directional peer networks and slow price adjustment | <https://doi.org/10.1016/j.jfineco.2026.104274> (Avramov et al., *JFE* 2026, [FT]) | Peer information moves slowly along economic links. An ML event-time version is open (feeds Proposal 3). |
| Causal temporal interaction graphs for validating temporal link prediction | <https://arxiv.org/abs/2602.02161> (Rahman & Coon 2026, [SNIP]) | Synthetic graphs with known excitatory/inhibitory effects. These could provide ground truth for signed lead-lag models (Proposal 1). |
| Lead-lag forecasting benchmarks outside finance | <https://arxiv.org/abs/2511.03877> (2025, [SNIP]) | Formalises lead-lag forecasting as a benchmark task. Its datasets and baselines may transfer. |
| 2025 tariff shocks through public firm networks (earlier R4 / D-2) | <https://arxiv.org/abs/2609.33881> (Hong & Li 2026, [ABS, 2 Nov]) | The tariff windows are well documented. Best used as a regime test inside Proposals 1–3. |

## Method and caveats
- All five dossiers follow the same template (problem, gap evidence, literature, data with access tests, plan, verdict, questions). Every paper is tagged [FT]/[ABS]/[SNIP]/[UNVERIFIED]/[BG]. Papers marked "(1 Nov)" or "(2 Nov)" were opened in the earlier scouting sessions and not re-opened today.
- **Blocked:** Google Scholar and Stooq refuse automated tools (robots), even with approval. Springer, SSRN, ScienceDirect and OpenReview also refused, so Krstev et al. are covered by the 2 Nov reading plus their Crossref record. One arXiv paper (2610.33171) stayed rate-limited after four tries. The AIR 2026 review could not be opened (repository: access denied; Springer: error). Price data could not be pulled from this cloud environment.
- **Recovered in a third pass (7 Nov, built-in browser pane):** Krstev et al. full text (future-work quote; their "negative" lead-lag is still same-direction), the AIR 2026 review (cybersecurity only), GeomHerd Appendix I (13F fund-overlap graph, quantitative test deferred), and the abstract of arXiv 2610.33171 (retrospective reconstruction; tangential). ScienceDirect (Cartea et al.) and Wiley (Frankel et al.) showed a bot-verification page, which I did not try to pass: open those yourself.
- **Recovered in a second pass (6 Nov, 17:50, with Frank present):** the FinReflectKG paper (full text), the *J. Empirical Finance* 2026 version of Cartea et al. (Crossref), Krstev et al.'s dates and licence (Crossref), and the identity of the 6 stocks missing from the anchor's price files.
- **For you to do:** run Google Scholar "cited by" on the closest papers of your chosen proposal; email the FinKGR author if you choose Proposal 4; ask UU about delisted prices.
