def modular_exp(base, exponent, modulus):
    return pow(base, exponent, modulus)

# Basic modular exponentiation
def modular_exp_basic(base, exponent, modulus):
    """Basic modular exponentiation. Misses:
    - Handling of negative exponents with valid and invalid inverses
    - Handling of negative moduli
    - Implementation is naively slow, rather than efficient
    """
    if not all(isinstance(x, int) for x in (base, exponent, modulus)):
        raise TypeError("All arguments must be integers")
    
    if modulus <= 0:
        raise ValueError("Modulus must be a positive integer")
    
    # Trivial case
    if modulus == 1:
        return 0
    
    # Special case: 0^0 mod m is defined as 1 mod m; saves computation
    if base == 0 and exponent == 0:
        return 1 % modulus
    
    if exponent < 0:
        raise ValueError("Negative exponent not supported yet")
    
    # Naive implementation: iterative multiplication and modulus at each step
    result = 1
    for _ in range(exponent):
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

def modular_inverse(base, base_reduced, modulus):
    """Computes the modular inverse of 'base' modulo 'modulus'."""
    gcd, inverse, _ = extended_gcd(base_reduced, modulus)
    if gcd != 1:
        raise ValueError(f"No modular inverse exists for {base} modulo {modulus}")
    return inverse % modulus

# Complete modular exponentiation
def modular_exp_eff(base, exponent, modulus):
    
    """
    Efficient modular exponentiation (due to exponentiation by squaring) that supports +ve and -ve modulus.

    Arguments:
    - base (int): can be negative
    - exponent (int): can be negative
    - modulus (int): can be positive or negative

    Returns:
    - result (int): satisfies result ≡ base^exponent (mod abs(modulus))
      and result lies in [0, modulus) if modulus > 0,
      or in [modulus, 0) if modulus < 0.

    Notes:
    - If base is negative, it is reduced modulo 'modulus' before computation.
    - If exponent is negative, the modular inverse of the base is used.
    - Returns 0 immediately if modulus is 1 (trivial group).
    - Considers 0^0 as 1, like Python's built-in pow(base, exponent, modulus).

    Raises:
    - TypeError if any argument is not an int.
    - ValueError if modulus == 0 or modular inverse does not exist for negative exponent.
    """
    
    if not all(isinstance(x, int) for x in (base, exponent, modulus)):
        raise TypeError("All arguments must be integers")

    if modulus == 0:
        raise ValueError("Modulus must be non-zero")
    
    abs_modulus = abs(modulus)
    
    # Trivial case
    if abs_modulus == 1:
        return 0

    # Special case: 0^0 mod ±m is defined as ±1 mod m; saves computation
    if base == 0 and exponent == 0:
        return 1 % abs_modulus if modulus > 0 else -1 % abs_modulus

    base_reduced = base % abs_modulus

    # Handle negative exponent
    if exponent < 0:
        base_reduced = modular_inverse(base, base_reduced, abs_modulus)
        exponent = -exponent

    result = 1
    while exponent > 0:
        if exponent & 1:  # if exp is odd (bitwise AND check for least sig. bit)
            result = (result * base_reduced) % abs_modulus
        base_reduced = (base_reduced * base_reduced) % abs_modulus
        exponent >>= 1  # division by 2 (bitwise right shift by 1)

    if modulus < 0 and result != 0:
        result -= abs_modulus

    return result