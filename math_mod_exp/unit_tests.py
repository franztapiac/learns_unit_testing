import unittest
import app

class TestApp(unittest.TestCase):

  def test_1_basic(self):
    '''Tests basic modular exponentiation with positive, zero and negative bases.'''
    
    # all positive
    self.assertEqual(app.modular_exp(2, 3, 5), 3)
    self.assertEqual(app.modular_exp(5, 5, 13), 5)
    
    # negative base
    self.assertEqual(app.modular_exp(-3, 2, 7), 2)
    
    # exponent = 0
    self.assertEqual(app.modular_exp(5, 0, 7), 1)
    self.assertEqual(app.modular_exp(-3, 0, 4), 1)

    # base = 0
    self.assertEqual(app.modular_exp(0, 13, 5), 0)


  def test_2_invalid_inputs(self):
    '''Raises TypeError for non-integer base, exponent, or modulus.'''

    for args in [
      ("base", 3, 5),
      (2.5, 3, 5),
      (2, "exponent", 5),
      (2, 3.5, 5),
      (2, 3, "mod"),
      (2, 3, None), # TODO this works fine in pow(), no type error. Ask for type error, if m is None.
    ]:
      with self.assertRaises(TypeError):
        app.modular_exp(*args)

  def test_3_incorrect_modulus(self):
    '''Raises ValueError when modulus is zero.'''
    with self.assertRaises(ValueError):
      app.modular_exp(2, 3, 0)


  def test_4_handle_negative_modulus(self):
    '''Verifies correct handling of negative modulus and various exponent signs.'''

    # exp > 0, varying base
    self.assertEqual(app.modular_exp(2, 3, -5), -2)
    self.assertEqual(app.modular_exp(-2, 3, -5), -3)
    self.assertEqual(app.modular_exp(0, 3, -5), 0)

    # exp < 0, varying base
    self.assertEqual(app.modular_exp(13, -4, -7), -6)
    self.assertEqual(app.modular_exp(-13, -4, -7), -6)
    with self.assertRaises(ValueError):
      app.modular_exp(0, -4, -7)


  def test_5_abs_mod_equals_one(self):
    '''Checks that result is always 0 when |modulus| == 1.'''

    # mod = 1, exp > 0, varying base
    self.assertEqual(app.modular_exp(10, 100, 1), 0)
    self.assertEqual(app.modular_exp(-10, 100, 1), 0)
    self.assertEqual(app.modular_exp(0, 100, 1), 0)

    # mod = 1, exp < 0, varying base
    self.assertEqual(app.modular_exp(10, -100, 1), 0)
    self.assertEqual(app.modular_exp(-10, -100, 1), 0)
    self.assertEqual(app.modular_exp(0, -100, 1), 0)

    # mod = -1, exp > 0, varying base
    self.assertEqual(app.modular_exp(10, 100, -1), 0)
    self.assertEqual(app.modular_exp(-10, 100, -1), 0)
    self.assertEqual(app.modular_exp(0, 100, -1), 0)

    # mod = -1, exp < 0, varying base
    self.assertEqual(app.modular_exp(10, -100, -1), 0)
    self.assertEqual(app.modular_exp(-10, -100, -1), 0)
    self.assertEqual(app.modular_exp(0, -100, -1), 0)


  # 5 Modular exp: base & exp = 0
  def test_6_zero_base_and_exponent(self):
    '''Ensures 0^0 mod m is correctly treated as 1 % m.'''
    
    self.assertEqual(app.modular_exp(0, 0, 7), 1)
    self.assertEqual(app.modular_exp(0, 0, -7), -6)
    
    self.assertEqual(app.modular_exp(0, 0, 1), 0)
    self.assertEqual(app.modular_exp(0, 0, -1), 0)


  def test_7_negative_exp_valid(self):
    '''Computes result using modular inverse for valid negative exponents.'''
    
    self.assertEqual(app.modular_exp(-5, -13, 17), 11)
    self.assertEqual(app.modular_exp(5, -13, 17), 6)

    self.assertEqual(app.modular_exp(-5, -13, -17), -6)
    self.assertEqual(app.modular_exp(5, -13, -17), -11)


  def test_8_no_modular_inverse(self):
    '''Raises ValueError when no modular inverse exists for the negative exponent.'''
    
    # mod > 0
    with self.assertRaises(ValueError) as e:
      app.modular_exp(-34, -13, 17) # -34 and 17 not coprime, inverse does not exist
    self.assertEqual(str(e.exception), "No modular inverse exists for -34 modulo 17")
    
    with self.assertRaises(ValueError) as e:
      app.modular_exp(0, -13, 17) # 0 has no inverse under any modulus
    self.assertEqual(str(e.exception), "No modular inverse exists for 0 modulo 17")

    with self.assertRaises(ValueError) as e:
      app.modular_exp(34, -13, 17) # 34 and 17 not coprime
    self.assertEqual(str(e.exception), "No modular inverse exists for 34 modulo 17")

    # mod < 0
    with self.assertRaises(ValueError) as e:
      app.modular_exp(-28, -9, -14) # -28 and -14 not coprime, inverse does not exist
    self.assertEqual(str(e.exception), "No modular inverse exists for -28 modulo -14")
    
    with self.assertRaises(ValueError) as e:
      app.modular_exp(0, -9, -14) # 0 has no inverse under any modulus
    self.assertEqual(str(e.exception), "No modular inverse exists for 0 modulo -14")

    with self.assertRaises(ValueError) as e:
      app.modular_exp(28, -9, -14) # 28 and -14 not coprime
    self.assertEqual(str(e.exception), "No modular inverse exists for 28 modulo -14")


  def test_9_inverse_edge_case(self):
    '''Varieis correct result for trivial bases (±1) with large negative exponents.'''
    self.assertEqual(app.modular_exp(1, -123456, 101), 1)
    self.assertEqual(app.modular_exp(-1, -123456, 101), 1)
    self.assertEqual(app.modular_exp(-1, -123457, 101), 100)  # (-1)^odd = -1 ≡ 100 mod 101


  def test_10_large_exponents(self):
    '''Tests correctness with large positive and negative exponents.'''
    
    # exp > 0
    self.assertEqual(app.modular_exp(2, 1000, 1009), 942)
    self.assertEqual(app.modular_exp(2, 1000, -1009), -67)

    # exp < 0
    self.assertEqual(app.modular_exp(3, -98765, 10007), 2405)
    self.assertEqual(app.modular_exp(3, -98765, -10007), -7602)


  def test_11_extremely_large_values(self):
    '''Verifies correctness and performance with very large base and exponent.'''
    base = 123456789
    exponent = 987654321
    mod = 1000000007
    self.assertEqual(app.modular_exp(base, exponent, mod), 652541198)
    self.assertEqual(app.modular_exp(base, exponent, -mod), -347458809) 


  def test_12_custom_inverse_logic_used(self):
    '''Ensures implementation does not fall back to built-in pow() for inverses.'''
    # TODO This test needs to check that every return point does not return pow()
    with self.assertRaises(ValueError) as context:
      app.modular_exp(6, -1, 9)  # 6 and 9 are not coprime → no inverse

    msg = str(context.exception)

    # If LLM lazily uses built-in pow(), the error message will include:
    self.assertNotIn("base is not invertible", msg,
        msg="Implementation may be using built-in pow() instead of custom logic.")

    # If you expect a specific message from your custom function:
    self.assertIn("No modular inverse exists", msg,
        msg="Expected custom error message not found.")

if __name__ == '__main__':
    unittest.main()