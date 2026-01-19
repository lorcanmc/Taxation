"""
US Federal Income Tax Calculator

This module provides a simple calculator for US federal income tax
based on progressive tax brackets.
"""

from enum import Enum
from typing import Dict, List, Tuple


class FilingStatus(Enum):
    """Tax filing status options"""
    SINGLE = "single"
    MARRIED_FILING_JOINTLY = "married_filing_jointly"
    MARRIED_FILING_SEPARATELY = "married_filing_separately"
    HEAD_OF_HOUSEHOLD = "head_of_household"


class TaxCalculator:
    """
    Calculator for US federal income tax using progressive tax brackets.

    Supports multiple filing statuses and standard deductions.
    """

    # 2024 Tax brackets: (upper_limit, rate)
    # None for upper_limit means no upper bound
    TAX_BRACKETS_2024 = {
        FilingStatus.SINGLE: [
            (11600, 0.10),
            (47150, 0.12),
            (100525, 0.22),
            (191950, 0.24),
            (243725, 0.32),
            (609350, 0.35),
            (None, 0.37)
        ],
        FilingStatus.MARRIED_FILING_JOINTLY: [
            (23200, 0.10),
            (94300, 0.12),
            (201050, 0.22),
            (383900, 0.24),
            (487450, 0.32),
            (731200, 0.35),
            (None, 0.37)
        ],
        FilingStatus.MARRIED_FILING_SEPARATELY: [
            (11600, 0.10),
            (47150, 0.12),
            (100525, 0.22),
            (191950, 0.24),
            (243725, 0.32),
            (365600, 0.35),
            (None, 0.37)
        ],
        FilingStatus.HEAD_OF_HOUSEHOLD: [
            (16550, 0.10),
            (63100, 0.12),
            (100500, 0.22),
            (191950, 0.24),
            (243700, 0.32),
            (609350, 0.35),
            (None, 0.37)
        ]
    }

    # 2024 Standard deductions
    STANDARD_DEDUCTIONS_2024 = {
        FilingStatus.SINGLE: 14600,
        FilingStatus.MARRIED_FILING_JOINTLY: 29200,
        FilingStatus.MARRIED_FILING_SEPARATELY: 14600,
        FilingStatus.HEAD_OF_HOUSEHOLD: 21900
    }

    def __init__(self, year: int = 2024):
        """
        Initialize the tax calculator.

        Args:
            year: Tax year (currently only 2024 is supported)
        """
        self.year = year
        if year != 2024:
            raise ValueError(f"Tax year {year} is not supported. Only 2024 is currently available.")

        self.tax_brackets = self.TAX_BRACKETS_2024
        self.standard_deductions = self.STANDARD_DEDUCTIONS_2024

    def calculate_tax(
        self,
        income: float,
        filing_status: FilingStatus,
        use_standard_deduction: bool = True,
        itemized_deductions: float = 0.0
    ) -> Dict:
        """
        Calculate federal income tax based on income and filing status.

        Args:
            income: Gross annual income
            filing_status: Filing status (Single, Married, etc.)
            use_standard_deduction: Whether to use standard deduction
            itemized_deductions: Amount of itemized deductions (if not using standard)

        Returns:
            Dictionary containing tax calculation details:
                - gross_income: Original income
                - deductions: Total deductions applied
                - taxable_income: Income after deductions
                - total_tax: Total tax owed
                - effective_rate: Effective tax rate as percentage
                - marginal_rate: Highest tax bracket rate as percentage
                - breakdown: Tax amount per bracket
        """
        if income < 0:
            raise ValueError("Income cannot be negative")

        # Determine deductions
        if use_standard_deduction:
            deductions = self.standard_deductions[filing_status]
        else:
            deductions = max(0, itemized_deductions)

        # Calculate taxable income
        taxable_income = max(0, income - deductions)

        # Get tax brackets for filing status
        brackets = self.tax_brackets[filing_status]

        # Calculate tax using progressive brackets
        total_tax = 0.0
        previous_limit = 0
        breakdown = []
        marginal_rate = 0.0

        for upper_limit, rate in brackets:
            if upper_limit is None:
                # This is the highest bracket
                if taxable_income > previous_limit:
                    amount_in_bracket = taxable_income - previous_limit
                    tax_in_bracket = amount_in_bracket * rate
                    total_tax += tax_in_bracket
                    marginal_rate = rate
                    breakdown.append({
                        'bracket': f"Over ${previous_limit:,}",
                        'rate': rate,
                        'amount': amount_in_bracket,
                        'tax': tax_in_bracket
                    })
                break

            if taxable_income > upper_limit:
                # Income exceeds this bracket
                amount_in_bracket = upper_limit - previous_limit
                tax_in_bracket = amount_in_bracket * rate
                total_tax += tax_in_bracket
                breakdown.append({
                    'bracket': f"${previous_limit:,} - ${upper_limit:,}",
                    'rate': rate,
                    'amount': amount_in_bracket,
                    'tax': tax_in_bracket
                })
                previous_limit = upper_limit
                marginal_rate = rate
            else:
                # This is the final bracket for this income
                amount_in_bracket = taxable_income - previous_limit
                tax_in_bracket = amount_in_bracket * rate
                total_tax += tax_in_bracket
                marginal_rate = rate
                breakdown.append({
                    'bracket': f"${previous_limit:,} - ${upper_limit:,}",
                    'rate': rate,
                    'amount': amount_in_bracket,
                    'tax': tax_in_bracket
                })
                break

        # Calculate effective rate
        effective_rate = (total_tax / income * 100) if income > 0 else 0.0

        return {
            'gross_income': income,
            'deductions': deductions,
            'taxable_income': taxable_income,
            'total_tax': round(total_tax, 2),
            'effective_rate': round(effective_rate, 2),
            'marginal_rate': round(marginal_rate * 100, 2),
            'breakdown': breakdown
        }

    def compare_filing_statuses(self, income: float) -> Dict[FilingStatus, float]:
        """
        Compare tax owed under different filing statuses.

        Args:
            income: Gross annual income

        Returns:
            Dictionary mapping filing status to total tax owed
        """
        results = {}
        for status in FilingStatus:
            tax_result = self.calculate_tax(income, status)
            results[status] = tax_result['total_tax']
        return results

    def estimate_quarterly_tax(
        self,
        annual_income: float,
        filing_status: FilingStatus
    ) -> float:
        """
        Estimate quarterly tax payment for self-employed individuals.

        Args:
            annual_income: Expected annual income
            filing_status: Filing status

        Returns:
            Estimated quarterly tax payment amount
        """
        tax_result = self.calculate_tax(annual_income, filing_status)
        return round(tax_result['total_tax'] / 4, 2)
