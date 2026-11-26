import re

lt, gt = chr(60), chr(62)

# 1. Update dashboard.html with tab bar + Tab 2 container
html_path = "demo-auto-dealership/dashboard.html"
h = open(html_path, encoding="utf-8").read()

tab_bar = f"""{lt}div style="display:flex;gap:10px;margin-bottom:20px;"{gt}
  {lt}button id="btnTab1" onclick="switchTab(1)" style="background:#dc2626;color:#fff;border:none;padding:10px 18px;border-radius:8px;font-weight:700;cursor:pointer;font-size:13.5px;"{gt}1. Executive &amp; Fixed-Ops Overview{lt}/button{gt}
  {lt}button id="btnTab2" onclick="switchTab(2)" style="background:#1e293b;color:#cbd5e1;border:1px solid #334155;padding:10px 18px;border-radius:8px;font-weight:700;cursor:pointer;font-size:13.5px;"{gt}2. Showroom Sales &amp; F&amp;I Desk (Front / Back PVR){lt}/button{gt}
{lt}/div{gt}
{lt}div id="tab1View"{gt}"""

if "btnTab1" not in h:
    h = h.replace(f'{lt}div class="kpis" id="kpiRow"{gt}{lt}/div{gt}', f'{tab_bar}\n{lt}div class="kpis" id="kpiRow"{gt}{lt}/div{gt}')
    tab2_html = f"""{lt}/div{gt}
{lt}div id="tab2View" style="display:none;"{gt}
  {lt}div class="kpis" id="deskKpis"{gt}{lt}/div{gt}
  {lt}div class="gridEq"{gt}
    {lt}div class="card"{gt}
      {lt}h3{gt}F&amp;I Backend Product Mix (VSC Warranties, GAP &amp; Paint/Tire Protection){lt}/h3{gt}
      {lt}div id="fiMixBars"{gt}{lt}/div{gt}
    {lt}/div{gt}
    {lt}div class="card"{gt}
      {lt}h3{gt}F&amp;I Coaching &amp; Desk Profit Opportunity{lt}/h3{gt}
      {lt}div class="ibox" style="border-color:#10b981;margin-bottom:12px;"{gt}
        {lt}h4{gt}Backend PVR Spread: $1,780 Top vs. $1,320 Bottom{lt}/h4{gt}
        {lt}div class="bstat"{gt}+$184,000 Annual F&amp;I Lift Potential{lt}/div{gt}
        {lt}p style="margin:0;color:#cbd5e1;"{gt}Bringing Salisbury &amp; Lake Norman F&amp;I menus up to Charlotte Honda's VSC + GAP penetration adds ~$310/copy across 600 retail turns.{lt}/p{gt}
      {lt}/div{gt}
      {lt}div class="ibox" style="border-color:#f59e0b;"{gt}
        {lt}h4{gt}Front-End Gross Retention on Pre-Owned Units{lt}/h4{gt}
        {lt}div class="bstat"{gt}+$425/Unit Front Gross Advantage{lt}/div{gt}
        {lt}p style="margin:0;color:#cbd5e1;"{gt}Reps who present trade-in equity + Pre-Paid Maintenance early hold $1,720–$1,874 front PVR vs. $1,110–$1,380 for discount-first floor reps.{lt}/p{gt}
      {lt}/div{gt}
    {lt}/div{gt}
  {lt}/div{gt}
  {lt}div class="card" style="margin-bottom:24px;"{gt}
    {lt}h3{gt}Salesperson Unit Volume &amp; Front-End Gross Leaderboard (New vs. Pre-Owned){lt}/h3{gt}
    {lt}div class="twrap" style="max-height:320px;"{gt}
      {lt}table id="salesTable"{gt}
        {lt}thead{gt}{lt}tr{gt}{lt}th{gt}Salesperson{lt}/th{gt}{lt}th{gt}Rooftop{lt}/th{gt}{lt}th{gt}New Units{lt}/th{gt}{lt}th{gt}Used Units{lt}/th{gt}{lt}th{gt}Total Units{lt}/th{gt}{lt}th{gt}Front-End Gross ($){lt}/th{gt}{lt}th{gt}Front PVR ($){lt}/th{gt}{lt}/tr{gt}{lt}/thead{gt}
        {lt}tbody{gt}{lt}/tbody{gt}
      {lt}/table{gt}
    {lt}/div{gt}
  {lt}/div{gt}
  {lt}div class="card"{gt}
    {lt}h3{gt}Finance Manager (F&amp;I) Backend Gross &amp; Product Penetration Scoreboard{lt}/h3{gt}
    {lt}div class="twrap" style="max-height:300px;"{gt}
      {lt}table id="fiTable"{gt}
        {lt}thead{gt}{lt}tr{gt}{lt}th{gt}Finance Manager{lt}/th{gt}{lt}th{gt}Rooftop{lt}/th{gt}{lt}th{gt}Deals Turned{lt}/th{gt}{lt}th{gt}VSC / Warranties{lt}/th{gt}{lt}th{gt}GAP Insurance{lt}/th{gt}{lt}th{gt}Paint / Tire / Ancil.{lt}/th{gt}{lt}th{gt}Total Backend Gross{lt}/th{gt}{lt}th{gt}Backend PVR{lt}/th{gt}{lt}/tr{gt}{lt}/thead{gt}
        {lt}tbody{gt}{lt}/tbody{gt}
      {lt}/table{gt}
    {lt}/div{gt}
  {lt}/div{gt}
{lt}/div{gt}
{lt}script src="app.js?v=8"{gt}{lt}/script{gt}"""
    h = re.sub(r'<script src="app\.js[^"]*"></script>', tab2_html, h)
    open(html_path, "w", encoding="utf-8").write(h)

# 2. Append Tab 2 rendering + switchTab() logic to app.js
js_path = "demo-auto-dealership/app.js"
js = open(js_path, encoding="utf-8").read()
if "switchTab" not in js:
    desk_js = """
function switchTab(n) {
  document.getElementById('tab1View').style.display = n === 1 ? 'block' : 'none';
  document.getElementById('tab2View').style.display = n === 2 ? 'block' : 'none';
  document.getElementById('btnTab1').style.background = n === 1 ? '#dc2626' : '#1e293b';
  document.getElementById('btnTab1').style.color = n === 1 ? '#fff' : '#cbd5e1';
  document.getElementById('btnTab2').style.background = n === 2 ? '#dc2626' : '#1e293b';
  document.getElementById('btnTab2').style.color = n === 2 ? '#fff' : '#cbd5e1';
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
    const c = el('div', 'card');
    c.appendChild(el('h3', '', k.at(0)));
    const v = el('div', 'val', k.at(1)); v.style.color = k.at(3);
    const sb = el('div', 'sub', k.at(2)); sb.style.color = k.at(4);
    c.append(v, sb);
    document.getElementById('deskKpis').appendChild(c);
  });

  const totVsc = D.fiManagers.reduce((s, r) => s + r.at(3), 0);
  const totGap = D.fiManagers.reduce((s, r) => s + r.at(4), 0);
  const totAnc = D.fiManagers.reduce((s, r) => s + r.at(5), 0);
  new Array(
    new Array('Vehicle Service Contracts (VSC / Extended Warranties)', totVsc, '#10b981'),
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
    const uTot = r.at(2) + r.at(3);
    tr.append(el('td', '', r.at(0)), el('td', '', r.at(1)), el('td', '', r.at(2)), el('td', '', r.at(3)), el('td', '', uTot), el('td', 'pos', fmt(r.at(4))), el('td', 'pos', fmt(r.at(5))));
    document.querySelector('#salesTable tbody').appendChild(tr);
  });

  D.fiManagers.forEach(r => {
    const tr = el('tr');
    tr.append(el('td', '', r.at(0)), el('td', '', r.at(1)), el('td', '', r.at(2)), el('td', '', fmt(r.at(3))), el('td', '', fmt(r.at(4))), el('td', '', fmt(r.at(5))), el('td', 'pos', fmt(r.at(6))), el('td', 'pos', fmt(r.at(7))));
    document.querySelector('#fiTable tbody').appendChild(tr);
  });
}
"""
    open(js_path, "w", encoding="utf-8").write(js + "\n" + desk_js)
print("ADDED SHOWROOM & F&I TAB TO CAROLINAS AUTO GROUP!")
