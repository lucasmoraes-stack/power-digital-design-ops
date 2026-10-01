"""Replace the V2 COMPONENTS block in both DS copies with kp_v2.css (keeps them in sync)."""
import io, os, re
D = os.path.dirname(os.path.abspath(__file__))
css = io.open(os.path.join(D, "kp_v2.css"), encoding="utf-8").read().rstrip() + "\n"
assert css.rstrip().endswith("/* END V2 COMPONENTS */")
for f in [os.path.join(D, "katapult-ds-src.html"), os.path.join(D, "katapult-ds", "index.html")]:
    t = io.open(f, encoding="utf-8").read()
    start = t.index("/* =================================================================\n   V2 COMPONENTS")
    end = t.index("\n@media (max-width:640px){", start)
    t = t[:start] + css + t[end:]
    io.open(f, "w", encoding="utf-8", newline="\n").write(t)
print("synced")
