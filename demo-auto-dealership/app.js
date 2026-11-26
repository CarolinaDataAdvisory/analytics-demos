
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
const fvWinback = fvBase.map((v, i) => v + Math.round(monthlyLift * (0.6 + i * 0.16)));
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
  new Array('3-Year Dealership Revenue', fmt(tot), '~$68.4M/Yr 4-Rooftop Run-Rate', '#38bdf8', '#10b981'),
  new Array('Active DMS Customers (2026)', ds.active2026.toLocaleString() + ' (' + ds.totalUnique.toLocaleString() + ' Total)', netLabel, '#38bdf8', netColor),
  new Array('6-Mo Forecast (Baseline)', fmt(fBaseTot), 'H1 2027 Sales & Fixed-Ops Forecast', '#a78bfa', '#10b981'),
  new Array('6-Mo With Churn Outreach', fmt(fWinTot), '+' + fmt(liftGain) + ' Gain (Cost: ~' + fmt(outCost) + ')', '#10b981', '#10b981'),
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
tr.append(el('td', '', r.at(0)), el('td', '', r.at(1)), el('td', '', fmt(r.at(3))), el('td', '', fmt(r.at(4))), el('td', Number(r.at(5)) >= 0 ? 'pos' : 'neg', r.at(5) + '%'));
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
  new Array(1, 2, 3, 4).forEach(i => {
    document.getElementById('tab' + i + 'View').style.display = i === n ? 'block' : 'none';
    const b = document.getElementById('btnTab' + i);
    b.style.background = i === n ? '#dc2626' : '#1e293b';
    b.style.color = i === n ? '#fff' : '#cbd5e1';
  });
}

if (D.salesReps && D.fiManagers) {
  const totNew = D.salesReps.reduce((s, r) => s + r.at(2), 0);
  const totUsed = D.salesReps.reduce((s, r) => s + r.at(3), 0);
  const totUnits = totNew + totUsed;
  const totFront = D.salesReps.reduce((s, r) => s + r.at(4), 0);
  const totBack = D.fiManagers.reduce((s, r) => s + r.at(6), 0);
  const avgFrontPvr = Math.round(totFront / totUnits);
  const avgBackPvr = Math.round(totBack / D.fiManagers.reduce((s, r) => s + r.at(2), 0));

  new Array(
    new Array('Total Retail Units', totUnits.toLocaleString() + ' Units', totNew + ' New | ' + totUsed + ' Pre-Owned', '#38bdf8', '#10b981'),
    new Array('Total Front-End Gross', fmt(totFront), 'Avg Front PVR: ' + fmt(avgFrontPvr), '#38bdf8', '#10b981'),
    new Array('Total F&I Backend Gross', fmt(totBack), 'Avg Backend PVR: ' + fmt(avgBackPvr), '#10b981', '#10b981'),
    new Array('Combined Front + Back Gross', fmt(totFront + totBack), 'Combined PVR: ' + fmt(avgFrontPvr + avgBackPvr), '#f59e0b', '#10b981'),
    new Array('F&I Share of Variable Gross', Math.round(totBack / (totFront + totBack) * 100) + '% Backend', 'VSC, GAP & Protection Menus', '#a78bfa', '#10b981')
  ).forEach(k => {
    const c = el('div', 'card'); c.appendChild(el('h3', '', k.at(0)));
    const v = el('div', 'val', k.at(1)); v.style.color = k.at(3);
    const sb = el('div', 'sub', k.at(2)); sb.style.color = k.at(4);
    c.append(v, sb); document.getElementById('deskKpis').appendChild(c);
  });

  const totVsc = D.fiManagers.reduce((s, r) => s + r.at(3), 0);
  const totGap = D.fiManagers.reduce((s, r) => s + r.at(4), 0);
  const totAnc = D.fiManagers.reduce((s, r) => s + r.at(5), 0);
  new Array(
    new Array('Vehicle Service Contracts (VSC / Warranties)', totVsc, '#10b981'),
new Array('GAP Insurance & Loan Protection', totGap, '#38bdf8'),
new Array('Paint, Interior, Tire & Wheel Protection', totAnc, '#f59e0b')
).forEach(m => {
const rw = el('div', 'brow'), lb = el('div', 'blbl');
lb.append(el('span', '', m.at(0)), el('span', '', fmt(m.at(1)) + ' (' + Math.round(m.at(1) / totBack * 100) + '%)'));
const tk = el('div', 'btrk'), fl = el('div', 'bfil');
fl.style.width = Math.round(m.at(1) / totVsc * 100) + '%'; fl.style.background = m.at(2);
tk.appendChild(fl); rw.append(lb, tk); document.getElementById('fiMixBars').appendChild(rw);
});
D.salesReps.forEach(r => {
const tr = el('tr');
tr.append(el('td', '', r.at(0)), el('td', '', r.at(1)), el('td', '', r.at(2)), el('td', '', r.at(3)), el('td', '', r.at(2) + r.at(3)), el('td', 'pos', fmt(r.at(4))), el('td', 'pos', fmt(r.at(5))));
document.querySelector('#salesTable tbody').appendChild(tr);
});
D.fiManagers.forEach(r => {
const tr = el('tr');
tr.append(el('td', '', r.at(0)), el('td', '', r.at(1)), el('td', '', r.at(2)), el('td', '', fmt(r.at(3))), el('td', '', fmt(r.at(4))), el('td', '', fmt(r.at(5))), el('td', 'pos', fmt(r.at(6))), el('td', 'pos', fmt(r.at(7))));
document.querySelector('#fiTable tbody').appendChild(tr);
});
}
if (D.serviceAdvisors) {
const totRos = D.serviceAdvisors.reduce((s, r) => s + r.at(2), 0);
const totCp = D.serviceAdvisors.reduce((s, r) => s + r.at(3), 0);
const totWar = D.serviceAdvisors.reduce((s, r) => s + r.at(4), 0);
const avgHrs = (D.serviceAdvisors.reduce((s, r) => s + r.at(5), 0) / D.serviceAdvisors.length).toFixed(1);
const avgElr = Math.round(D.serviceAdvisors.reduce((s, r) => s + r.at(6), 0) / D.serviceAdvisors.length);
new Array(
new Array('Total Closed Repair Orders', totRos.toLocaleString() + ' ROs', 'Customer-Pay + Warranty', '#38bdf8', '#10b981'),
new Array('Total Service Labor Gross', fmt(totCp + totWar), '67.5% Dept Gross Margin', '#10b981', '#10b981'),
new Array('Customer-Pay Labor Gross', fmt(totCp), Math.round(totCp / (totCp + totWar) * 100) + '% of Total Labor', '#38bdf8', '#10b981'),
new Array('Avg Hours Per RO', avgHrs + ' Hrs / RO', 'Target Benchmark: 2.5 Hrs', '#f59e0b', '#f59e0b'),
new Array('Effective Labor Rate (ELR)', '$' + avgElr + ' / Hr', 'Top Advisor: $168 / Hr', '#a78bfa', '#10b981')
).forEach(k => {
const c = el('div', 'card'); c.appendChild(el('h3', '', k.at(0)));
const v = el('div', 'val', k.at(1)); v.style.color = k.at(3);
const sb = el('div', 'sub', k.at(2)); sb.style.color = k.at(4);
c.append(v, sb); document.getElementById('svcKpis').appendChild(c);
});
const maxSvc = Math.max(...D.serviceAdvisors.map(r => r.at(3) + r.at(4)));
D.serviceAdvisors.forEach((r, i) => {
const tot = r.at(3) + r.at(4);
const rw = el('div', 'brow'), lb = el('div', 'blbl');
lb.append(el('span', '', r.at(0) + ' (' + r.at(5) + ' hrs/RO)'), el('span', '', fmt(tot)));
const tk = el('div', 'btrk'), fl = el('div', 'bfil');
fl.style.width = Math.round(tot / maxSvc * 100) + '%'; fl.style.background = i < 2 ? '#10b981' : '#38bdf8';
tk.appendChild(fl); rw.append(lb, tk); document.getElementById('svcBars').appendChild(rw);
});
D.serviceAdvisors.forEach(r => {
const tr = el('tr');
tr.append(el('td', '', r.at(0)), el('td', '', r.at(1)), el('td', '', r.at(2).toLocaleString()), el('td', 'pos', fmt(r.at(3))), el('td', '', fmt(r.at(4))), el('td', '', r.at(5)), el('td', 'pos', '$' + r.at(6) + '/hr'));
document.querySelector('#svcTable tbody').appendChild(tr);
});
}
if (D.partsChannels) {
const pSales = D.partsChannels.reduce((s, r) => s + r.at(3), 0);
const pGross = D.partsChannels.reduce((s, r) => s + r.at(4), 0);
const pAged = D.partsChannels.reduce((s, r) => s + r.at(6), 0);
const pGmPct = (pGross / pSales * 100).toFixed(1);
new Array(
new Array('Total Parts Sales', fmt(pSales), 'RO, Wholesale & Counter', '#38bdf8', '#10b981'),
new Array('Total Parts Gross Profit', fmt(pGross), pGmPct + '% Blended Gross Margin', '#10b981', '#10b981'),
new Array('Service RO Parts Gross', fmt(D.partsChannels.at(0).at(4)), '39.0% Internal/CP Margin', '#38bdf8', '#10b981'),
new Array('Wholesale Collision Gross', fmt(D.partsChannels.at(1).at(4)), '29.0% Wholesale Margin', '#a78bfa', '#10b981'),
new Array('Aged Parts (>90 Days)', fmt(pAged), 'Eligible for OEM Return Reserve', '#f43f5e', '#f59e0b')
).forEach(k => {
const c = el('div', 'card'); c.appendChild(el('h3', '', k.at(0)));
const v = el('div', 'val', k.at(1)); v.style.color = k.at(3);
const sb = el('div', 'sub', k.at(2)); sb.style.color = k.at(4);
c.append(v, sb); document.getElementById('partsKpis').appendChild(c);
});
const maxP = Math.max(...D.partsChannels.map(r => r.at(4)));
D.partsChannels.forEach((r, i) => {
const rw = el('div', 'brow'), lb = el('div', 'blbl');
lb.append(el('span', '', r.at(0) + ' (' + r.at(5) + '% GM)'), el('span', '', fmt(r.at(4))));
const tk = el('div', 'btrk'), fl = el('div', 'bfil');
fl.style.width = Math.round(r.at(4) / maxP * 100) + '%'; fl.style.background = i < 2 ? '#10b981' : '#f59e0b';
tk.appendChild(fl); rw.append(lb, tk); document.getElementById('partsBars').appendChild(rw);
});
D.partsChannels.forEach(r => {
const tr = el('tr');
tr.append(el('td', '', r.at(0)), el('td', '', r.at(1)), el('td', '', r.at(2).toLocaleString()), el('td', '', fmt(r.at(3))), el('td', 'pos', fmt(r.at(4))), el('td', 'pos', r.at(5) + '%'), el('td', 'neg', fmt(r.at(6))));
document.querySelector('#partsTable tbody').appendChild(tr);
});
}
