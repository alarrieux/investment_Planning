"""Plotting utilities for visualization of optimization results."""

from typing import Dict, List, Optional, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set default style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def plot_allocation(
    allocations: Dict[str, float],
    title: str = "Resource Allocation",
    xlabel: str = "Category",
    ylabel: str = "Amount ($)",
    save_path: Optional[str] = None
) -> plt.Figure:
    """Create a bar plot of resource allocations.

    Args:
        allocations: Dictionary mapping categories to allocated amounts
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        save_path: Optional path to save the figure

    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    categories = list(allocations.keys())
    values = list(allocations.values())

    # Create color palette
    colors = sns.color_palette("husl", len(categories))

    bars = ax.bar(categories, values, color=colors, edgecolor='black', linewidth=1.2)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${height:,.0f}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig


def plot_production_schedule(
    periods: List[int],
    production: List[float],
    demand: List[float],
    inventory: List[float],
    title: str = "Production and Inventory Schedule",
    save_path: Optional[str] = None
) -> plt.Figure:
    """Create a multi-line plot showing production, demand, and inventory.

    Args:
        periods: List of time periods
        production: Production amounts for each period
        demand: Demand amounts for each period
        inventory: Inventory levels for each period
        title: Plot title
        save_path: Optional path to save the figure

    Returns:
        matplotlib Figure object
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # Plot 1: Production and Demand
    ax1.plot(periods, production, 'o-', label='Production', linewidth=2, markersize=8, color='#2ecc71')
    ax1.plot(periods, demand, 's-', label='Demand', linewidth=2, markersize=8, color='#e74c3c')
    ax1.fill_between(periods, production, alpha=0.3, color='#2ecc71')
    ax1.fill_between(periods, demand, alpha=0.3, color='#e74c3c')

    ax1.set_ylabel('Units', fontsize=12, fontweight='bold')
    ax1.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax1.legend(loc='upper left', fontsize=11, framealpha=0.9)
    ax1.grid(True, alpha=0.3)

    # Plot 2: Inventory Levels
    ax2.bar(periods, inventory, color='#3498db', alpha=0.7, edgecolor='black', linewidth=1.2)
    ax2.set_xlabel('Period', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Inventory (Units)', fontsize=12, fontweight='bold')
    ax2.set_title('Ending Inventory Levels', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    # Add value labels on inventory bars
    for i, (period, inv) in enumerate(zip(periods, inventory)):
        if inv > 0:
            ax2.text(period, inv, f'{inv:.0f}', ha='center', va='bottom', fontsize=9)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig


def plot_inventory_levels(
    periods: List[int],
    inventory: List[float],
    title: str = "Inventory Levels Over Time",
    save_path: Optional[str] = None
) -> plt.Figure:
    """Create a line plot of inventory levels.

    Args:
        periods: List of time periods
        inventory: Inventory levels for each period
        title: Plot title
        save_path: Optional path to save the figure

    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(periods, inventory, 'o-', linewidth=2, markersize=10, color='#3498db')
    ax.fill_between(periods, inventory, alpha=0.3, color='#3498db')

    # Add value labels
    for period, inv in zip(periods, inventory):
        ax.text(period, inv + max(inventory)*0.02, f'{inv:.0f}',
               ha='center', va='bottom', fontsize=10)

    ax.set_xlabel('Period', fontsize=12, fontweight='bold')
    ax.set_ylabel('Inventory (Units)', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig


def plot_comparison(
    categories: List[str],
    values_dict: Dict[str, List[float]],
    title: str = "Comparison",
    ylabel: str = "Value",
    save_path: Optional[str] = None
) -> plt.Figure:
    """Create a grouped bar plot for comparing multiple series.

    Args:
        categories: List of category names
        values_dict: Dictionary mapping series names to value lists
        title: Plot title
        ylabel: Y-axis label
        save_path: Optional path to save the figure

    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    x = np.arange(len(categories))
    width = 0.8 / len(values_dict)

    colors = sns.color_palette("husl", len(values_dict))

    for i, (name, values) in enumerate(values_dict.items()):
        offset = width * i - (width * len(values_dict) / 2 - width / 2)
        bars = ax.bar(x + offset, values, width, label=name, color=colors[i],
                     edgecolor='black', linewidth=0.8)

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.0f}',
                       ha='center', va='bottom', fontsize=8)

    ax.set_xlabel('Category', fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.legend(loc='upper left', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig


def plot_sensitivity_analysis(
    parameter_values: List[float],
    objective_values: List[float],
    parameter_name: str = "Parameter",
    title: str = "Sensitivity Analysis",
    save_path: Optional[str] = None
) -> plt.Figure:
    """Create a sensitivity analysis plot.

    Args:
        parameter_values: List of parameter values tested
        objective_values: Corresponding objective function values
        parameter_name: Name of the parameter being varied
        title: Plot title
        save_path: Optional path to save the figure

    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(parameter_values, objective_values, 'o-', linewidth=2,
           markersize=8, color='#e74c3c')
    ax.fill_between(parameter_values, objective_values, alpha=0.3, color='#e74c3c')

    # Mark the optimal point
    optimal_idx = np.argmax(objective_values)
    ax.plot(parameter_values[optimal_idx], objective_values[optimal_idx],
           'g*', markersize=20, label='Optimal')

    ax.set_xlabel(parameter_name, fontsize=12, fontweight='bold')
    ax.set_ylabel('Objective Value', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='best', fontsize=11, framealpha=0.9)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig


def plot_pie_chart(
    allocations: Dict[str, float],
    title: str = "Allocation Distribution",
    save_path: Optional[str] = None
) -> plt.Figure:
    """Create a pie chart of allocations.

    Args:
        allocations: Dictionary mapping categories to values
        title: Plot title
        save_path: Optional path to save the figure

    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Filter out zero allocations
    filtered_allocations = {k: v for k, v in allocations.items() if v > 0}

    categories = list(filtered_allocations.keys())
    values = list(filtered_allocations.values())

    colors = sns.color_palette("husl", len(categories))

    wedges, texts, autotexts = ax.pie(
        values,
        labels=categories,
        autopct=lambda pct: f'{pct:.1f}%\n(${pct/100*sum(values):,.0f})',
        colors=colors,
        startangle=90,
        textprops={'fontsize': 10, 'fontweight': 'bold'}
    )

    # Enhance text visibility
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(9)

    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig


def create_dashboard(
    allocations: Dict[str, float],
    production_data: Optional[Dict] = None,
    title: str = "Optimization Dashboard",
    save_path: Optional[str] = None
) -> plt.Figure:
    """Create a comprehensive dashboard with multiple plots.

    Args:
        allocations: Resource allocation data
        production_data: Optional production schedule data
        title: Dashboard title
        save_path: Optional path to save the figure

    Returns:
        matplotlib Figure object
    """
    if production_data:
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    else:
        fig = plt.figure(figsize=(16, 6))
        gs = fig.add_gridspec(1, 2, hspace=0.3, wspace=0.3)

    fig.suptitle(title, fontsize=16, fontweight='bold', y=0.98)

    # Plot 1: Bar chart
    ax1 = fig.add_subplot(gs[0, 0])
    categories = list(allocations.keys())
    values = list(allocations.values())
    colors = sns.color_palette("husl", len(categories))
    bars = ax1.bar(categories, values, color=colors, edgecolor='black', linewidth=1.2)
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:,.0f}', ha='center', va='bottom', fontsize=9)
    ax1.set_title('Allocation by Category', fontweight='bold')
    ax1.set_ylabel('Amount ($)')
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # Plot 2: Pie chart
    ax2 = fig.add_subplot(gs[0, 1])
    filtered_allocations = {k: v for k, v in allocations.items() if v > 0}
    wedges, texts, autotexts = ax2.pie(
        list(filtered_allocations.values()),
        labels=list(filtered_allocations.keys()),
        autopct='%1.1f%%',
        colors=sns.color_palette("husl", len(filtered_allocations)),
        startangle=90
    )
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    ax2.set_title('Distribution', fontweight='bold')

    if production_data:
        # Plot 3: Production schedule
        ax3 = fig.add_subplot(gs[1, :])
        periods = production_data.get('periods', [])
        production = production_data.get('production', [])
        demand = production_data.get('demand', [])

        ax3.plot(periods, production, 'o-', label='Production', linewidth=2, markersize=8)
        ax3.plot(periods, demand, 's-', label='Demand', linewidth=2, markersize=8)
        ax3.fill_between(periods, production, alpha=0.3)
        ax3.set_xlabel('Period')
        ax3.set_ylabel('Units')
        ax3.set_title('Production Schedule', fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig
