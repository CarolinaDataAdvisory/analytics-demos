p = "demo-enterprise-impact/app.js"
s = open(p, encoding="utf-8").read()

old_split = """const wbSec = el('div', '');
wbSec.style.marginTop = '20px';
wbSec.style.paddingTop = '16px';
wbSec.style.borderTop = '1px solid #334155';"""

new_split = """const rightCol = document.getElementById('volBars').parentElement;
rightCol.style.background = 'transparent';
rightCol.style.border = 'none';
rightCol.style.padding = '0';
rightCol.style.display = 'flex';
rightCol.style.flexDirection = 'column';
rightCol.style.gap = '18px';

const topCard = el('div', 'card');
while (rightCol.firstChild) { topCard.appendChild(rightCol.firstChild); }
rightCol.appendChild(topCard);

const wbSec = el('div', 'card');"""

s = s.replace(old_split, new_split)
s = s.replace("summary.style.borderColor = '#10b981';", "summary.className = 'ibox'; summary.style.borderColor = '#10b981'; summary.style.marginTop = '14px';")
s = s.replace("document.getElementById('volBars').appendChild(wbSec);", "rightCol.appendChild(wbSec);")

open(p, "w", encoding="utf-8").write(s)
print("SEPARATE CARDS POLISHED!")
