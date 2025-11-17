"""Utility functions for LP solver operations."""

from typing import Dict, Any, Optional
from pulp import LpProblem, LpStatus


def validate_solution(model: LpProblem) -> bool:
    """Validate that an LP solution is optimal.

    Args:
        model: The solved LP model

    Returns:
        True if solution is optimal, False otherwise
    """
    if model is None:
        return False

    status = LpStatus[model.status]
    return status == "Optimal"


def get_solver_status(model: LpProblem) -> Dict[str, Any]:
    """Get detailed solver status information.

    Args:
        model: The solved LP model

    Returns:
        Dictionary with solver status details
    """
    if model is None:
        return {
            "status": "No Model",
            "is_optimal": False,
            "message": "Model has not been created"
        }

    status_name = LpStatus[model.status]
    is_optimal = status_name == "Optimal"

    status_messages = {
        "Optimal": "Optimal solution found",
        "Not Solved": "Problem not yet solved",
        "Infeasible": "Problem is infeasible - no solution exists",
        "Unbounded": "Problem is unbounded",
        "Undefined": "Solution status is undefined",
    }

    return {
        "status": status_name,
        "is_optimal": is_optimal,
        "message": status_messages.get(status_name, "Unknown status"),
        "objective_value": model.objective.value() if is_optimal else None,
    }


def format_currency(value: float, decimals: int = 2) -> str:
    """Format a numeric value as currency.

    Args:
        value: The numeric value to format
        decimals: Number of decimal places

    Returns:
        Formatted currency string
    """
    return f"${value:,.{decimals}f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format a numeric value as percentage.

    Args:
        value: The numeric value (0-1 range) to format
        decimals: Number of decimal places

    Returns:
        Formatted percentage string
    """
    return f"{value * 100:.{decimals}f}%"


def export_solution_to_dict(
    model: LpProblem,
    variable_names: Optional[Dict] = None
) -> Dict[str, Any]:
    """Export LP solution to a dictionary format.

    Args:
        model: The solved LP model
        variable_names: Optional mapping of variable names to display names

    Returns:
        Dictionary containing solution details
    """
    if not validate_solution(model):
        return {"error": "Model does not have an optimal solution"}

    solution = {
        "status": LpStatus[model.status],
        "objective_value": model.objective.value(),
        "variables": {},
        "constraints": {},
    }

    # Extract variable values
    for var in model.variables():
        var_name = var.name
        display_name = variable_names.get(var_name, var_name) if variable_names else var_name
        solution["variables"][display_name] = var.value()

    # Extract constraint slack/surplus
    for name, constraint in model.constraints.items():
        solution["constraints"][name] = {
            "slack": constraint.slack,
            "pi": constraint.pi,  # Shadow price/dual value
        }

    return solution
