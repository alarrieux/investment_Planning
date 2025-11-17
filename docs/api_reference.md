# API Reference

Complete API documentation for the Investment Planning Optimization package.

## Table of Contents

- [Models](#models)
  - [BankLoanOptimizer](#bankloanoptimizer)
  - [ProductionInventoryOptimizer](#productioninventoryoptimizer)
  - [OilRefiningOptimizer](#oilrefiningoptimizer)
- [Utilities](#utilities)
  - [Solver Utils](#solver-utils)
  - [Validation](#validation)
- [Visualization](#visualization)
  - [Plot Utils](#plot-utils)

---

## Models

### BankLoanOptimizer

Optimize bank loan portfolio allocation across multiple loan types.

#### Class Definition

```python
class BankLoanOptimizer(
    total_funds: float = 12_000_000,
    interest_rates: Optional[List[float]] = None,
    bad_debt_ratios: Optional[List[float]] = None,
    loan_types: Optional[List[str]] = None
)
```

#### Parameters

- **total_funds** (float): Total funds available for lending. Default: 12,000,000
- **interest_rates** (List[float], optional): Interest rates for each loan type. Default: [0.14, 0.13, 0.12, 0.125, 0.10]
- **bad_debt_ratios** (List[float], optional): Bad debt ratios for each loan type. Default: [0.10, 0.07, 0.03, 0.05, 0.02]
- **loan_types** (List[str], optional): Names of loan types. Default: ["Personal", "Car", "Home", "Farm", "Commercial"]

#### Methods

##### `build_model() -> LpProblem`

Build the linear programming model.

**Returns:**
- LpProblem: The constructed LP model

**Example:**
```python
optimizer = BankLoanOptimizer()
model = optimizer.build_model()
```

##### `solve() -> Dict`

Solve the optimization problem.

**Returns:**
- Dict: Dictionary containing:
  - `status` (str): Solution status ("Optimal", "Infeasible", etc.)
  - `allocations` (Dict[str, float]): Allocation amounts by loan type
  - `total_allocated` (float): Total funds allocated
  - `net_return` (float): Net return in dollars
  - `roi_percentage` (float): Return on investment percentage

**Example:**
```python
solution = optimizer.solve()
print(f"Net Return: ${solution['net_return']:,.2f}")
```

##### `print_summary()`

Print a formatted summary of the solution.

**Example:**
```python
optimizer.print_summary()
```

---

### ProductionInventoryOptimizer

Optimize production and inventory levels across multiple time periods.

#### Class Definition

```python
class ProductionInventoryOptimizer(
    production_costs: Optional[List[float]] = None,
    storage_cost: float = 8.0,
    demands: Optional[List[int]] = None
)
```

#### Parameters

- **production_costs** (List[float], optional): Production cost per unit for each period. Default: [50, 45, 55, 48, 52, 50]
- **storage_cost** (float): Storage cost per unit per period. Default: 8.0
- **demands** (List[int], optional): Demand requirements for each period. Default: [100, 250, 190, 140, 220, 110]

#### Methods

##### `build_model() -> LpProblem`

Build the linear programming model.

**Returns:**
- LpProblem: The constructed LP model

##### `solve() -> Dict`

Solve the optimization problem.

**Returns:**
- Dict: Dictionary containing:
  - `status` (str): Solution status
  - `production_schedule` (List[float]): Production quantities by period
  - `inventory_schedule` (List[float]): Ending inventory by period
  - `total_cost` (float): Total cost (production + storage)
  - `production_cost` (float): Total production cost
  - `storage_cost` (float): Total storage cost

**Example:**
```python
optimizer = ProductionInventoryOptimizer()
solution = optimizer.solve()

for period, production in enumerate(solution['production_schedule'], 1):
    print(f"Period {period}: Produce {production:.0f} units")
```

##### `print_summary()`

Print a formatted summary of the solution.

---

### OilRefiningOptimizer

Optimize crude oil refining and gasoline blending operations.

#### Class Definition

```python
class OilRefiningOptimizer(
    crude_capacity: float = 1_500_000,
    cracker_capacity: float = 200_000,
    octane_numbers: Optional[Dict] = None,
    demand_limits: Optional[Dict] = None,
    profit_margins: Optional[Dict] = None
)
```

#### Parameters

- **crude_capacity** (float): Crude oil processing capacity (barrels/day). Default: 1,500,000
- **cracker_capacity** (float): Cracker unit capacity (barrels/day). Default: 200,000
- **octane_numbers** (Dict, optional): Octane numbers for feedstock, cracker, and products
- **demand_limits** (Dict, optional): Maximum demand for each gasoline type
- **profit_margins** (Dict, optional): Profit per barrel for each gasoline type

#### Methods

##### `build_model() -> LpProblem`

Build the linear programming model.

**Returns:**
- LpProblem: The constructed LP model

##### `solve() -> Dict`

Solve the optimization problem.

**Returns:**
- Dict: Dictionary containing:
  - `status` (str): Solution status
  - `production` (Dict): Production amounts by product and source
  - `total_profit` (float): Total daily profit
  - `daily_profit` (float): Daily profit (same as total_profit)

**Example:**
```python
optimizer = OilRefiningOptimizer()
solution = optimizer.solve()

for product in ['regular', 'premium', 'super']:
    total = solution['production'][product]['total']
    print(f"{product.capitalize()}: {total:,.0f} bbl/day")
```

##### `print_summary()`

Print a formatted summary of the solution.

---

## Utilities

### Solver Utils

Utility functions for LP solver operations.

#### Functions

##### `validate_solution(model: LpProblem) -> bool`

Validate that an LP solution is optimal.

**Parameters:**
- **model** (LpProblem): The solved LP model

**Returns:**
- bool: True if solution is optimal, False otherwise

**Example:**
```python
from src.utils.solver_utils import validate_solution

is_optimal = validate_solution(model)
if is_optimal:
    print("Solution is optimal!")
```

##### `get_solver_status(model: LpProblem) -> Dict[str, Any]`

Get detailed solver status information.

**Parameters:**
- **model** (LpProblem): The solved LP model

**Returns:**
- Dict: Dictionary with status details including:
  - `status` (str): Status name
  - `is_optimal` (bool): Whether solution is optimal
  - `message` (str): Human-readable status message
  - `objective_value` (float): Objective function value if optimal

##### `format_currency(value: float, decimals: int = 2) -> str`

Format a numeric value as currency.

**Parameters:**
- **value** (float): The numeric value to format
- **decimals** (int): Number of decimal places. Default: 2

**Returns:**
- str: Formatted currency string

**Example:**
```python
print(format_currency(1234567.89))  # Output: "$1,234,567.89"
```

##### `format_percentage(value: float, decimals: int = 2) -> str`

Format a numeric value as percentage.

**Parameters:**
- **value** (float): The numeric value (0-1 range) to format
- **decimals** (int): Number of decimal places. Default: 2

**Returns:**
- str: Formatted percentage string

**Example:**
```python
print(format_percentage(0.0834))  # Output: "8.34%"
```

---

### Validation

Input validation and constraint checking utilities.

#### Functions

##### `validate_inputs(values: List[float], min_value: float = 0, max_value: float = float('inf'), name: str = "values") -> Tuple[bool, str]`

Validate input values are within acceptable ranges.

**Parameters:**
- **values** (List[float]): List of values to validate
- **min_value** (float): Minimum acceptable value. Default: 0
- **max_value** (float): Maximum acceptable value. Default: infinity
- **name** (str): Name of the parameter being validated. Default: "values"

**Returns:**
- Tuple[bool, str]: (is_valid, error_message)

**Example:**
```python
from src.utils.validation import validate_inputs

is_valid, error = validate_inputs([0.1, 0.2, 0.3], min_value=0, max_value=1)
if not is_valid:
    print(f"Validation error: {error}")
```

##### `validate_positive(values: List[float], name: str = "values") -> Tuple[bool, str]`

Validate that all values are positive.

##### `validate_percentage(values: List[float], name: str = "percentages") -> Tuple[bool, str]`

Validate that all values are valid percentages (0-1).

##### `check_constraints(solution: Dict[str, Any], constraints: Dict[str, callable]) -> Dict[str, bool]`

Check if a solution satisfies given constraints.

**Parameters:**
- **solution** (Dict): Dictionary containing solution values
- **constraints** (Dict[str, callable]): Dictionary mapping constraint names to validation functions

**Returns:**
- Dict[str, bool]: Dictionary mapping constraint names to satisfaction status

---

## Visualization

### Plot Utils

Plotting utilities for visualization of optimization results.

#### Functions

##### `plot_allocation(allocations: Dict[str, float], title: str = "Resource Allocation", xlabel: str = "Category", ylabel: str = "Amount ($)", save_path: Optional[str] = None) -> plt.Figure`

Create a bar plot of resource allocations.

**Parameters:**
- **allocations** (Dict[str, float]): Dictionary mapping categories to allocated amounts
- **title** (str): Plot title
- **xlabel** (str): X-axis label
- **ylabel** (str): Y-axis label
- **save_path** (Optional[str]): Optional path to save the figure

**Returns:**
- plt.Figure: matplotlib Figure object

**Example:**
```python
from src.visualization.plot_utils import plot_allocation

allocations = {"Home": 7200000, "Commercial": 4800000}
fig = plot_allocation(allocations, title="Loan Allocation")
fig.savefig("allocation.png")
```

##### `plot_production_schedule(periods: List[int], production: List[float], demand: List[float], inventory: List[float], title: str = "Production and Inventory Schedule", save_path: Optional[str] = None) -> plt.Figure`

Create a multi-line plot showing production, demand, and inventory.

**Parameters:**
- **periods** (List[int]): List of time periods
- **production** (List[float]): Production amounts for each period
- **demand** (List[float]): Demand amounts for each period
- **inventory** (List[float]): Inventory levels for each period
- **title** (str): Plot title
- **save_path** (Optional[str]): Optional path to save the figure

**Returns:**
- plt.Figure: matplotlib Figure object

##### `plot_comparison(categories: List[str], values_dict: Dict[str, List[float]], title: str = "Comparison", ylabel: str = "Value", save_path: Optional[str] = None) -> plt.Figure`

Create a grouped bar plot for comparing multiple series.

##### `plot_sensitivity_analysis(parameter_values: List[float], objective_values: List[float], parameter_name: str = "Parameter", title: str = "Sensitivity Analysis", save_path: Optional[str] = None) -> plt.Figure`

Create a sensitivity analysis plot.

##### `plot_pie_chart(allocations: Dict[str, float], title: str = "Allocation Distribution", save_path: Optional[str] = None) -> plt.Figure`

Create a pie chart of allocations.

##### `create_dashboard(allocations: Dict[str, float], production_data: Optional[Dict] = None, title: str = "Optimization Dashboard", save_path: Optional[str] = None) -> plt.Figure`

Create a comprehensive dashboard with multiple plots.

---

## Examples

### Complete Example

```python
from src.models.bank_loan import BankLoanOptimizer
from src.visualization.plot_utils import plot_allocation
from src.utils.solver_utils import validate_solution

# Create and solve optimization problem
optimizer = BankLoanOptimizer(
    total_funds=15_000_000,
    interest_rates=[0.15, 0.14, 0.13, 0.12, 0.11]
)

solution = optimizer.solve()

# Validate solution
if validate_solution(optimizer.model):
    print("Solution is optimal!")
    optimizer.print_summary()

    # Visualize results
    fig = plot_allocation(solution['allocations'])
    fig.savefig("results.png")
```

---

*For more examples, see the `examples/` directory in the repository.*
