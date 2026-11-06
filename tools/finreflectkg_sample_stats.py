"""Sample statistics of company-company relations in FinReflectKG (a few parquet shards).
Usage: python -I tools/finreflectkg_sample_stats.py <shard.parquet ...> <sp500.csv from fja05680/sp500>"""
import sys, pandas as pd
shards, spfile = sys.argv[1:-1], sys.argv[-1]
d = pd.concat([pd.read_parquet(f, columns=['entity', 'entity_type', 'relationship', 'target', 'target_type', 'ticker', 'year'])
               for f in shards], ignore_index=True)
print('rows', len(d), 'tickers', d.ticker.nunique(), sorted(d.ticker.unique()))
sp = pd.read_csv(spfile)
def norm(s):
    return (s.str.lower().str.replace(r'[^a-z0-9 ]', '', regex=True)
             .str.replace(r'\b(inc|corp|corporation|company|co|plc|ltd|group|holdings|the)\b', '', regex=True)
             .str.replace(r'\s+', ' ', regex=True).str.strip())
nm = dict(zip(norm(sp.Security), sp.Symbol))
tk = {s.lower(): s for s in sp.Symbol}
tgt = norm(d.target).map(nm)
tgt = tgt.fillna(d.target.str.lower().map(tk))
d['tgt_tic'] = tgt
m = d[d.tgt_tic.notna() & (d.tgt_tic.str.lower() != d.ticker.str.lower()) & d.target_type.isin(['ORG', 'COMP', 'FIN_INST'])]
rel_map = {'competes_with': 'compete', 'competes_against': 'compete', 'competes': 'compete', 'partners_with': 'partner',
           'collaborates': 'partner', 'works_with': 'partner', 'depends_on': 'depends', 'supply': 'supply', 'supplies': 'supply',
           'has_stake_in': 'stake', 'invests_in': 'stake', 'own': 'stake'}
m = m.assign(rel=m.relationship.map(rel_map)).dropna(subset=['rel'])
e = m[['ticker', 'tgt_tic', 'rel', 'year']].drop_duplicates()
print('distinct (src,dst,rel,year) edges', len(e), '| distinct (src,dst,rel)', len(e[['ticker', 'tgt_tic', 'rel']].drop_duplicates()))
print(e.rel.value_counts().to_dict())
print('edges per ticker-year', round(len(e) / d.groupby(['ticker', 'year']).ngroups, 2))
s = set(map(tuple, e.values)); y0 = e.year.min()
later = [x for x in s if x[3] > y0]
print('share of yearly edges also present in the previous year', round(sum((a, b, r, y - 1) in s for a, b, r, y in later) / len(later), 3), 'n', len(later))
ever, new = set(), 0
for y in sorted(e.year.unique()):
    cur = set(map(tuple, e[e.year == y][['ticker', 'tgt_tic', 'rel']].values))
    if y > y0: new += len(cur - ever)
    ever |= cur
print('never-seen-before edges after the first year', new, 'of', len(later))
print('edges per year', e.groupby('year').size().to_dict())
