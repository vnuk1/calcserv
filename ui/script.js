let current = 'a';

document.querySelectorAll('.btn').forEach(btn => {
    btn.onclick = function() {
        const text = this.textContent;
        const input = document.getElementById(current);
        
        if (text === 'Следующий') {
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
        a: a,
        b: b,
        c: c
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
        
        // Простой вывод результатов
        if (result.error) {
            document.getElementById('result').innerHTML = `Ошибка: ${result.error}`;
        } else {
            let html = `Дискриминант: D = ${result.discriminant}<br>`;
            
            if (result.x1 && result.x2) {
                html += `Корни: x₁ = ${result.x1}, x₂ = ${result.x2}`;
            } else if (result.x1) {
                html += `Корень: x = ${result.x1}`;
            } else {
                html += `Действительных корней нет`;
            }
            
            document.getElementById('result').innerHTML = html;
        }
        
    } catch (error) {
        document.getElementById('result').innerHTML = `Ошибка: ${error.message}`;
    }
}

document.getElementById('a').style.borderColor = 'red';