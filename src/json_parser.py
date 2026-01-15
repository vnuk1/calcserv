"""
Модуль обработки и валидации JSON-данных.

Обеспечивает корректную конвертацию входящих HTTP-запросов в объекты Python
и подготовку вычисленных результатов (включая комплексные числа) для 
отправки обратно клиенту в формате JSON.
"""
import json
import logging


# Настройка логирования
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def parse_request(json_string):
    """
    Парсит запрос из json от клиента.
    
    Пример запроса:
    {
        "params": {
            "a": 1,
            "b": -5, 
            "c": 6
        }
    }
    
    Возвращает:
        (a, b, c) или (None, None, None) при ошибке
    """
    try:
        # Парсим весь json
        data = json.loads(json_string)

    except json.JSONDecodeError as err:
        # Логируем ошибку парсинга JSON
        logger.warning(f"Ошибка парсинга JSON: {err}")
        return None, None, None
    
    except Exception as err:
        # Ловим любые другие неожиданные ошибки
        logger.error(f"Неожиданная ошибка при парсинге JSON: {err}")
        return None, None, None
    

    if "params" not in data:
        logger.warning("Отсутствует ключ 'params' в JSON запросе")
        return None, None, None
        
    # Извлекаем только коэффиценты
    params = data["params"]

    # Проверяем наличие всех необходимых коэффициентов
    missing_coefficients = []
    if "a" not in params:
        missing_coefficients.append("a")
    if "b" not in params:
        missing_coefficients.append("b")
    if "c" not in params:
        missing_coefficients.append("c")
    
    if missing_coefficients:
        logger.warning(f"Отсутствуют коэффициенты: {', '.join(missing_coefficients)}")
        return None, None, None

    try:    
        # Превращаем в числа
        a = float(params["a"])
        b = float(params["b"])
        c = float(params["c"])

        return a, b, c
    
    except ValueError as err:
        # Если коэффициенты не являются числами
        logger.warning(f"Коэффициенты не являются числами: {err}")
        return None, None, None
        
    except TypeError as err:
        # Если тип данных неправильный (например, None)
        logger.warning(f"Неправильный тип данных коэффициентов: {err}")
        return None, None, None


def create_response(roots, discriminant, error = None):
    """
    Парсит ответ в json для клиента.

    Пример ответа:
    {
        "result": {
            "roots": [корень1, корень2] или [],
            "discriminant": число,
            "message": "успех или описание"
        },
        "error": null или "текст ошибки"
    }
    """
    # Автоматически определяем сообщение на основе результатов
    if roots == ["Любое число"]:
        message = "Успех! Бесконечное число решений"
    elif len(roots) == 0:
        message = "Успех! Нет действительных корней"
    elif len(roots) == 1:
        message = "Успех! Один корень"
    else:  # len(roots) == 2
        message = "Успех! Два корня"

    # Преобразуем комплексные числа в строки, чтобы не было ошибки TypeError
    json_safe_roots = []
    for root in roots:
        if isinstance(root, complex):
            # Комплексное число -> строка
            # Используем стандартное строковое представление
            json_safe_roots.append(str(root))
        else:
            # Все остальное оставляем как есть
            json_safe_roots.append(root)

    # Собираем структуру ответа
    response_data = {
        "result": {
            "roots": json_safe_roots,
            "discriminant": discriminant,
            "message": message
        },
        "error": error
    }

    try:
        # Преобразуем в JSON строку
        return json.dumps(response_data, ensure_ascii=False)
        
    except TypeError as err:
        logger.error(f"TypeError: {err}")
        return error_response(f"Ошибка типа: {err}")
        
    except ValueError as err:
        logger.error(f"ValueError: {err}")
        return error_response(f"Ошибка значения: {err}")
    
    except Exception as err:
        logger.critical(f"Критическая ошибка: {type(err).__name__}: {err}")
        return error_response("Критическая ошибка")


def error_response(error_msg):
    """
    Создает простой ответ об ошибке.
    """
    return json.dumps({
        "result": {
            "roots": [],
            "discriminant": 0.0,
            "message": "Ошибка"
        },
        "error": error_msg
    }, ensure_ascii=False)