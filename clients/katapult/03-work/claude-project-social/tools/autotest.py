"""Local test: serve studio/, open the page in headless Chrome with #autotest, save the PNGs and checks it produces.
Usage: python tools/autotest.py [post.html]   (default: the built-in example). Writes studio/_test/."""
import base64, json, re, subprocess, sys, threading, functools, http.server, socketserver
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]; ST = HERE / "studio"; OUT = ST / "_test"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
post = sys.argv[1] if len(sys.argv) > 1 else None
if post:
    (ST / "_post.html").write_text(Path(post).read_text(encoding="utf-8"), encoding="utf-8")
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ST))
H.log_message = lambda *a: None
srv = socketserver.TCPServer(("127.0.0.1", 0), H); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{port}/katapult-social-studio.html?post={'_post.html' if post else 'none'}&autotest=1"
dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=120000", "--run-all-compositor-stages-before-draw",
                      "--window-size=1400,1000", "--dump-dom", url], capture_output=True, text=True, encoding="utf-8", timeout=300).stdout
srv.shutdown()
m = re.search(r'<pre id="autotest-out">(.*?)</pre>', dom, re.S)
if not m:
    sys.exit("no autotest output; page may have failed\n" + dom[-2000:])
import html as H2
data = json.loads(H2.unescape(m.group(1)))
OUT.mkdir(exist_ok=True)
for d in data:
    (OUT / f"{d['name']}.png").write_bytes(base64.b64decode(d["png"].split(",", 1)[1]))
    print(d["name"], "|", "; ".join(d["checks"]))
