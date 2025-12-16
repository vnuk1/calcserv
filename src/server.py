from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import os

# Получаем корневую папку проекта
PROJECT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
UI_DIR = os.path.join(PROJECT_ROOT, 'ui')  # Папка с фронтендом
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')  # Папка с Python кодом

# Добавляем src в путь Python
sys.path.insert(0, SRC_DIR)

from quadratic import solve_quadratic
from json_parser import parse_request, create_response


class QuadraticHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Обработка GET запросов - отдаём HTML, CSS и JS файлы"""
        # Определяем, что отправляем в браузер (html css js)
        if self.path == '/':
            filename = 'index.html'
            content_type = 'text/html'
        elif self.path == '/styles.css':
            filename = 'styles.css'
            content_type = 'text/css'
        elif self.path == '/script.js':
            filename = 'script.js'
            content_type = 'application/javascript'
        else:
            self.send_error(404, "Not found")
            return
        
        # Путь к файлам внутри папки ui
        full_file_path = os.path.join(UI_DIR, filename)
        
        # Если любой файл в папке ui не найден-ошибка 404
        if not os.path.exists(full_file_path):
            self.send_error(404, f"{filename} not found")
            return
        
        # Читаем файлы в бинарном режиме и отправляем
        try:
            with open(full_file_path, 'rb') as file:
                file_content = file.read()
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.end_headers()
            self.wfile.write(file_content)

        # Обработка ошибок   
        except FileNotFoundError:
            self.send_error(404, f"{filename} not found")
        except PermissionError:
            self.send_error(403, f"No access to {filename}")
        except Exception as error:
            self.send_error(500, f"Server error: {str(error)}")
    

    def do_POST(self):
        """Обработка POST запросов"""
        try:
            if self.path != '/calculate?quadratic':
                self.send_error(404, "Use POST /calculate?quadratic")
                return
            
            # Читаем запрос
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            # Парсим коэффиценты из json
            a, b, c = parse_request(body)
            
            if a is None or b is None or c is None:
                self.send_error(400, "Invalid request")
                return
            
            # Используем функцию из quadratic.py
            roots, discriminant = solve_quadratic(a, b, c)
            
            # Создаем ответ в формате json при помощи функции из парсера
            response = create_response(roots, discriminant)
            
            # Отправляем ответ
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")


if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), QuadraticHandler)
    print("Server: http://localhost:8000")
    server.serve_forever()