"""
Тесты для модуля json_parser.py
"""

import unittest
import sys
import os
import json
import logging

# Отключаем логирование в тестах
logging.disable(logging.CRITICAL)

# Добавляем путь к src для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
# Импортируем
from src.json_parser import parse_request, create_response, error_response


class TestParseRequest(unittest.TestCase):
    """Тесты для функции parse_request"""
    
    def test_valid_request(self):
        json_str = '{"params": {"a": 1, "b": -5, "c": 6}}'
        a, b, c = parse_request(json_str)
        
        self.assertEqual(a, 1.0)
        self.assertEqual(b, -5.0)
        self.assertEqual(c, 6.0)
    
    def test_valid_request_with_floats(self):
        json_str = '{"params": {"a": 1.5, "b": -2.5, "c": 0.75}}'
        a, b, c = parse_request(json_str)
        
        self.assertEqual(a, 1.5)
        self.assertEqual(b, -2.5)
        self.assertEqual(c, 0.75)
    
    def test_valid_request_string_numbers(self):
        json_str = '{"params": {"a": "1", "b": "-5", "c": "6"}}'
        a, b, c = parse_request(json_str)
        
        self.assertEqual(a, 1.0)
        self.assertEqual(b, -5.0)
        self.assertEqual(c, 6.0)
    
    def test_missing_params_key(self):
        json_str = '{"a": 1, "b": -5, "c": 6}'
        result = parse_request(json_str)
        
        self.assertEqual(result, (None, None, None))
    
    def test_missing_coefficient(self):
        json_str = '{"params": {"a": 1, "b": -5}}'  # нет 'c'
        result = parse_request(json_str)
        
        self.assertEqual(result, (None, None, None))
    
    def test_invalid_json(self):
        json_str = 'не json строка'
        result = parse_request(json_str)
        
        self.assertEqual(result, (None, None, None))
    
    def test_empty_json(self):
        json_str = '{}'
        result = parse_request(json_str)
        
        self.assertEqual(result, (None, None, None))
    
    def test_non_numeric_coefficient(self):
        json_str = '{"params": {"a": "текст", "b": -5, "c": 6}}'
        result = parse_request(json_str)
        
        self.assertEqual(result, (None, None, None))
    
    def test_null_coefficient(self):
        json_str = '{"params": {"a": null, "b": -5, "c": 6}}'
        result = parse_request(json_str)
        
        self.assertEqual(result, (None, None, None))
    
    def test_extra_fields_ignored(self):
        json_str = '{"params": {"a": 1, "b": -5, "c": 6, "d": 10}}'
        a, b, c = parse_request(json_str)
        
        self.assertEqual(a, 1.0)
        self.assertEqual(b, -5.0)
        self.assertEqual(c, 6.0)


class TestCreateResponse(unittest.TestCase):
    """Тесты для функции create_response"""
    
    def test_two_real_roots(self):
        roots = [2.0, 3.0]
        discriminant = 1.0
        response = create_response(roots, discriminant)
        
        # Парсим обратно для проверки структуры
        data = json.loads(response)
        
        self.assertEqual(data["result"]["roots"], roots)
        self.assertEqual(data["result"]["discriminant"], discriminant)
        self.assertEqual(data["result"]["message"], "Успех! Два корня")
        self.assertIsNone(data["error"])
    
    def test_one_root(self):
        roots = [2.0]
        discriminant = 0.0
        response = create_response(roots, discriminant)
        
        data = json.loads(response)
        
        self.assertEqual(data["result"]["roots"], roots)
        self.assertEqual(data["result"]["discriminant"], discriminant)
        self.assertEqual(data["result"]["message"], "Успех! Один корень")
        self.assertIsNone(data["error"])
    
    def test_no_roots(self):
        roots = []
        discriminant = -4.0
        response = create_response(roots, discriminant)
        
        data = json.loads(response)
        
        self.assertEqual(data["result"]["roots"], roots)
        self.assertEqual(data["result"]["discriminant"], discriminant)
        self.assertEqual(data["result"]["message"], "Успех! Нет действительных корней")
        self.assertIsNone(data["error"])
    
    def test_complex_roots(self):
        roots = [-1j, 1j]  # x² + 1 = 0
        discriminant = -4.0
        response = create_response(roots, discriminant)
        
        data = json.loads(response)
        
        # Ожидаем строковое представление
        expected_roots = [("(-0-1j)"), ("1j")]
        self.assertEqual(data["result"]["roots"], expected_roots)
        self.assertEqual(data["result"]["discriminant"], discriminant)
        self.assertEqual(data["result"]["message"], "Успех! Два корня")
        self.assertIsNone(data["error"])
    
    def test_infinite_solutions(self):
        roots = ["Любое число"]
        discriminant = 0.0
        response = create_response(roots, discriminant)
        
        data = json.loads(response)
        
        self.assertEqual(data["result"]["roots"], roots)
        self.assertEqual(data["result"]["discriminant"], discriminant)
        self.assertEqual(data["result"]["message"], "Успех! Бесконечное число решений")
        self.assertIsNone(data["error"])
    
    def test_with_error(self):
        roots = []
        discriminant = 0.0
        error_msg = "Неверный формат запроса"
        response = create_response(roots, discriminant, error_msg)
        
        data = json.loads(response)
        
        self.assertEqual(data["result"]["roots"], roots)
        self.assertEqual(data["result"]["discriminant"], discriminant)
        self.assertEqual(data["result"]["message"], "Успех! Нет действительных корней")
        self.assertEqual(data["error"], error_msg)
    
    def test_mixed_real_complex_roots(self):
        roots = [2.0, 1+2j]
        discriminant = -16.0
        response = create_response(roots, discriminant)
        
        data = json.loads(response)
        
        expected_roots = [2.0, "(1+2j)"]
        self.assertEqual(data["result"]["roots"], expected_roots)

    def test_empty_roots_with_error(self):
        response = create_response([], 0.0, "Ошибка")
        data = json.loads(response)
        
        self.assertEqual(data["result"]["roots"], [])
        self.assertEqual(data["error"], "Ошибка")


class TestErrorResponse(unittest.TestCase):
    """Тесты для функции error_response"""
    
    def test_error_response_structure(self):
        error_msg = "Тестовая ошибка"
        response = error_response(error_msg)
        
        data = json.loads(response)
        
        self.assertEqual(data["result"]["roots"], [])
        self.assertEqual(data["result"]["discriminant"], 0.0)
        self.assertEqual(data["result"]["message"], "Ошибка")
        self.assertEqual(data["error"], error_msg)
    
    def test_error_response_empty_string(self):
        response = error_response("")
        data = json.loads(response)
        
        self.assertEqual(data["error"], "")
    
    def test_error_response_special_chars(self):
        error_msg = 'Ошибка с кавычками: "текст" и \\n переносом'
        response = error_response(error_msg)
        
        # Должен создаться валидный JSON
        data = json.loads(response)
        self.assertEqual(data["error"], error_msg)


class TestFullCycle(unittest.TestCase):
    """Тесты с полным циклом парсинга запроса и создания ответа"""
    
    def test_parse_and_create_response(self):
        # Входной запрос
        request_json = '{"params": {"a": 1, "b": -5, "c": 6}}'
        
        # Парсим
        a, b, c = parse_request(request_json)
        self.assertEqual((a, b, c), (1.0, -5.0, 6.0))
        
        # "Решаем уравнение" (тестовые корни)
        roots = [2.0, 3.0]
        discriminant = 1.0
        
        # Создаем ответ
        response_json = create_response(roots, discriminant)
        
        # Проверяем ответ
        data = json.loads(response_json)
        self.assertEqual(data["result"]["roots"], roots)
        self.assertEqual(data["result"]["discriminant"], discriminant)
        self.assertEqual(data["result"]["message"], "Успех! Два корня")
    
    def test_wrong_input_json(self):
        # Неправильный входной запрос
        request_json = '{"params": {"a": 1, "b": -5}}'  # нет 'c'
        
        # Парсим (должна быть ошибка)
        a, b, c = parse_request(request_json)
        self.assertEqual((a, b, c), (None, None, None))
        
        # Создаем ответ с ошибкой
        response_json = create_response([], 0.0, "Неверный формат запроса")
        
        # Проверяем ответ
        data = json.loads(response_json)
        self.assertEqual(data["error"], "Неверный формат запроса")
    
if __name__ == '__main__':
    unittest.main()