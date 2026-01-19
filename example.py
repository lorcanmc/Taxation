"""
Example usage of the Taxation Calculator

This script demonstrates various features of the tax calculator.
"""

from tax_calculator import TaxCalculator, FilingStatus


def print_separator():
    print("\n" + "=" * 70 + "\n")


def main():
    # Initialize calculator for 2024
    calculator = TaxCalculator(year=2024)

    print("US Federal Income Tax Calculator - 2024")
    print_separator()

    # Example 1: Single filer with $75,000 income
    print("Example 1: Single Filer")
    print("Income: $75,000")
    print()

    result = calculator.calculate_tax(
        income=75000,
        filing_status=FilingStatus.SINGLE,
        use_standard_deduction=True
    )

    print(f"Gross Income:      ${result['gross_income']:>12,.2f}")
    print(f"Standard Deduction: ${result['deductions']:>12,.2f}")
    print(f"Taxable Income:    ${result['taxable_income']:>12,.2f}")
    print(f"\nTotal Tax Owed:    ${result['total_tax']:>12,.2f}")
    print(f"Effective Rate:    {result['effective_rate']:>12.2f}%")
    print(f"Marginal Rate:     {result['marginal_rate']:>12.2f}%")

    print("\nTax Breakdown by Bracket:")
    for bracket_info in result['breakdown']:
        if bracket_info['amount'] > 0:
            print(f"  {bracket_info['bracket']:<25} @ {bracket_info['rate']*100:>5.0f}%: "
                  f"${bracket_info['tax']:>10,.2f}")

    print_separator()

    # Example 2: Married filing jointly with $150,000 income
    print("Example 2: Married Filing Jointly")
    print("Income: $150,000")
    print()

    result = calculator.calculate_tax(
        income=150000,
        filing_status=FilingStatus.MARRIED_FILING_JOINTLY,
        use_standard_deduction=True
    )

    print(f"Gross Income:      ${result['gross_income']:>12,.2f}")
    print(f"Standard Deduction: ${result['deductions']:>12,.2f}")
    print(f"Taxable Income:    ${result['taxable_income']:>12,.2f}")
    print(f"\nTotal Tax Owed:    ${result['total_tax']:>12,.2f}")
    print(f"Effective Rate:    {result['effective_rate']:>12.2f}%")
    print(f"Marginal Rate:     {result['marginal_rate']:>12.2f}%")

    print_separator()

    # Example 3: Compare filing statuses
    print("Example 3: Compare Filing Statuses")
    print("Income: $100,000")
    print()

    comparison = calculator.compare_filing_statuses(100000)
    print("Tax Owed by Filing Status:")
    for status, tax in comparison.items():
        print(f"  {status.value.replace('_', ' ').title():<30}: ${tax:>10,.2f}")

    print_separator()

    # Example 4: Quarterly estimated tax for self-employed
    print("Example 4: Quarterly Estimated Tax Payment")
    print("Expected Annual Income: $120,000")
    print("Filing Status: Single")
    print()

    quarterly_payment = calculator.estimate_quarterly_tax(
        annual_income=120000,
        filing_status=FilingStatus.SINGLE
    )

    annual_result = calculator.calculate_tax(120000, FilingStatus.SINGLE)

    print(f"Estimated Annual Tax:     ${annual_result['total_tax']:>12,.2f}")
    print(f"Quarterly Payment:        ${quarterly_payment:>12,.2f}")
    print(f"\nDue dates: April 15, June 15, September 15, January 15 (next year)")

    print_separator()

    # Example 5: High income earner
    print("Example 5: High Income Earner")
    print("Income: $500,000")
    print("Filing Status: Head of Household")
    print()

    result = calculator.calculate_tax(
        income=500000,
        filing_status=FilingStatus.HEAD_OF_HOUSEHOLD,
        use_standard_deduction=True
    )

    print(f"Gross Income:      ${result['gross_income']:>12,.2f}")
    print(f"Standard Deduction: ${result['deductions']:>12,.2f}")
    print(f"Taxable Income:    ${result['taxable_income']:>12,.2f}")
    print(f"\nTotal Tax Owed:    ${result['total_tax']:>12,.2f}")
    print(f"Effective Rate:    {result['effective_rate']:>12.2f}%")
    print(f"Marginal Rate:     {result['marginal_rate']:>12.2f}%")

    print_separator()


if __name__ == "__main__":
    main()
