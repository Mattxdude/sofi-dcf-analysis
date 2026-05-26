# SoFi Technologies (SOFI) — DCF & Comparable Companies Valuation

A Python-based equity valuation model for SoFi Technologies, built as a finance/tech project for investment banking recruiting. Automates financial data collection, runs a full DCF analysis, performs a comparable companies analysis, and outputs a formatted Excel workbook and football field chart.

---

## Key Findings (May 2026)
- DCF base case implied price: **~$20.52** (+31% upside)
- DCF sensitivity range: **$11.31 – $28.18**
- Comps implied price (growth-adjusted peers): **~$8.56**
- Current price: **$15.62**

---

## Methodologies

**DCF:** FY2025 base year net income, projected FY2026–2030 at 45/38/30/22/16% growth, 9% WACC, 3.5% terminal growth rate. Net income used instead of FCF — standard practice for fintechs/banks where loan originations distort operating cash flow.

**Comps:** Full table across LC, UPST, NU, ALLY, HOOD. Median forward P/E applied from growth-comparable peers only (UPST, NU, HOOD) — ALLY and LC excluded due to incomparable growth profiles (12–19% vs SoFi's 42%).

---

## Files

| File | Description |
|------|-------------|
| `dcf.py` | DCF model with sensitivity table |
| `comps.py` | Comparable companies analysis |
| `output.py` | Excel export + football field chart |
| `SOFI_DCF_Model.xlsx` | Formatted 3-tab Excel workbook |
| `SOFI_Football_Field.png` | Football field valuation chart |

---

## How to Run

```bash
pip install yfinance pandas numpy openpyxl matplotlib
python dcf.py
python comps.py
python output.py
```

---

## Tech Stack
`yfinance` · `pandas` · `numpy` · `openpyxl` · `matplotlib`
