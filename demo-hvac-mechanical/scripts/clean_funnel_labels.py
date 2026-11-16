folders = (
    "demo-hvac-mechanical",
    "demo-legal-partners",
    "demo-freight-logistics",
    "demo-electrical-supply",
    "demo-enterprise-impact"
)

old_draw = "fCtx.fillStyle = '#94a3b8'; fCtx.fillText(r.at(0).split(' ').slice(0, 2).join(' '), x, fH - 8);"
new_draw = "fCtx.fillStyle = '#94a3b8'; fCtx.font = '600 9.5px Segoe UI'; const pts = r.at(0).replace('(', '').replace(')', '').split(' '); fCtx.fillText(pts.at(0), x, fH - 15); if (pts.length > 1) { fCtx.fillText(pts.at(1), x, fH - 4); } fCtx.font = 'bold 10px Segoe UI';"

for folder in folders:
    p = f"{folder}/app.js"
    try:
        s = open(p, encoding="utf-8").read()
        s = s.replace("fCanvas.width = 480; fCanvas.height = 155;", "fCanvas.width = 540; fCanvas.height = 170;")
        s = s.replace("fP = 54;", "fP = 46;").replace("fP = 48;", "fP = 46;").replace("fP = 28;", "fP = 46;")
        s = s.replace(old_draw, new_draw)
        open(p, "w", encoding="utf-8").write(s)
        print("CLEANED FUNNEL LABELS:", folder)
    except Exception as e:
        print("Skipped:", folder, e)

# Also make HVAC middle labels concise two-word pairs
d_hvac = open("demo-hvac-mechanical/data.js", encoding="utf-8").read()
d_hvac = d_hvac.replace("Good-Better-Best Sent", "Options Sent").replace("Financing Reviewed", "Financing Check")
open("demo-hvac-mechanical/data.js", "w", encoding="utf-8").write(d_hvac)
