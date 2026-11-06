"""Copy BibTeX entries by key from the earlier scouting repos into references.bib (skips keys already present).
Usage: python tools/bib_pull.py key1 key2 ...   (run from the repo root)"""
import re, sys, pathlib
SRC = [pathlib.Path('/home/claude/lennyamsterdam1717/thesis-proposals/references.bib'),
       pathlib.Path('/home/claude/lennyamsterdam1717/thesis-attempt-2/references.bib')]
OUT = pathlib.Path('references.bib')
def entries(text):
    out, i = {}, 0
    for m in re.finditer(r'@\w+\{([^,]+),', text):
        start = m.start(); depth = 0
        for j in range(text.index('{', start), len(text)):
            depth += text[j] == '{'; depth -= text[j] == '}'
            if depth == 0: out[m.group(1).strip()] = text[start:j+1]; break
    return out
have = entries(OUT.read_text()) if OUT.exists() else {}
src = {}
for p in SRC: src.update({k: v for k, v in entries(p.read_text()).items() if k not in src})
add = []
for k in sys.argv[1:]:
    if k in have: continue
    if k not in src: print('MISSING', k); continue
    add.append(src[k])
with OUT.open('a') as f:
    for e in add: f.write('\n' + e + '\n')
print('added', len(add))
