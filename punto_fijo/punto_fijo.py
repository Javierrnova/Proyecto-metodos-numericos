from flask import Flask, request, render_template_string
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Página principal con formulario para ingresar los datos
formulario_html = '''
<h1> Punto Fijo</h1>
    <form method="post">
        <label>Introduce la función f(x):</label>
        <input type="text" name="funcion_f" placeholder="x**2 - 2*x - 5"><br>
         <h2></h2>
        <label>Introduce la función iterativa g(x):</label>
        <input type="text" name="funcion_g" placeholder="sqrt(2*x + 5)"><br>
         <h2></h2>
        <label>Introduce el valor inicial para la iteración:</label>
        <input type="text" name="valor_inicial" placeholder="2.0"><br>
        <input type="submit" value="Calcular">
    </form>
'''

@app.route('/puntofijo', methods=['GET', 'POST'])
def calcular_raiz():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            funcion_f_str = request.form['funcion_f']
            funcion_g_str = request.form['funcion_g']
            valor_inicial_str = request.form['valor_inicial']
            
            # Convertir a expresiones simbólicas y validar el valor inicial
            f = sp.sympify(funcion_f_str)
            g = sp.sympify(funcion_g_str)
            xi = float(valor_inicial_str)

            # Crear funciones lambda para el método de punto fijo
            f_lambda = sp.lambdify(sp.symbols('x'), f, 'numpy')
            g_lambda = sp.lambdify(sp.symbols('x'), g, 'numpy')

            # Iteración y método de punto fijo
            iteraciones = [xi]
            max_iteraciones = 1000
            convergencia = 0.00001

            for _ in range(max_iteraciones):
                xn = g_lambda(xi)
                iteraciones.append(xn)

                if abs(xn - xi) / xn < convergencia:
                    break

                xi = xn
            else:
                return 'Advertencia: límite máximo de iteraciones alcanzado.', 400

            # Crear la gráfica
            x = np.linspace(min(iteraciones) - 1, max(iteraciones) + 1, 100)
            plt.figure()
            plt.plot(x, f_lambda(x), label="f(x)")
            plt.axhline(y=0, color='black', linestyle='-', linewidth=2, label="Eje X")
            plt.axvline(x=0, color='black', linestyle='--', linewidth=2, label="Eje Y")
            plt.plot(xn, f_lambda(xn), 'o', color='red', label=f"Raíz: {xn:.5f}")
            plt.title("Grafica de Método de Punto Fijo con Raíz")
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

            return f'''<h3>Valor de la raíz aproximada: {xn}</h3>
                    <img src="data:image/png;base64,{img_data}" alt="Gráfica de raíz">'''
        
        except SympifyError:
            return 'Error en las funciones ingresadas. Inténtalo de nuevo.', 400
        except ValueError:
            return 'Valor inicial no válido. Inténtalo de nuevo.', 400
    else:
        return formulario_html

if __name__ == '__main__':
    app.run(debug=True)