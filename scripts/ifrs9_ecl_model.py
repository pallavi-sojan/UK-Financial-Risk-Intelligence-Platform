# ============================================================
# CALEDONIA BANK PLC
# IFRS 9 ECL MODEL — PYTHON IMPLEMENTATION
# Author   : Pallavi Sojan
# Basis    : IFRS 9 IASB | Basel III | BoE ACS
# Database : BoE_Finance_Platform.db
# Date     : 2025
# ============================================================

import pandas as pds
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

print("=" * 60)
print("  CALEDONIA BANK PLC — IFRS 9 ECL MODEL")
print("  Author: Pallavi Sojan | MSc Finance & Risk Management")
print("=" * 60)

# ── SECTOR DATA ──────────────────────────────────────────────
# Source: Credit_Risk_Scorecard.xlsx RISK_METRICS sheet
# PD Proxy = Sector write-offs / Total sector lending (BoE data)
# LGD: 45% secured (Basel III) | 65% unsecured (Basel III)
# EAD: Total lending exposure per sector (£millions)

sectors = {
    'Mortgage Lending':       {'PD': 0.003, 'LGD': 0.45, 'EAD': 86957},
    'Consumer Credit':        {'PD': 0.018, 'LGD': 0.65, 'EAD': 21739},
    'Corporate Lending':      {'PD': 0.021, 'LGD': 0.55, 'EAD': 36232},
    'Commercial Real Estate': {'PD': 0.032, 'LGD': 0.60, 'EAD': 12000},
    'Small Business':         {'PD': 0.028, 'LGD': 0.58, 'EAD':  6500},
}

print(f"\nSector data loaded: {len(sectors)} sectors")
print(f"Total EAD: £{sum(s['EAD'] for s in sectors.values()):,.0f}m")

# ── IFRS 9 STAGING LOGIC ─────────────────────────────────────
# Stage 1: PD < 1%  → 12-month ECL (no significant deterioration)
# Stage 2: PD 1-5%  → Lifetime ECL (significant deterioration)
# Stage 3: PD > 5%  → Lifetime ECL (credit-impaired)
# Reference: IFRS 9 paragraph 5.5.3

def get_stage(prob_default):
    if prob_default < 0.01:
        return 'Stage 1'
    elif prob_default < 0.05:
        return 'Stage 2'
    else:
        return 'Stage 3'

def calculate_ecl(prob_default, lgd, ead, stage):
    if stage == 'Stage 1':
        # 12-month ECL — single year calculation
        return prob_default * lgd * ead
    else:
        # Lifetime ECL — simplified 5-year horizon
        # Apply discount factor of 0.95 per year
        lifetime_ecl = 0
        for year in range(1, 6):
            annual_ecl = prob_default * lgd * ead * (0.95 ** year)
            lifetime_ecl += annual_ecl
        return lifetime_ecl

# ── BASE CASE ECL ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  BASE CASE ECL CALCULATION")
print("=" * 60)
print(f"{'Sector':<25} {'Stage':<10} {'PD':>6} {'LGD':>6} {'EAD':>10} {'ECL':>10}")
print("-" * 60)

base_results = []
total_base_ecl = 0

for sector_name, data in sectors.items():
    prob_default = data['PD']
    lgd          = data['LGD']
    ead          = data['EAD']
    stage        = get_stage(prob_default)
    ecl          = calculate_ecl(prob_default, lgd, ead, stage)
    total_base_ecl += ecl

    base_results.append({
        'Sector':    sector_name,
        'PD %':      f"{prob_default*100:.1f}%",
        'LGD %':     f"{lgd*100:.0f}%",
        'EAD (£m)':  int(ead),
        'Stage':     stage,
        'ECL (£m)':  round(ecl),
        'ECL Basis': '12-month ECL' if stage == 'Stage 1' else 'Lifetime ECL'
    })

    print(f"{sector_name:<25} {stage:<10} {prob_default*100:>5.1f}% {lgd*100:>5.0f}% {ead:>10,.0f} {ecl:>10,.0f}")

print("-" * 60)
print(f"{'TOTAL PORTFOLIO':<25} {'':10} {'':>6} {'':>6} {sum(s['EAD'] for s in sectors.values()):>10,.0f} {total_base_ecl:>10,.0f}")
print(f"\nTotal Portfolio ECL: £{total_base_ecl:,.0f}m")
print(f"ECL as % of Total EAD: {total_base_ecl/sum(s['EAD'] for s in sectors.values())*100:.2f}%")

# ── STRESS TEST SCENARIOS ─────────────────────────────────────
# Calibrated to BoE Annual Cyclical Scenario (ACS)
# Mild +100bps | Moderate +200bps | Severe +300bps

print("\n" + "=" * 60)
print("  STRESS TEST — BoE ANNUAL CYCLICAL SCENARIO")
print("=" * 60)
print(f"{'Scenario':<20} {'Multiplier':>12} {'Total ECL':>12} {'vs Base £m':>12} {'vs Base %':>10}")
print("-" * 60)

scenario_list = [
    ('BASE',          1.00),
    ('MILD',          1.15),
    ('MODERATE',      1.35),
    ('SEVERE STRESS', 1.65),
]

stress_results = []
base_ecl_value = None

for scenario_name, multiplier in scenario_list:
    scenario_ecl = 0
    for sector_name, data in sectors.items():
        pd_stressed  = data['PD'] * multiplier
        lgd          = data['LGD']
        ead          = data['EAD']
        stage        = get_stage(pd_stressed)
        ecl          = calculate_ecl(pd_stressed, lgd, ead, stage)
        scenario_ecl += ecl

    if base_ecl_value is None:
        base_ecl_value = scenario_ecl

    vs_base_abs = scenario_ecl - base_ecl_value
    vs_base_pct = (scenario_ecl / base_ecl_value - 1) * 100

    stress_results.append({
        'Scenario':       scenario_name,
        'PD Multiplier':  f"{multiplier}x",
        'Total ECL (£m)': round(scenario_ecl),
        'vs Base (£m)':   round(vs_base_abs),
        'vs Base %':      f"{vs_base_pct:+.1f}%"
    })

    print(f"{scenario_name:<20} {multiplier:>12.2f}x {scenario_ecl:>12,.0f} {vs_base_abs:>+12,.0f} {vs_base_pct:>+9.1f}%")

print("-" * 60)
print(f"\nSevere stress ECL increase vs base: £{stress_results[3]['vs Base (£m)']:,.0f}m ({stress_results[3]['vs Base %']})")

# ── IFRS 9 STAGING SUMMARY ────────────────────────────────────
print("\n" + "=" * 60)
print("  IFRS 9 STAGING SUMMARY")
print("=" * 60)

stage1_ecl = sum(r['ECL (£m)'] for r in base_results if r['Stage'] == 'Stage 1')
stage2_ecl = sum(r['ECL (£m)'] for r in base_results if r['Stage'] == 'Stage 2')
stage3_ecl = sum(r['ECL (£m)'] for r in base_results if r['Stage'] == 'Stage 3')

print(f"Stage 1 (12-month ECL):  £{stage1_ecl:,.0f}m  — {stage1_ecl/total_base_ecl*100:.1f}% of total ECL")
print(f"Stage 2 (Lifetime ECL):  £{stage2_ecl:,.0f}m  — {stage2_ecl/total_base_ecl*100:.1f}% of total ECL")
print(f"Stage 3 (Credit-impaired): £{stage3_ecl:,.0f}m  — {stage3_ecl/total_base_ecl*100:.1f}% of total ECL")

# ── EXPORT CSV FILES ──────────────────────────────────────────
print("\n" + "=" * 60)
print("  EXPORTING RESULTS")
print("=" * 60)

output_path = "portfolio"
os.makedirs(output_path, exist_ok=True)

# Base case ECL by sector
df_base = pds.DataFrame(base_results)
df_base.to_csv(f"{output_path}/ifrs9_ecl_base_case.csv", index=False)
print(f"✓ Base case ECL exported: {output_path}/ifrs9_ecl_base_case.csv")

# Stress scenario results
df_stress = pds.DataFrame(stress_results)
df_stress.to_csv(f"{output_path}/ifrs9_ecl_stress_scenarios.csv", index=False)
print(f"✓ Stress scenarios exported: {output_path}/ifrs9_ecl_stress_scenarios.csv")

# ── CHARTS ────────────────────────────────────────────────────
print("\nGenerating charts...")

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Caledonia Bank plc — IFRS 9 ECL Analysis\nAuthor: Pallavi Sojan | Data: Bank of England',
             fontsize=13, fontweight='bold', color='#1F3864', y=1.02)

navy  = '#1F3864'
gold  = '#C9A227'
green = '#1D9E75'
amber = '#C9A227'
red   = '#D85A30'
colors = [navy, green, amber, red, '#6C8EBF']

# Chart 1 — ECL by Sector (bar)
ax1 = axes[0]
sector_names  = [r['Sector'].replace(' ', '\n') for r in base_results]
sector_ecls   = [r['ECL (£m)'] for r in base_results]
bars = ax1.bar(sector_names, sector_ecls, color=colors, edgecolor='white', linewidth=0.5)
ax1.set_title('ECL by Sector — Base Case', fontweight='bold', color=navy, pad=10)
ax1.set_ylabel('ECL (£m)', color=navy)
ax1.set_xlabel('')
ax1.tick_params(axis='x', labelsize=8)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
for bar, val in zip(bars, sector_ecls):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
             f'£{val:,.0f}m', ha='center', va='bottom', fontsize=8, color=navy)

# Chart 2 — Stress Test (bar)
ax2 = axes[1]
scenario_names = [r['Scenario'] for r in stress_results]
scenario_ecls  = [r['Total ECL (£m)'] for r in stress_results]
stress_colors  = [navy, green, amber, red]
bars2 = ax2.bar(scenario_names, scenario_ecls, color=stress_colors, edgecolor='white', linewidth=0.5)
ax2.set_title('Total ECL by Stress Scenario\n(BoE ACS Calibrated)', fontweight='bold', color=navy, pad=10)
ax2.set_ylabel('Total ECL (£m)', color=navy)
ax2.axhline(y=scenario_ecls[0], color=navy, linestyle='--', linewidth=1, alpha=0.5, label='Base')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
for bar, val in zip(bars2, scenario_ecls):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
             f'£{val:,.0f}m', ha='center', va='bottom', fontsize=8, color=navy)

# Chart 3 — IFRS 9 Staging (donut)
ax3 = axes[2]
stage_labels = ['Stage 1\n(12-month ECL)', 'Stage 2\n(Lifetime ECL)', 'Stage 3\n(Credit-impaired)']
stage_values = [stage1_ecl, stage2_ecl, max(stage3_ecl, 0.01)]
stage_colors = [green, amber, red]
wedges, texts, autotexts = ax3.pie(
    stage_values, labels=stage_labels, colors=stage_colors,
    autopct='%1.1f%%', startangle=90,
    wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2),
    textprops={'fontsize': 9}
)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
ax3.set_title('ECL by IFRS 9 Stage\n(Base Case)', fontweight='bold', color=navy, pad=10)

plt.tight_layout()
chart_path = f"{output_path}/ifrs9_ecl_chart.png"
plt.savefig(chart_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"✓ Chart exported: {chart_path}")

# ── FINAL SUMMARY ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  MODEL COMPLETE — SUMMARY")
print("=" * 60)
print(f"Total Portfolio EAD:      £{sum(s['EAD'] for s in sectors.values()):,.0f}m")
print(f"Base Case ECL:            £{total_base_ecl:,.0f}m")
print(f"ECL / EAD ratio:          {total_base_ecl/sum(s['EAD'] for s in sectors.values())*100:.2f}%")
print(f"Stage 1 sectors:          {sum(1 for r in base_results if r['Stage']=='Stage 1')}")
print(f"Stage 2 sectors:          {sum(1 for r in base_results if r['Stage']=='Stage 2')}")
print(f"Severe stress ECL:        £{stress_results[3]['Total ECL (£m)']:,.0f}m")
print(f"Severe stress increase:   {stress_results[3]['vs Base %']}")
print(f"\nOutputs saved to: {output_path}/")
print(f"  - ifrs9_ecl_base_case.csv")
print(f"  - ifrs9_ecl_stress_scenarios.csv")
print(f"  - ifrs9_ecl_chart.png")
print("\n" + "=" * 60)
print("  IFRS 9 ECL MODEL COMPLETE")
print("  Caledonia Bank plc | Pallavi Sojan | 2025")
print("=" * 60)