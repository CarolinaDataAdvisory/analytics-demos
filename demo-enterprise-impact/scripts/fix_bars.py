p = "demo-enterprise-impact/app.js"
s = open(p, encoding="utf-8").read()
s = s.replace("'bar-row'", "'brow'").replace("'bar-label'", "'blbl'").replace("'bar-track'", "'btrk'").replace("'bar-fill'", "'bfil'")
open(p, "w", encoding="utf-8").write(s)
print("BAR CLASSES FIXED!")
