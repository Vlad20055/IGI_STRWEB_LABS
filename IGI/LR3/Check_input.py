def is_int(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False  
     

def is_non_negative_int(s: str) -> bool:
    if (not is_int(s)): return False
    n = int(s)
    if(n < 0): return False
    return True


def is_float(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_abs_not_more_than_one(s: str) -> bool:
    if (not is_float(s)): return False
    f = float(s)
    if abs(f) > 1: return False
    return True
