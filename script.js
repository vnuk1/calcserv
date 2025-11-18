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
            const a = parseFloat(document.getElementById('a').value);
            const b = parseFloat(document.getElementById('b').value);
            const c = parseFloat(document.getElementById('c').value);
            const D = b*b - 4*a*c;
            const x1 = (-b + Math.sqrt(D)) / (2*a);
            const x2 = (-b - Math.sqrt(D)) / (2*a);
            document.getElementById('result').innerHTML = `x₁ = ${x1}<br>x₂ = ${x2}`;
        }
        else if (text === 'C') input.value = '0';
        else if (text === '-') input.value = input.value.startsWith('-') ? input.value.slice(1) : '-' + input.value;
        else input.value = input.value === '0' ? text : input.value + text;
    };
});

document.getElementById('a').style.borderColor = 'red';