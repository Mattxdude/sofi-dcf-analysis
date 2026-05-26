import yfinance as yf
import pandas as pd

tickers = ['SOFI', 'LC', 'UPST', 'NU', 'ALLY', 'HOOD']

rows = []
for t in tickers:
    stock = yf.Ticker(t)
    info  = stock.info

    name            = info.get('shortName', t)
    market_cap      = info.get('marketCap', None)
    enterprise_val  = info.get('enterpriseValue', None)
    pe_ratio        = info.get('trailingPE', None)
    fwd_pe          = info.get('forwardPE', None)
    ev_revenue      = info.get('enterpriseToRevenue', None)
    revenue_growth  = info.get('revenueGrowth', None)
    price           = stock.fast_info['last_price']

    rows.append({
        'Ticker':          t,
        'Company':         name,
        'Price':           f"${price:.2f}",
        'Market Cap ($B)': f"${market_cap/1e9:.1f}B" if market_cap else 'N/A',
        'EV ($B)':         f"${enterprise_val/1e9:.1f}B" if enterprise_val else 'N/A',
        'P/E (TTM)':       f"{pe_ratio:.1f}x" if pe_ratio else 'N/A',
        'Fwd P/E':         f"{fwd_pe:.1f}x" if fwd_pe else 'N/A',
        'EV/Revenue':      f"{ev_revenue:.1f}x" if ev_revenue else 'N/A',
        'Rev Growth':      f"{revenue_growth*100:.1f}%" if revenue_growth else 'N/A',
    })

df = pd.DataFrame(rows)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
print(df.to_string(index=False))

# ── Implied price from median Forward P/E (high-growth comps only) ──
sofi     = yf.Ticker('SOFI')
sofi_eps = sofi.info.get('forwardEps', None)

fwd_pes = []
for t in ['UPST', 'NU', 'HOOD']:   # growth-comparable comps only
    v = yf.Ticker(t).info.get('forwardPE', None)
    if v and v > 0:
        fwd_pes.append(v)

median_fwd_pe       = sorted(fwd_pes)[len(fwd_pes)//2]
implied_comps_price = median_fwd_pe * sofi_eps

print(f"\n=== COMPS VALUATION (growth-comparable: UPST, NU, HOOD) ===")
print(f"Median Fwd P/E of comps:  {median_fwd_pe:.1f}x")
print(f"SoFi Forward EPS:         ${sofi_eps:.2f}")
print(f"Implied Price (comps):    ${implied_comps_price:.2f}")
print(f"Current Price:            ${sofi.fast_info['last_price']:.2f}")
print(f"Upside/Downside:          {((implied_comps_price/sofi.fast_info['last_price'])-1)*100:.1f}%")