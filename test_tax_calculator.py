"""
Unit tests for the Tax Calculator

Run with: python -m pytest test_tax_calculator.py
or simply: python test_tax_calculator.py
"""

import unittest
from tax_calculator import TaxCalculator, FilingStatus


class TestTaxCalculator(unittest.TestCase):
    """Test cases for TaxCalculator"""

    def setUp(self):
        """Set up test calculator"""
        self.calculator = TaxCalculator(year=2024)

    def test_initialization(self):
        """Test calculator initialization"""
        calculator = TaxCalculator(year=2024)
        self.assertEqual(calculator.year, 2024)

        # Test unsupported year
        with self.assertRaises(ValueError):
            TaxCalculator(year=2023)

    def test_zero_income(self):
        """Test calculation with zero income"""
        result = self.calculator.calculate_tax(
            income=0,
            filing_status=FilingStatus.SINGLE
        )
        self.assertEqual(result['total_tax'], 0)
        self.assertEqual(result['effective_rate'], 0)

    def test_negative_income(self):
        """Test that negative income raises error"""
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(
                income=-1000,
                filing_status=FilingStatus.SINGLE
            )

    def test_low_income_single(self):
        """Test single filer with income below standard deduction"""
        result = self.calculator.calculate_tax(
            income=10000,
            filing_status=FilingStatus.SINGLE
        )
        # Income below standard deduction should result in no tax
        self.assertEqual(result['total_tax'], 0)
        self.assertEqual(result['taxable_income'], 0)

    def test_single_filer_75k(self):
        """Test single filer with $75,000 income"""
        result = self.calculator.calculate_tax(
            income=75000,
            filing_status=FilingStatus.SINGLE
        )

        # Taxable income should be income minus standard deduction
        expected_taxable = 75000 - 14600
        self.assertEqual(result['taxable_income'], expected_taxable)

        # Tax should be positive
        self.assertGreater(result['total_tax'], 0)

        # Effective rate should be less than marginal rate
        self.assertLess(result['effective_rate'], result['marginal_rate'])

    def test_married_filing_jointly(self):
        """Test married filing jointly status"""
        result = self.calculator.calculate_tax(
            income=150000,
            filing_status=FilingStatus.MARRIED_FILING_JOINTLY
        )

        # Check standard deduction is applied correctly
        expected_deduction = 29200
        self.assertEqual(result['deductions'], expected_deduction)

        # Tax should be positive
        self.assertGreater(result['total_tax'], 0)

    def test_itemized_deductions(self):
        """Test using itemized deductions instead of standard"""
        income = 100000
        itemized = 20000

        result = self.calculator.calculate_tax(
            income=income,
            filing_status=FilingStatus.SINGLE,
            use_standard_deduction=False,
            itemized_deductions=itemized
        )

        self.assertEqual(result['deductions'], itemized)
        self.assertEqual(result['taxable_income'], income - itemized)

    def test_high_income_bracket(self):
        """Test calculation for high income (top bracket)"""
        result = self.calculator.calculate_tax(
            income=700000,
            filing_status=FilingStatus.SINGLE
        )

        # Should be in top bracket (37%)
        self.assertEqual(result['marginal_rate'], 37.0)

        # Effective rate should be significantly lower than marginal
        self.assertLess(result['effective_rate'], 32)

    def test_compare_filing_statuses(self):
        """Test comparing different filing statuses"""
        comparison = self.calculator.compare_filing_statuses(100000)

        # Should have results for all filing statuses
        self.assertEqual(len(comparison), 4)

        # All should have positive tax
        for status, tax in comparison.items():
            self.assertGreater(tax, 0)

        # Married filing jointly should generally have lower tax than single
        # for the same income
        self.assertLess(
            comparison[FilingStatus.MARRIED_FILING_JOINTLY],
            comparison[FilingStatus.SINGLE]
        )

    def test_quarterly_estimate(self):
        """Test quarterly tax estimate"""
        quarterly = self.calculator.estimate_quarterly_tax(
            annual_income=100000,
            filing_status=FilingStatus.SINGLE
        )

        # Should be positive
        self.assertGreater(quarterly, 0)

        # Should be approximately 1/4 of annual tax
        annual_result = self.calculator.calculate_tax(100000, FilingStatus.SINGLE)
        expected_quarterly = annual_result['total_tax'] / 4
        self.assertAlmostEqual(quarterly, expected_quarterly, places=2)

    def test_breakdown_structure(self):
        """Test that breakdown has correct structure"""
        result = self.calculator.calculate_tax(
            income=100000,
            filing_status=FilingStatus.SINGLE
        )

        # Should have breakdown list
        self.assertIsInstance(result['breakdown'], list)
        self.assertGreater(len(result['breakdown']), 0)

        # Each bracket should have required fields
        for bracket in result['breakdown']:
            self.assertIn('bracket', bracket)
            self.assertIn('rate', bracket)
            self.assertIn('amount', bracket)
            self.assertIn('tax', bracket)

    def test_all_filing_statuses(self):
        """Test that all filing statuses work"""
        income = 80000

        for status in FilingStatus:
            result = self.calculator.calculate_tax(
                income=income,
                filing_status=status
            )

            # Should have valid results
            self.assertIsNotNone(result['total_tax'])
            self.assertGreaterEqual(result['total_tax'], 0)

    def test_edge_case_bracket_boundaries(self):
        """Test income exactly at bracket boundaries"""
        # Test income exactly at first bracket boundary for single filer
        result = self.calculator.calculate_tax(
            income=11600 + 14600,  # Bracket limit plus standard deduction
            filing_status=FilingStatus.SINGLE
        )

        # Should have valid calculation
        self.assertGreater(result['total_tax'], 0)

    def test_effective_rate_calculation(self):
        """Test effective rate is calculated correctly"""
        income = 100000
        result = self.calculator.calculate_tax(
            income=income,
            filing_status=FilingStatus.SINGLE
        )

        # Calculate effective rate manually
        expected_rate = (result['total_tax'] / income) * 100

        self.assertAlmostEqual(result['effective_rate'], expected_rate, places=2)


def run_tests():
    """Run all tests and display results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestTaxCalculator)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
