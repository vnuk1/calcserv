let current = 'a';

document.querySelectorAll('.btn').forEach(btn => {
    btn.onclick = function() {
        const text = this.textContent;
        const input = document.getElementById(current);
        
        if (text === 'Следующий') {
            document.getElementById(current).style.borderColor = '#4CAF50';
            current = current === 'a' ? 'b' : current === 'b' ? 'c' : 'a';
            document.getElementById(current).style.borderColor = 'red';
        }
        else if (text === 'Решить') {
            solveEquation();
        }
        else if (text === 'C') {
            input.value = '0';
        }
        else if (text === '-') {
            input.value = input.value.startsWith('-') ? input.value.slice(1) : '-' + input.value;
        }
        else {
            input.value = input.value === '0' ? text : input.value + text;
        }
    };
});

async function solveEquation() {
    const a = parseFloat(document.getElementById('a').value);
    const b = parseFloat(document.getElementById('b').value);
    const c = parseFloat(document.getElementById('c').value);
    
    const equationData = {
        params: {
            a: a,
            b: b,
            c: c
        }
    };
    
    try {
        document.getElementById('result').innerHTML = 'Вычисление...';
        
        const response = await fetch('/calculate?quadratic', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(equationData)
        });
        
        const result = await response.json();
        
        if (result.error) {
            document.getElementById('result').innerHTML = `Ошибка: ${result.error}`;
        } else {
            const roots = result.result.roots;
            const discriminant = result.result.discriminant;
            const message = result.result.message;

            let html = `<h3>${message}</h3>`;
            html += `<p><strong>Дискриминант:</strong> ${discriminant}</p>`;
            
            if (roots[0] === "Любое число") {
                html += `<p><strong>Корни:</strong> Любое число</p>`;
            } else if (roots.length === 0) {
                html += `<p><strong>Корни:</strong> Нет действительных корней</p>`;
            } else if (roots.length === 1) {
                html += `<p><strong>Корень:</strong> ${roots[0]}</p>`;
            } else {
                html += `<p><strong>Корни:</strong> ${roots[0]}, ${roots[1]}</p>`;
            }
            
            document.getElementById('result').innerHTML = html;
        }
        
    } catch (error) {
        document.getElementById('result').innerHTML = `Ошибка: ${error.message}`;
    }
}

// Начальное выделение поля 'a'
document.getElementById('a').style.borderColor = 'red';