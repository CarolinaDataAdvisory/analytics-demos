
const D = window.DASH_DATA;
const el = (t, c, x) => { const n = document.createElement(t); if (c) n.className = c; if (x !== undefined) n.textContent = x; return n; };
const fmt = n => '$' + Number(n).toLocaleString('en-US', {maximumFractionDigits: 0});

const tot = D.rev.reduce((s, r) => s + Number(r.at(2)), 0);
const fvBase = D.rev.slice(24, 30).map(r => Math.round(Number(r.at(2)) * 1.09));
const fBaseTot = fvBase.reduce((s, v) => s + v, 0);

const annualPool = D.churnPoolLtv / 2.8;
const fullRev = Math.round(annualPool * 0.09);
const halfRev = Math.round(annualPool * 0.09);
const yrRev = fullRev + halfRev;
const monthlyLift = Math.round(yrRev / 12);
const fvWinback = fvBase.map((v, i) => v + Math.round(monthlyLift * (0.6 + i * 0.16)) + Math.round(145000 + i * 36667));
const fWinTot = fvWinback.reduce((s, v) => s + v, 0);
const liftGain = fWinTot - fBaseTot;
const outCost = D.churnCount * 35;
const wbPct = Math.round((yrRev / annualPool) * 100);
const wbRoi = (yrRev / outCost).toFixed(1);

document.getElementById('wbStat').textContent = '+' + fmt(liftGain) + ' (6-Mo) / +' + fmt(yrRev) + '/yr';
document.getElementById('wbDesc').textContent = 'Reaching all ' + D.churnCount.toLocaleString() + ' lapsed $1,000+ buyers via VIP Sales Mgr calls, equity appraisals &amp; service passes at ' + wbPct + '% reactivation.';

const ds = D.donorStats;
const netSign = ds.netChange >= 0 ? '+' : '';
const netLabel = (ds.netChange >= 0 ? 'UP ' : 'DOWN ') + netSign + ds.netChange.toLocaleString() + ' Net Customers (' + netSign + ds.pctChange + '% vs 2025)';
const netColor = ds.netChange >= 0 ? '#10b981' : '#f43f5e';

new Array(
  new Array('Trailing 12-Mo Revenue', fmt(D.rev.slice(24).reduce((s, r) => s + Number(r.at(2)), 0)), 'Current Mo: ' + fmt(Number(D.rev.at(35).at(2))) + ' | 6-Mo: ' + fmt(D.rev.slice(30).reduce((s, r) => s + Number(r.at(2)), 0)), '#38bdf8', '#10b981'),
  new Array('Active DMS Customers (2026)', ds.active2026.toLocaleString() + ' (' + ds.totalUnique.toLocaleString() + ' Total)', netLabel, '#38bdf8', netColor),
  new Array('6-Mo Forecast (Baseline)', fmt(fBaseTot), 'H1 2027 Sales & Fixed-Ops Forecast', '#a78bfa', '#10b981'),
  new Array('6-Mo Optimized Forecast', fmt(fWinTot), '+' + fmt(liftGain) + ' Gain (Cost: ~' + fmt(outCost) + ')', '#10b981', '#10b981'),
  new Array('Actionable Alerts', D.alerts.length + ' Items', 'Aged Lot, Declined MPI & CIT', '#f59e0b', '#f59e0b')
).forEach(k => {
  const c = el('div', 'card');
  c.appendChild(el('h3', '', k.at(0)));
  const v = el('div', 'val', k.at(1)); v.style.color = k.at(3); v.style.fontSize = '22px';
  const sb = el('div', 'sub', k.at(2)); sb.style.color = k.at(4);
  c.append(v, sb);
  document.getElementById('kpiRow').appendChild(c);
});

const cv = document.getElementById('lineCanvas'), ctx = cv.getContext('2d'), W = cv.width, H = cv.height, P = 34;
const allV = D.rev.map(r => Number(r.at(2))).concat(fvWinback), mx = Math.max(...allV) * 1.06, totPts = D.rev.length + fvBase.length;
const lastIdx = D.rev.length - 1;
const gx = i => P + (i / (totPts - 1)) * (W - P * 2), gy = v => H - P - (v / mx) * (H - P * 2);
const fX0 = gx(lastIdx), fW = gx(totPts - 1) - fX0;
ctx.font = '600 10px Segoe UI';
new Array(0.25, 0.5, 0.75, 1).forEach(st => {
  const val = mx * st, gyVal = H - P - (val / mx) * (H - P * 2);
  ctx.strokeStyle = 'rgba(148,163,184,0.14)'; ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(P, gyVal); ctx.lineTo(W - P, gyVal); ctx.stroke();
  ctx.fillStyle = '#94a3b8'; ctx.fillText('$' + (val / 1e6).toFixed(1) + 'M', 4, gyVal + 3);
});
ctx.fillStyle = 'rgba(167,139,250,0.14)'; ctx.fillRect(fX0, 16, fW, H - P - 16);
ctx.strokeStyle = '#a78bfa'; ctx.setLineDash(new Array(4, 4)); ctx.beginPath(); ctx.moveTo(fX0, 16); ctx.lineTo(fX0, H - P); ctx.stroke(); ctx.setLineDash(new Array());
ctx.fillStyle = '#c4b5fd'; ctx.font = 'bold 11px Segoe UI'; ctx.fillText('FORECAST ZONE', fX0 + 10, 30);

ctx.beginPath(); ctx.moveTo(gx(0), H - P); D.rev.forEach((r, i) => ctx.lineTo(gx(i), gy(Number(r.at(2))))); ctx.lineTo(gx(lastIdx), H - P); ctx.closePath();
ctx.fillStyle = 'rgba(56,189,248,0.15)'; ctx.fill();

ctx.beginPath(); D.rev.forEach((r, i) => { const x = gx(i), y = gy(Number(r.at(2))); i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y); });
ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 2.8; ctx.stroke();

const lastAct = Number(D.rev.at(lastIdx).at(2));
ctx.setLineDash(new Array(6, 4));
ctx.beginPath(); ctx.moveTo(gx(lastIdx), gy(lastAct)); fvBase.forEach((v, i) => ctx.lineTo(gx(lastIdx + 1 + i), gy(v))); ctx.strokeStyle = '#a78bfa'; ctx.lineWidth = 2.8; ctx.stroke();
ctx.beginPath(); ctx.moveTo(gx(lastIdx), gy(lastAct)); fvWinback.forEach((v, i) => ctx.lineTo(gx(lastIdx + 1 + i), gy(v))); ctx.strokeStyle = '#10b981'; ctx.lineWidth = 2.8; ctx.stroke();
ctx.setLineDash(new Array());

D.rev.forEach((r, i) => { const q4 = r.at(0).endsWith('-11') || r.at(0).endsWith('-12'); ctx.beginPath(); ctx.arc(gx(i), gy(Number(r.at(2))), q4 ? 4 : 2.3, 0, Math.PI * 2); ctx.fillStyle = q4 ? '#f59e0b' : '#38bdf8'; ctx.fill(); });
fvBase.forEach((v, i) => { ctx.beginPath(); ctx.arc(gx(lastIdx + 1 + i), gy(v), 3.5, 0, Math.PI * 2); ctx.fillStyle = '#a78bfa'; ctx.fill(); });
fvWinback.forEach((v, i) => { ctx.beginPath(); ctx.arc(gx(lastIdx + 1 + i), gy(v), 4, 0, Math.PI * 2); ctx.fillStyle = '#10b981'; ctx.fill(); });

const ml = Math.max(...D.vol.map(r => Number(r.at(3))));
D.vol.forEach((r, i) => {
  const rw = el('div', 'brow'), lb = el('div', 'blbl');
  lb.append(el('span', '', r.at(0) + ' (' + Number(r.at(1)).toLocaleString() + ' buyers | ' + r.at(2) + ' ROs & deals)'), el('span', '', fmt(r.at(3))));
  const tk = el('div', 'btrk'), fl = el('div', 'bfil');
  fl.style.width = (Number(r.at(3)) / ml * 100).toFixed(1) + '%'; fl.style.background = i === 0 ? '#10b981' : '#64748b';
  tk.appendChild(fl); rw.append(lb, tk); document.getElementById('volBars').appendChild(rw);
});
const tp = el('div', 'ibox', 'Quick Win: Enrolling 15% of Sales-Only buyers into Pre-Paid Maintenance adds ~$880K in cumulative 3-yr Fixed-Ops & trade-in gross.');
tp.style.marginTop = '14px'; document.getElementById('volBars').appendChild(tp);

const churnTable = document.getElementById('churnTable');
D.churn.forEach((r, i) => {
  const tr = el('tr'), ac = i < 5 ? 'VIP Sales Mgr Equity Appraisal + Service Pass' : (i < 10 ? 'Service BDC 30K/60K Maintenance Voucher' : 'VIP Gala & loyal accounts Preview Invite');
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
  new Array('Outreach Cost (' + D.churnCount.toLocaleString() + ' customers @ $35)', outCost, '#f43f5e'),
  new Array('6-Mo Recovered Revenue (H1 2027)', liftGain, '#38bdf8'),
  new Array('12-Mo Recovered Revenue (18% Reactivation)', yrRev, '#10b981')
).forEach(it => {
  const rw = el('div', 'brow'), lb = el('div', 'blbl');
  const sp = el('span', '', fmt(it.at(1))); sp.style.color = it.at(2);
  lb.append(el('span', '', it.at(0)), sp);
  const tk = el('div', 'btrk'), fl = el('div', 'bfil');
  fl.style.width = Math.max(4, (it.at(1) / maxBar * 100)).toFixed(1) + '%'; fl.style.background = it.at(2);
  tk.appendChild(fl); rw.append(lb, tk); wbCard.appendChild(rw);
});
const wbSum = el('div', 'ibox', 'Net 12-Mo Gain: +' + fmt(yrRev - outCost) + ' (' + wbRoi + 'x ROI) -- ' + fmt(fullRev) + ' from 5% full-gift + ' + fmt(halfRev) + ' from 10% half-gift reactivations.');
wbSum.style.borderColor = '#10b981'; wbSum.style.marginTop = '12px';
wbCard.appendChild(wbSum);

const playbook = el('div', 'card');
playbook.style.margin = '0'; playbook.style.background = '#0f172a'; playbook.style.border = '1px solid #334155';
playbook.appendChild(el('h3', '', '90-Day Lapsed buyer Outreach Playbook (' + D.churnCount.toLocaleString() + ' Targets)'));
new Array(
  new Array('Tier 1 - Top 50 High-Equity Buyers ($5,500+ Gross)', 'Personal call from VIP Sales Manager + complimentary trade-in appraisal & detail.', '#10b981'),
  new Array('Tier 2 - Next 150 Service-Loyal Buyers ($3,500-$5,499)', 'Service Director outreach + $75 factory maintenance & alignment credit.', '#38bdf8'),
  new Array('Tier 3 - Remaining Lapsed Buyers ($2,800-$3,499)', 'Automated BDC text/email with seasonal tire & oil-change package.', '#a78bfa')
).forEach(st => {
  const b = el('div', 'ibox'); b.style.borderColor = st.at(2); b.style.marginBottom = '10px'; b.style.padding = '10px 12px'; b.style.background = '#1e293b';
  const t = el('h4', '', st.at(0)); t.style.fontSize = '13px';
  const p = el('p', '', st.at(1)); p.style.margin = '0'; p.style.color = '#cbd5e1'; p.style.fontSize = '12px';
  b.append(t, p); playbook.appendChild(b);
});

bottomRow.append(wbCard, playbook);
insightsSection.appendChild(bottomRow);

const progWrap = document.getElementById('progBars');
const mc = Math.max(...D.prog.map(r => Number(r.at(4))));
D.prog.forEach((r, i) => {
  const rw = el('div', 'brow'), lb = el('div', 'blbl');
  lb.append(el('span', '', r.at(0) + ' (' + fmt(r.at(2)) + ' rev)'), el('span', '', '$' + Number(r.at(4)).toFixed(2) + ' / person'));
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
funnelCard.appendChild(el('h3', '', 'BDC Lead-to-Showroom Funnel & Stalled Lead Recovery'));
const fCanvas = document.createElement('canvas');
fCanvas.width = 540; fCanvas.height = 170;
fCanvas.style.width = '100%'; fCanvas.style.height = 'auto';
fCanvas.style.background = '#0f172a'; fCanvas.style.borderRadius = '8px'; fCanvas.style.border = '1px solid #334155';
funnelCard.appendChild(fCanvas);
const fData = D.funnel;
const fCtx = fCanvas.getContext('2d'), funW = fCanvas.width, fH = fCanvas.height, fP = 46;
const fMax = Math.max(...fData.map(r => Number(r.at(1)))) * 1.15;
const fx = i => fP + (i / (fData.length - 1)) * (funW - fP * 2);
const fy = v => fH - fP - (v / fMax) * (fH - fP * 2);
fCtx.beginPath(); fCtx.moveTo(fx(0), fH - fP);
fData.forEach((r, i) => fCtx.lineTo(fx(i), fy(Number(r.at(1)))));
fCtx.lineTo(fx(fData.length - 1), fH - fP); fCtx.closePath();
fCtx.fillStyle = 'rgba(16, 185, 129, 0.14)'; fCtx.fill();
fCtx.beginPath();
fData.forEach((r, i) => { const x = fx(i), y = fy(Number(r.at(1))); i === 0 ? fCtx.moveTo(x, y) : fCtx.lineTo(x, y); });
fCtx.strokeStyle = '#10b981'; fCtx.lineWidth = 2.8; fCtx.stroke();
fCtx.font = 'bold 10px Segoe UI'; fCtx.textAlign = 'center';
fData.forEach((r, i) => {
const x = fx(i), y = fy(Number(r.at(1)));
fCtx.beginPath(); fCtx.arc(x, y, 4.5, 0, Math.PI * 2); fCtx.fillStyle = i >= 3 ? '#f59e0b' : '#10b981'; fCtx.fill();
fCtx.fillStyle = '#f8fafc'; fCtx.fillText(Number(r.at(1)).toLocaleString(), x, y - 9);
fCtx.fillStyle = '#94a3b8'; fCtx.font = '600 9.5px Segoe UI'; const pts = r.at(0).replace('(', '').replace(')', '').split(' '); fCtx.fillText(pts.at(0), x, fH - 15); if (pts.length > 1) { fCtx.fillText(pts.at(1), x, fH - 4); } fCtx.font = 'bold 10px Segoe UI';
});
const abCount = Number(fData.at(3).at(1)), recGifts = Number(fData.at(4).at(1)), recDollars = recGifts * 3700;
const fCallout = el('div', 'ibox', 'BDC Recovery Play: ' + abCount.toLocaleString() + ' showroom & internet leads sit unworked past 7 days. VIP Manager follow-up closes ~15% (' + recGifts + ' units = +' + fmt(recDollars) + ' incremental revenue at $0 ad spend).');
fCallout.style.borderColor = '#f59e0b'; fCallout.style.marginTop = '12px'; fCallout.style.fontSize = '12px';
funnelCard.appendChild(fCallout);
splitHolder.appendChild(funnelCard);
D.camp.forEach(r => {
  const tr = el('tr');
  const pct = r.length > 5 ? r.at(5) : r.at(4);
  tr.append(el('td', '', r.at(0)), el('td', '', Number(r.at(1)).toLocaleString()), el('td', '', fmt(r.at(2))), el('td', 'pos', fmt(r.at(3))), el('td', 'pos', Number(pct).toFixed(1) + '%'));
  document.querySelector('#campTable tbody').appendChild(tr);
});
function renderAlerts() {
const f = document.getElementById('alertFilter').value, q = document.getElementById('searchBox').value.toLowerCase(), tb = document.querySelector('#alertTable tbody');
tb.innerHTML = '';
D.alerts.filter(r => (f === 'ALL' || r.at(0) === f) && r.join(' ').toLowerCase().includes(q)).slice(0, 150).forEach(r => {
const tr = el('tr'), td = el('td'), cl = r.at(0) === 'Aged Lot >45d' ? 'p-grant' : (r.at(0) === 'Declined MPI' ? 'p-exp' : 'p-rec');
td.appendChild(el('span', 'pill ' + cl, r.at(0)));
tr.append(td, el('td', '', r.at(1)), el('td', '', r.at(2)), el('td', '', r.at(3)), el('td', '', fmt(r.at(4))), el('td', '', r.at(5)));
tb.appendChild(tr);
});
}
renderAlerts();




function switchTab(n) {
  [1, 2, 3, 4].forEach(i => {
    const v = document.getElementById('tab' + i + 'View');
    const b = document.getElementById('btnTab' + i);
    if (v) v.style.display = i === n ? 'block' : 'none';
    if (b) { b.style.background = i === n ? '#dc2626' : '#1e293b'; b.style.color = i === n ? '#fff' : '#cbd5e1'; }
  });
}

if (D.salesReps && D.fiManagers) {
  const totNew = D.salesReps.reduce((s, r) => s + r[2], 0);
  const totUsed = D.salesReps.reduce((s, r) => s + r[3], 0);
  const totUnits = totNew + totUsed;
  const totFront = D.salesReps.reduce((s, r) => s + r[4], 0);
  const totBack = D.fiManagers.reduce((s, r) => s + r[6], 0);
  const avgFrontPvr = Math.round(totFront / totUnits);
  const avgBackPvr = Math.round(totBack / D.fiManagers.reduce((s, r) => s + r[2], 0));

  [
    ['Retail Units Sold (12-Mo)', totUnits.toLocaleString() + ' Units', totNew + ' New | ' + totUsed + ' Pre-Owned', '#38bdf8', '#10b981'],
    ['Front-End Gross (12-Mo)', fmt(totFront), 'Avg Front PVR: ' + fmt(avgFrontPvr), '#38bdf8', '#10b981'],
    ['F&I Backend Gross (12-Mo)', fmt(totBack), 'Avg Backend PVR: ' + fmt(avgBackPvr), '#10b981', '#10b981'],
    ['Combined Variable Gross (12-Mo)', fmt(totFront + totBack), 'Combined PVR: ' + fmt(avgFrontPvr + avgBackPvr), '#f59e0b', '#10b981'],
    ['F&I Share of Gross (12-Mo)', Math.round(totBack / (totFront + totBack) * 100) + '% Backend', 'VSC, GAP & Protection Menus', '#a78bfa', '#10b981']
  ].forEach(k => {
    const c = el('div', 'card'); c.appendChild(el('h3', '', k[0]));
    const v = el('div', 'val', k[1]); v.style.color = k[3];
    const sb = el('div', 'sub', k[2]); sb.style.color = k[4];
    c.append(v, sb); document.getElementById('deskKpis').appendChild(c);
  });

  const totVsc = D.fiManagers.reduce((s, r) => s + r[3], 0);
  const totGap = D.fiManagers.reduce((s, r) => s + r[4], 0);
  const totAnc = D.fiManagers.reduce((s, r) => s + r[5], 0);
  [
    ['Vehicle Service Contracts (VSC / Warranties)', totVsc, '#10b981'],
    ['GAP Insurance & Loan Protection', totGap, '#38bdf8'],
    ['Paint, Interior, Tire & Wheel Protection', totAnc, '#f59e0b']
  ].forEach(m => {
    const rw = el('div', 'brow'), lb = el('div', 'blbl');
    lb.append(el('span', '', m[0]), el('span', '', fmt(m[1]) + ' (' + Math.round(m[1] / totBack * 100) + '%)'));
    const tk = el('div', 'btrk'), fl = el('div', 'bfil');
    fl.style.width = Math.round(m[1] / totVsc * 100) + '%'; fl.style.background = m[2];
    tk.appendChild(fl); rw.append(lb, tk); document.getElementById('fiMixBars').appendChild(rw);
  });
}

if (D.serviceAdvisors) {
  const totRos = D.serviceAdvisors.reduce((s, r) => s + r[2], 0);
  const totCp = D.serviceAdvisors.reduce((s, r) => s + r[3], 0);
  const totWar = D.serviceAdvisors.reduce((s, r) => s + r[4], 0);
  const avgHrs = (D.serviceAdvisors.reduce((s, r) => s + r[5], 0) / D.serviceAdvisors.length).toFixed(1);
  const avgElr = Math.round(D.serviceAdvisors.reduce((s, r) => s + r[6], 0) / D.serviceAdvisors.length);

  [
    ['Closed Repair Orders (12-Mo)', totRos.toLocaleString() + ' ROs', 'Customer-Pay + Warranty', '#38bdf8', '#10b981'],
    ['Service Labor Gross (12-Mo)', fmt(totCp + totWar), '67.5% Dept Gross Margin', '#10b981', '#10b981'],
    ['Customer-Pay Gross (12-Mo)', fmt(totCp), Math.round(totCp / (totCp + totWar) * 100) + '% of Total Labor', '#38bdf8', '#10b981'],
    ['Avg Hours Per RO (12-Mo)', avgHrs + ' Hrs / RO', 'Target Benchmark: 2.5 Hrs', '#f59e0b', '#f59e0b'],
    ['Effective Labor Rate (12-Mo)', '$' + avgElr + ' / Hr', 'Top Advisor: $168 / Hr', '#a78bfa', '#10b981']
  ].forEach(k => {
    const c = el('div', 'card'); c.appendChild(el('h3', '', k[0]));
    const v = el('div', 'val', k[1]); v.style.color = k[3];
    const sb = el('div', 'sub', k[2]); sb.style.color = k[4];
    c.append(v, sb); document.getElementById('svcKpis').appendChild(c);
  });

  const maxSvc = Math.max(...D.serviceAdvisors.map(r => r[3] + r[4]));
  D.serviceAdvisors.forEach((r, i) => {
    const tot = r[3] + r[4];
    const rw = el('div', 'brow'), lb = el('div', 'blbl');
    lb.append(el('span', '', r[0] + ' (' + r[5] + ' hrs/RO)'), el('span', '', fmt(tot)));
    const tk = el('div', 'btrk'), fl = el('div', 'bfil');
    fl.style.width = Math.round(tot / maxSvc * 100) + '%'; fl.style.background = i < 2 ? '#10b981' : '#38bdf8';
    tk.appendChild(fl); rw.append(lb, tk); document.getElementById('svcBars').appendChild(rw);
  });

  D.serviceAdvisors.forEach(r => {
    const tr = el('tr');
    tr.append(el('td', '', r[0]), el('td', '', r[1]), el('td', '', r[2].toLocaleString()), el('td', 'pos', fmt(r[3])), el('td', '', fmt(r[4])), el('td', '', r[5]), el('td', 'pos', '$' + r[6] + '/hr'));
    document.querySelector('#svcTable tbody').appendChild(tr);
  });
}

if (D.partsChannels) {
  const pSales = D.partsChannels.reduce((s, r) => s + r[3], 0);
  const pGross = D.partsChannels.reduce((s, r) => s + r[4], 0);
  const pAged = D.partsChannels.reduce((s, r) => s + r[6], 0);
  const pGmPct = (pGross / pSales * 100).toFixed(1);

  [
    ['Total Parts Sales (12-Mo)', fmt(pSales), 'RO, Wholesale & Counter', '#38bdf8', '#10b981'],
    ['Parts Gross Profit (12-Mo)', fmt(pGross), pGmPct + '% Blended Gross Margin', '#10b981', '#10b981'],
    ['Service RO Parts Gross (12-Mo)', fmt(D.partsChannels[0][4]), '39.0% Internal/CP Margin', '#38bdf8', '#10b981'],
    ['Wholesale Collision Gross (12-Mo)', fmt(D.partsChannels[1][4]), '29.0% Wholesale Margin', '#a78bfa', '#10b981'],
    ['Aged Parts (>90 Days)', fmt(pAged), 'Current On-Hand • OEM Return Eligible', '#f43f5e', '#f59e0b']
  ].forEach(k => {
    const c = el('div', 'card'); c.appendChild(el('h3', '', k[0]));
    const v = el('div', 'val', k[1]); v.style.color = k[3];
    const sb = el('div', 'sub', k[2]); sb.style.color = k[4];
    c.append(v, sb); document.getElementById('partsKpis').appendChild(c);
  });

  const maxP = Math.max(...D.partsChannels.map(r => r[4]));
  D.partsChannels.forEach((r, i) => {
    const rw = el('div', 'brow'), lb = el('div', 'blbl');
    lb.append(el('span', '', r[0] + ' (' + r[5] + '% GM)'), el('span', '', fmt(r[4])));
    const tk = el('div', 'btrk'), fl = el('div', 'bfil');
    fl.style.width = Math.round(r[4] / maxP * 100) + '%'; fl.style.background = i < 2 ? '#10b981' : '#f59e0b';
    tk.appendChild(fl); rw.append(lb, tk); document.getElementById('partsBars').appendChild(rw);
  });

  D.partsChannels.forEach(r => {
    const tr = el('tr');
    tr.append(el('td', '', r[0]), el('td', '', r[1]), el('td', '', r[2].toLocaleString()), el('td', '', fmt(r[3])), el('td', 'pos', fmt(r[4])), el('td', 'pos', r[5] + '%'), el('td', 'neg', fmt(r[6])));
    document.querySelector('#partsTable tbody').appendChild(tr);
  });
}

function renderPartsChart() {
  if (!D.partsSeries) return;
  const sel = document.getElementById('partsLocSelect');
  const key = sel ? sel.value : 'ALL';
  const rows = D.partsSeries[key] || D.partsSeries['ALL'];
  const lbl = sel ? sel.options[sel.selectedIndex].text : 'All 4 Rooftops';
  const tEl = document.getElementById('partsChartTitle');
  if (tEl) tEl.textContent = 'Parts Sales & Forecast — ' + lbl;

  const baseF = rows.slice(24, 30).map(r => Math.round(Number(r[1]) * 1.07));
  const optF = baseF.map((v, i) => Math.round(v * (1.05 + i * 0.012)));

  const cv = document.getElementById('partsCanvas');
  if (!cv) return;
  const ctx = cv.getContext('2d'), W = cv.width, H = cv.height, P = 38;
  ctx.clearRect(0, 0, W, H);

  const allVals = rows.map(r => Number(r[1])).concat(optF);
  const mx = Math.max(...allVals) * 1.08;
  const totPts = rows.length + baseF.length;
  const lastIdx = rows.length - 1;
  const gx = i => P + (i / (totPts - 1)) * (W - P * 2);
  const gy = v => H - P - (v / mx) * (H - P * 2);

  const fX0 = gx(lastIdx), fW = gx(totPts - 1) - fX0;
  ctx.fillStyle = 'rgba(167,139,250,0.14)'; ctx.fillRect(fX0, 14, fW, H - P - 14);
  ctx.strokeStyle = '#a78bfa'; ctx.setLineDash([4, 4]); ctx.beginPath(); ctx.moveTo(fX0, 14); ctx.lineTo(fX0, H - P); ctx.stroke(); ctx.setLineDash([]);
  ctx.fillStyle = '#c4b5fd'; ctx.font = 'bold 11px Segoe UI'; ctx.fillText('FORECAST ZONE', fX0 + 10, 28);

  ctx.beginPath(); ctx.moveTo(gx(0), H - P); rows.forEach((r, i) => ctx.lineTo(gx(i), gy(Number(r[1])))); ctx.lineTo(gx(lastIdx), H - P); ctx.closePath();
  ctx.fillStyle = 'rgba(56,189,248,0.13)'; ctx.fill();
  ctx.beginPath(); rows.forEach((r, i) => { const x = gx(i), y = gy(Number(r[1])); i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y); });
  ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 2.5; ctx.stroke();

  ctx.beginPath(); rows.forEach((r, i) => { const x = gx(i), y = gy(Number(r[2])); i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y); });
  ctx.strokeStyle = '#10b981'; ctx.lineWidth = 2.2; ctx.stroke();

  const lastSales = Number(rows[lastIdx][1]);
  ctx.setLineDash([6, 4]);
  ctx.beginPath(); ctx.moveTo(gx(lastIdx), gy(lastSales)); baseF.forEach((v, i) => ctx.lineTo(gx(lastIdx + 1 + i), gy(v))); ctx.strokeStyle = '#a78bfa'; ctx.lineWidth = 2.4; ctx.stroke();
  ctx.beginPath(); ctx.moveTo(gx(lastIdx), gy(lastSales)); optF.forEach((v, i) => ctx.lineTo(gx(lastIdx + 1 + i), gy(v))); ctx.strokeStyle = '#f59e0b'; ctx.lineWidth = 2.6; ctx.stroke();
  ctx.setLineDash([]);

  ctx.fillStyle = '#94a3b8'; ctx.font = '600 10px Segoe UI';
  ctx.fillText(fmt(mx), 6, 18);
  ctx.fillText(fmt(mx * 0.5), 6, (H - P) * 0.5 + 8);
}
renderPartsChart();


function renderEquityTab() {
  if (!D.equitySeries || !D.equityQueue) return;
  const sel = document.getElementById('eqLocSelect');
  const loc = sel ? sel.value : 'ALL';
  const rows = D.equitySeries[loc] || D.equitySeries['ALL'];
  const baseF = rows.slice(6, 12).map(r => Math.round(r.at(1) * 1.06));
  const optF = baseF.map((v, i) => Math.round(v * (1.16 + i * 0.025)));
  const cv = document.getElementById('eqCanvas');
  if (cv) {
    const ctx = cv.getContext('2d'), W = cv.width, H = cv.height, L = 54, R = 18, T = 26, B = 28;
    ctx.clearRect(0, 0, W, H);
    const allV = rows.map(r => r.at(1)).concat(optF);
    const mx = Math.ceil((Math.max(...allV) * 1.12) / 10000) * 10000;
    const mn = Math.floor((Math.min(...allV) * 0.78) / 10000) * 10000;
    const tot = rows.length + baseF.length, last = rows.length - 1;
    const gx = i => L + (i / (tot - 1)) * (W - L - R);
    const gy = v => H - B - ((v - mn) / (mx - mn)) * (H - T - B);

    // Horizontal gridlines + Y-axis dollar labels
    ctx.font = '600 10px Segoe UI';
    new Array(0, 0.25, 0.5, 0.75, 1).forEach(st => {
      const val = mn + (mx - mn) * st, y = gy(val);
      ctx.strokeStyle = 'rgba(148,163,184,0.14)'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(L, y); ctx.lineTo(W - R, y); ctx.stroke();
      ctx.fillStyle = '#94a3b8'; ctx.fillText('$' + Math.round(val / 1000) + 'K', 8, y + 3);
    });

    // Shaded 6-month forecast zone + divider
    const fx0 = gx(last);
    ctx.fillStyle = 'rgba(167,139,250,0.12)'; ctx.fillRect(fx0, T, W - R - fx0, H - T - B);
    ctx.strokeStyle = '#a78bfa'; ctx.setLineDash(new Array(4, 4)); ctx.beginPath(); ctx.moveTo(fx0, T); ctx.lineTo(fx0, H - B); ctx.stroke(); ctx.setLineDash(new Array());
    ctx.fillStyle = '#c4b5fd'; ctx.font = 'bold 10px Segoe UI'; ctx.fillText('6-MO FORECAST ZONE', fx0 + 10, T + 13);

    // Area fill + Actual Upgrade Gross line
    ctx.beginPath(); ctx.moveTo(gx(0), H - B); rows.forEach((r, i) => ctx.lineTo(gx(i), gy(r.at(1)))); ctx.lineTo(gx(last), H - B); ctx.closePath();
    ctx.fillStyle = 'rgba(16,185,129,0.16)'; ctx.fill();
    ctx.beginPath(); rows.forEach((r, i) => i === 0 ? ctx.moveTo(gx(i), gy(r.at(1))) : ctx.lineTo(gx(i), gy(r.at(1))));
    ctx.strokeStyle = '#10b981'; ctx.lineWidth = 2.8; ctx.stroke();

    // Baseline & VIP Handoff Forecast lines
    const lastV = rows.at(last).at(1);
    ctx.setLineDash(new Array(6, 4));
    ctx.beginPath(); ctx.moveTo(gx(last), gy(lastV)); baseF.forEach((v, i) => ctx.lineTo(gx(last + 1 + i), gy(v))); ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 2.2; ctx.stroke();
    ctx.beginPath(); ctx.moveTo(gx(last), gy(lastV)); optF.forEach((v, i) => ctx.lineTo(gx(last + 1 + i), gy(v))); ctx.strokeStyle = '#f59e0b'; ctx.lineWidth = 2.6; ctx.stroke();
    ctx.setLineDash(new Array());

    // Data point dots + X-axis month labels
    const fMos = new Array('Jan 27', 'Feb 27', 'Mar 27', 'Apr 27', 'May 27', 'Jun 27');
    rows.forEach((r, i) => {
      ctx.beginPath(); ctx.arc(gx(i), gy(r.at(1)), 3.2, 0, Math.PI * 2); ctx.fillStyle = '#10b981'; ctx.fill();
      if (i % 2 === 0 || i === last) { ctx.fillStyle = '#94a3b8'; ctx.fillText(r.at(0), gx(i) - 16, H - 10); }
    });
    optF.forEach((v, i) => {
      ctx.beginPath(); ctx.arc(gx(last + 1 + i), gy(v), 3.6, 0, Math.PI * 2); ctx.fillStyle = '#f59e0b'; ctx.fill();
      if (i % 2 === 1) { ctx.fillStyle = '#cbd5e1'; ctx.fillText(fMos.at(i), gx(last + 1 + i) - 16, H - 10); }
    });
  }
  const tb = document.querySelector('#eqTable tbody');
  if (tb) {
    tb.innerHTML = '';
    (loc === 'ALL' ? D.equityQueue : D.equityQueue.filter(r => r.at(1) === loc)).forEach(r => {
      const tr = el('tr');
      tr.append(el('td', '', r.at(0)), el('td', '', r.at(1)), el('td', '', r.at(2)), el('td', '', r.at(3)), el('td', '', r.at(4)), el('td', 'pos', '+$' + r.at(5).toLocaleString()), el('td', 'pos', r.at(6)), el('td', '', r.at(7)));
      tb.appendChild(tr);
    });
  }
}
renderEquityTab();
