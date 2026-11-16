p = "demo-electrical-supply/app.js"
s = open(p, encoding="utf-8").read()
s = s.replace("fP = 28;", "fP = 48;")
s = s.replace("Checkout Recovery Play:", "Bid Recovery Play:")
s = s.replace("gifts =", "jobs =")
open(p, "w", encoding="utf-8").write(s)
print("FUNNEL POLISHED!")
