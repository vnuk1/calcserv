import json
import sys
import math

input_data = sys.stdin.read()

data = json.loads(input_data)
a = float(data['a'])
b = float(data['b']) 
c = float(data['c'])
    
discriminant = b*b - 4*a*c
    
result = {
    "discriminant": discriminant
}
    
if discriminant >= 0:
    x1 = (-b + math.sqrt(discriminant)) / (2*a)
    x2 = (-b - math.sqrt(discriminant)) / (2*a)
    result["x1"] = round(x1, 3)
    result["x2"] = round(x2, 3)
else:
    result = {
        "error": "Нет действительных корней"
    }

print("Content-type: application/json\n")
print(json.dumps(result))