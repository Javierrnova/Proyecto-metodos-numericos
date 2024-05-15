from flask import Flask, request, render_template_string
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from sympy.core.sympify import SympifyError

app = Flask(__name__)

# Página principal con formulario para ingresar los datos
formulario_html = '''
<h1> Metodo de Bisección</h1>
<body style="background-color:D9CECB;">
</body>
    <form method="post">
        <label>Introduce la función f(x):</label>
        <input type="text" name="funcion_f" placeholder="x**2 - 2*x - 5"><br>
        <h2></h2>
        <label>Introduce el límite inferior (a):</label>
        <input type="text" name="limite_inferior" placeholder="1"><br>
        <h2></h2>
        <label>Introduce el límite superior (b):</label>
        <input type="text" name="limite_superior" placeholder="5"><br>
        <input type="submit" value="Calcular">
    </form>

'''

@app.route('/biseccion', methods=['GET', 'POST'])
def metodo_biseccion():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            funcion_f_str = request.form['funcion_f']
            limite_inferior_str = request.form['limite_inferior']
            limite_superior_str = request.form['limite_superior']
            
            # Convertir la función a expresión simbólica y validar límites
            f = sp.sympify(funcion_f_str)
            a = float(limite_inferior_str)
            b = float(limite_superior_str)

            # Comprobar que f(a) y f(b) tienen signos opuestos
            f_lambda = sp.lambdify(sp.symbols('x'), f, 'numpy')
            if f_lambda(a) * f_lambda(b) >= 0:
                return 'El intervalo no es válido o no tiene  raiz, cambiar intervalo.', 400
            
            # Método de bisección
            tolerancia = 0.00001
            iteraciones = []
            while abs(b - a) >= tolerancia:
                c = (a + b) / 2
                iteraciones.append(c)

                if f_lambda(c) == 0:
                    break  # Encontramos una raíz exacta

                if f_lambda(a) * f_lambda(c) < 0:
                    b = c
                else:
                    a = c
            
            # Resultado de la raíz aproximada
            raiz_aproximada = (a + b) / 2
            
            # Crear la gráfica
            x = np.linspace(min(a, b) - 1, max(a, b) + 1, 100)
            plt.figure()
            plt.plot(x, f_lambda(x), label="f(x)")
            plt.axhline(y=0, color='black', linestyle='-', linewidth=2, label="Eje X")
            plt.axvline(x=0, color='black', linestyle='--', linewidth=2, label="Eje Y")
            plt.plot(raiz_aproximada, f_lambda(raiz_aproximada), 'o', color='red', label=f"Raíz: {raiz_aproximada:.5f}")
            plt.title("Grafica de metodo de Bisección con Raíz")
            plt.xlabel("x")
            plt.ylabel("f(x)")
            plt.legend()
            plt.grid()

            # Guardar la imagen en un buffer de memoria para mostrarla en la web
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png')
            plt.close()
            img_buffer.seek(0)

            # Codificar la imagen en base64 para mostrarla en HTML
            img_data = base64.b64encode(img_buffer.read()).decode('utf-8')

            return f'''<p>Raíz aproximada: {raiz_aproximada}</p>
                    <body style="background-color:D9CECB;">
                    <img src="data:image/png;base64,{img_data}" alt="Gráfica de raíz">'''
        
        except SympifyError:
            return 'Error al interpretar la función ingresada. Inténtalo de nuevo.', 400
        except ValueError:
            return 'Límites no válidos. Deben ser números.', 400
    else:
        return formulario_html

if __name__ == '__main__':
    app.run(debug=True)