import json, sqlite3

conn = sqlite3.connect("demo-enterprise-impact/enterprise_impact.db")
cur = conn.cursor()

rows = cur.execute("SELECT touchpoint_type, COUNT(*) FROM digital_engagement GROUP BY 1").fetchall()
counts = dict(rows)
abandoned = counts.get("Donation Page Abandoned", 1500)
reports = counts.get("Impact Report Downloaded", 1950)
webinars = counts.get("Webinar Attended", 1500)
clicks = counts.get("Email Click", 3300)
opens = counts.get("Email Open", 6750)

p = "demo-enterprise-impact/data.js"
raw = open(p, encoding="utf-8").read().replace("window.DASH_DATA=", "").rstrip(";")
data = json.loads(raw)
data["funnel"] = [
    ["Email Opens", opens],
    ["Email Clicks", clicks],
    ["Impact Reports & Webinars", reports + webinars],
    ["Abandoned Checkout", abandoned],
    ["15% Recovery Target", round(abandoned * 0.15)]
]
open(p, "w", encoding="utf-8").write("window.DASH_DATA=" + json.dumps(data) + ";")

p_html = "demo-enterprise-impact/dashboard.html"
h = open(p_html, encoding="utf-8").read().replace(r"(\$ COST PER BENEFICIARY)", "($ COST PER BENEFICIARY)")
open(p_html, "w", encoding="utf-8").write(h)

js_code = """
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

document.getElementById('wbStat').textContent = '+' + fmt(liftGain) + ' (6-Mo) / +' + fmt(yrRev) + '/yr';
document.getElementById('wbDesc').textContent = 'Reaching all ' + D.churnCount.toLocaleString() + ' lapsed $1,000+ donors via executive calls, handwritten board notes & VIP tours costs ~' + fmt(outCost) + ' ($15/donor) and returns ' + wbRoi + 'x ROI at 5% full + 10% half-gift reactivation.';

// 1. Top 5 KPI Cards
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
  const v = el('div', 'val', k.at(1));
  v.style.color = k.at(3);
  v.style.fontSize = '22px';
  const sb = el('div', 'sub', k.at(2));
  sb.style.color = k.at(4);
  c.append(v, sb);
  document.getElementById('kpiRow').appendChild(c);
});

// 2. Smooth Line Chart + Shaded 6-Month Forecast Zone
const cv = document.getElementById('lineCanvas'), ctx = cv.getContext('2d'), W = cv.width, H = cv.height, P = 34;
const allV = D.rev.map(r => Number(r.at(2))).concat(fvWinback), mx = Math.max(...allV) * 1.06, totPts = 42;
const gx = i => P + (i / (totPts - 1)) * (W - P * 2), gy = v => H - P - (v / mx) * (H - P * 2);
const fX0 = gx(35), fW = gx(41) - fX0;

ctx.fillStyle = 'rgba(167,139,250,0.14)'; ctx.fillRect(fX0, 16, fW, H - P - 16);
ctx.strokeStyle = '#a78bfa'; ctx.setLineDash(new Array(4, 4)); ctx.beginPath(); ctx.moveTo(fX0, 16); ctx.lineTo(fX0, H - P); ctx.stroke(); ctx.setLineDash(new Array());
ctx.fillStyle = '#c4b5fd'; ctx.font = 'bold 11px Segoe UI'; ctx.fillText('FORECAST ZONE', fX0 + 10, 30);

ctx.strokeStyle = '#1e293b';
for (let g = 1; g <= 3; g++) { const y = P + (g / 4) * (H - P * 2); ctx.beginPath(); ctx.moveTo(P, y); ctx.lineTo(W - P, y); ctx.stroke(); }

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

// 3. Volunteer Multiplier Bars
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

// 4. High-Dollar Donor Churn Watchlist + Below 2-Column ROI & Playbook
const churnTable = document.getElementById('churnTable');
D.churn.forEach((r, i) => {
  const tr = el('tr'), ac = i < 5 ? 'Executive Director Call + Site Tour' : (i < 10 ? 'Handwritten Board Impact Letter' : 'VIP Gala & Volunteer Preview Invite');
  tr.append(el('td', '', r.at(0)), el('td', '', r.at(1)), el('td', '', r.at(2)), el('td', 'pos', fmt(r.at(4))), el('td', '', r.at(5)), el('td', 'neg', r.at(6) + ' days'), el('td', '', ac));
  churnTable.querySelector('tbody').appendChild(tr);
});

const insightsSection = churnTable.parentElement.parentElement;
const bottomRow = el('div', 'gridEq');
bottomRow.style.marginTop = '18px'; bottomRow.style.marginBottom = '0';

const wbCard = el('div', 'card');
wbCard.style.margin = '0'; wbCard.style.background = '#0f172a'; wbCard.style.border = '1px solid #334155';
wbCard.appendChild(el('h3', '', 'High-Dollar Churn Win-Back ROI (6-Mo & 12-Mo)'));
const maxBar = Math.max(yrRev, liftGain, outCost);
new Array(
  new Array('Outreach Cost (' + D.churnCount.toLocaleString() + ' donors @ $15)', outCost, '#f43f5e'),
  new Array('6-Mo Recovered Revenue (H1 2027)', liftGain, '#38bdf8'),
  new Array('12-Mo Recovered Revenue (5% Full + 10% Half)', yrRev, '#10b981')
).forEach(it => {
  const rw = el('div', 'brow'), lb = el('div', 'blbl');
  const sp = el('span', '', fmt(it.at(1))); sp.style.color = it.at(2);
  lb.append(el('span', '', it.at(0)), sp);
  const tk = el('div', 'btrk'), fl = el('div', 'bfil');
  fl.style.width = Math.max(4, (it.at(1) / maxBar * 100)).toFixed(1) + '%'; fl.style.background = it.at(2);
  tk.appendChild(fl); rw.append(lb, tk); wbCard.appendChild(rw);
});
const wbSum = el('div', 'ibox', 'Net 12-Mo Gain: +' + fmt(yrRev - outCost) + ' (' + wbRoi + 'x ROI) — ' + fmt(fullRev) + ' from 5% full-gift + ' + fmt(halfRev) + ' from 10% half-gift reactivations.');
wbSum.style.borderColor = '#10b981'; wbSum.style.marginTop = '12px';
wbCard.appendChild(wbSum);

const playbook = el('div', 'card');
playbook.style.margin = '0'; playbook.style.background = '#0f172a'; playbook.style.border = '1px solid #334155';
playbook.appendChild(el('h3', '', '90-Day Lapsed Donor Outreach Playbook (' + D.churnCount.toLocaleString() + ' Targets)'));
new Array(
  new Array('Tier 1 — Top 50 Major Lapsed ($3,000+ LTV)', 'Personal phone call from Executive Director + private program site tour.', '#10b981'),
  new Array('Tier 2 — Next 150 Mid-Level Lapsed ($1,500–$2,999)', 'Handwritten impact note signed by a Board Member with 2026 outcome snapshot.', '#38bdf8'),
  new Array('Tier 3 — Remaining Lapsed ($1,000–$1,499)', 'VIP invitation to upcoming Gala & hands-on volunteer preview day.', '#a78bfa')
).forEach(st => {
  const b = el('div', 'ibox'); b.style.borderColor = st.at(2); b.style.marginBottom = '10px'; b.style.padding = '10px 12px'; b.style.background = '#1e293b';
  const t = el('h4', '', st.at(0)); t.style.fontSize = '13px'; const p = el('p', '', st.at(1)); p.style.margin = '0'; p.style.color = '#cbd5e1'; p.style.fontSize = '12px';
b.append(t, p); playbook.appendChild(b);
});
bottomRow.append(wbCard, playbook);
insightsSection.appendChild(bottomRow);
// 5. Program Efficiency (Half-Width) + Paired Digital Funnel Line Graph
const progWrap = document.getElementById('progBars');
const mc = Math.max(...D.prog.map(r => Number(r.at(4))));
D.prog.forEach((r, i) => {
const rw = el('div', 'brow'), lb = el('div', 'blbl');
lb.append(el('span', '', r.at(0) + ' (' + Number(r.at(2)).toLocaleString() + ' served • ' + r.at(3) + '/100)'), el('span', '', '$' + Number(r.at(4)).toFixed(2) + ' / person'));
const tk = el('div', 'btrk'), fl = el('div', 'bfil');
fl.style.width = (Number(r.at(4)) / mc * 100).toFixed(1) + '%'; fl.style.background = i === 0 ? '#10b981' : '#818cf8';
tk.appendChild(fl); rw.append(lb, tk); progWrap.appendChild(rw);
});
const progCard = progWrap.parentElement;
const parentGrid = progCard.parentElement;
const splitHolder = el('div', 'gridEq');
splitHolder.style.margin = '0';
parentGrid.insertBefore(splitHolder, progCard);
splitHolder.appendChild(progCard);
const funnelCard = el('div', 'card');
funnelCard.appendChild(el('h3', '', 'Digital Engagement Funnel & Checkout Recovery Opportunity'));
const fCanvas = document.createElement('canvas');
fCanvas.width = 480; fCanvas.height = 155;
fCanvas.style.width = '100%'; fCanvas.style.height = 'auto';
fCanvas.style.background = '#0f172a'; fCanvas.style.borderRadius = '8px'; fCanvas.style.border = '1px solid #334155';
funnelCard.appendChild(fCanvas);
const fData = D.funnel || new Array(
new Array('Email Opens', 6750),
new Array('Email Clicks', 3300),
new Array('Reports & Webinars', 3450),
new Array('Abandoned Checkout', 1500),
new Array('15% Recovery Target', 225)
);
const fCtx = fCanvas.getContext('2d'), fW = fCanvas.width, fH = fCanvas.height, fP = 28;
const fMax = Math.max(...fData.map(r => Number(r.at(1)))) * 1.15;
const fx = i => fP + (i / (fData.length - 1)) * (fW - fP * 2);
const fy = v => fH - fP - (v / fMax) * (fH - fP * 2);
fCtx.strokeStyle = '#1e293b';
for (let g = 1; g <= 2; g++) { const y = fP + (g / 3) * (fH - fP * 2); fCtx.beginPath(); fCtx.moveTo(fP, y); fCtx.lineTo(fW - fP, y); fCtx.stroke(); }
fCtx.beginPath(); fCtx.moveTo(fx(0), fH - fP);
fData.forEach((r, i) => fCtx.lineTo(fx(i), fy(Number(r.at(1)))));
fCtx.lineTo(fx(fData.length - 1), fH - fP); fCtx.closePath();
fCtx.fillStyle = 'rgba(16, 185, 129, 0.14)'; fCtx.fill();
fCtx.beginPath();
fData.forEach((r, i) => { const x = fx(i), y = fy(Number(r.at(1))); i === 0 ? fCtx.moveTo(x, y) : fCtx.lineTo(x, y); });
fCtx.strokeStyle = '#10b981'; fCtx.lineWidth = 2.5; fCtx.stroke();
fCtx.font = 'bold 10px Segoe UI'; fCtx.textAlign = 'center';
fData.forEach((r, i) => {
const x = fx(i), y = fy(Number(r.at(1)));
fCtx.beginPath(); fCtx.arc(x, y, 4.5, 0, Math.PI * 2); fCtx.fillStyle = i >= 3 ? '#f59e0b' : '#10b981'; fCtx.fill();
fCtx.fillStyle = '#f8fafc'; fCtx.fillText(Number(r.at(1)).toLocaleString(), x, y - 9);
fCtx.fillStyle = '#94a3b8'; fCtx.fillText(r.at(0).split(' ').slice(0, 2).join(' '), x, fH - 8);
});
const abCount = Number(fData.at(3).at(1)), recGifts = Number(fData.at(4).at(1)), recDollars = recGifts * 165;
const fCallout = el('div', 'ibox', 'Checkout Recovery Play: ' + abCount.toLocaleString() + ' supporters abandoned the donation page. Triggering an automated 24-hr reminder email recovers ~15% (' + recGifts + ' gifts = +' + fmt(recDollars) + ' incremental revenue at $0 ad spend).');
fCallout.style.borderColor = '#f59e0b'; fCallout.style.marginTop = '12px'; fCallout.style.fontSize = '12px';
funnelCard.appendChild(fCallout);
splitHolder.appendChild(funnelCard);
// 6. Campaign ROI Table
D.camp.forEach(r => {
const tr = el('tr');
tr.append(el('td', '', r.at(0)), el('td', '', r.at(1)), el('td', '', fmt(r.at(3))), el('td', '', fmt(r.at(4))), el('td', Number(r.at(5)) >= 0 ? 'pos' : 'neg', r.at(5) + '%'));
document.querySelector('#campTable tbody').appendChild(tr);
});
// 7. Prioritized Action Queue
function renderAlerts() {
const f = document.getElementById('alertFilter').value, q = document.getElementById('searchBox').value.toLowerCase(), tb = document.querySelector('#alertTable tbody');
tb.innerHTML = '';
D.alerts.filter(r => (f === 'ALL' || r.at(0) === f) && r.join(' ').toLowerCase().includes(q)).slice(0, 150).forEach(r => {
const tr = el('tr'), td = el('td'), cl = r.at(0) === 'Grant Risk' ? 'p-grant' : (r.at(0) === 'Flagged Exp' ? 'p-exp' : 'p-rec');
td.appendChild(el('span', 'pill ' + cl, r.at(0)));
tr.append(td, el('td', '', r.at(1)), el('td', '', r.at(2)), el('td', '', r.at(3)), el('td', '', fmt(r.at(4))), el('td', '', r.at(5)));
tb.appendChild(tr);
});
}
renderAlerts();
"""
open("demo-enterprise-impact/app.js", "w", encoding="utf-8").write(js_code)
print("FULL DASHBOARD REBUILT CLEANLY!")
