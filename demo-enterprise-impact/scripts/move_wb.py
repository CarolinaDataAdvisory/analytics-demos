p_html = "demo-enterprise-impact/dashboard.html"
h = open(p_html, encoding="utf-8").read()
h = h.replace(r"LTV \,000+", "LTV $1,000+").replace(r"estimated \,000+", "estimated $68,000+")
open(p_html, "w", encoding="utf-8").write(h)

p_js = "demo-enterprise-impact/app.js"
j = open(p_js, encoding="utf-8").read()

move_code = """
const churnTable = document.getElementById('churnTable');
const churnWrap = churnTable.parentElement;
const churnHeader = churnWrap.previousElementSibling;
const insightsSection = churnWrap.parentElement;

wbSec.style.marginTop = '16px';
wbSec.style.marginBottom = '18px';
wbSec.style.background = '#0f172a';
wbSec.style.border = '1px solid #334155';

insightsSection.insertBefore(wbSec, churnHeader);
"""

open(p_js, "w", encoding="utf-8").write(j + "\n" + move_code)
print("MOVED WIN-BACK CHART ABOVE CHURN WATCHLIST & CLEANED TYPOS!")
