p_html = "demo-enterprise-impact/dashboard.html"
h = open(p_html, encoding="utf-8").read()
h = h.replace(r"(\$ COST PER BENEFICIARY)", "($ COST PER BENEFICIARY)")
open(p_html, "w", encoding="utf-8").write(h)

p_js = "demo-enterprise-impact/app.js"
j = open(p_js, encoding="utf-8").read()

split_code = """
const progWrap = document.getElementById('progBars');
const progCard = progWrap.parentElement;
const parentGrid = progCard.parentElement;

const splitHolder = el('div', 'gridEq');
splitHolder.style.margin = '0';

parentGrid.insertBefore(splitHolder, progCard);
splitHolder.appendChild(progCard);

const funnelCard = el('div', 'card');
funnelCard.appendChild(el('h3', '', 'Digital Engagement Funnel & Checkout Recovery Opportunity'));

const fCanvas = document.createElement('canvas');
fCanvas.width = 480;
fCanvas.height = 155;
fCanvas.style.width = '100%';
fCanvas.style.height = 'auto';
fCanvas.style.background = '#0f172a';
fCanvas.style.borderRadius = '8px';
fCanvas.style.border = '1px solid #334155';
funnelCard.appendChild(fCanvas);

const fData = D.funnel || new Array(
  new Array('Email Opens', 6750),
  new Array('Email Clicks', 3300),
  new Array('Reports & Webinars', 3450),
  new Array('Abandoned Cart', 1500),
  new Array('15% Recovery Target', 225)
);

const fCtx = fCanvas.getContext('2d');
const fW = fCanvas.width, fH = fCanvas.height, fP = 28;
const fMax = Math.max(...fData.map(r => Number(r.at(1)))) * 1.15;
const fx = i => fP + (i / (fData.length - 1)) * (fW - fP * 2);
const fy = v => fH - fP - (v / fMax) * (fH - fP * 2);

fCtx.strokeStyle = '#1e293b';
for (let g = 1; g <= 2; g++) {
  const y = fP + (g / 3) * (fH - fP * 2);
  fCtx.beginPath(); fCtx.moveTo(fP, y); fCtx.lineTo(fW - fP, y); fCtx.stroke();
}

fCtx.beginPath();
fCtx.moveTo(fx(0), fH - fP);
fData.forEach((r, i) => fCtx.lineTo(fx(i), fy(Number(r.at(1)))));
fCtx.lineTo(fx(fData.length - 1), fH - fP);
fCtx.closePath();
fCtx.fillStyle = 'rgba(16, 185, 129, 0.14)';
fCtx.fill();

fCtx.beginPath();
fData.forEach((r, i) => {
  const x = fx(i), y = fy(Number(r.at(1)));
  i === 0 ? fCtx.moveTo(x, y) : fCtx.lineTo(x, y);
});
fCtx.strokeStyle = '#10b981';
fCtx.lineWidth = 2.5;
fCtx.stroke();

fCtx.font = 'bold 10px Segoe UI';
fCtx.textAlign = 'center';
fData.forEach((r, i) => {
  const x = fx(i), y = fy(Number(r.at(1)));
  const isAlert = i >= 3;
  fCtx.beginPath();
  fCtx.arc(x, y, 4.5, 0, Math.PI * 2);
  fCtx.fillStyle = isAlert ? '#f59e0b' : '#10b981';
  fCtx.fill();
  fCtx.fillStyle = '#f8fafc';
  fCtx.fillText(Number(r.at(1)).toLocaleString(), x, y - 9);
  fCtx.fillStyle = '#94a3b8';
  fCtx.fillText(r.at(0).split(' ').slice(0, 2).join(' '), x, fH - 8);
});

const abCount = Number(fData.at(3).at(1));
const recGifts = Number(fData.at(4).at(1));
const recDollars = recGifts * 165;
const fCallout = el('div', 'ibox', 'Checkout Recovery Play: ' + abCount.toLocaleString() + ' supporters abandoned the donation page. Triggering an automated 24-hr reminder email recovers ~15% (' + recGifts + ' gifts = +' + fmt(recDollars) + ' incremental revenue at $0 ad spend).');
fCallout.style.borderColor = '#f59e0b';
fCallout.style.marginTop = '12px';
fCallout.style.fontSize = '12px';
funnelCard.appendChild(fCallout);

splitHolder.appendChild(funnelCard);
"""

open(p_js, "w", encoding="utf-8").write(j + "\n" + split_code)
print("PROGRAM EFFICIENCY SPLIT & PAIRED WITH DIGITAL FUNNEL GRAPH!")
