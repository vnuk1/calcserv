"""
Тесты для quadratic.py
"""
import unittest
import sys
import os


# Добавляем путь к src для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
# Импортируем
from src.quadratic import solve_quadratic


class TestQuadraticBasic(unittest.TestCase):
    """Базовые тесты"""
    
    def test_two_real_roots(self):
        # Уравнение: x**2 + 5x + 6 = 0. Корни: -3.0 и -2.0.
        roots, discriminant = solve_quadratic(1, 5, 6)
        
        # Проверяем, что каждый из ожидаемых корней присутствует в списке roots
        self.assertEqual(len(roots), 2)
        self.assertAlmostEqual(roots[0], -3.0) 
        self.assertAlmostEqual(roots[1], -2.0)
        # Проверяем правильность типа данных
        self.assertTrue(isinstance(roots[0], float))  

        # Проверяем дискриминант
        self.assertAlmostEqual(discriminant, 1.0)

    def test_two_complex_roots(self):
        # Уравнение: x**2 + 0x + 1 = 0. Корни: -1j и 1j.
        roots, discriminant = solve_quadratic(1, 0, 1)
        
        # Проверяем, что каждый из ожидаемых корней присутствует в списке roots
        self.assertEqual(len(roots), 2)
        self.assertAlmostEqual(roots[0], -1j)
        self.assertAlmostEqual(roots[1], 1j)
        # Проверяем, что корни являются комплексными числами а не вещественными
        self.assertTrue(isinstance(roots[0], complex))

        # Проверяем дискриминант
        self.assertAlmostEqual(discriminant, -4.0) 
             
    def test_one_root(self):
        # Уравнение: x**2 + 2x + 1 = 0. Корень: -1.0.
        root, discriminant = solve_quadratic(1, 2, 1)
        
        # Проверяем, что корень в списке один и верен
        self.assertEqual(len(root), 1)
        self.assertAlmostEqual(root[0], -1.0)
        # Проверяем правильность типа данных
        self.assertTrue(isinstance(root[0], float)) 

        # Проверяем дискриминант
        self.assertAlmostEqual(discriminant, 0.0)  
        
    def test_no_roots(self):
        # Уравнение: 0*x**2 + 0x + 5 = 0. Корней нет.
        roots, discriminant = solve_quadratic(0, 0, 5)
        
        # Проверяем, что корней в списке нет
        self.assertEqual(len(roots), 0)
        self.assertEqual(roots, [])

        # Проверяем дискриминант
        self.assertAlmostEqual(discriminant, 0.0)  
        
    def test_any_roots(self):
        # Уравнение: 0*x**2 + 0x + 0 = 0. Корни: "Любое число".
        roots, discriminant = solve_quadratic(0, 0, 0)
        
        # Проверяем, выводится ли ответ "Любое число"
        self.assertEqual(len(roots), 1)
        self.assertEqual(roots[0], "Любое число")
        # Проверяем правильность типа данных
        self.assertTrue(isinstance(roots[0], str))

        # Проверяем дискриминант
        self.assertAlmostEqual(discriminant, 0.0)
        
    def test_linear_equation(self):
        # Уравнение: 0*x**2 + 2x - 4 = 0. Корень: 2.0.
        root, discriminant = solve_quadratic(0, 2, -4)
        
        # Проверяем, что корень в списке один и верен
        self.assertEqual(len(root), 1)
        self.assertAlmostEqual(root[0], 2.0)
        self.assertTrue(isinstance(root[0], float))

        # Проверяем дискриминант
        self.assertAlmostEqual(discriminant, 0.0)

class TestQuadraticExceptions(unittest.TestCase):
    """Тесты на обработку исключительных ситуаций"""
    
    def test_string_input_raises_error(self):
        # Проверяем, что передача строк вызывает ошибку TypeError
        with self.assertRaises(TypeError):
            solve_quadratic("1", "2", "3")
    
    def test_none_input_raises_error(self):
        # Проверяем, что передача None вызывает ошибку TypeError
        with self.assertRaises(TypeError):
            solve_quadratic(None, 2, 3)
            
if __name__ == '__main__':
    unittest.main()