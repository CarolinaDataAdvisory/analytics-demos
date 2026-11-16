elec_card = """
<div class="card" style="margin-top:24px;border-color:#10b981;">
  <h3>Executive Summary: Top 3 Action Items, Execution Plan &amp; Expected ROI</h3>
  <div class="grid3" style="margin-bottom:0;">
    <div class="ibox" style="border-color:#f59e0b;">
      <h4>1. Recover Stalled Commercial Bids (460 Quotes)</h4>
      <p style="margin:0 0 8px;color:#cbd5e1;"><strong>What to Do:</strong> Have Inside Sales &amp; Estimators send a 48-hour price-lock follow-up on all 460 commercial quotes open past 21 days.</p>
      <p style="margin:0 0 8px;color:#cbd5e1;"><strong>Why:</strong> Contractors often delay submittals over minor spec questions; proactive follow-up beats competing supply houses before re-bidding.</p>
      <div class="bstat" style="font-size:15px;color:#10b981;">Expected Result: +$1.69M Revenue (~15% / 69 Jobs Won)</div>
    </div>
    <div class="ibox" style="border-color:#10b981;">
      <h4>2. Execute 90-Day Lapsed Contractor Win-Back</h4>
      <p style="margin:0 0 8px;color:#cbd5e1;"><strong>What to Do:</strong> Assign Branch Managers &amp; Outside Reps to conduct job-site visits for Top 15 lapsed accounts ($350K+) and offer a 2% lighting/PLC rebate to mid-tier accounts.</p>
      <p style="margin:0 0 8px;color:#cbd5e1;"><strong>Why:</strong> Retaining an established $50K+ contractor costs ~90% less than acquiring a new commercial account from scratch.</p>
      <div class="bstat" style="font-size:15px;color:#10b981;">Expected Result: +$650K–$950K Recovered Annual Spend</div>
    </div>
    <div class="ibox" style="border-color:#f43f5e;">
      <h4>3. Clear Backorders, Change Orders &amp; Overdue AR</h4>
      <p style="margin:0 0 8px;color:#cbd5e1;"><strong>What to Do:</strong> Review the 78 prioritized Operational Alerts weekly—billing unbilled spec changes before closeout and offering approved switchgear substitutes.</p>
      <p style="margin:0 0 8px;color:#cbd5e1;"><strong>Why:</strong> Unbilled change orders and Net-30 overages silently erode 1.5+ points of net EBITDA on otherwise profitable commercial jobs.</p>
      <div class="bstat" style="font-size:15px;color:#10b981;">Expected Result: +$620K+ Protected Margin &amp; Faster Cash</div>
    </div>
  </div>
</div>
"""

nonprofit_card = """
<div class="card" style="margin-top:24px;border-color:#10b981;">
  <h3>Executive Summary: Top 3 Action Items, Execution Plan &amp; Expected ROI</h3>
  <div class="grid3" style="margin-bottom:0;">
    <div class="ibox" style="border-color:#f43f5e;">
      <h4>1. Recover 959 Failed Recurring Monthly Pledges</h4>
      <p style="margin:0 0 8px;color:#cbd5e1;"><strong>What to Do:</strong> Launch an automated 3-step SMS and email card-updater sequence for all 959 failed recurring payments in the Action Queue.</p>
      <p style="margin:0 0 8px;color:#cbd5e1;"><strong>Why:</strong> Expired cards cause 20%–30% of annual sustainer churn; donors rarely cancel intentionally when given a 1-click mobile update link.</p>
      <div class="bstat" style="font-size:15px;color:#10b981;">Expected Result: +$68,000+ Recovered Annual Pledges</div>
    </div>
    <div class="ibox" style="border-color:#f59e0b;">
      <h4>2. Launch 90-Day High-Dollar Lapsed Donor Win-Back</h4>
      <p style="margin:0 0 8px;color:#cbd5e1;"><strong>What to Do:</strong> Have the Executive Director call the Top 50 lapsed $3,000+ donors and send handwritten Board impact notes to the next 150 mid-level supporters.</p>
      <p style="margin:0 0 8px;color:#cbd5e1;"><strong>Why:</strong> Re-engaging proven $1,000+ supporters costs ~$15/donor and delivers 4.5x net ROI compared to cold donor acquisition.</p>
      <div class="bstat" style="font-size:15px;color:#10b981;">Expected Result: +$33,378 Gross / +$25,878 Net (4.5x ROI)</div>
    </div>
    <div class="ibox" style="border-color:#10b981;">
      <h4>3. Convert Top Donors Into Volunteers + Checkout Follow-Up</h4>
      <p style="margin:0 0 8px;color:#cbd5e1;"><strong>What to Do:</strong> Invite 500 Donor-Only supporters to VIP hands-on impact days and trigger a 24-hour reminder email for the 1,500 abandoned checkouts.</p>
      <p style="margin:0 0 8px;color:#cbd5e1;"><strong>Why:</strong> Donor+Volunteers give 3.0x more ($1,443 vs. $482 LTV), and 15% of abandoned checkouts convert with a single timely reminder.</p>
      <div class="bstat" style="font-size:15px;color:#10b981;">Expected Result: +$92,000+ Combined Annual Revenue Lift</div>
    </div>
  </div>
</div>
"""

for path, block in (("demo-electrical-supply/dashboard.html", elec_card), ("demo-enterprise-impact/dashboard.html", nonprofit_card)):
    h = open(path, encoding="utf-8").read()
    if "Executive Summary: Top 3 Action Items" not in h:
        h = h.replace('<script src="app.js"></script>', block + '\n<script src="app.js"></script>')
        open(path, "w", encoding="utf-8").write(h)
        print("UPDATED:", path)
