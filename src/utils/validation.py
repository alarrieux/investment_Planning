"""Input validation and constraint checking utilities."""

from typing import List, Dict, Any, Tuple
import numpy as np


def validate_inputs(
    values: List[float],
    min_value: float = 0,
    max_value: float = float('inf'),
    name: str = "values"
) -> Tuple[bool, str]:
    """Validate input values are within acceptable ranges.

    Args:
        values: List of values to validate
        min_value: Minimum acceptable value
        max_value: Maximum acceptable value
        name: Name of the parameter being validated

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not values:
        return False, f"{name} cannot be empty"

    if not all(isinstance(v, (int, float)) for v in values):
        return False, f"{name} must contain only numeric values"

    if not all(min_value <= v <= max_value for v in values):
        return False, f"All {name} must be between {min_value} and {max_value}"

    return True, ""


def validate_positive(values: List[float], name: str = "values") -> Tuple[bool, str]:
    """Validate that all values are positive.

    Args:
        values: List of values to validate
        name: Name of the parameter

    Returns:
        Tuple of (is_valid, error_message)
    """
    return validate_inputs(values, min_value=0, name=name)


def validate_percentage(values: List[float], name: str = "percentages") -> Tuple[bool, str]:
    """Validate that all values are valid percentages (0-1).

    Args:
        values: List of values to validate
        name: Name of the parameter

    Returns:
        Tuple of (is_valid, error_message)
    """
    return validate_inputs(values, min_value=0, max_value=1, name=name)


def validate_equal_length(
    *lists: List,
    names: List[str] = None
) -> Tuple[bool, str]:
    """Validate that all lists have equal length.

    Args:
        *lists: Variable number of lists to validate
        names: Optional names for the lists

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not lists:
        return True, ""

    lengths = [len(lst) for lst in lists]
    if len(set(lengths)) != 1:
        if names and len(names) == len(lists):
            length_info = ", ".join([f"{name}={len(lst)}" for name, lst in zip(names, lists)])
            return False, f"All lists must have equal length: {length_info}"
        return False, f"All lists must have equal length, got lengths: {lengths}"

    return True, ""


def check_constraints(
    solution: Dict[str, Any],
    constraints: Dict[str, callable]
) -> Dict[str, bool]:
    """Check if a solution satisfies given constraints.

    Args:
        solution: Dictionary containing solution values
        constraints: Dictionary mapping constraint names to validation functions

    Returns:
        Dictionary mapping constraint names to satisfaction status
    """
    results = {}

    for name, constraint_func in constraints.items():
        try:
            results[name] = constraint_func(solution)
        except Exception as e:
            results[name] = False
            print(f"Error checking constraint '{name}': {e}")

    return results


def calculate_constraint_violations(
    actual_value: float,
    required_value: float,
    constraint_type: str = "<=",
    tolerance: float = 1e-6
) -> Tuple[bool, float]:
    """Calculate constraint violation amount.

    Args:
        actual_value: Actual value in solution
        required_value: Required value from constraint
        constraint_type: Type of constraint ('<=', '>=', '==')
        tolerance: Numerical tolerance for equality

    Returns:
        Tuple of (is_satisfied, violation_amount)
    """
    if constraint_type == "<=":
        satisfied = actual_value <= required_value + tolerance
        violation = max(0, actual_value - required_value)
    elif constraint_type == ">=":
        satisfied = actual_value >= required_value - tolerance
        violation = max(0, required_value - actual_value)
    elif constraint_type == "==":
        satisfied = abs(actual_value - required_value) <= tolerance
        violation = abs(actual_value - required_value)
    else:
        raise ValueError(f"Unknown constraint type: {constraint_type}")

    return satisfied, violation


def validate_model_inputs(
    **kwargs
) -> Tuple[bool, List[str]]:
    """Comprehensive validation of model inputs.

    Args:
        **kwargs: Keyword arguments containing model parameters

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Validate each parameter type
    for param_name, param_value in kwargs.items():
        if param_value is None:
            continue

        if isinstance(param_value, (list, tuple)):
            if len(param_value) == 0:
                errors.append(f"{param_name} cannot be empty")
            elif not all(isinstance(v, (int, float)) for v in param_value):
                errors.append(f"{param_name} must contain only numeric values")
        elif isinstance(param_value, (int, float)):
            if param_value < 0:
                errors.append(f"{param_name} must be non-negative")
        elif isinstance(param_value, dict):
            if len(param_value) == 0:
                errors.append(f"{param_name} cannot be empty")

    is_valid = len(errors) == 0
    return is_valid, errors
