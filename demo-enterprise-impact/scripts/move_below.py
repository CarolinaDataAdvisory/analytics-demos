p_html = "demo-enterprise-impact/dashboard.html"
h = open(p_html, encoding="utf-8").read()
h = h.replace(r"(\S COST PER BENEFICIARY)", "($ COST PER BENEFICIARY)")
open(p_html, "w", encoding="utf-8").write(h)

p_js = "demo-enterprise-impact/app.js"
j = open(p_js, encoding="utf-8").read()

old_move = """const churnTable = document.getElementById('churnTable');
const churnWrap = churnTable.parentElement;
const churnHeader = churnWrap.previousElementSibling;
const insightsSection = churnWrap.parentElement;

wbSec.style.marginTop = '16px';
wbSec.style.marginBottom = '18px';
wbSec.style.background = '#0f172a';
wbSec.style.border = '1px solid #334155';

insightsSection.insertBefore(wbSec, churnHeader);"""

new_move = """const churnTable = document.getElementById('churnTable');
const churnWrap = churnTable.parentElement;
const insightsSection = churnWrap.parentElement;

const bottomRow = el('div', 'gridEq');
bottomRow.style.marginTop = '18px';
bottomRow.style.marginBottom = '0';

wbSec.style.margin = '0';
wbSec.style.background = '#0f172a';
wbSec.style.border = '1px solid #334155';

const playbook = el('div', 'card');
playbook.style.margin = '0';
playbook.style.background = '#0f172a';
playbook.style.border = '1px solid #334155';
playbook.appendChild(el('h3', '', '90-Day Lapsed Donor Outreach Playbook (500 Targets)'));

const steps = new Array(
  new Array('Tier 1 — Top 50 Major Lapsed ($3,000+ LTV)', 'Personal phone call from Executive Director + private program site tour.', '#10b981'),
  new Array('Tier 2 — Next 150 Mid-Level Lapsed ($1,500–$2,999)', 'Handwritten impact note signed by a Board Member with 2026 outcome snapshot.', '#38bdf8'),
  new Array('Tier 3 — Remaining 300 Lapsed ($1,000–$1,499)', 'VIP invitation to upcoming Gala & hands-on volunteer preview day.', '#a78bfa')
);

steps.forEach(st => {
  const b = el('div', 'ibox');
  b.style.borderColor = st.at(2);
  b.style.marginBottom = '10px';
  b.style.padding = '10px 12px';
  b.style.background = '#1e293b';
  const t = el('h4', '', st.at(0));
  t.style.fontSize = '13px';
  const p = el('p', '', st.at(1));
  p.style.margin = '0';
  p.style.color = '#cbd5e1';
  p.style.fontSize = '12px';
  b.append(t, p);
  playbook.appendChild(b);
});

bottomRow.append(wbSec, playbook);
insightsSection.appendChild(bottomRow);"""

open(p_js, "w", encoding="utf-8").write(j.replace(old_move, new_move))
print("MOVED BELOW WATCHLIST IN COMPACT 2-COLUMN LAYOUT!")
