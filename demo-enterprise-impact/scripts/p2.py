p2 = """
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

const fData = D.funnel || new Array(new Array('Email Opens', 6750), new Array('Email Clicks', 3300), new Array('Reports & Webinars', 3450), new Array('Abandoned Checkout', 1500), new Array('15% Recovery Target', 225));
const fCtx = fCanvas.getContext('2d'), fW = fCanvas.width, fH = fCanvas.height, fP = 28;
const fMax = Math.max(...fData.map(r => Number(r.at(1)))) * 1.15;
const fx = i => fP + (i / (fData.length - 1)) * (fW - fP * 2);
const fy = v => fH - fP - (v / fMax) * (fH - fP * 2);

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

D.camp.forEach(r => {
  const tr = el('tr');
  tr.append(el('td', '', r.at(0)), el('td', '', r.at(1)), el('td', '', fmt(r.at(3))), el('td', '', fmt(r.at(4))), el('td', Number(r.at(5)) >= 0 ? 'pos' : 'neg', r.at(5) + '%'));
  document.querySelector('#campTable tbody').appendChild(tr);
});

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
open("demo-enterprise-impact/app.js", "a", encoding="utf-8").write("\n" + p2)
print("PART 2 APPENDED — FULL DASHBOARD READY!")
