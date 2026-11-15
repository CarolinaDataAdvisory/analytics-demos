p_css = "demo-enterprise-impact/style.css"
css = open(p_css, encoding="utf-8").read().replace("repeat(4,1fr)", "repeat(5,1fr)")
open(p_css, "w", encoding="utf-8").write(css)

p_js = "demo-enterprise-impact/app.js"
js = open(p_js, encoding="utf-8").read()

old_kpis = """new Array(new Array('3-Year Net Revenue',fmt(tot),'↑ 22% YoY Recurring Growth','#38bdf8'),new Array('6-Mo Forecast (Baseline)',fmt(fBaseTot),'H1 2027 Run-Rate Projection','#a78bfa'),new Array('6-Mo With Churn Outreach',fmt(fWinTot),'+'+fmt(liftGain)+' Gain (Cost: ~'+fmt(outreachCost)+')','#10b981'),new Array('Actionable Alerts',D.alerts.length+' Items','Grants, Audits & Failed Gifts','#f59e0b')).forEach(k=>{const c=el('div','card');c.appendChild(el('h3','',k.at(0)));const v=el('div','val',k.at(1));v.style.color=k.at(3);c.append(v,el('div','sub',k.at(2)));document.getElementById('kpiRow').appendChild(c)});"""

new_kpis = """const ds = D.donorStats;
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
  v.style.fontSize = '24px';
  const sb = el('div', 'sub', k.at(2));
  sb.style.color = k.at(4);
  c.append(v, sb);
  document.getElementById('kpiRow').appendChild(c);
});"""

open(p_js, "w", encoding="utf-8").write(js.replace(old_kpis, new_kpis))
print("5-CARD KPI ROW UPDATED!")
