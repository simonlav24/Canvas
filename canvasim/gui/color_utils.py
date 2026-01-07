

def lighten(color: tuple[int, int, int], amount: int=20) -> tuple[int, int, int]:
    r = min(int(color[0] + amount), 255)
    g = min(int(color[1] + amount), 255)
    b = min(int(color[2] + amount), 255)
    return (r, g, b)