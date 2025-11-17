"""Crude Oil Refining and Gasoline Blending Optimization Model.

This module implements a linear programming model for optimizing
crude oil refining operations and gasoline blending.
"""

from typing import List, Dict, Optional, Tuple
import numpy as np
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus, value


class OilRefiningOptimizer:
    """Optimize crude oil refining and gasoline blending operations.

    This class implements an LP model to maximize profit from refining
    crude oil into different gasoline products with octane constraints.

    Attributes:
        crude_capacity (float): Crude oil processing capacity (bbl/day)
        cracker_capacity (float): Cracker unit capacity (bbl/day)
        octane_numbers (Dict): Octane numbers for feedstock and cracker output
        demand_limits (Dict): Demand limits for each gasoline type
        profit_margins (Dict): Profit per barrel for each gasoline type
    """

    def __init__(
        self,
        crude_capacity: float = 1_500_000,
        cracker_capacity: float = 200_000,
        octane_numbers: Optional[Dict] = None,
        demand_limits: Optional[Dict] = None,
        profit_margins: Optional[Dict] = None,
    ):
        """Initialize the Oil Refining Optimizer.

        Args:
            crude_capacity: Crude oil processing capacity (barrels/day)
            cracker_capacity: Cracker unit capacity (barrels/day)
            octane_numbers: Octane numbers for feedstock and cracker
            demand_limits: Maximum demand for each gasoline type
            profit_margins: Profit per barrel for each gasoline type
        """
        self.crude_capacity = crude_capacity
        self.cracker_capacity = cracker_capacity

        # Default octane numbers
        self.octane_numbers = octane_numbers or {
            "feedstock": 82,
            "cracker": 98,
            "regular": 87,
            "premium": 89,
            "super": 92,
        }

        # Default demand limits (barrels/day)
        self.demand_limits = demand_limits or {
            "regular": 50_000,
            "premium": 30_000,
            "super": 40_000,
        }

        # Default profit margins ($/barrel)
        self.profit_margins = profit_margins or {
            "regular": 6.70,
            "premium": 7.20,
            "super": 8.10,
        }

        self.model = None
        self.variables = None
        self.solution = None

    def build_model(self) -> LpProblem:
        """Build the linear programming model.

        Returns:
            LpProblem: The constructed LP model
        """
        # Create the model
        self.model = LpProblem("Oil_Refining_Optimization", LpMaximize)

        # Decision variables: amount of each source for each product
        # x[source][product] where source in {feedstock, cracker}
        # product in {regular, premium, super}

        self.variables = {
            "feedstock": {
                "regular": LpVariable("x_feed_regular", lowBound=0),
                "premium": LpVariable("x_feed_premium", lowBound=0),
                "super": LpVariable("x_feed_super", lowBound=0),
            },
            "cracker": {
                "regular": LpVariable("x_crack_regular", lowBound=0),
                "premium": LpVariable("x_crack_premium", lowBound=0),
                "super": LpVariable("x_crack_super", lowBound=0),
            }
        }

        # Objective function: maximize total profit
        total_profit = lpSum([
            self.profit_margins[product] * (
                self.variables["feedstock"][product] +
                self.variables["cracker"][product]
            )
            for product in ["regular", "premium", "super"]
        ])

        self.model += total_profit, "Total_Profit"

        # Constraint 1: Crude oil capacity
        # Feedstock uses crude at 5:1 ratio, cracker at 10:1
        total_feedstock = lpSum([
            self.variables["feedstock"][p]
            for p in ["regular", "premium", "super"]
        ])

        total_cracker = lpSum([
            self.variables["cracker"][p]
            for p in ["regular", "premium", "super"]
        ])

        self.model += (
            5 * total_feedstock + 10 * total_cracker <= self.crude_capacity,
            "Crude_Capacity"
        )

        # Constraint 2: Cracker unit capacity
        self.model += (
            2 * total_cracker <= self.cracker_capacity,
            "Cracker_Capacity"
        )

        # Constraint 3: Demand limits for each product
        for product in ["regular", "premium", "super"]:
            self.model += (
                self.variables["feedstock"][product] +
                self.variables["cracker"][product] <=
                self.demand_limits[product],
                f"Demand_{product}"
            )

        # Constraint 4: Octane number requirements
        # For each product, weighted average octane must meet minimum

        # Regular (87): 82*x_feed + 98*x_crack >= 87*(x_feed + x_crack)
        # Rearranged: -5*x_feed + 11*x_crack >= 0
        self.model += (
            -5 * self.variables["feedstock"]["regular"] +
            11 * self.variables["cracker"]["regular"] >= 0,
            "Octane_Regular"
        )

        # Premium (89): 82*x_feed + 98*x_crack >= 89*(x_feed + x_crack)
        # Rearranged: -7*x_feed + 9*x_crack >= 0
        self.model += (
            -7 * self.variables["feedstock"]["premium"] +
            9 * self.variables["cracker"]["premium"] >= 0,
            "Octane_Premium"
        )

        # Super (92): 82*x_feed + 98*x_crack >= 92*(x_feed + x_crack)
        # Rearranged: -10*x_feed + 6*x_crack >= 0
        self.model += (
            -10 * self.variables["feedstock"]["super"] +
            6 * self.variables["cracker"]["super"] >= 0,
            "Octane_Super"
        )

        return self.model

    def solve(self) -> Dict:
        """Solve the optimization problem.

        Returns:
            Dictionary containing solution details
        """
        if self.model is None:
            self.build_model()

        # Solve the model
        self.model.solve()

        # Extract solution
        status = LpStatus[self.model.status]

        if status == "Optimal":
            production = {
                product: {
                    "feedstock": value(self.variables["feedstock"][product]),
                    "cracker": value(self.variables["cracker"][product]),
                    "total": value(self.variables["feedstock"][product]) +
                            value(self.variables["cracker"][product])
                }
                for product in ["regular", "premium", "super"]
            }

            total_profit = value(self.model.objective)

            self.solution = {
                "status": status,
                "production": production,
                "total_profit": total_profit,
                "daily_profit": total_profit,
                "model": self.model,
            }
        else:
            self.solution = {
                "status": status,
                "error": "Optimization failed to find optimal solution"
            }

        return self.solution

    def print_summary(self):
        """Print a formatted summary of the solution."""
        if self.solution is None:
            print("No solution available. Run solve() first.")
            return

        print("=" * 80)
        print("OIL REFINING & GASOLINE BLENDING OPTIMIZATION RESULTS")
        print("=" * 80)
        print(f"\nStatus: {self.solution['status']}")

        if self.solution['status'] == "Optimal":
            print(f"\nDaily Profit: ${self.solution['daily_profit']:,.2f}")
            print(f"Annual Profit (365 days): ${self.solution['daily_profit'] * 365:,.2f}")

            print("\n" + "-" * 80)
            print("Production Schedule (barrels/day):")
            print("-" * 80)
            print(f"{'Product':<12} {'Feedstock':>12} {'Cracker':>12} {'Total':>12} {'Demand Limit':>15} {'Utilization':>12}")
            print("-" * 80)

            for product in ["regular", "premium", "super"]:
                prod_data = self.solution['production'][product]
                feedstock = prod_data['feedstock']
                cracker = prod_data['cracker']
                total = prod_data['total']
                limit = self.demand_limits[product]
                utilization = (total / limit * 100) if limit > 0 else 0

                print(f"{product.capitalize():<12} {feedstock:>12.0f} {cracker:>12.0f} "
                      f"{total:>12.0f} {limit:>15,} {utilization:>11.1f}%")

            # Calculate resource utilization
            total_feedstock = sum([
                self.solution['production'][p]['feedstock']
                for p in ["regular", "premium", "super"]
            ])

            total_cracker = sum([
                self.solution['production'][p]['cracker']
                for p in ["regular", "premium", "super"]
            ])

            crude_used = 5 * total_feedstock + 10 * total_cracker
            cracker_used = 2 * total_cracker

            print("\n" + "-" * 80)
            print("Resource Utilization:")
            print("-" * 80)
            print(f"Crude Oil: {crude_used:,.0f} / {self.crude_capacity:,.0f} bbl/day "
                  f"({crude_used/self.crude_capacity*100:.1f}%)")
            print(f"Cracker Unit: {cracker_used:,.0f} / {self.cracker_capacity:,.0f} bbl/day "
                  f"({cracker_used/self.cracker_capacity*100:.1f}%)")

            print("=" * 80)
        else:
            print(f"\nError: {self.solution.get('error', 'Unknown error')}")


if __name__ == "__main__":
    # Example usage
    optimizer = OilRefiningOptimizer()
    solution = optimizer.solve()
    optimizer.print_summary()
