s = open("demo-enterprise-impact/app.js", encoding="utf-8").read()
wrapped = "try {\n" + s + "\n} catch (err) { document.getElementById('kpiRow').innerHTML = '<div style=\"background:#dc2626;color:#fff;padding:16px;border-radius:8px;grid-column:1/-1;font-weight:bold;\">JS ERROR: ' + err.message + ' | ' + err.stack + '</div>'; }"
open("demo-enterprise-impact/app.js", "w", encoding="utf-8").write(wrapped)
print("ERROR REPORTER ACTIVE!")
