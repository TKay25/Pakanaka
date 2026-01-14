import re
from pathlib import Path
p=Path('c:/Users/Lenovo/Documents/GitHub/Pakanaka/main.html')
s=p.read_text(encoding='utf8')
m=re.search(r'<script[^>]*>([\s\S]*?)</script>', s, re.I)
if not m:
    print('No <script> block found')
    raise SystemExit(2)
script=m.group(1)
stack=[]
line=1
col=0
in_s=None
escape=False
for i,ch in enumerate(script):
    if ch=='\n':
        line+=1; col=0; escape=False; continue
    col+=1
    if escape:
        escape=False
        continue
    if in_s:
        if ch=='\\':
            escape=True
            continue
        if in_s=='"' and ch=='"':
            in_s=None; continue
        if in_s=="'" and ch=="'":
            in_s=None; continue
        if in_s=='`':
            if ch=='`':
                in_s=None; continue
            if ch=='$' and i+1 < len(script) and script[i+1]=='{':
                stack.append(('${', line, col))
                continue
            continue
        continue
    else:
        if ch in ('"',"'",'`'):
            in_s=ch
            continue
        if ch in '([{':
            stack.append((ch,line,col))
            continue
        if ch in ')]}':
            if not stack:
                print(f'Unexpected closing {ch} at line {line} col {col}')
                raise SystemExit(1)
            top,tl,tc=stack.pop()
            pairs={ '(':')','[':']','{':'}','${':'}' }
            expected=pairs.get(top)
            if expected!=ch:
                print(f'Mismatch: opened {top} at {tl}:{tc} but closed with {ch} at {line}:{col}')
                raise SystemExit(1)

if in_s:
    print(f'Unterminated string starting with {in_s} at line {line} col {col}')
    raise SystemExit(1)
if stack:
    print('Unclosed tokens:')
    for t,tl,tc in stack:
        print(f'  {t} opened at {tl}:{tc}')
    raise SystemExit(1)
print('No bracket/quote mismatches found')
