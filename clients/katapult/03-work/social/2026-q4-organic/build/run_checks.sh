export PYTHONIOENCODING=utf-8
D="C:/Users/lucas/AppData/Local/Temp/claude/c--Users-lucas-OneDrive-Desktop-VAZIO-power-digital-ops/93dbe328-a65f-4b12-958f-086bc971a00c/scratchpad/katapult-q4"
C="/c/Program Files/Google/Chrome/Application/chrome.exe"
cat "$D/index.html" "$D/checker.js" > "$D/check.html"
"$C" --headless=new --disable-gpu --virtual-time-budget=10000 --window-size=1400,1000 --dump-dom "file:///$D/check.html" > "$D/dom.html" 2>/dev/null
python - "$D/dom.html" <<'P'
import sys,re,html
t=open(sys.argv[1],encoding='utf-8').read()
m=re.search(r'<pre id="layout-report">(.*?)</pre>',t,re.S)
print(html.unescape(m.group(1)) if m else "NO REPORT")
P
