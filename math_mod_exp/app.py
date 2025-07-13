def validate_inputs(base, exponent, modulus):
    """Validate input arguments for modular exponentiation."""
    if not all(isinstance(arg, int) for arg in (base, exponent, modulus)):
        raise TypeError("All arguments must be integers.")
    
    if modulus is None:
        raise TypeError("Modulus must not be None.")

    if modulus == 0:
        raise ValueError("Modulus must be non-zero.")


def handle_edge_cases(base, exponent, modulus):
    """Handle edge cases for modular exponentiation."""
    if abs(modulus) == 1:
        return 0
    
    if base == 0 and exponent == 0:
        return 1 % modulus
    
    return None


def extended_gcd(a, b):
    """Extended Euclidean Algorithm to compute the GCD and coefficients."""
    if b == 0:
        return a, 1, 0
    gcd, x_prev, y_prev = extended_gcd(b, a % b)
    x = y_prev
    y = x_prev - (a // b) * y_prev
    return gcd, x, y


def modular_inverse(base, modulus):
    """Computes the modular inverse of 'base' modulo 'modulus'."""
    gcd, inverse, inverse_other = extended_gcd(base % abs(modulus), abs(modulus))
    if gcd != 1:
        raise ValueError(f"No modular inverse exists for {base} modulo {modulus}.")
    return inverse % abs(modulus), inverse_other


def power_by_squaring(base_reduced, exponent, modulus):
    """Compute modular exponentiation using exponentiation by squaring."""
    interim_values = []
    
    result = 1
    interim_values.append((base_reduced, result))

    while exponent > 0:
        if exponent & 1:  # if exp is odd (bitwise AND check for least sig. bit)
            result = (result * base_reduced) % abs(modulus)
        base_reduced = (base_reduced * base_reduced) % abs(modulus)
        exponent >>= 1  # division by 2 (bitwise right shift by 1)

        interim_values.append((base_reduced, result))

    if modulus < 0 and result != 0:
        result -= abs(modulus)

    return result, interim_values


def modular_exp(base, exponent, modulus):
    
    """
    Efficient modular exponentiation (due to exponentiation by squaring) that supports +ve and -ve exponent, and +ve and -ve modulus, like pow().

    Arguments:
    - base (int)
    - exponent (int)
    - modulus (int): cannot be zero

    Returns:
    - result (int): satisfies result ≡ base^exponent (mod abs(modulus))
      and result lies in [0, modulus) if modulus > 0,
      or in [modulus, 0) if modulus < 0.
    - base_reduced (int): the first reduction of the base. Returned for testing app functionality.

    Notes:
    - If base is negative, it is reduced modulo 'modulus' before computation.
    - If exponent is negative, the modular inverse of the base is used.
    - If modulus is negative, result is adjusted to lie within the negative modular range [modulus, 0).
    - Returns 0 immediately if modulus is ±1 (trivial group).
    - Considers 0^0 as 1, like Python's built-in pow(base, exponent, modulus).

    Raises:
    - TypeError if any argument is not an int.
    - ValueError if modulus == 0 or modular inverse does not exist for negative exponent.
    """

    validate_inputs(base, exponent, modulus)

    base_reduced = base % modulus

    edge_result = handle_edge_cases(base, exponent, modulus)
    if edge_result is not None:
        return edge_result, base_reduced

    if exponent < 0:
        base_reduced = modular_inverse(base, modulus)[0]
        return power_by_squaring(base_reduced, -exponent, modulus)[0], base_reduced

    else:
        return power_by_squaring(base_reduced, exponent, modulus)[0], base_reduced