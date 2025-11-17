"""Unit tests for Oil Refining Optimization model."""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.oil_refining import OilRefiningOptimizer


class TestOilRefiningOptimizer:
    """Test suite for OilRefiningOptimizer class."""

    def test_initialization_default(self):
        """Test default initialization."""
        optimizer = OilRefiningOptimizer()

        assert optimizer.crude_capacity == 1_500_000
        assert optimizer.cracker_capacity == 200_000
        assert 'feedstock' in optimizer.octane_numbers
        assert 'cracker' in optimizer.octane_numbers
        assert len(optimizer.demand_limits) == 3
        assert len(optimizer.profit_margins) == 3

    def test_initialization_custom(self):
        """Test custom initialization."""
        optimizer = OilRefiningOptimizer(
            crude_capacity=1_000_000,
            cracker_capacity=100_000,
            demand_limits={'regular': 40_000, 'premium': 25_000, 'super': 30_000}
        )

        assert optimizer.crude_capacity == 1_000_000
        assert optimizer.cracker_capacity == 100_000
        assert optimizer.demand_limits['regular'] == 40_000

    def test_model_building(self):
        """Test that model builds without errors."""
        optimizer = OilRefiningOptimizer()
        model = optimizer.build_model()

        assert model is not None
        assert optimizer.model is not None
        assert optimizer.variables is not None
        assert 'feedstock' in optimizer.variables
        assert 'cracker' in optimizer.variables

    def test_solve(self):
        """Test solving the optimization problem."""
        optimizer = OilRefiningOptimizer()
        solution = optimizer.solve()

        assert solution is not None
        assert 'status' in solution
        assert solution['status'] == 'Optimal'
        assert 'production' in solution
        assert 'total_profit' in solution

    def test_capacity_constraints(self):
        """Test that solution respects capacity constraints."""
        optimizer = OilRefiningOptimizer()
        solution = optimizer.solve()

        production = solution['production']

        # Calculate total feedstock and cracker usage
        total_feedstock = sum([
            production[p]['feedstock']
            for p in ['regular', 'premium', 'super']
        ])

        total_cracker = sum([
            production[p]['cracker']
            for p in ['regular', 'premium', 'super']
        ])

        # Check crude capacity constraint
        crude_used = 5 * total_feedstock + 10 * total_cracker
        assert crude_used <= optimizer.crude_capacity + 1e-6

        # Check cracker capacity constraint
        cracker_used = 2 * total_cracker
        assert cracker_used <= optimizer.cracker_capacity + 1e-6

    def test_demand_constraints(self):
        """Test that solution respects demand limits."""
        optimizer = OilRefiningOptimizer()
        solution = optimizer.solve()

        production = solution['production']

        for product in ['regular', 'premium', 'super']:
            total_prod = production[product]['total']
            demand_limit = optimizer.demand_limits[product]
            assert total_prod <= demand_limit + 1e-6

    def test_octane_constraints(self):
        """Test that solution satisfies octane requirements."""
        optimizer = OilRefiningOptimizer()
        solution = optimizer.solve()

        production = solution['production']
        octane_feed = optimizer.octane_numbers['feedstock']
        octane_crack = optimizer.octane_numbers['cracker']

        for product in ['regular', 'premium', 'super']:
            feedstock = production[product]['feedstock']
            cracker = production[product]['cracker']
            total = production[product]['total']

            if total > 1e-6:
                # Calculate weighted average octane
                avg_octane = (octane_feed * feedstock + octane_crack * cracker) / total
                required_octane = optimizer.octane_numbers[product]

                # Should meet or exceed required octane (with small tolerance)
                assert avg_octane >= required_octane - 1e-3

    def test_non_negative_production(self):
        """Test that all production values are non-negative."""
        optimizer = OilRefiningOptimizer()
        solution = optimizer.solve()

        production = solution['production']

        for product in ['regular', 'premium', 'super']:
            assert production[product]['feedstock'] >= -1e-6
            assert production[product]['cracker'] >= -1e-6
            assert production[product]['total'] >= -1e-6

    def test_profit_calculation(self):
        """Test that profit calculation is correct."""
        optimizer = OilRefiningOptimizer()
        solution = optimizer.solve()

        production = solution['production']

        # Calculate expected profit
        expected_profit = sum([
            production[product]['total'] * optimizer.profit_margins[product]
            for product in ['regular', 'premium', 'super']
        ])

        assert abs(solution['total_profit'] - expected_profit) < 1e-3

    def test_print_summary(self):
        """Test that print_summary runs without error."""
        optimizer = OilRefiningOptimizer()
        optimizer.solve()
        # Should not raise an exception
        optimizer.print_summary()

    def test_consistency(self):
        """Test that feedstock + cracker = total for each product."""
        optimizer = OilRefiningOptimizer()
        solution = optimizer.solve()

        production = solution['production']

        for product in ['regular', 'premium', 'super']:
            feedstock = production[product]['feedstock']
            cracker = production[product]['cracker']
            total = production[product]['total']

            assert abs(feedstock + cracker - total) < 1e-6


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
