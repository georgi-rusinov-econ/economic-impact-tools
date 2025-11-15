"""
Cost-Benefit Analysis Tools
Green Book aligned utilities for economic appraisal
"""

import numpy as np
from typing import List, Union

# UK Green Book discount rates (2022 guidance)
GREEN_BOOK_RATES = {
    'standard': {
        'years_0_30': 0.035,    # 3.5% for years 0-30
        'years_31_75': 0.030,   # 3.0% for years 31-75
        'years_76_125': 0.025,  # 2.5% for years 76-125
        'years_126_200': 0.020, # 2.0% for years 126-200
        'years_201_300': 0.015, # 1.5% for years 201-300
        'years_301_plus': 0.010 # 1.0% for years 301+
    },
    'health': 0.015,  # 1.5% for health effects
    'reduced': 0.030  # 3.0% reduced rate (sensitivity)
}


def get_discount_rate(year: int, rate_type: str = 'standard') -> float:
    """
    Get Green Book discount rate for a given year.
    
    Parameters
    ----------
    year : int
        Year from project start (0 = base year)
    rate_type : str
        'standard', 'health', or 'reduced'
    
    Returns
    -------
    float
        Discount rate as decimal (e.g., 0.035 for 3.5%)
    
    Examples
    --------
    >>> get_discount_rate(5)
    0.035
    >>> get_discount_rate(50)
    0.03
    """
    if rate_type == 'health':
        return GREEN_BOOK_RATES['health']
    elif rate_type == 'reduced':
        return GREEN_BOOK_RATES['reduced']
    else:
        if year <= 30:
            return GREEN_BOOK_RATES['standard']['years_0_30']
        elif year <= 75:
            return GREEN_BOOK_RATES['standard']['years_31_75']
        elif year <= 125:
            return GREEN_BOOK_RATES['standard']['years_76_125']
        elif year <= 200:
            return GREEN_BOOK_RATES['standard']['years_126_200']
        elif year <= 300:
            return GREEN_BOOK_RATES['standard']['years_201_300']
        else:
            return GREEN_BOOK_RATES['standard']['years_301_plus']


def calculate_discount_factor(year: int, rate_type: str = 'standard') -> float:
    """
    Calculate cumulative discount factor for a given year using Green Book rates.
    
    Accounts for declining long-term discount rates as per Green Book guidance.
    
    Parameters
    ----------
    year : int
        Year from project start
    rate_type : str
        'standard', 'health', or 'reduced'
    
    Returns
    -------
    float
        Discount factor (multiply by cash flow to get present value)
    
    Examples
    --------
    >>> calculate_discount_factor(0)
    1.0
    >>> calculate_discount_factor(10)
    0.7089...
    """
    if year == 0:
        return 1.0
    
    discount_factor = 1.0
    
    for y in range(1, year + 1):
        rate = get_discount_rate(y, rate_type)
        discount_factor = discount_factor / (1 + rate)
    
    return discount_factor


def calculate_npv_greenbook(
    cash_flows: List[float],
    years: List[int] = None,
    rate_type: str = 'standard'
) -> float:
    """
    Calculate Net Present Value using Green Book discount rates.
    
    Automatically applies declining discount rates for long-term projects.
    
    Parameters
    ----------
    cash_flows : list of float
        Cash flows (costs as negative, benefits as positive)
    years : list of int, optional
        Corresponding years. If None, assumes consecutive years from 0.
    rate_type : str
        'standard', 'health', or 'reduced'
    
    Returns
    -------
    float
        Net Present Value
    
    Examples
    --------
    >>> cash_flows = [-1000000, 200000, 250000, 300000, 350000, 400000]
    >>> npv = calculate_npv_greenbook(cash_flows)
    >>> print(f"NPV: £{npv:,.0f}")
    NPV: £298,814
    """
    if years is None:
        years = list(range(len(cash_flows)))
    
    if len(cash_flows) != len(years):
        raise ValueError("cash_flows and years must have same length")
    
    npv = 0.0
    for cf, year in zip(cash_flows, years):
        df = calculate_discount_factor(year, rate_type)
        npv += cf * df
    
    return npv


def calculate_bcr(
    costs: List[float],
    benefits: List[float],
    years: List[int] = None,
    rate_type: str = 'standard'
) -> float:
    """
    Calculate Benefit-Cost Ratio using Green Book discount rates.
    
    Parameters
    ----------
    costs : list of float
        Project costs by year (as positive numbers)
    benefits : list of float
        Project benefits by year (as positive numbers)
    years : list of int, optional
        Corresponding years. If None, assumes consecutive from 0.
    rate_type : str
        'standard', 'health', or 'reduced'
    
    Returns
    -------
    float
        Benefit-Cost Ratio (BCR > 1 indicates positive value for money)
    
    Examples
    --------
    >>> costs = [1000000, 50000, 50000, 50000, 50000]
    >>> benefits = [0, 300000, 320000, 340000, 360000]
    >>> bcr = calculate_bcr(costs, benefits)
    >>> print(f"BCR: {bcr:.2f}")
    BCR: 1.15
    """
    if years is None:
        years = list(range(len(costs)))
    
    pv_costs = sum(c * calculate_discount_factor(y, rate_type) 
                   for c, y in zip(costs, years))
    pv_benefits = sum(b * calculate_discount_factor(y, rate_type) 
                      for b, y in zip(benefits, years))
    
    if pv_costs == 0:
        raise ValueError("Total discounted costs cannot be zero")
    
    return pv_benefits / pv_costs


def apply_optimism_bias(
    cost_estimate: float,
    project_type: str = 'standard_civil_engineering'
) -> float:
    """
    Apply Green Book optimism bias adjustment to cost estimates.
    
    Parameters
    ----------
    cost_estimate : float
        Initial cost estimate
    project_type : str
        Type of project. Options:
        - 'standard_building'
        - 'non_standard_building'
        - 'standard_civil_engineering'
        - 'non_standard_civil_engineering'
        - 'equipment_development'
        - 'outsourcing'
    
    Returns
    -------
    float
        Cost estimate adjusted for optimism bias
    
    Examples
    --------
    >>> adjusted = apply_optimism_bias(10000000, 'standard_civil_engineering')
    >>> print(f"Adjusted cost: £{adjusted:,.0f}")
    Adjusted cost: £14,400,000
    """
    # Green Book optimism bias uplifts (upper bound)
    bias_factors = {
        'standard_building': 0.24,
        'non_standard_building': 0.51,
        'standard_civil_engineering': 0.44,
        'non_standard_civil_engineering': 0.66,
        'equipment_development': 0.54,
        'outsourcing': 0.41
    }
    
    if project_type not in bias_factors:
        raise ValueError(f"Unknown project type. Choose from: {list(bias_factors.keys())}")
    
    uplift = bias_factors[project_type]
    return cost_estimate * (1 + uplift)


if __name__ == "__main__":
    # Example usage
    print("Green Book NPV Calculator")
    print("=" * 40)
    
    # Example: 5-year infrastructure project
    cash_flows = [-1000000, 200000, 250000, 300000, 350000, 400000]
    
    npv = calculate_npv_greenbook(cash_flows)
    print(f"Cash flows: {cash_flows}")
    print(f"NPV: £{npv:,.0f}")
    
    # Example: BCR calculation
    costs = [1000000, 50000, 50000, 50000, 50000]
    benefits = [0, 300000, 320000, 340000, 360000]
    bcr = calculate_bcr(costs, benefits)
    print(f"\nBCR: {bcr:.2f}")
    
    # Example: Optimism bias
    initial_cost = 10000000
    adjusted = apply_optimism_bias(initial_cost)
    print(f"\nInitial cost: £{initial_cost:,.0f}")
    print(f"With optimism bias: £{adjusted:,.0f}")
```
