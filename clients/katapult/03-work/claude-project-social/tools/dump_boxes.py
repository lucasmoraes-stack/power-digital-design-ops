"""Measure every image slot's visible box per layout (headless Chrome) -> studio/boxes.json, used by build_project.py."""
import functools, html, http.server, json, re, socketserver, subprocess, threading
from pathlib import Path
ST = Path(__file__).resolve().parents[1] / "studio"
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ST)); H.log_message = lambda *a: None
srv = socketserver.TCPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{srv.server_address[1]}/katapult-social-studio.html?dump=1"
dom = subprocess.run([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "--headless=new", "--virtual-time-budget=20000", "--dump-dom", url],
                     capture_output=True, text=True, encoding="utf-8", timeout=200).stdout
srv.shutdown()
data = json.loads(html.unescape(re.search(r'<pre id="autotest-out">(.*?)</pre>', dom, re.S).group(1)))
(ST / "boxes.json").write_text(json.dumps(data, indent=1), encoding="utf-8")
print(len(data), "layouts with image slots")
