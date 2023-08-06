def is_numeric(x):
    if isinstance(x, float): return True
    if isinstance(x, int): return True
    if isinstance(x, str): return x.isnumeric()
    return False
