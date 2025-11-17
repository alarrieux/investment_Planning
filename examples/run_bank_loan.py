#!/usr/bin/env python3
"""Example script for Bank Loan Portfolio Optimization.

This script demonstrates how to use the BankLoanOptimizer class
to solve a loan portfolio allocation problem.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.bank_loan import BankLoanOptimizer
from src.visualization.plot_utils import plot_allocation, plot_pie_chart


def main():
    """Run the bank loan optimization example."""
    print("=" * 70)
    print("BANK LOAN PORTFOLIO OPTIMIZATION EXAMPLE")
    print("=" * 70)
    print()

    # Create optimizer with default parameters
    print("Initializing optimizer with parameters:")
    print(f"  Total Funds: $12,000,000")
    print(f"  Loan Types: Personal, Car, Home, Farm, Commercial")
    print(f"  Interest Rates: 14%, 13%, 12%, 12.5%, 10%")
    print(f"  Bad Debt Ratios: 10%, 7%, 3%, 5%, 2%")
    print()

    optimizer = BankLoanOptimizer()

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

        # Bar chart
        fig1 = plot_allocation(
            solution['allocations'],
            title="Bank Loan Portfolio Allocation",
            ylabel="Amount Allocated ($)"
        )

        # Pie chart
        fig2 = plot_pie_chart(
            solution['allocations'],
            title="Loan Portfolio Distribution"
        )

        # Save figures
        os.makedirs('output', exist_ok=True)
        fig1.savefig('output/bank_loan_allocation.png', dpi=300, bbox_inches='tight')
        fig2.savefig('output/bank_loan_distribution.png', dpi=300, bbox_inches='tight')

        print("✓ Visualizations saved to output/")
        print("  - bank_loan_allocation.png")
        print("  - bank_loan_distribution.png")
        print()

        # Print key insights
        print("-" * 70)
        print("KEY INSIGHTS:")
        print("-" * 70)

        allocations = solution['allocations']
        total = solution['total_allocated']

        # Find top allocations
        sorted_allocs = sorted(allocations.items(), key=lambda x: x[1], reverse=True)

        print(f"\nTop Recommended Allocations:")
        for loan_type, amount in sorted_allocs[:3]:
            if amount > 0:
                pct = (amount / total * 100) if total > 0 else 0
                print(f"  • {loan_type}: ${amount:,.0f} ({pct:.1f}%)")

        print(f"\nNet ROI: {solution['roi_percentage']:.2f}%")
        print(f"Expected Annual Return: ${solution['net_return']:,.2f}")
        print()

        # Analysis
        if allocations.get('Home', 0) > 0:
            print("Analysis:")
            print("  • Home loans receive significant allocation due to:")
            print("    - Low bad debt ratio (3%)")
            print("    - Competitive interest rate (12%)")
            print("    - Meeting regulatory requirements")

        if allocations.get('Commercial', 0) > 0:
            print("  • Commercial loans are included to satisfy the")
            print("    40% minimum for Farm + Commercial loans constraint")

        print()


if __name__ == "__main__":
    main()
