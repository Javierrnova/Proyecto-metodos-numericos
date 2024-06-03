document.addEventListener('DOMContentLoaded', () => {
    const display = document.getElementById('calc-display');
    const funcionFInput = document.getElementById('funcion_f');
    const funcionGInput = document.getElementById('funcion_g');
    let activeInput = null;
    display.focus();

    funcionFInput.addEventListener('focus', () => {
        activeInput = funcionFInput;
    });

    funcionGInput.addEventListener('focus', () => {
        activeInput = funcionGInput;
    });

    window.appendToDisplay = function(value) {
        const input = document.getElementById('calc-display');
        const startPos = input.selectionStart;
        const endPos = input.selectionEnd;
        const currentValue = input.value;

        // Insertar el valor en la posición actual del cursor
        input.value = currentValue.substring(0, startPos) + value + currentValue.substring(endPos);

        // Colocar el cursor al final del valor insertado
        input.setSelectionRange(startPos + value.length, startPos + value.length);
        if (value === 'sqrt(') {
            input.value += ')';
            // Mover el cursor después del paréntesis de cierre
            input.setSelectionRange(startPos + value.length + 1, startPos + value.length + 1);
        }
        // Renderizar LaTeX
        renderLatex();
    }
    
    window.clearDisplay = function() {
        display.value = '';
    };

    window.appendToFunction = function() {
        if (activeInput) {
            let value = display.value;
            activeInput.value = value;
        } else {
            alert('Por favor, seleccione un campo de función para agregar el valor.');
        }
        clearDisplay();
    };
    
    window.transformInputValues = function() {
        funcionFInput.value = funcionFInput.value.replace(/\\sqrt\{([^}]*)\}/g, 'sqrt($1)').replace(/\^/g, '**');
        funcionGInput.value = funcionGInput.value.replace(/\\sqrt\{([^}]*)\}/g, 'sqrt($1)').replace(/\^/g, '**');
        return true;
    };


    window.renderLatex = function() {
        const input = document.getElementById('calc-display').value;
        const latexRendered = document.getElementById('latex-rendered');
    
        // Mapear los valores visibles en la calculadora a los valores para LaTeX
        const latexValueMap = {
            '**': '^',
            'sqrt(': '\\sqrt{',
            ')': '}',
        };
    
        // Reemplazar los valores en el input por sus correspondientes LaTeX
        let latexString = input;
        for (const [key, value] of Object.entries(latexValueMap)) {
            latexString = latexString.split(key).join(value);
        }
    
        // Manejar los valores dentro de sqrt()
        const sqrtIndex = latexString.lastIndexOf('\\sqrt{');
        if (sqrtIndex !== -1) {
            const closingParenIndex = latexString.indexOf(')', sqrtIndex);
            if (closingParenIndex !== -1) {
                // Extraer el contenido dentro de sqrt()
                const sqrtContent = latexString.substring(sqrtIndex + 6, closingParenIndex);
                // Procesar el contenido dentro de sqrt() como LaTeX
                const sqrtContentProcessed = processSqrtContent(sqrtContent);
                // Reemplazar el contenido dentro de sqrt() con su versión procesada
                latexString = latexString.substring(0, sqrtIndex + 6) + sqrtContentProcessed + latexString.substring(closingParenIndex);
            }
        }
        // Verificar si el superíndice (^) está seguido de un número o expresión válida
        latexString = latexString.replace(/\^(\D|$)/g, '^{ }$1');
    
        latexRendered.innerHTML = `\\[${latexString}\\]`;
        MathJax.typesetPromise([latexRendered]);
    }
    

    // Función para mover el cursor a la izquierda
    window.moveCursorLeft = function() {
        const input = document.getElementById('calc-display');
        const currentPosition = input.selectionStart;
        if (currentPosition > 0) {
            input.setSelectionRange(currentPosition - 1, currentPosition - 1);
            updateCursorHighlight(input, currentPosition - 1);
        }
    };

    // Función para mover el cursor a la derecha
    window.moveCursorRight = function() {
        const input = document.getElementById('calc-display');
        const currentPosition = input.selectionStart;
        const totalLength = input.value.length;
        if (currentPosition < totalLength) {
            input.setSelectionRange(currentPosition + 1, currentPosition + 1);
            updateCursorHighlight(input, currentPosition + 1);
        }
    };

    // Función para borrar el último carácter
    window.deleteLastChar = function() {
        const input = document.getElementById('calc-display');
        const startPos = input.selectionStart;
        const endPos = input.selectionEnd;
        let currentValue = input.value;

        // Verificar si la expresión LaTeX es igual a \sqrt{} o ^{}
        const isSqrt = currentValue.endsWith('\\sqrt{}');
        const isExponent = currentValue.endsWith('^{}');
        const isDoubleAsterisk = currentValue.endsWith('**');
        const isSqrtFunction = currentValue.endsWith('sqrt()');

        if (isSqrt || isExponent|| isDoubleAsterisk || isSqrtFunction) {
            // Borrar toda la expresión LaTeX
            input.value = '';
        } else {
            // Borrar el último carácter
            currentValue = currentValue.substring(0, startPos - 1) + currentValue.substring(endPos);
            input.value = currentValue;
        }

        // Renderizar LaTeX
        renderLatex();
    };

   
});