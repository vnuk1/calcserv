"""
Модуль математических вычислений для решения квадратных уравнений.

Содержит универсальный алгоритм решения уравнений вида ax² + bx + c = 0,
включая обработку линейных случаев (a=0) и вычисление комплексных корней.
"""
import cmath

ResultType = str | float | complex
def solve_quadratic(a: float, b: float, c: float) -> tuple[list[ResultType], float]:
    """
    Решает квадратное уравнение вида ax² + bx + c = 0.
    
    Args:
        a: коэффициент при x²
        b: коэффициент при x  
        c: свободный член
        
    Returns:
        tuple[list, float]: Кортеж, содержащий список корней и значение дискриминанта.
              Варианты списка корней:
              - []: нет решений
              - ['Любое число']: бесконечное число решений
              - [x]: один корень (линейное уравнение или D=0)
              - [x1, x2]: два корня (действительные или комплексные)
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
    discriminant = b**2 - 4*a*c  # Дискриминант

    if discriminant == 0:
        # Один корень
        x = -b / (2*a)
        return [x], discriminant
    
    sqrt_d = cmath.sqrt(discriminant) # Квадратный корень дискриминанта
    x1 = (-b + sqrt_d) / (2 * a) # Первый корень
    x2 = (-b - sqrt_d) / (2 * a) # Второй корень
    
    roots = []
    for root in [x1, x2]:
        # Чистим от -0.0 и микро-ошибок
        r = 0.0 if cmath.isclose(root.real, 0, abs_tol=1e-9) else root.real
        i = 0.0 if cmath.isclose(root.imag, 0, abs_tol=1e-9) else root.imag

        if i == 0:
            # Сюда попадет и обычное число (2.0), и чистый ноль (0.0)
            roots.append(r)
        elif r == 0:
            # Сюда попадет чисто мнимое число (1j)
            roots.append(complex(0.0, i))
        else:
            # Сюда попадет смешанное число (1+2j)
            roots.append(complex(r, i))

    return roots, float(discriminant)