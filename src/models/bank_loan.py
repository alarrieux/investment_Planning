"""Bank Loan Portfolio Optimization Model.

This module implements a linear programming model to optimize
bank loan portfolio allocation across multiple loan types.
"""

from typing import List, Dict, Optional, Tuple
import numpy as np
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus, value


class BankLoanOptimizer:
    """Optimize bank loan portfolio allocation.

    This class implements an LP model to maximize net returns (interest - bad debt)
    while satisfying various business and regulatory constraints.

    Attributes:
        total_funds (float): Total funds available for lending (in dollars)
        interest_rates (List[float]): Interest rates for each loan type
        bad_debt_ratios (List[float]): Bad debt ratios for each loan type
        loan_types (List[str]): Names of loan types
    """

    def __init__(
        self,
        total_funds: float = 12_000_000,
        interest_rates: Optional[List[float]] = None,
        bad_debt_ratios: Optional[List[float]] = None,
        loan_types: Optional[List[str]] = None,
    ):
        """Initialize the Bank Loan Optimizer.

        Args:
            total_funds: Total funds available for lending
            interest_rates: List of interest rates for each loan type
            bad_debt_ratios: List of bad debt ratios for each loan type
            loan_types: Names of loan types
        """
        self.total_funds = total_funds

        # Default values based on the original problem
        self.interest_rates = interest_rates or [0.14, 0.13, 0.12, 0.125, 0.10]
        self.bad_debt_ratios = bad_debt_ratios or [0.10, 0.07, 0.03, 0.05, 0.02]
        self.loan_types = loan_types or ["Personal", "Car", "Home", "Farm", "Commercial"]

        self.model = None
        self.variables = None
        self.solution = None

    def _calculate_net_returns(self) -> List[float]:
        """Calculate net return coefficients for objective function.

        Returns:
            List of net return coefficients
        """
        net_returns = []
        for i in range(len(self.loan_types)):
            # Net return = Interest rate * (1 - bad debt) - bad debt
            # Simplifies to: Interest rate - (Interest rate * bad debt) - bad debt
            # = Interest rate - bad debt * (1 + interest rate)
            # Actually: Net return = Interest on good loans - bad debt loss
            good_loan_fraction = 1 - self.bad_debt_ratios[i]
            interest_earned = self.interest_rates[i] * good_loan_fraction
            net_return = interest_earned - self.bad_debt_ratios[i]
            net_returns.append(net_return)
        return net_returns

    def build_model(self) -> LpProblem:
        """Build the linear programming model.

        Returns:
            LpProblem: The constructed LP model
        """
        # Create the model
        self.model = LpProblem("Bank_Loan_Portfolio_Optimization", LpMaximize)

        # Decision variables (non-negative loan amounts)
        self.variables = [
            LpVariable(f"x_{loan_type}", lowBound=0)
            for loan_type in self.loan_types
        ]

        # Objective function: maximize net returns
        net_returns = self._calculate_net_returns()
        self.model += lpSum([
            net_returns[i] * self.variables[i]
            for i in range(len(self.loan_types))
        ]), "Total_Net_Return"

        # Constraint 1: Total funds should not exceed available amount
        self.model += (
            lpSum(self.variables) <= self.total_funds,
            "Total_Funds_Constraint"
        )

        # Constraint 2: Minimum funds allocated (optional, ensures all funds used)
        self.model += (
            lpSum(self.variables) >= 0,
            "Minimum_Allocation"
        )

        # Constraint 3: Farm and commercial loans >= 40% of all loans
        # x[3] + x[4] >= 0.4 * (x[0] + x[1] + x[2] + x[3] + x[4])
        # Rearranged: 0.4*x[0] + 0.4*x[1] + 0.4*x[2] - 0.6*x[3] - 0.6*x[4] <= 0
        self.model += (
            0.4 * self.variables[0] +
            0.4 * self.variables[1] +
            0.4 * self.variables[2] -
            0.6 * self.variables[3] -
            0.6 * self.variables[4] <= 0,
            "Farm_Commercial_Minimum"
        )

        # Constraint 4: Home loans >= 50% of (personal + car + home)
        # x[2] >= 0.5 * (x[0] + x[1] + x[2])
        # Rearranged: 0.5*x[0] + 0.5*x[1] - 0.5*x[2] <= 0
        self.model += (
            0.5 * self.variables[0] +
            0.5 * self.variables[1] -
            0.5 * self.variables[2] <= 0,
            "Home_Loan_Minimum"
        )

        # Constraint 5: Bad debt ratio <= 4% of all loans
        # Sum(bad_debt[i] * x[i]) <= 0.04 * Sum(x[i])
        # Rearranged: Sum((bad_debt[i] - 0.04) * x[i]) <= 0
        self.model += (
            lpSum([
                (self.bad_debt_ratios[i] - 0.04) * self.variables[i]
                for i in range(len(self.loan_types))
            ]) <= 0,
            "Bad_Debt_Limit"
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
            allocations = {
                self.loan_types[i]: value(self.variables[i])
                for i in range(len(self.loan_types))
            }

            total_allocated = sum(allocations.values())
            objective_value = value(self.model.objective)
            roi = (objective_value / total_allocated) if total_allocated > 0 else 0

            self.solution = {
                "status": status,
                "allocations": allocations,
                "total_allocated": total_allocated,
                "net_return": objective_value,
                "roi_percentage": roi * 100,
                "model": self.model,
            }
        else:
            self.solution = {
                "status": status,
                "allocations": None,
                "error": "Optimization failed to find optimal solution"
            }

        return self.solution

    def print_summary(self):
        """Print a formatted summary of the solution."""
        if self.solution is None:
            print("No solution available. Run solve() first.")
            return

        print("=" * 60)
        print("BANK LOAN PORTFOLIO OPTIMIZATION RESULTS")
        print("=" * 60)
        print(f"\nStatus: {self.solution['status']}")

        if self.solution['status'] == "Optimal":
            print(f"\nTotal Funds Available: ${self.total_funds:,.2f}")
            print(f"Total Allocated: ${self.solution['total_allocated']:,.2f}")
            print(f"Net Return: ${self.solution['net_return']:,.2f}")
            print(f"ROI: {self.solution['roi_percentage']:.2f}%")

            print("\n" + "-" * 60)
            print("Loan Allocation by Type:")
            print("-" * 60)
            print(f"{'Loan Type':<15} {'Amount':>15} {'Percentage':>12}")
            print("-" * 60)

            for loan_type, amount in self.solution['allocations'].items():
                percentage = (amount / self.solution['total_allocated'] * 100) if self.solution['total_allocated'] > 0 else 0
                print(f"{loan_type:<15} ${amount:>14,.2f} {percentage:>11.2f}%")

            print("=" * 60)
        else:
            print(f"\nError: {self.solution.get('error', 'Unknown error')}")


if __name__ == "__main__":
    # Example usage
    optimizer = BankLoanOptimizer()
    solution = optimizer.solve()
    optimizer.print_summary()
