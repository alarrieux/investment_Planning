#!/usr/bin/env python3
"""Example script for Oil Refining Optimization.

This script demonstrates how to use the OilRefiningOptimizer class
to solve a crude oil refining and gasoline blending problem.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.oil_refining import OilRefiningOptimizer
from src.visualization.plot_utils import plot_allocation, plot_comparison


def main():
    """Run the oil refining optimization example."""
    print("=" * 70)
    print("CRUDE OIL REFINING & GASOLINE BLENDING OPTIMIZATION")
    print("=" * 70)
    print()

    # Create optimizer with default parameters
    print("Initializing optimizer with parameters:")
    print(f"  Crude Oil Capacity: 1,500,000 bbl/day")
    print(f"  Cracker Capacity: 200,000 bbl/day")
    print(f"  Octane Numbers: Feedstock=82, Cracker=98")
    print(f"  Products: Regular (87), Premium (89), Super (92)")
    print(f"  Profit Margins: $6.70, $7.20, $8.10 per barrel")
    print()

    optimizer = OilRefiningOptimizer()

    # Build and solve the model
    print("Building optimization model...")
    optimizer.build_model()

    print("Solving...")
    solution = optimizer.solve()
    print()

    # Display results
    optimizer.print_summary()
    print()

    # Generate visualizations
    if solution['status'] == 'Optimal':
        print("Generating visualizations...")

        # Production totals by product
        production_totals = {
            product.capitalize(): solution['production'][product]['total']
            for product in ['regular', 'premium', 'super']
        }

        fig1 = plot_allocation(
            production_totals,
            title="Daily Gasoline Production by Type",
            ylabel="Production (barrels/day)"
        )

        # Source breakdown
        products = ['Regular', 'Premium', 'Super']
        feedstock_amounts = [
            solution['production'][p.lower()]['feedstock']
            for p in products
        ]
        cracker_amounts = [
            solution['production'][p.lower()]['cracker']
            for p in products
        ]

        fig2 = plot_comparison(
            categories=products,
            values_dict={
                "From Feedstock": feedstock_amounts,
                "From Cracker": cracker_amounts
            },
            title="Production Source Breakdown",
            ylabel="Production (barrels/day)"
        )

        # Save figures
        os.makedirs('output', exist_ok=True)
        fig1.savefig('output/refining_production.png', dpi=300, bbox_inches='tight')
        fig2.savefig('output/refining_sources.png', dpi=300, bbox_inches='tight')

        print("✓ Visualizations saved to output/")
        print("  - refining_production.png")
        print("  - refining_sources.png")
        print()

        # Print key insights
        print("-" * 70)
        print("KEY INSIGHTS:")
        print("-" * 70)

        print("\nProduction Strategy:")
        for product in ['regular', 'premium', 'super']:
            prod_data = solution['production'][product]
            total = prod_data['total']
            feedstock = prod_data['feedstock']
            cracker = prod_data['cracker']

            if total > 0:
                feed_pct = (feedstock / total * 100) if total > 0 else 0
                crack_pct = (cracker / total * 100) if total > 0 else 0

                print(f"\n  {product.capitalize()}:")
                print(f"    • Total: {total:,.0f} bbl/day")
                print(f"    • Feedstock: {feedstock:,.0f} bbl/day ({feed_pct:.1f}%)")
                print(f"    • Cracker: {cracker:,.0f} bbl/day ({crack_pct:.1f}%)")

        # Profitability analysis
        daily_profit = solution['daily_profit']
        annual_profit = daily_profit * 365

        print(f"\nProfitability:")
        print(f"  • Daily Profit: ${daily_profit:,.2f}")
        print(f"  • Annual Profit: ${annual_profit:,.2f}")

        # Calculate profit per product
        print(f"\nProfit by Product:")
        for product in ['regular', 'premium', 'super']:
            total_prod = solution['production'][product]['total']
            margin = optimizer.profit_margins[product]
            product_profit = total_prod * margin
            pct_contrib = (product_profit / daily_profit * 100) if daily_profit > 0 else 0

            print(f"  • {product.capitalize()}: ${product_profit:,.2f}/day ({pct_contrib:.1f}%)")

        print("\nRecommendation:")
        print("  Maximize Super gasoline production as it has the highest")
        print("  profit margin ($8.10/bbl) while maintaining octane requirements")
        print("  through optimal blending of feedstock and cracker output.")
        print()


if __name__ == "__main__":
    main()
