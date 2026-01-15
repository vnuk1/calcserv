"""
Тесты для модуля вычисления квадратных уравнений.

Данный набор тестов использует фреймворк Pytest для проверки корректности
математической логики, включая работу с комплексными числами и обработку ошибок.
"""
import sys
import os
import pytest
from pytest import approx

# Добавляем путь к src для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
# Импортируем
from src.quadratic import solve_quadratic


# Базовые тесты
@pytest.mark.parametrize("a, b, c, expected_roots, expected_d", [
    (1, 5, 6, [-3.0, -2.0], 1.0),       # Действительные
    (1, 0, 1, [1j, -1j], -4.0),         # Комплексные
    (1, 2, 1, [-1.0], 0.0),             # Один корень (discriminant == 0)
    (0, 0, 0, ["Любое число"], 0.0),    # Корень == Любое число
    (0, 0, 5, [], 0.0),                 # Нет корней
    (0, 3, 4, [-4 / 3], 0.0),           # Линейное уравнение
    (1.0, -2.0, 1.0, [1.0], 0.0),       # Вещественные коэффициенты
], ids=[
    "Two_Real_Roots",
    "Complex_Roots",
    "One_Root",
    "Any_Root",
    "No_Roots",
    "Linear_Equation",
    "Float_Coeff",
])
def test_solve_quadratic_logic(a, b, c, expected_roots, expected_d):
    """Тестирование корректности вычисления корней и дискриминанта."""
    roots, d = solve_quadratic(a, b, c)
    
    # Проверяем дискриминант
    assert d == approx(expected_d)
    # Проверяем количество корней
    assert len(roots) == len(expected_roots)
    # Проверяем наличие каждого корня (независимо от порядка)
    for exp in expected_roots:
        if isinstance(exp, (int, float, complex)):
            assert any(root == approx(exp) for root in roots)
        else:
            assert exp in roots

# Тесты на ошибки
@pytest.mark.parametrize("a, b, c", [
    ("1", 2, 3),                        # Строка вместо числа
    (None, 2, 3),                       # Отсутствие значения
    (1, [], 3),                         # Список вместо числа
    (1, 2, {}),                         # Словарь вместо числа
    (complex(1, 2), 2, 3),              # Комплексный КОЭФФИЦИЕНТ (наша функция ждет float на входе)
], ids=[
    "String_Input", 
    "None_Input", 
    "List_Input", 
    "Dict_Input", 
    "Complex_Coeff_Input",
])
def test_solve_quadratic_errors(a, b, c):
    """Проверка генерации исключений при некорректных типах или значениях входных данных."""
    with pytest.raises(TypeError):
        solve_quadratic(a, b, c)
