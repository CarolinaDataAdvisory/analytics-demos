p1 = """
const D = window.DASH_DATA;
const el = (t, c, x) => { const n = document.createElement(t); if (c) n.className = c; if (x !== undefined) n.textContent = x; return n; };
const fmt = n => '$' + Number(n).toLocaleString('en-US', {maximumFractionDigits: 0});

const tot = D.rev.reduce((s, r) => s + Number(r.at(2)), 0);
const fvBase = D.rev.slice(24, 30).map(r => Math.round(Number(r.at(2)) * 1.18));
const fBaseTot = fvBase.reduce((s, v) => s + v, 0);

const annualPool = D.churnPoolLtv / 2.5;
const fullRev = Math.round(annualPool * 0.05);
const halfRev = Math.round(annualPool * 0.05);
const yrRev = fullRev + halfRev;
const monthlyLift = Math.round(yrRev / 12);
const fvWinback = fvBase.map((v, i) => v + Math.round(monthlyLift * (0.6 + i * 0.16)));
const fWinTot = fvWinback.reduce((s, v) => s + v, 0);
const liftGain = fWinTot - fBaseTot;
const outCost = D.churnCount * 15;
const wbRoi = (yrRev / outCost).toFixed(1);

if (document.getElementById('wbStat')) {
  document.getElementById('wbStat').textContent = '+' + fmt(liftGain) + ' (6-Mo) / +' + fmt(yrRev) + '/yr';
  document.getElementById('wbDesc').textContent = 'Reaching all ' + D.churnCount.toLocaleString() + ' lapsed $1,000+ donors via calls, handwritten board notes & VIP tours costs ~' + fmt(outCost) + ' ($15/donor) and returns ' + wbRoi + 'x ROI at 5% full + 10% half-gift reactivation.';
}

const ds = D.donorStats || {totalUnique: 7787, active2026: 5420, netChange: 312, pctChange: 6.1};
const netSign = ds.netChange >= 0 ? '+' : '';
const netLabel = (ds.netChange >= 0 ? '↑ ' : '↓ ') + netSign + ds.netChange.toLocaleString() + ' Net Donors (' + netSign + ds.pctChange + '% vs 2025)';
const netColor = ds.netChange >= 0 ? '#10b981' : '#f43f5e';

new Array(
  new Array('3-Year Net Revenue', fmt(tot), '↑ 22% YoY Recurring Growth', '#38bdf8', '#10b981'),
  new Array('Active Donors (2026)', ds.active2026.toLocaleString() + ' (' + ds.totalUnique.toLocaleString() + ' Total)', netLabel, '#38bdf8', netColor),
  new Array('6-Mo Forecast (Baseline)', fmt(fBaseTot), 'H1 2027 Run-Rate Projection', '#a78bfa', '#10b981'),
  new Array('6-Mo With Churn Outreach', fmt(fWinTot), '+' + fmt(liftGain) + ' Gain (Cost: ~' + fmt(outCost) + ')', '#10b981', '#10b981'),
  new Array('Actionable Alerts', D.alerts.length + ' Items', 'Grants, Audits & Failed Gifts', '#f59e0b', '#f59e0b')
).forEach(k => {
  const c = el('div', 'card');
  c.appendChild(el('h3', '', k.at(0)));
  const v = el('div', 'val', k.at(1)); v.style.color = k.at(3); v.style.fontSize = '22px';
  const sb = el('div', 'sub', k.at(2)); sb.style.color = k.at(4);
  c.append(v, sb);
  document.getElementById('kpiRow').appendChild(c);
});

const cv = document.getElementById('lineCanvas'), ctx = cv.getContext('2d'), W = cv.width, H = cv.height, P = 34;
const allV = D.rev.map(r => Number(r.at(2))).concat(fvWinback), mx = Math.max(...allV) * 1.06, totPts = 42;
const gx = i => P + (i / (totPts - 1)) * (W - P * 2), gy = v => H - P - (v / mx) * (H - P * 2);
const fX0 = gx(35), fW = gx(41) - fX0;
ctx.fillStyle = 'rgba(167,139,250,0.14)'; ctx.fillRect(fX0, 16, fW, H - P - 16);
ctx.strokeStyle = '#a78bfa'; ctx.setLineDash(new Array(4, 4)); ctx.beginPath(); ctx.moveTo(fX0, 16); ctx.lineTo(fX0, H - P); ctx.stroke(); ctx.setLineDash(new Array());
ctx.fillStyle = '#c4b5fd'; ctx.font = 'bold 11px Segoe UI'; ctx.fillText('FORECAST ZONE', fX0 + 10, 30);
ctx.beginPath(); ctx.moveTo(gx(0), H - P); D.rev.forEach((r, i) => ctx.lineTo(gx(i), gy(Number(r.at(2))))); ctx.lineTo(gx(35), H - P); ctx.closePath();
ctx.fillStyle = 'rgba(56,189,248,0.15)'; ctx.fill();
ctx.beginPath(); D.rev.forEach((r, i) => { const x = gx(i), y = gy(Number(r.at(2))); i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y); });
ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 2.5; ctx.stroke();
const lastAct = Number(D.rev.at(35).at(2));
ctx.setLineDash(new Array(6, 4));
ctx.beginPath(); ctx.moveTo(gx(35), gy(lastAct)); fvBase.forEach((v, i) => ctx.lineTo(gx(36 + i), gy(v))); ctx.strokeStyle = '#a78bfa'; ctx.lineWidth = 2.5; ctx.stroke();
ctx.beginPath(); ctx.moveTo(gx(35), gy(lastAct)); fvWinback.forEach((v, i) => ctx.lineTo(gx(36 + i), gy(v))); ctx.strokeStyle = '#10b981'; ctx.lineWidth = 2.8; ctx.stroke();
ctx.setLineDash(new Array());
D.rev.forEach((r, i) => { const q4 = r.at(0).endsWith('-11') || r.at(0).endsWith('-12'); ctx.beginPath(); ctx.arc(gx(i), gy(Number(r.at(2))), q4 ? 4 : 2.3, 0, Math.PI * 2); ctx.fillStyle = q4 ? '#f59e0b' : '#38bdf8'; ctx.fill(); });
fvBase.forEach((v, i) => { ctx.beginPath(); ctx.arc(gx(36 + i), gy(v), 3.5, 0, Math.PI * 2); ctx.fillStyle = '#a78bfa'; ctx.fill(); });
fvWinback.forEach((v, i) => { ctx.beginPath(); ctx.arc(gx(36 + i), gy(v), 4, 0, Math.PI * 2); ctx.fillStyle = '#10b981'; ctx.fill(); });

const ml = Math.max(...D.vol.map(r => Number(r.at(3))));
D.vol.forEach((r, i) => {
  const rw = el('div', 'brow'), lb = el('div', 'blbl');
  lb.append(el('span', '', r.at(0) + ' (' + Number(r.at(1)).toLocaleString() + ' donors • ' + r.at(2) + ' gifts/ea)'), el('span', '', fmt(r.at(3))));
  const tk = el('div', 'btrk'), fl = el('div', 'bfil');
  fl.style.width = (Number(r.at(3)) / ml * 100).toFixed(1) + '%'; fl.style.background = i === 0 ? '#10b981' : '#64748b';
  tk.appendChild(fl); rw.append(lb, tk); document.getElementById('volBars').appendChild(rw);
});
const tp = el('div', 'ibox', 'Quick Win: Converting 10% of Donor-Only supporters into volunteers adds ~$550K in cumulative lifetime giving.');
tp.style.marginTop = '14px'; document.getElementById('volBars').appendChild(tp);
"""
open("demo-enterprise-impact/app.js", "w", encoding="utf-8").write(p1)
print("PART 1 WRITTEN!")
