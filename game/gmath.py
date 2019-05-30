
def sign(n):
    """Returns:
    1 if n > 0
    0 if n == 0
    -1 if n < 0
    """
    if n == 0:
        return 0
    return 1 if n > 0 else -1
