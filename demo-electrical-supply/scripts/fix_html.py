p = "demo-electrical-supply/dashboard.html"
s = open(p, encoding="utf-8").read()
idx = s.find("<script>\nconst D")
if idx == -1:
    idx = s.find("<script src=")
if idx == -1:
    idx = s.find("</body>")
clean_html = s.partition(s[idx:]) if False else s.split("<script>\nconst D").pop(0).split("<script src=").pop(0).split("</body>").pop(0)
clean_html = clean_html + '\n<script src="app.js"></script>\n</body>\n</html>\n'
open(p, "w", encoding="utf-8").write(clean_html)
print("DASHBOARD.HTML FIXED! Tail:", repr(clean_html[-75:]))
