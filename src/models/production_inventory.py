"""Multi-Period Production-Inventory Optimization Model.

This module implements a linear programming model for production
and inventory planning across multiple time periods.
"""

from typing import List, Dict, Optional
import numpy as np
from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpStatus, value


class ProductionInventoryOptimizer:
    """Optimize production and inventory levels across multiple periods.

    This class implements an LP model to minimize total costs (production + storage)
    while meeting demand requirements for each period.

    Attributes:
        production_costs (List[float]): Production cost per unit for each period
        storage_cost (float): Storage cost per unit per period
        demands (List[int]): Demand requirements for each period
        num_periods (int): Number of time periods
    """

    def __init__(
        self,
        production_costs: Optional[List[float]] = None,
        storage_cost: float = 8.0,
        demands: Optional[List[int]] = None,
    ):
        """Initialize the Production-Inventory Optimizer.

        Args:
            production_costs: List of production costs per unit for each period
            storage_cost: Storage cost per unit per period
            demands: List of demand requirements for each period
        """
        # Default values from the original problem
        self.production_costs = production_costs or [50, 45, 55, 48, 52, 50]
        self.storage_cost = storage_cost
        self.demands = demands or [100, 250, 190, 140, 220, 110]
        self.num_periods = len(self.demands)

        self.model = None
        self.production_vars = None
        self.inventory_vars = None
        self.solution = None

    def build_model(self) -> LpProblem:
        """Build the linear programming model.

        Returns:
            LpProblem: The constructed LP model
        """
        # Create the model
        self.model = LpProblem("Production_Inventory_Optimization", LpMinimize)

        # Decision variables
        # Production quantities (non-negative)
        self.production_vars = [
            LpVariable(f"x_{i+1}", lowBound=0)
            for i in range(self.num_periods)
        ]

        # Ending inventory levels (non-negative)
        self.inventory_vars = [
            LpVariable(f"I_{i+1}", lowBound=0)
            for i in range(self.num_periods)
        ]

        # Objective function: minimize total cost (production + storage)
        total_production_cost = lpSum([
            self.production_costs[i] * self.production_vars[i]
            for i in range(self.num_periods)
        ])

        total_storage_cost = lpSum([
            self.storage_cost * self.inventory_vars[i]
            for i in range(self.num_periods)
        ])

        self.model += (
            total_production_cost + total_storage_cost,
            "Total_Cost"
        )

        # Constraints: Inventory balance equations
        # Period 1: Beginning inventory (0) + Production - Ending inventory = Demand
        self.model += (
            self.production_vars[0] - self.inventory_vars[0] == self.demands[0],
            "Period_1_Balance"
        )

        # Periods 2 through n:
        # Beginning inventory + Production - Ending inventory = Demand
        for i in range(1, self.num_periods):
            self.model += (
                self.inventory_vars[i-1] + self.production_vars[i] -
                self.inventory_vars[i] == self.demands[i],
                f"Period_{i+1}_Balance"
            )

        # Optional: Ending inventory in last period should be zero
        # (uncomment if desired)
        # self.model += (
        #     self.inventory_vars[-1] == 0,
        #     "Zero_Final_Inventory"
        # )

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
            production_schedule = [
                value(self.production_vars[i])
                for i in range(self.num_periods)
            ]

            inventory_schedule = [
                value(self.inventory_vars[i])
                for i in range(self.num_periods)
            ]

            total_cost = value(self.model.objective)

            # Calculate cost breakdown
            production_cost = sum([
                self.production_costs[i] * production_schedule[i]
                for i in range(self.num_periods)
            ])

            storage_cost = sum([
                self.storage_cost * inventory_schedule[i]
                for i in range(self.num_periods)
            ])

            self.solution = {
                "status": status,
                "production_schedule": production_schedule,
                "inventory_schedule": inventory_schedule,
                "total_cost": total_cost,
                "production_cost": production_cost,
                "storage_cost": storage_cost,
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
        print("PRODUCTION-INVENTORY OPTIMIZATION RESULTS")
        print("=" * 80)
        print(f"\nStatus: {self.solution['status']}")

        if self.solution['status'] == "Optimal":
            print(f"\nTotal Cost: ${self.solution['total_cost']:,.2f}")
            print(f"  Production Cost: ${self.solution['production_cost']:,.2f}")
            print(f"  Storage Cost: ${self.solution['storage_cost']:,.2f}")

            print("\n" + "-" * 80)
            print("Production and Inventory Schedule:")
            print("-" * 80)
            print(f"{'Period':<8} {'Demand':>10} {'Produce':>10} {'Inventory':>12} {'Prod Cost':>12} {'Notes':<20}")
            print("-" * 80)

            for i in range(self.num_periods):
                prod = self.solution['production_schedule'][i]
                inv = self.solution['inventory_schedule'][i]
                demand = self.demands[i]
                cost = self.production_costs[i]

                notes = ""
                if prod > demand:
                    notes = f"Build {int(prod - demand)} units"
                elif inv > 0:
                    notes = f"Use {int(inv)} from stock"

                print(f"{i+1:<8} {demand:>10} {prod:>10.0f} {inv:>12.0f} ${cost:>11.2f} {notes:<20}")

            print("=" * 80)
        else:
            print(f"\nError: {self.solution.get('error', 'Unknown error')}")


if __name__ == "__main__":
    # Example usage
    optimizer = ProductionInventoryOptimizer()
    solution = optimizer.solve()
    optimizer.print_summary()
