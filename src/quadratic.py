import math
import cmath


def solve_quadratic(a: float, b: float, c: float) -> list:
    """
    Решает квадратное уравнение вида ax² + bx + c = 0.
    
    Args:
        a: коэффициент при x²
        b: коэффициент при x  
        c: свободный член
        
    Returns:
        list: список корней уравнения.
              Возможные варианты:
              - []: нет решений
              - ['Любое число']: бесконечное число решений
              - [x]: один корень
              - [x1, x2]: два корня (могут быть комплексными)
    """
    # Линейное уравнение (a = 0)
    if a == 0:
        if b == 0:
            if c == 0:
                return ["Любое число"], 0.0  # 0 = 0
            else:
                return [], 0.0  # c = 0, но c ≠ 0
        else:
            x = -c / b
            return [x], 0.0
    
    # Квадратное уравнение
    discriminant = b**2 - 4*a*c  # дискриминант
    
    if discriminant > 0:
        # Два действительных корня
        x1 = (-b - math.sqrt(discriminant)) / (2*a)
        x2 = (-b + math.sqrt(discriminant)) / (2*a)
        return [x1, x2], discriminant
    
    elif discriminant < 0:
        # Два комплексных корня
        x1 = (-b - cmath.sqrt(discriminant)) / (2*a)
        x2 = (-b + cmath.sqrt(discriminant)) / (2*a)
        return [x1, x2], discriminant
    
    else:  # discriminant == 0
        # Один корень
        x = -b / (2*a)
        return [x], discriminant