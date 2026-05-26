import yfinance as yf
import pandas as pd
import numpy as np

sofi = yf.Ticker("SOFI")

inc  = sofi.financials
bs   = sofi.balance_sheet
info = sofi.info

# ── 1. Base year: FY2025 actuals ───────────────────────────────────
net_income = inc.loc['Net Income'].iloc[0]
print(f"FY2025 Net Income (base): ${net_income/1e6:.1f}M")

# ── 2. Assumptions ─────────────────────────────────────────────────
growth_rates    = [0.45, 0.38, 0.30, 0.22, 0.16]  # FY2026–2030
terminal_growth = 0.035
wacc            = 0.09

# ── 3. Project FY2026–2030 ─────────────────────────────────────────
projected = []
base = net_income
for i, g in enumerate(growth_rates):
    base = base * (1 + g)
    projected.append(base)
    print(f"  FY{2026 + i} projected earnings: ${base/1e6:.1f}M")

# ── 4. Discount to present value ───────────────────────────────────
pv_earnings = [e / (1 + wacc)**(i+1) for i, e in enumerate(projected)]
sum_pv = sum(pv_earnings)
print(f"\nPV of Earnings: ${sum_pv/1e6:.1f}M")

# ── 5. Terminal Value ───────────────────────────────────────────────
terminal_value = projected[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
pv_terminal    = terminal_value / (1 + wacc)**5
print(f"PV of Terminal Value: ${pv_terminal/1e6:.1f}M")

# ── 6. Implied Price ────────────────────────────────────────────────
equity_value  = sum_pv + pv_terminal
shares        = info['sharesOutstanding']
implied_price = equity_value / shares
current_price = sofi.fast_info['last_price']

print(f"\n{'='*40}")
print(f"Equity Value:    ${equity_value/1e9:.2f}B")
print(f"Implied Price:   ${implied_price:.2f}")
print(f"Current Price:   ${current_price:.2f}")
print(f"Upside/Downside: {((implied_price/current_price)-1)*100:.1f}%")

# ── 7. Sensitivity Table ───────────────────────────────────────────
print("\n=== SENSITIVITY TABLE: Implied Price ===")
print("WACC →        8%      9%     10%     11%     12%")

tgr_list  = [0.02, 0.025, 0.03, 0.035, 0.04]
wacc_list = [0.08, 0.09,  0.10, 0.11,  0.12]

for tgr in tgr_list:
    row = f"TGR {tgr*100:.1f}%  "
    for w in wacc_list:
        pv_e  = sum([projected[i] / (1+w)**(i+1) for i in range(5)])
        tv    = projected[-1] * (1+tgr) / (w - tgr)
        pv_tv = tv / (1+w)**5
        price = (pv_e + pv_tv) / shares
        row  += f"  ${price:6.2f}"
    print(row)
    