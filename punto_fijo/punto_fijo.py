from flask import Flask, request, render_template
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from sympy.core.sympify import SympifyError

app = Flask(__name__)

@app.route('/puntofijo', methods=['GET', 'POST'])
def calcular_raiz():
    if request.method == 'POST':
        try:
            funcion_f_str = request.form['funcion_f']
            funcion_g_str = request.form['funcion_g']
            valor_inicial_str = request.form['valor_inicial']
            
            f = sp.sympify(funcion_f_str)
            g = sp.sympify(funcion_g_str)
            xi = float(valor_inicial_str)

            f_lambda = sp.lambdify(sp.symbols('x'), f, 'numpy')
            g_lambda = sp.lambdify(sp.symbols('x'), g, 'numpy')

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

            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png')
            plt.close()
            img_buffer.seek(0)

            img_data = base64.b64encode(img_buffer.read()).decode('utf-8')

            return render_template('punto_fijo_result.html', raiz_aproximada=xn, img_data=img_data)
        
        except SympifyError:
            return 'Error en las funciones ingresadas. Inténtalo de nuevo.', 400
        except ValueError:
            return 'Valor inicial no válido. Inténtalo de nuevo.', 400
    else:
        return render_template('punto_fijo_form.html')

if __name__ == '__main__':
    app.run(debug=True)