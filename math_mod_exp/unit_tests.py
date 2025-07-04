import unittest
import app

class TestApp(unittest.TestCase):

  # 1 Modular exp: Basic tests
  def test_mod_exp_basic(self):
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


  # 2 Modular exp: invalid inputs
  def test_mod_exp_invalid_inputs(self):
    with self.assertRaises(TypeError):
      app.modular_exp("base", 3, 5)
    
    with self.assertRaises(TypeError):
      app.modular_exp(2.5, 3, 5)

    with self.assertRaises(TypeError):
        app.modular_exp(2, "exponent", 5)

    with self.assertRaises(TypeError):
      app.modular_exp(2, 3.5, 5)

    with self.assertRaises(TypeError):
      app.modular_exp(2, 3, "mod")

    with self.assertRaises(TypeError):
        app.modular_exp(2, 3, None)


  # 3 Modular exp: mod <= 0
  def test_mod_exp_incorrect_modulus(self):
    with self.assertRaises(ValueError):
        app.modular_exp(2, 3, -5)
      
    with self.assertRaises(ValueError):
      app.modular_exp(2, 3, 0)


  # 4 Modular exp: mod = 1
  def test_mod_exp_mod_equals_one(self):
    self.assertEqual(app.modular_exp(10, 100, 1), 0)
    self.assertEqual(app.modular_exp(-10, 100, 1), 0)
    self.assertEqual(app.modular_exp(0, 100, 1), 0)

    self.assertEqual(app.modular_exp(10, -100, 1), 0)
    self.assertEqual(app.modular_exp(-10, -100, 1), 0)
    self.assertEqual(app.modular_exp(0, -100, 1), 0)


  # 5 Modular exp: base & exp = 0
  def test_mod_exp_zero_base_and_exponent(self):
    # By definition, 0^0 mod m returns 1 % m.
    self.assertEqual(app.modular_exp(0, 0, 7), 1)
    self.assertEqual(app.modular_exp(0, 0, 1), 0)


  # 6 Modular exp: negative exponent, valid
  def test_mod_exp_negative_exp_valid(self):
    self.assertEqual(app.modular_exp(-5, -13, 17), 11)
    self.assertEqual(app.modular_exp(5, -13, 17), 6)


  # 7 Modular exp: negative exponent, invalid (no modular inverse)
  def test_mod_exp_no_modular_inverse(self):
    with self.assertRaises(ValueError) as e:
      app.modular_exp(-34, -13, 17) # -34 and 17 not coprime, inverse does not exist
    self.assertEqual(str(e.exception), "No modular inverse exists for -34 modulo 17")
    
    with self.assertRaises(ValueError) as e:
      app.modular_exp(0, -13, 17) # 0 has no inverse under any modulus
    self.assertEqual(str(e.exception), "No modular inverse exists for 0 modulo 17")

    with self.assertRaises(ValueError) as e:
      app.modular_exp(34, -13, 17) # 34 and 17 not coprime
    self.assertEqual(str(e.exception), "No modular inverse exists for 34 modulo 17")


  # 8 Modular exp: large exponents
  def test_large_exponents(self):
    # 2^1000 mod 1009 (1009 is prime)
    expected = pow(2, 1000, 1009)  # Using Python's built-in pow for expected value
    self.assertEqual(app.modular_exp(2, 1000, 1009), expected)

    # Large base and exponent
    base = 123456789
    exponent = 987654321
    mod = 1000000007
    expected = pow(base, exponent, mod)
    self.assertEqual(app.modular_exp(base, exponent, mod), expected)

if __name__ == '__main__':
    unittest.main()