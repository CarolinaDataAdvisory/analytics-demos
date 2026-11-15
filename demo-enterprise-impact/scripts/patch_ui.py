p = "demo-enterprise-impact/dashboard.html"
s = open(p, encoding="utf-8").read()
s = s.replace(r"3.0x Higher LTV (\,443 vs \)", "3.0x Higher LTV ($1,443 vs $482)")
s = s.replace("8%–15% High-Touch Reactivation", "<span id='wbStat'>Calculating Win-Back ROI...</span>")
s = s.replace(r"While mass lapsed mailings convert at 2%–5%, personal calls & VIP invites to \,000+ donors reactivate ~5% at full gift + ~10% at half gift (10% net run-rate lift).", "<span id='wbDesc'>Calculating outreach cost & return...</span>")
open(p, "w", encoding="utf-8").write(s)

p2 = "demo-enterprise-impact/app.js"
s2 = open(p2, encoding="utf-8").read()
extra = """
const outCost = D.churnCount * 15, wbRoi = (recoveredAnnual / outCost).toFixed(1);
document.getElementById('wbStat').textContent = '+' + fmt(liftGain) + ' (6-Mo) / +' + fmt(recoveredAnnual) + '/yr';
document.getElementById('wbDesc').textContent = 'Reaching all ' + D.churnCount.toLocaleString() + ' lapsed $1,000+ donors via executive calls, handwritten board notes & VIP tours costs ~' + fmt(outCost) + ' ($15/donor) and returns ' + wbRoi + 'x ROI at 5% full + 10% half-gift reactivation.';
"""
open(p2, "w", encoding="utf-8").write(s2 + extra)
print("BOTH FILES UPDATED CLEANLY!")
