# Investment Planning Optimization

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![R 4.0+](https://img.shields.io/badge/R-4.0+-276DC3.svg)](https://www.r-project.org/)

## Description

A comprehensive suite of **Linear Programming (LP) optimization models** designed for investment planning and financial decision-making. This repository demonstrates how LP techniques can be applied across various investment scenarios to maximize returns, minimize costs, and optimize resource allocation.

Numerous opportunities are available to today's investor. In many of these situations, Linear Programming can be used to select the optimal mix of opportunities that will maximize returns while satisfying various business constraints. This repository provides practical, real-world examples from banking, manufacturing, and petroleum refining industries.

## Features

- **Multiple Optimization Models**:
  - Bank Loan Portfolio Optimization
  - Multi-Period Production-Inventory Planning
  - Crude Oil Refining and Gasoline Blending

- **Dual Language Support**: Implementation in both R and Python
- **Interactive Jupyter Notebooks**: Step-by-step walkthroughs with explanations
- **Visualization Tools**: Graphical representation of optimal solutions
- **Extensible Framework**: Easy to adapt for custom scenarios
- **Comprehensive Testing**: Unit tests for all optimization functions

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Models](#models)
- [Project Structure](#project-structure)
- [Usage Examples](#usage-examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [References](#references)

## Installation

### Prerequisites

- Python 3.8 or higher
- R 4.0 or higher (for R notebooks)
- Git

### Option 1: Using Conda (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/investment_Planning.git
cd investment_Planning

# Create conda environment
conda env create -f environment.yml

# Activate the environment
conda activate investment_planning
```

### Option 2: Using pip

```bash
# Clone the repository
git clone https://github.com/yourusername/investment_Planning.git
cd investment_Planning

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Option 3: Development Installation

```bash
# For development with editable install
pip install -e ".[dev]"
```

### R Dependencies

If using R notebooks, install the required packages:

```r
install.packages(c("lpSolve", "ggplot2", "dplyr", "tidyr"))
```

## Quick Start

### Python Example

```python
from models.bank_loan import BankLoanOptimizer

# Initialize the optimizer
optimizer = BankLoanOptimizer(
    total_funds=12_000_000,
    interest_rates=[0.14, 0.13, 0.12, 0.125, 0.10],
    bad_debt_ratios=[0.10, 0.07, 0.03, 0.05, 0.02]
)

# Solve the optimization problem
solution = optimizer.solve()

# Display results
solution.print_summary()
solution.visualize()
```

### R Example

```r
# Load the package
library(lpSolve)

# Source the utility functions
source("src/utils/optimization_utils.R")

# Run bank loan optimization
result <- optimize_bank_loans(
  total_funds = 12e6,
  interest_rates = c(0.14, 0.13, 0.12, 0.125, 0.10),
  bad_debt_ratios = c(0.10, 0.07, 0.03, 0.05, 0.02)
)

# View results
print(result)
```

## Models

### 1. Bank Loan Portfolio Optimization

**Problem**: A bank needs to allocate $12 million across five loan types (Personal, Car, Home, Farm, Commercial) to maximize net returns while managing risk and meeting regulatory requirements.

**Key Constraints**:
- Total funds limit: $12 million
- Farm + Commercial loans ≥ 40% of total
- Home loans ≥ 50% of (Personal + Car + Home)
- Bad debt ratio ≤ 4% overall

**Objective**: Maximize (Interest Revenue - Bad Debt Losses)

### 2. Multi-Period Production-Inventory Model

**Problem**: ACME Manufacturing must deliver specific quantities of windows over 6 months. Production costs vary by month, and holding inventory incurs storage costs.

**Key Features**:
- Variable production costs by period
- Storage cost: $8 per unit per month
- Demand must be met each period
- Opportunity to leverage cost fluctuations

**Objective**: Minimize (Total Production Cost + Total Storage Cost)

### 3. Crude Oil Refining & Gasoline Blending

**Problem**: ABC Oil refinery must determine optimal production mix for three gasoline types (Regular, Premium, Super) with different octane numbers.

**Key Constraints**:
- Crude oil capacity: 1.5 million barrels/day
- Cracker unit capacity: 200,000 barrels/day
- Octane number requirements
- Demand limits for each product

**Objective**: Maximize Total Profit

## Project Structure

```
investment_Planning/
├── README.md                 # This file
├── LICENSE                   # MIT License
├── requirements.txt          # Python dependencies
├── environment.yml           # Conda environment specification
├── setup.py                  # Package installation script
├── .gitignore               # Git ignore rules
│
├── notebooks/               # Jupyter notebooks
│   ├── Investment_Planning_Optimization.ipynb  # Main R notebook
│   ├── Python_Bank_Loan_Model.ipynb
│   ├── Python_Production_Inventory.ipynb
│   └── Python_Oil_Refining.ipynb
│
├── src/                     # Source code
│   ├── __init__.py
│   ├── models/             # Optimization model implementations
│   │   ├── __init__.py
│   │   ├── bank_loan.py
│   │   ├── production_inventory.py
│   │   └── oil_refining.py
│   ├── utils/              # Utility functions
│   │   ├── __init__.py
│   │   ├── solver_utils.py
│   │   └── validation.py
│   └── visualization/      # Plotting and visualization
│       ├── __init__.py
│       └── plot_utils.py
│
├── data/                   # Data files
│   ├── raw/               # Raw input data
│   └── processed/         # Processed results
│
├── tests/                 # Unit tests
│   ├── __init__.py
│   ├── test_bank_loan.py
│   ├── test_production_inventory.py
│   └── test_oil_refining.py
│
├── examples/              # Example scripts
│   ├── run_bank_loan.py
│   ├── run_production.py
│   └── run_refining.py
│
└── docs/                  # Documentation
    ├── mathematical_formulations.md
    ├── api_reference.md
    └── tutorials/
```

## Usage Examples

### Running Jupyter Notebooks

```bash
# Start Jupyter
jupyter notebook

# Navigate to notebooks/ and open desired notebook
```

### Running Example Scripts

```bash
# Bank loan optimization
python examples/run_bank_loan.py

# Production-inventory planning
python examples/run_production.py

# Oil refining optimization
python examples/run_refining.py
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_bank_loan.py
```

## Documentation

Detailed documentation is available in the `docs/` directory:

- **[Mathematical Formulations](docs/mathematical_formulations.md)**: Complete LP formulations for all models
- **[API Reference](docs/api_reference.md)**: Function and class documentation
- **[Tutorials](docs/tutorials/)**: Step-by-step guides

### Building Documentation

```bash
cd docs
sphinx-build -b html . _build
```

## Key Insights

### Bank Loan Model Results

The optimal solution allocates:
- **$7.2M to Home Loans** (60%)
- **$4.8M to Commercial Loans** (40%)
- **$0 to Personal, Car, and Farm Loans**

This yields a **net return of 8.34%**, which is slightly less than the best individual rate (8.64% for home loans) due to the constraint requiring 40% allocation to farm and commercial loans.

### Production-Inventory Insights

The model recommends **overproduction in Month 2** (440 units vs 250 needed) to take advantage of lower production costs ($45/unit) and carry over 190 units to Month 3 when production costs are higher ($55/unit).

**Key Learning**: Strategic inventory buildup can reduce total costs when production costs fluctuate significantly.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone and install in development mode
git clone https://github.com/yourusername/investment_Planning.git
cd investment_Planning
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests before committing
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

- Taha, Hamdy A. *Operations Research: An Introduction* (10th Edition). Pearson, 2017.
- Winston, Wayne L. *Operations Research: Applications and Algorithms*. Brooks/Cole, 2003.
- Hillier, Frederick S., and Gerald J. Lieberman. *Introduction to Operations Research*. McGraw-Hill, 2015.

## Citation

If you use this code in your research or projects, please cite:

```bibtex
@software{investment_planning_optimization,
  title = {Investment Planning Optimization: Linear Programming Models},
  author = {Your Name},
  year = {2024},
  url = {https://github.com/yourusername/investment_Planning}
}
```

## Acknowledgments

- Based on examples from Taha's *Operations Research* textbook
- Built using the excellent `lpSolve` (R) and `PuLP` (Python) libraries
- Thanks to the open-source optimization community

## Contact

- **Author**: Your Name
- **Email**: your.email@example.com
- **GitHub**: [@yourusername](https://github.com/yourusername)

## Support

If you found this project helpful, please consider:
- Starring the repository ⭐
- Reporting issues or requesting features
- Contributing improvements
- Sharing with others who might benefit

---

**Made with ❤️ for the Operations Research and Optimization community**
