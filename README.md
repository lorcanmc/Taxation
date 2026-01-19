# Taxation Calculator

A simple Python library for calculating income tax based on progressive tax brackets.

## Features

- Progressive tax bracket calculations
- Support for standard deductions
- Multiple filing status support (Single, Married Filing Jointly, Head of Household)
- 2024 US Federal Tax brackets included
- Easy to extend with additional tax years or jurisdictions

## Installation

No external dependencies required. Just clone and use:

```bash
git clone <repository-url>
cd Taxation
```

## Usage

```python
from tax_calculator import TaxCalculator, FilingStatus

# Create a calculator for 2024
calculator = TaxCalculator(year=2024)

# Calculate tax for a single filer with $75,000 income
tax = calculator.calculate_tax(
    income=75000,
    filing_status=FilingStatus.SINGLE,
    use_standard_deduction=True
)

print(f"Total tax owed: ${tax['total_tax']:,.2f}")
print(f"Effective tax rate: {tax['effective_rate']:.2f}%")
```

## Tax Brackets (2024)

### Single Filers
- 10% on income up to $11,600
- 12% on income $11,601 to $47,150
- 22% on income $47,151 to $100,525
- 24% on income $100,526 to $191,950
- 32% on income $191,951 to $243,725
- 35% on income $243,726 to $609,350
- 37% on income over $609,350

### Standard Deduction (2024)
- Single: $14,600
- Married Filing Jointly: $29,200
- Head of Household: $21,900

## Future Enhancements

- [ ] Support for itemized deductions
- [ ] State tax calculations
- [ ] Tax credit support (Child Tax Credit, EITC, etc.)
- [ ] Historical tax year data
- [ ] Tax planning and projection features
- [ ] Export tax summary to PDF

## License

MIT License
