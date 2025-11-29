import unittest
import math

def solve_quadratic(a, b, c):
    discriminant = b*b - 4*a*c
    result = {"discriminant": discriminant}
    
    if discriminant >= 0:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        result["x1"] = round(x1, 3)
        result["x2"] = round(x2, 3)
    
    return result

# Тесты
class TestQuadraticSolver(unittest.TestCase):
    
    def test_two_roots(self):
        """Тест уравнения с двумя корнями: x² - 3x + 2 = 0"""
        result = solve_quadratic(1, -3, 2)
        self.assertEqual(result["discriminant"], 1)
        self.assertEqual(result["x1"], 2.0)
        self.assertEqual(result["x2"], 1.0)
    
    def test_one_root(self):
        """Тест уравнения с одним корнем: x² - 2x + 1 = 0"""
        result = solve_quadratic(1, -2, 1)
        self.assertEqual(result["discriminant"], 0)
        self.assertEqual(result["x1"], 1.0)
        self.assertEqual(result["x2"], 1.0)
    
    def test_no_real_roots(self):
        """Тест уравнения без действительных корней: x² + x + 1 = 0"""
        result = solve_quadratic(1, 1, 1)
        self.assertEqual(result["discriminant"], -3)
        self.assertNotIn("x1", result)  # или проверить что корней нет
        self.assertNotIn("x2", result)
    
    def test_negative_coefficients(self):
        """Тест с отрицательными коэффициентами: -x² + 4x - 3 = 0"""
        result = solve_quadratic(-1, 4, -3)
        self.assertEqual(result["discriminant"], 4)
        self.assertEqual(result["x1"], 1.0)
        self.assertEqual(result["x2"], 3.0)

# Запуск тестов при выполнении файла
if __name__ == '__main__':
    print("Запуск тестов...")
    unittest.main()