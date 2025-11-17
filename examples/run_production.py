#!/usr/bin/env python3
"""Example script for Production-Inventory Optimization.

This script demonstrates how to use the ProductionInventoryOptimizer class
to solve a multi-period production planning problem.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.production_inventory import ProductionInventoryOptimizer
from src.visualization.plot_utils import plot_production_schedule, plot_comparison


def main():
    """Run the production-inventory optimization example."""
    print("=" * 70)
    print("PRODUCTION-INVENTORY OPTIMIZATION EXAMPLE")
    print("=" * 70)
    print()

    # Create optimizer with default parameters
    print("Initializing optimizer with parameters:")
    print(f"  Planning Horizon: 6 months")
    print(f"  Production Costs: $50, $45, $55, $48, $52, $50 per unit")
    print(f"  Storage Cost: $8 per unit per month")
    print(f"  Demand Schedule: 100, 250, 190, 140, 220, 110 units")
    print()

    optimizer = ProductionInventoryOptimizer()

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

        periods = list(range(1, 7))
        production = solution['production_schedule']
        demand = optimizer.demands
        inventory = solution['inventory_schedule']

        # Production schedule plot
        fig1 = plot_production_schedule(
            periods=periods,
            production=production,
            demand=demand,
            inventory=inventory,
            title="ACME Manufacturing: 6-Month Production Plan"
        )

        # Cost comparison
        production_costs = [
            optimizer.production_costs[i] * production[i]
            for i in range(len(periods))
        ]
        storage_costs = [
            optimizer.storage_cost * inventory[i]
            for i in range(len(periods))
        ]

        fig2 = plot_comparison(
            categories=[f"Month {i}" for i in periods],
            values_dict={
                "Production Cost": production_costs,
                "Storage Cost": storage_costs
            },
            title="Cost Breakdown by Period",
            ylabel="Cost ($)"
        )

        # Save figures
        os.makedirs('output', exist_ok=True)
        fig1.savefig('output/production_schedule.png', dpi=300, bbox_inches='tight')
        fig2.savefig('output/production_costs.png', dpi=300, bbox_inches='tight')

        print("✓ Visualizations saved to output/")
        print("  - production_schedule.png")
        print("  - production_costs.png")
        print()

        # Print key insights
        print("-" * 70)
        print("KEY INSIGHTS:")
        print("-" * 70)

        # Find overproduction periods
        print("\nProduction Strategy:")
        for i in range(len(periods)):
            if production[i] > demand[i]:
                overprod = production[i] - demand[i]
                savings = optimizer.production_costs[i+1] - optimizer.production_costs[i] if i < len(periods)-1 else 0
                print(f"  • Month {periods[i]}: Produce {int(overprod)} extra units")
                print(f"    (Production cost: ${optimizer.production_costs[i]:.0f}/unit)")
                if i < len(periods)-1:
                    print(f"    (Next month cost: ${optimizer.production_costs[i+1]:.0f}/unit)")

        total_prod = sum(production)
        total_demand = sum(demand)
        total_inv = sum(inventory)

        print(f"\nSummary:")
        print(f"  • Total Production: {total_prod:.0f} units")
        print(f"  • Total Demand: {total_demand:.0f} units")
        print(f"  • Average Inventory: {total_inv/len(periods):.1f} units")
        print(f"  • Total Cost: ${solution['total_cost']:,.2f}")
        print(f"    - Production: ${solution['production_cost']:,.2f}")
        print(f"    - Storage: ${solution['storage_cost']:,.2f}")

        print("\nRecommendation:")
        print("  Take advantage of low production costs in Month 2 ($45/unit)")
        print("  by overproducing and storing inventory for Month 3.")
        print()


if __name__ == "__main__":
    main()
