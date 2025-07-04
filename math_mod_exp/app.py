
def add(x, y):
    """Add Function"""
    return x + y


def subtract(x, y):
    """Subtract Function"""
    return x - y


def multiply(x, y):
    """Multiply Function"""
    return x * y


def divide(x, y):
    """Divide Function"""
    if y == 0:
        raise ValueError('Can not divide by zero!')
    return x / y

# Modular exponentiation
def modular_exp(base, power, modulus):
    """Basic modular exponentiation"""
    if modulus == 1:
        return 0
    elif modulus == 0:
        raise ValueError("Modulus cannot be zero")
    
    if power < 0:
        raise ValueError("Negative exponent not supported yet")
    
    # Naive implementation: iterative multiplication and modulus at each step
    result = 1
    for _ in range(power):
        result = (result * base) % modulus
    return result

def extended_gcd(a, b):
    """Extended Euclidean Algorithm to compute the GCD and coefficients."""
    if b == 0:
        return a, 1, 0
    gcd, x_prev, y_prev = extended_gcd(b, a % b)
    x = y_prev
    y = x_prev - (a // b) * y_prev
    return gcd, x, y

def modular_inverse(value, modulus):
    """Computes the modular inverse of 'value' modulo 'modulus'."""
    gcd, inverse, _ = extended_gcd(value, modulus)
    if gcd != 1:
        raise ValueError(f"No modular inverse exists for {value} modulo {modulus}")
    return inverse % modulus

def modular_exp_efficient(base, exponent, modulus):
    
    """
    Efficient modular exponentiation using exponentiation by squaring.

    Arguments:
    - base: the base integer (can be negative)
    - exponent: the exponent integer (can be negative)
    - modulus: the modulus integer (must be positive and non-zero)

    Notes:
    - If base is negative, it is reduced modulo 'modulus' before computation.
    - If exponent is negative, the modular inverse of the base is used.
    - Follows the behavior of Python's built-in pow(base, exponent, modulus) for integers.

    Raises:
    - ValueError if modulus is zero or modular inverse does not exist.
    - TypeError if base, exponent, or modulus is not an integer.
    """
    
    # TODO Testing this?
    if not all(isinstance(x, int) for x in (base, exponent, modulus)):
        raise TypeError("All arguments must be integers")

    if modulus <= 0:
        raise ValueError("Modulus must be a positive integer")
    
    # TODO Checking mod==1 before inverse only works when only expect to not handle inverses
    if modulus == 1:
        return 0
    
    # Match result of Python's pow() when base & exponent = 0
    if base == 0 and exponent == 0:
        return 1 % modulus
    
    # TODO This is not always, true. pow(0,-4,1) works, but pow(0,-100,13) doesn't. So check actual invertibility
    if base == 0 and exponent < 0:
        raise ValueError("Base is invertible for given modulus")


    base_reduced = base % modulus

    # Handle negative exponent
    if exponent < 0:
        base_reduced = modular_inverse(base_reduced, modulus)
        exponent = -exponent

    result = 1

    while exponent > 0:
        if exponent % 2 == 1:  # if exp is odd
            result = (result * base_reduced) % modulus
        base_reduced = (base_reduced * base_reduced) % modulus
        exponent //= 2

    return result


# factorial

# modulus

# remainder

# square root

# Floor division

# Factorial

# Logarithm

