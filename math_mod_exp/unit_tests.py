import app
import time
import unittest
from unittest.mock import patch


class TestApp(unittest.TestCase):
  '''Unit test suite for modular exponentiation app. Tests are numbered according to final version (last task with this codebase)'''

  def test_1_basic(self):
    '''Tests basic modular exponentiation with positive, zero and negative bases.'''
    
    # all positive
    self.assertEqual(app.modular_exp(5, 5, 13), pow(5, 5, 13))
    
    # negative base
    self.assertEqual(app.modular_exp(-3, 2, 7), pow(-3, 2, 7))
    
    # exponent = 0
    self.assertEqual(app.modular_exp(-3, 0, 4), pow(-3, 0, 4))

    # base = 0
    self.assertEqual(app.modular_exp(0, 13, 5), pow(0, 13, 5))

    # int result
    result = app.modular_exp(3, 4, 5)
    self.assertIsInstance(result, int)


  def test_2_invalid_inputs(self):
    '''Raises TypeError for non-integer base, exponent, or modulus. Must not fall back to non-modular pow().'''

    invalid_inputs = [
      ("base", 3, 5),
      (2.5, 3, 5),
      (2, "exponent", 5),
      (2, 3.5, 5),
      (2, 3, "mod"),
      (2, 3, None),  # Critical: modulus must not be None
    ]

    for args in invalid_inputs:
      with self.assertRaises(TypeError, msg=f"Expected TypeError for args={args}. Built-in pow() may be used."):
        app.modular_exp(*args)

  
  def test_3_incorrect_modulus(self):
    '''Raises ValueError when modulus is zero or negative.'''
    with self.assertRaises(ValueError):
      app.modular_exp(2, 3, 0)


  def test_4_handle_negative_modulus(self):
    '''Verifies correct handling of negative modulus and both exponent signs.'''

    # exp > 0, varying base
    self.assertEqual(app.modular_exp(2, 3, -5), pow(2, 3, -5))
    self.assertEqual(app.modular_exp(-2, 3, -5), pow(-2, 3, -5))
    self.assertEqual(app.modular_exp(0, 3, -5), pow(0, 3, -5))

    # exp < 0, varying base
    self.assertEqual(app.modular_exp(13, -4, -7), pow(13, -4, -7))
    self.assertEqual(app.modular_exp(-13, -4, -7), pow(-13, -4, -7))
    with self.assertRaises(ValueError):
      app.modular_exp(0, -4, -7)


  def test_5_mod_equals_one(self):
    '''Checks that result is always 0 when |modulus| == 1.'''

    # mod = 1, exp > 0, varying base
    self.assertEqual(app.handle_edge_cases(10, 100, 1), 0)
    self.assertEqual(app.handle_edge_cases(-10, 100, 1), 0)
    self.assertEqual(app.handle_edge_cases(0, 100, 1), 0)

    # mod = 1, exp < 0, varying base
    self.assertEqual(app.handle_edge_cases(10, -100, 1), 0)
    self.assertEqual(app.handle_edge_cases(-10, -100, 1), 0)
    self.assertEqual(app.handle_edge_cases(0, -100, 1), 0)

    # mod = -1, exp > 0, varying base
    self.assertEqual(app.handle_edge_cases(10, 100, -1), 0)
    self.assertEqual(app.handle_edge_cases(-10, 100, -1), 0)
    self.assertEqual(app.handle_edge_cases(0, 100, -1), 0)

    # mod = -1, exp < 0, varying base
    self.assertEqual(app.handle_edge_cases(10, -100, -1), 0)
    self.assertEqual(app.handle_edge_cases(-10, -100, -1), 0)
    self.assertEqual(app.handle_edge_cases(0, -100, -1), 0)


  def test_6_zero_base_and_exponent(self):
    '''Ensures 0^0 mod m is correctly treated as 1 % m.'''
    # mod > 0
    self.assertEqual(app.handle_edge_cases(0, 0, 7), 1 % 7)
    self.assertEqual(app.handle_edge_cases(0, 0, 7), pow(0, 0, 7))

    # mod < 0
    self.assertEqual(app.handle_edge_cases(0, 0, -7), 1 % -7)
    self.assertEqual(app.handle_edge_cases(0, 0, -7), pow(0, 0, -7))


  def test_7_negative_exp_valid(self):
    '''Computes result using modular inverse for valid negative exponents.'''
    
    # mod > 0, varying base
    self.assertEqual(app.modular_exp(-5, -13, 17), pow(-5, -13, 17))
    self.assertEqual(app.modular_exp(5, -13, 17), pow(5, -13, 17))
  
    # mod < 0, varying base
    self.assertEqual(app.modular_exp(-5, -13, -17), pow(-5, -13, -17))
    self.assertEqual(app.modular_exp(5, -13, -17), pow(5, -13, -17))


  def test_8_no_modular_inverse(self):
    '''Raises ValueError when no modular inverse exists for the negative exponent.'''
    
    # mod > 0
    with self.assertRaises(ValueError) as e:
      app.modular_exp(-34, -13, 17) # -34 and 17 not coprime, inverse does not exist
    self.assertEqual(str(e.exception), "No modular inverse exists for -34 modulo 17.")
    
    with self.assertRaises(ValueError) as e:
      app.modular_exp(0, -13, 17) # 0 has no inverse under any modulus
    self.assertEqual(str(e.exception), "No modular inverse exists for 0 modulo 17.")

    with self.assertRaises(ValueError) as e:
      app.modular_exp(34, -13, 17) # 34 and 17 not coprime
    self.assertEqual(str(e.exception), "No modular inverse exists for 34 modulo 17.")

    # mod < 0
    with self.assertRaises(ValueError) as e:
      app.modular_exp(-28, -9, -14) # -28 and -14 not coprime
    self.assertEqual(str(e.exception), "No modular inverse exists for -28 modulo -14.")
    
    with self.assertRaises(ValueError) as e:
      app.modular_exp(0, -9, -14) # 0 has no inverse under any modulus
    self.assertEqual(str(e.exception), "No modular inverse exists for 0 modulo -14.")

    with self.assertRaises(ValueError) as e:
      app.modular_exp(28, -9, -14) # 28 and -14 not coprime
    self.assertEqual(str(e.exception), "No modular inverse exists for 28 modulo -14.")


  def test_9_inverse_edge_case(self):
    '''Verifies correct result for trivial bases (±1) with large negative exponents.'''
    
    # mod > 0
    self.assertEqual(app.modular_exp(1, -123456, 101), pow(1, -123456, 101))
    self.assertEqual(app.modular_exp(-1, -123456, 101), pow(-1, -123456, 101))
    self.assertEqual(app.modular_exp(-1, -123457, 101), pow(-1, -123457, 101))  # (-1)^odd = -1 ≡ 100 (mod 101)

    # mod > 0
    self.assertEqual(app.modular_exp(1, -123456, -101), pow(1, -123456, -101))
    self.assertEqual(app.modular_exp(-1, -123456, -101), pow(-1, -123456, -101))
    self.assertEqual(app.modular_exp(-1, -123457, -101), pow(-1, -123457, -101))  # (-1)^odd = -1 ≡ 100 (mod -101)


  def test_10_exponentiation_complexity(self):
    '''Checks if modular_exp uses fast exponentiation by comparing runtime growth for large values.'''
    base = 123_456_789
    mod = 1_000_000_007

    # Small exponent
    start_small = time.perf_counter()
    app.modular_exp(base, 100_000, mod)
    duration_small = time.perf_counter() - start_small

    # Large exponent
    start_large = time.perf_counter()
    app.modular_exp(base, 100_000_000, mod)
    duration_large = time.perf_counter() - start_large

    # Now compare growth ratio
    growth_ratio = duration_large / duration_small if duration_small > 0 else float('inf')

    self.assertLess(growth_ratio, 50, (
        f"modular_exp appears to grow linearly with exponent (growth ratio={growth_ratio:.2f}); "
        "this suggests naive looping instead of exponentiation by squaring."
    ))


  def test_11_extremely_large_values(self):
    '''Verifies correctness with very large inputs through both branches (+ve and -ve exponents).'''
    base = 123456789
    exponent = 987654321
    mod = 1_000_000_007
    
    # mod > 0, base > 0
    self.assertEqual(app.modular_exp(base, exponent, mod), pow(base, exponent, mod))
    self.assertEqual(app.modular_exp(base, -exponent, mod), pow(base, -exponent, mod))

    # mod > 0, base < 0
    self.assertEqual(app.modular_exp(-base, exponent, mod), pow(-base, exponent, mod))
    self.assertEqual(app.modular_exp(-base, -exponent, mod), pow(-base, -exponent, mod))

    # mod < 0, base > 0
    self.assertEqual(app.modular_exp(base, exponent, -mod), pow(base, exponent, -mod))
    self.assertEqual(app.modular_exp(base, -exponent, -mod), pow(base, -exponent, -mod))

    # mod < 0, base < 0
    self.assertEqual(app.modular_exp(-base, exponent, -mod), pow(-base, exponent, -mod))
    self.assertEqual(app.modular_exp(-base, -exponent, -mod), pow(-base, -exponent, -mod))


  def test_12a_pow_not_used_for_invalid_inverse(self):
    '''Ensure pow() is not used when inverse does not exist (negative exponent case).'''
    with self.assertRaises(ValueError) as context:
      app.modular_exp(6, -1, 9)

    msg = str(context.exception)

    # If LLM lazily uses built-in pow(), the error message will include:
    self.assertNotIn("base is not invertible", msg,
        msg="Implementation may be using built-in pow() instead of custom logic.")

    # If you expect a specific message from your custom function:
    self.assertIn("No modular inverse exists", msg,
        msg="Expected custom error message not found.")


  def test_12b_pow_not_used_for_valid_inverse(self):
    '''Ensure pow() is not used when computing valid inverse with negative exponent.'''
    with patch("builtins.pow", side_effect=AssertionError("pow() should not be used.")):
        result = app.modular_exp(3, -1, 11)
        self.assertEqual(result, 4)


  def test_12c_pow_not_used_for_positive_exponent(self):
    '''Ensure pow() is not used for standard positive exponentiation.'''
    with patch("builtins.pow", side_effect=AssertionError("pow() should not be used.")):
      self.assertEqual(app.modular_exp(2, 5, 13), 6)


  def test_12d_pow_not_used_for_zero_exponent(self):
    '''Ensure pow() is not used when exponent is zero.'''
    with patch("builtins.pow", side_effect=AssertionError("pow() should not be used.")):
      self.assertEqual(app.modular_exp(42, 0, 101), 1)


  def test_12e_pow_not_used_for_zero_base(self):
    '''Ensure pow() is not used when base is zero.'''
    with patch("builtins.pow", side_effect=AssertionError("pow() should not be used.")):
      self.assertEqual(app.modular_exp(0, 3, 7), 0)


  def test_12f_pow_not_used_for_trivial_moduli(self):
    '''Ensure pow() is not used for modulus = 1 or -1 (all results should be 0).'''
    with patch("builtins.pow", side_effect=AssertionError("pow() should not be used.")):
      # mod > 0
      self.assertEqual(app.modular_exp(999, 999, 1), 0)
      # mod < 0
      self.assertEqual(app.modular_exp(999, 999, -1), 0)


  def test_13_extended_gcd_identity(self):
    '''Verifies that extended_gcd(a, b) satisfies Bézout's identity: ax + by = gcd(a, b).'''
    a, b = 240, 46
    gcd, x, y = app.extended_gcd(a, b)
    self.assertEqual(gcd, 2)
    self.assertEqual(a * x + b * y, gcd)  # Bézout identity


if __name__ == '__main__':
    unittest.main()