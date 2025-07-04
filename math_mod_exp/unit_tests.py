import unittest
import app

class TestApp(unittest.TestCase):
  
  def test_add(self):

    # assert methods: https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug
    self.assertEqual(app.add(10, 5), 15)
    self.assertEqual(app.add(-1, 1), 0)
    self.assertEqual(app.add(-1, -1), -2)

  def test_subtract(self):
    self.assertEqual(app.subtract(10, 5), 5)
    self.assertEqual(app.subtract(-1, 1), -2)
    self.assertEqual(app.subtract(-1, -1), 0)

  def test_multiply(self):
    self.assertEqual(app.multiply(10, 5), 50)
    self.assertEqual(app.multiply(-1, 1), -1)
    self.assertEqual(app.multiply(-1, -1), 1)

  def test_divide(self):
    self.assertEqual(app.divide(10, 5), 2)
    self.assertEqual(app.divide(-1, 1), -1)
    self.assertEqual(app.divide(-1, -1), 1)
    self.assertEqual(app.divide(5, 2), 2.5)

    with self.assertRaises(ValueError):
      app.divide(10, 0)



  # Modular exp: Basic
  def test_basic_modular_exp(self):
    self.assertEqual(app.modular_exp(2, 3, 5), 3)
    self.assertEqual(app.modular_exp(10, 0, 7), 1)
    self.assertEqual(app.modular_exp(5, 5, 13), 5)

  # Modular exp: -base
  def test_negative_base(self):
    self.assertEqual(app.modular_exp(-2, 3, 5), 2)  # (-2)^3 = -8, -8 % 5 = 2
    self.assertEqual(app.modular_exp(-3, 2, 7), 2) 
  
  # Modular exp: exp < 0; no modular inverse
  def test_no_modular_inverse(self):
    with self.assertRaises(ValueError):
      app.modular_exp(2, -1, 4) # 2 and 4 not coprime, inverse does not exist

  # Modular exp: base & exp = 0
  def test_zero_base_and_exponent(self):
    # By definition, pow(0,0,mod) returns 1 % mod
    self.assertEqual(app.modular_exp(0, 0, 7), 1)
    self.assertEqual(app.modular_exp(0, 0, 1), 0)

  # Modular exp: base == 0 and negative exponent
  def test_zero_base_negative_exponent(self):
    with self.assertRaises(ValueError):
      app.modular_exp(0, -1, 7)

  # Modular exp: -base^0
  def test_zero_exponent_with_negative_base(self):
    self.assertEqual(app.modular_exp(-5, 0, 7), 1)  # anything^0 mod N = 1
    self.assertEqual(app.modular_exp(-3, 0, 4), 1)

  # Modular exp: mod <= 0
  def test_incorrect_modulus(self):
    with self.assertRaises(ValueError):
        app.modular_exp(2, 3, -5)
      
    with self.assertRaises(ValueError):
      app.modular_exp(2, 3, 0)

  # Modular exp: mod = 1
  def test_mod_one(self):
    # Mod 1 always returns 0
    self.assertEqual(app.modular_exp(10, 100, 1), 0)
  
  # Modular exp: large exponents
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

  # Modular exp: invalid inputs
  def test_invalid_inputs(self):
    with self.assertRaises(TypeError):
      app.modular_exp(2.5, 3, 5)

    with self.assertRaises(TypeError):
      app.modular_exp(2, 3.5, 5)

    with self.assertRaises(TypeError):
      app.modular_exp(2, 3, "mod")

if __name__ == '__main__':
    unittest.main()