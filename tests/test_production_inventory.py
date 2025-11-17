"""Unit tests for Production-Inventory Optimization model."""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.production_inventory import ProductionInventoryOptimizer


class TestProductionInventoryOptimizer:
    """Test suite for ProductionInventoryOptimizer class."""

    def test_initialization_default(self):
        """Test default initialization."""
        optimizer = ProductionInventoryOptimizer()

        assert len(optimizer.production_costs) == 6
        assert optimizer.storage_cost == 8.0
        assert len(optimizer.demands) == 6
        assert optimizer.num_periods == 6

    def test_initialization_custom(self):
        """Test custom initialization."""
        optimizer = ProductionInventoryOptimizer(
            production_costs=[100, 110, 105],
            storage_cost=5.0,
            demands=[50, 75, 60]
        )

        assert len(optimizer.production_costs) == 3
        assert optimizer.storage_cost == 5.0
        assert optimizer.num_periods == 3

    def test_model_building(self):
        """Test that model builds without errors."""
        optimizer = ProductionInventoryOptimizer()
        model = optimizer.build_model()

        assert model is not None
        assert optimizer.model is not None
        assert optimizer.production_vars is not None
        assert optimizer.inventory_vars is not None
        assert len(optimizer.production_vars) == optimizer.num_periods
        assert len(optimizer.inventory_vars) == optimizer.num_periods

    def test_solve(self):
        """Test solving the optimization problem."""
        optimizer = ProductionInventoryOptimizer()
        solution = optimizer.solve()

        assert solution is not None
        assert 'status' in solution
        assert solution['status'] == 'Optimal'
        assert 'production_schedule' in solution
        assert 'inventory_schedule' in solution
        assert 'total_cost' in solution

    def test_solution_meets_demand(self):
        """Test that solution meets all demand requirements."""
        optimizer = ProductionInventoryOptimizer()
        solution = optimizer.solve()

        production = solution['production_schedule']
        inventory = solution['inventory_schedule']
        demands = optimizer.demands

        # Check inventory balance equations
        # Period 1: production[0] - inventory[0] == demand[0]
        assert abs(production[0] - inventory[0] - demands[0]) < 1e-6

        # Other periods: inventory[i-1] + production[i] - inventory[i] == demand[i]
        for i in range(1, len(demands)):
            balance = inventory[i-1] + production[i] - inventory[i]
            assert abs(balance - demands[i]) < 1e-6

    def test_non_negative_production(self):
        """Test that production is non-negative."""
        optimizer = ProductionInventoryOptimizer()
        solution = optimizer.solve()

        production = solution['production_schedule']
        assert all(p >= -1e-6 for p in production)

    def test_non_negative_inventory(self):
        """Test that inventory is non-negative."""
        optimizer = ProductionInventoryOptimizer()
        solution = optimizer.solve()

        inventory = solution['inventory_schedule']
        assert all(i >= -1e-6 for i in inventory)

    def test_cost_calculation(self):
        """Test that cost breakdown is correct."""
        optimizer = ProductionInventoryOptimizer()
        solution = optimizer.solve()

        # Verify total cost equals production + storage
        expected_total = solution['production_cost'] + solution['storage_cost']
        assert abs(solution['total_cost'] - expected_total) < 1e-6

    def test_print_summary(self):
        """Test that print_summary runs without error."""
        optimizer = ProductionInventoryOptimizer()
        optimizer.solve()
        # Should not raise an exception
        optimizer.print_summary()

    def test_small_problem(self):
        """Test with a small problem instance."""
        optimizer = ProductionInventoryOptimizer(
            production_costs=[10, 12],
            storage_cost=2.0,
            demands=[100, 100]
        )

        solution = optimizer.solve()

        assert solution['status'] == 'Optimal'
        # With these costs, should produce exactly demand each period
        # (no incentive to store)
        production = solution['production_schedule']
        assert sum(production) >= sum(optimizer.demands) - 1e-6


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
