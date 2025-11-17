"""Unit tests for Bank Loan Portfolio Optimization model."""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.bank_loan import BankLoanOptimizer


class TestBankLoanOptimizer:
    """Test suite for BankLoanOptimizer class."""

    def test_initialization_default(self):
        """Test default initialization."""
        optimizer = BankLoanOptimizer()

        assert optimizer.total_funds == 12_000_000
        assert len(optimizer.loan_types) == 5
        assert len(optimizer.interest_rates) == 5
        assert len(optimizer.bad_debt_ratios) == 5

    def test_initialization_custom(self):
        """Test custom initialization."""
        optimizer = BankLoanOptimizer(
            total_funds=10_000_000,
            interest_rates=[0.15, 0.14],
            bad_debt_ratios=[0.08, 0.05],
            loan_types=["Type A", "Type B"]
        )

        assert optimizer.total_funds == 10_000_000
        assert len(optimizer.loan_types) == 2
        assert optimizer.interest_rates == [0.15, 0.14]

    def test_net_return_calculation(self):
        """Test net return coefficient calculation."""
        optimizer = BankLoanOptimizer()
        net_returns = optimizer._calculate_net_returns()

        assert len(net_returns) == len(optimizer.loan_types)
        # All net returns should be positive for valid inputs
        assert all(nr >= 0 for nr in net_returns)

    def test_model_building(self):
        """Test that model builds without errors."""
        optimizer = BankLoanOptimizer()
        model = optimizer.build_model()

        assert model is not None
        assert optimizer.model is not None
        assert optimizer.variables is not None
        assert len(optimizer.variables) == len(optimizer.loan_types)

    def test_solve(self):
        """Test solving the optimization problem."""
        optimizer = BankLoanOptimizer()
        solution = optimizer.solve()

        assert solution is not None
        assert 'status' in solution
        assert solution['status'] == 'Optimal'
        assert 'allocations' in solution
        assert 'total_allocated' in solution
        assert 'net_return' in solution

    def test_solution_constraints(self):
        """Test that solution satisfies constraints."""
        optimizer = BankLoanOptimizer()
        solution = optimizer.solve()

        allocations = solution['allocations']
        total_allocated = sum(allocations.values())

        # Constraint 1: Total funds should not exceed limit
        assert total_allocated <= optimizer.total_funds + 1e-6

        # All allocations should be non-negative
        assert all(v >= -1e-6 for v in allocations.values())

        # Constraint 2: Farm + Commercial >= 40% of total
        farm_commercial = allocations['Farm'] + allocations['Commercial']
        assert farm_commercial >= 0.4 * total_allocated - 1e-6

        # Constraint 3: Home >= 50% of (Personal + Car + Home)
        pch_total = allocations['Personal'] + allocations['Car'] + allocations['Home']
        if pch_total > 1e-6:
            assert allocations['Home'] >= 0.5 * pch_total - 1e-6

        # Constraint 4: Bad debt <= 4%
        total_bad_debt = sum([
            allocations[loan_type] * optimizer.bad_debt_ratios[i]
            for i, loan_type in enumerate(optimizer.loan_types)
        ])
        assert total_bad_debt <= 0.04 * total_allocated + 1e-6

    def test_print_summary(self):
        """Test that print_summary runs without error."""
        optimizer = BankLoanOptimizer()
        optimizer.solve()
        # Should not raise an exception
        optimizer.print_summary()

    def test_roi_calculation(self):
        """Test ROI percentage calculation."""
        optimizer = BankLoanOptimizer()
        solution = optimizer.solve()

        assert 'roi_percentage' in solution
        assert solution['roi_percentage'] > 0
        assert solution['roi_percentage'] < 100  # ROI should be realistic


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
