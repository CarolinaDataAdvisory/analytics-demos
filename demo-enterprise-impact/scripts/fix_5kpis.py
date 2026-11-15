p = "demo-enterprise-impact/app.js"
js = open(p, encoding="utf-8").read()

fix_kpis = """
const kpiBox = document.getElementById('kpiRow');
kpiBox.innerHTML = '';
const ds = D.donorStats;
const netSign = ds.netChange >= 0 ? '+' : '';
const netLabel = (ds.netChange >= 0 ? '↑ ' : '↓ ') + netSign + ds.netChange.toLocaleString() + ' Net Donors (' + netSign + ds.pctChange + '% vs 2025)';
const netColor = ds.netChange >= 0 ? '#10b981' : '#f43f5e';

new Array(
  new Array('3-Year Net Revenue', fmt(tot), '↑ 22% YoY Recurring Growth', '#38bdf8', '#10b981'),
  new Array('Active Donors (2026)', ds.active2026.toLocaleString() + ' (' + ds.totalUnique.toLocaleString() + ' Total)', netLabel, '#38bdf8', netColor),
  new Array('6-Mo Forecast (Baseline)', fmt(fBaseTot), 'H1 2027 Run-Rate Projection', '#a78bfa', '#10b981'),
  new Array('6-Mo With Churn Outreach', fmt(fWinTot), '+' + fmt(liftGain) + ' Gain (Cost: ~' + fmt(outreachCost) + ')', '#10b981', '#10b981'),
  new Array('Actionable Alerts', D.alerts.length + ' Items', 'Grants, Audits & Failed Gifts', '#f59e0b', '#f59e0b')
).forEach(k => {
  const c = el('div', 'card');
  c.appendChild(el('h3', '', k.at(0)));
  const v = el('div', 'val', k.at(1));
  v.style.color = k.at(3);
  v.style.fontSize = '22px';
  const sb = el('div', 'sub', k.at(2));
  sb.style.color = k.at(4);
  c.append(v, sb);
  kpiBox.appendChild(c);
});
"""

open(p, "w", encoding="utf-8").write(js + "\n" + fix_kpis)
print("ALL 5 KPI CARDS POPULATED!")
