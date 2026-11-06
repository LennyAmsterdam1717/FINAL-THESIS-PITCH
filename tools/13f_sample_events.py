"""Entry/exit base rates on the 13F sample of Izadifar & Rahmati (2026), repo e-izdfr/portfolio-holdings-prediction.
Usage: python -I tools/13f_sample_events.py <tgbn-13f_edgelist.csv>"""
import sys, pandas as pd
e = pd.read_csv(sys.argv[1])            # columns: Year (YYYYQ), CIK, CUSIP, VALUE (portfolio weight)
q = sorted(e.Year.unique())
print('quarters', len(q), q[0], '->', q[-1], '| managers', e.CIK.nunique(), '| securities', e.CUSIP.nunique(), '| edges', len(e))
hold = {k: set(map(tuple, g[['CIK', 'CUSIP']].values)) for k, g in e.groupby('Year')}
w = {k: dict(zip(map(tuple, g[['CIK', 'CUSIP']].values), g.VALUE)) for k, g in e.groupby('Year')}
rows = []
for a, b in zip(q, q[1:]):
    A, B = hold[a], hold[b]
    cont = A & B
    up = sum(w[b][x] > 1.25 * w[a][x] for x in cont); dn = sum(w[b][x] < 0.75 * w[a][x] for x in cont)
    rows.append(dict(q=b, held_prev=len(A), entries=len(B - A), exits=len(A - B), cont=len(cont), up25=up, down25=dn))
r = pd.DataFrame(rows)
print(r.describe().loc[['mean', 'min', 'max']].round(1).to_string())
tot = r[['entries', 'exits', 'cont']].sum()
print('share of next-quarter positions that are entries', round(tot.entries / (tot.entries + tot.cont), 3))
print('exit rate of held positions', round(tot.exits / (tot.exits + tot.cont), 3))
# re-entries: entries into a stock the manager held at some earlier quarter
seen, reent, ent = set(), 0, 0
for a, b in zip(q, q[1:]):
    seen |= hold[a]
    new = hold[b] - hold[a]; ent += len(new); reent += len(new & seen)
print('entries that are re-entries (held before at some earlier quarter)', round(reent / ent, 3))
