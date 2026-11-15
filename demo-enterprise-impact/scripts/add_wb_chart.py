p = "demo-enterprise-impact/app.js"
s = open(p, encoding="utf-8").read()
s = s.replace("adds ~ in cumulative", "adds ~$550K in cumulative")

chart_addon = """
const wbSec = el('div', '');
wbSec.style.marginTop = '20px';
wbSec.style.paddingTop = '16px';
wbSec.style.borderTop = '1px solid #334155';

const wbTitle = el('h3', '', 'High-Dollar Churn Win-Back ROI (6-Mo & 12-Mo)');
wbTitle.style.marginBottom = '10px';
wbSec.appendChild(wbTitle);

const oCost = D.churnCount * 15;
const fullRev = Math.round((D.churnPoolLtv / 2.5) * 0.05);
const halfRev = Math.round((D.churnPoolLtv / 2.5) * 0.05);
const yrRev = fullRev + halfRev;
const sixMoRev = liftGain;
const netProfit = yrRev - oCost;
const maxBar = Math.max(yrRev, sixMoRev, oCost);

const items = new Array(
  new Array('Outreach Cost (' + D.churnCount.toLocaleString() + ' donors @ $15)', oCost, '#f43f5e'),
  new Array('6-Mo Recovered Revenue (H1 2027)', sixMoRev, '#38bdf8'),
  new Array('12-Mo Recovered Revenue (5% Full + 10% Half)', yrRev, '#10b981')
);

items.forEach(it => {
  const rw = el('div', 'bar-row');
  rw.style.marginBottom = '10px';
  const lb = el('div', 'bar-label');
  lb.style.fontSize = '12px';
  const spVal = el('span', '', fmt(it.at(1)));
  spVal.style.color = it.at(2);
  lb.append(el('span', '', it.at(0)), spVal);
  const tk = el('div', 'bar-track');
  tk.style.height = '11px';
  const fl = el('div', 'bar-fill');
  fl.style.width = Math.max(4, (it.at(1) / maxBar * 100)).toFixed(1) + '%';
  fl.style.background = it.at(2);
  tk.appendChild(fl);
  rw.append(lb, tk);
  wbSec.appendChild(rw);
});

const summary = el('div', 'insight-box', 'Net 12-Mo Gain: +' + fmt(netProfit) + ' (' + (yrRev / oCost).toFixed(1) + 'x ROI) — ' + fmt(fullRev) + ' from 5% full-gift reactivations + ' + fmt(halfRev) + ' from 10% half-gift reactivations.');
summary.style.borderColor = '#10b981';
summary.style.fontSize = '12px';
summary.style.padding = '10px 12px';
wbSec.appendChild(summary);

document.getElementById('volBars').appendChild(wbSec);
"""

open(p, "w", encoding="utf-8").write(s + "\n" + chart_addon)
print("WIN-BACK CHART ADDED!")
