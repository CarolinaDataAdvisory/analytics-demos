import re

lt, gt = chr(60), chr(62)
html_path = "demo-auto-dealership/dashboard.html"
h = open(html_path, encoding="utf-8").read()

# Strip previous 2-tab wrapper if present so we start cleanly from tab1View
h = re.sub(r'<div style="display:flex;gap:10px;margin-bottom:20px;">.*?<div id="tab1View">', '', h, flags=re.DOTALL)
h = re.sub(r'</div>\s*<div id="tab2View".*?(<script src="app\.js[^"]*"></script>)', r'\1', h, flags=re.DOTALL)

tab_bar = f"""{lt}div style="display:flex;gap:10px;margin-bottom:20px;flex-wrap:wrap;"{gt}
  {lt}button id="btnTab1" onclick="switchTab(1)" style="background:#dc2626;color:#fff;border:none;padding:10px 16px;border-radius:8px;font-weight:700;cursor:pointer;font-size:13px;"{gt}1. Executive Overview (All Depts){lt}/button{gt}
  {lt}button id="btnTab2" onclick="switchTab(2)" style="background:#1e293b;color:#cbd5e1;border:1px solid #334155;padding:10px 16px;border-radius:8px;font-weight:700;cursor:pointer;font-size:13px;"{gt}2. Variable Ops: Showroom &amp; F&amp;I{lt}/button{gt}
  {lt}button id="btnTab3" onclick="switchTab(3)" style="background:#1e293b;color:#cbd5e1;border:1px solid #334155;padding:10px 16px;border-radius:8px;font-weight:700;cursor:pointer;font-size:13px;"{gt}3. Fixed Ops: Service Drive{lt}/button{gt}
  {lt}button id="btnTab4" onclick="switchTab(4)" style="background:#1e293b;color:#cbd5e1;border:1px solid #334155;padding:10px 16px;border-radius:8px;font-weight:700;cursor:pointer;font-size:13px;"{gt}4. Parts &amp; Wholesale{lt}/button{gt}
{lt}/div{gt}
{lt}div id="tab1View"{gt}"""

h = h.replace(f'{lt}div class="kpis" id="kpiRow"{gt}{lt}/div{gt}', f'{tab_bar}\n{lt}div class="kpis" id="kpiRow"{gt}{lt}/div{gt}')

dept_tabs = f"""{lt}/div{gt}
{lt}div id="tab2View" style="display:none;"{gt}
  {lt}div class="kpis" id="deskKpis"{gt}{lt}/div{gt}
  {lt}div class="gridEq"{gt}
    {lt}div class="card"{gt}{lt}h3{gt}F&amp;I Backend Product Mix (VSC Warranties, GAP &amp; Paint/Tire){lt}/h3{gt}{lt}div id="fiMixBars"{gt}{lt}/div{gt}{lt}/div{gt}
    {lt}div class="card"{gt}{lt}h3{gt}Variable Ops &amp; Desk Profit Opportunity{lt}/h3{gt}
      {lt}div class="ibox" style="border-color:#10b981;margin-bottom:12px;"{gt}{lt}h4{gt}Backend PVR Spread: $1,780 Top vs. $1,320 Bottom{lt}/h4{gt}{lt}div class="bstat"{gt}+$184,000 Annual F&amp;I Lift Potential{lt}/div{gt}{lt}p style="margin:0;color:#cbd5e1;"{gt}Aligning Salisbury &amp; Lake Norman F&amp;I menus to Charlotte Honda's VSC + GAP penetration adds ~$310/copy.{lt}/p{gt}{lt}/div{gt}
      {lt}div class="ibox" style="border-color:#f59e0b;"{gt}{lt}h4{gt}Aged Pre-Owned Lot (&gt;45d) &amp; Unfunded CIT Focus{lt}/h4{gt}{lt}div class="bstat"{gt}25 Aged Units • 21 Open CITs{lt}/div{gt}{lt}p style="margin:0;color:#cbd5e1;"{gt}Re-pricing 45+ day units stops ~$55/day floorplan bleed while clearing lender stips frees $620K+ in working capital.{lt}/p{gt}{lt}/div{gt}
    {lt}/div{gt}
  {lt}/div{gt}
  {lt}div class="card" style="margin-bottom:24px;"{gt}{lt}h3{gt}Salesperson Unit Volume &amp; Front-End Gross Leaderboard{lt}/h3{gt}{lt}div class="twrap" style="max-height:280px;"{gt}{lt}table id="salesTable"{gt}{lt}thead{gt}{lt}tr{gt}{lt}th{gt}Salesperson{lt}/th{gt}{lt}th{gt}Rooftop{lt}/th{gt}{lt}th{gt}New{lt}/th{gt}{lt}th{gt}Used{lt}/th{gt}{lt}th{gt}Total{lt}/th{gt}{lt}th{gt}Front Gross{lt}/th{gt}{lt}th{gt}Front PVR{lt}/th{gt}{lt}/tr{gt}{lt}/thead{gt}{lt}tbody{gt}{lt}/tbody{gt}{lt}/table{gt}{lt}/div{gt}{lt}/div{gt}
  {lt}div class="card"{gt}{lt}h3{gt}Finance Manager (F&amp;I) Backend Gross &amp; Product Penetration{lt}/h3{gt}{lt}div class="twrap" style="max-height:260px;"{gt}{lt}table id="fiTable"{gt}{lt}thead{gt}{lt}tr{gt}{lt}th{gt}Finance Manager{lt}/th{gt}{lt}th{gt}Rooftop{lt}/th{gt}{lt}th{gt}Turns{lt}/th{gt}{lt}th{gt}VSC / Warranty{lt}/th{gt}{lt}th{gt}GAP{lt}/th{gt}{lt}th{gt}Paint / Tire{lt}/th{gt}{lt}th{gt}Backend Gross{lt}/th{gt}{lt}th{gt}Backend PVR{lt}/th{gt}{lt}/tr{gt}{lt}/thead{gt}{lt}tbody{gt}{lt}/tbody{gt}{lt}/table{gt}{lt}/div{gt}{lt}/div{gt}
{lt}/div{gt}

{lt}div id="tab3View" style="display:none;"{gt}
  {lt}div class="kpis" id="svcKpis"{gt}{lt}/div{gt}
  {lt}div class="gridEq"{gt}
    {lt}div class="card"{gt}{lt}h3{gt}Service Advisor Customer-Pay vs. Warranty Gross{lt}/h3{gt}{lt}div id="svcBars"{gt}{lt}/div{gt}{lt}/div{gt}
    {lt}div class="card"{gt}{lt}h3{gt}Fixed-Ops Service Drive Action Priorities{lt}/h3{gt}
      {lt}div class="ibox" style="border-color:#10b981;margin-bottom:12px;"{gt}{lt}h4{gt}Hours Per RO Lift (1.8 hrs -> 2.4 hrs){lt}/h4{gt}{lt}div class="bstat"{gt}+$310,000 Annual Labor Gross Opportunity{lt}/div{gt}{lt}p style="margin:0;color:#cbd5e1;"{gt}Coaching Express &amp; Salisbury advisors on Multi-Point Inspection (MPI) walkarounds adds 0.6 hrs/RO at 67.5% labor margin.{lt}/p{gt}{lt}/div{gt}
      {lt}div class="ibox" style="border-color:#f59e0b;"{gt}{lt}h4{gt}31 Declined MPI Brake &amp; 30K/60K Service Alerts{lt}/h4{gt}{lt}div class="bstat"{gt}Immediate Service BDC Follow-Up Queue{lt}/div{gt}{lt}p style="margin:0;color:#cbd5e1;"{gt}Outbound Service BDC text/call reminders within 14 days recover ~22% of declined safety &amp; factory maintenance work.{lt}/p{gt}{lt}/div{gt}
    {lt}/div{gt}
  {lt}/div{gt}
  {lt}div class="card"{gt}{lt}h3{gt}Service Advisor Leaderboard (ROs, Effective Labor Rate &amp; Gross){lt}/h3{gt}{lt}div class="twrap" style="max-height:280px;"{gt}{lt}table id="svcTable"{gt}{lt}thead{gt}{lt}tr{gt}{lt}th{gt}Service Advisor{lt}/th{gt}{lt}th{gt}Rooftop{lt}/th{gt}{lt}th{gt}Closed ROs{lt}/th{gt}{lt}th{gt}Customer-Pay Gross{lt}/th{gt}{lt}th{gt}Warranty Gross{lt}/th{gt}{lt}th{gt}Hours / RO{lt}/th{gt}{lt}th{gt}ELR ($/Hr){lt}/th{gt}{lt}/tr{gt}{lt}/thead{gt}{lt}tbody{gt}{lt}/tbody{gt}{lt}/table{gt}{lt}/div{gt}{lt}/div{gt}
{lt}/div{gt}

{lt}div id="tab4View" style="display:none;"{gt}
  {lt}div class="kpis" id="partsKpis"{gt}{lt}/div{gt}
  {lt}div class="gridEq"{gt}
    {lt}div class="card"{gt}{lt}h3{gt}Parts Gross Profit by Channel (RO, Wholesale &amp; Counter){lt}/h3{gt}{lt}div id="partsBars"{gt}{lt}/div{gt}{lt}/div{gt}
    {lt}div class="card"{gt}{lt}h3{gt}Parts Inventory &amp; Wholesale Margin Priorities{lt}/h3{gt}
      {lt}div class="ibox" style="border-color:#f43f5e;margin-bottom:12px;"{gt}{lt}h4{gt}$160,000 Aged / Obsolete Parts (&gt;90 Days No Movement){lt}/h4{gt}{lt}div class="bstat"{gt}Return-Reserve &amp; Wholesale Liquidation{lt}/div{gt}{lt}p style="margin:0;color:#cbd5e1;"{gt}Using OEM factory return allowances before the 12-month cutoff recovers 85–90 cents on the dollar vs. write-offs.{lt}/p{gt}{lt}/div{gt}
      {lt}div class="ibox" style="border-color:#10b981;"{gt}{lt}h4{gt}Wholesale Body-Shop Matrix Pricing Audit{lt}/h4{gt}{lt}div class="bstat"{gt}+2.4% Wholesale Margin Lift (+$87K/yr){lt}/h4{gt}{lt}p style="margin:0;color:#cbd5e1;"{gt}Tightening off-matrix discounts on non-captive collision accounts lifts wholesale margin from 29.0% to 31.4%.{lt}/p{gt}{lt}/div{gt}
    {lt}/div{gt}
  {lt}/div{gt}
  {lt}div class="card"{gt}{lt}h3{gt}Parts &amp; Wholesale Channel Breakdown{lt}/h3{gt}{lt}div class="twrap" style="max-height:280px;"{gt}{lt}table id="partsTable"{gt}{lt}thead{gt}{lt}tr{gt}{lt}th{gt}Parts Channel{lt}/th{gt}{lt}th{gt}Scope{lt}/th{gt}{lt}th{gt}Orders / ROs{lt}/th{gt}{lt}th{gt}Gross Sales{lt}/th{gt}{lt}th{gt}Gross Profit{lt}/th{gt}{lt}th{gt}Margin %{lt}/th{gt}{lt}th{gt}Aged &gt;90d ($){lt}/th{gt}{lt}/tr{gt}{lt}/thead{gt}{lt}tbody{gt}{lt}/tbody{gt}{lt}/table{gt}{lt}/div{gt}{lt}/div{gt}
{lt}/div{gt}
{lt}script src="app.js?v=9"{gt}{lt}/script{gt}"""

h = re.sub(r'<script src="app\.js[^"]*"></script>', dept_tabs, h)
open(html_path, "w", encoding="utf-8").write(h)

# 3. Update app.js with 4-tab switcher + Service & Parts renderers
js_path = "demo-auto-dealership/app.js"
js = open(js_path, encoding="utf-8").read()
js = re.sub(r"function switchTab\(n\).*", "", js, flags=re.DOTALL)

new_tabs_js = """function switchTab(n) {
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
"""
open(js_path, "w", encoding="utf-8").write(js + "\n" + new_tabs_js)
print("4-TAB DEPARTMENT DASHBOARD READY!")
