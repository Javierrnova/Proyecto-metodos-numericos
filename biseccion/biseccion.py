from flask import Flask, request, render_template
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from sympy.core.sympify import SympifyError

app = Flask(__name__)

@app.route('/biseccion', methods=['GET', 'POST'])
def metodo_biseccion():
    if request.method == 'POST':
        try:
            funcion_f_str = request.form['funcion_f']
            intervalo_a_str = request.form['intervalo_a']
            intervalo_b_str = request.form['intervalo_b']
            
            f = sp.sympify(funcion_f_str)
            a = float(intervalo_a_str)
            b = float(intervalo_b_str)

            f_lambda = sp.lambdify(sp.symbols('x'), f, 'numpy')
            if f_lambda(a) * f_lambda(b) >= 0:
                return 'El intervalo no es válido o no tiene raíz, cambiar intervalo.', 400
            
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
            
            raiz_aproximada = (a + b) / 2
            
            x = np.linspace(min(a, b) - 1, max(a, b) + 1, 100)
            plt.figure()
            plt.plot(x, f_lambda(x), label="f(x)")
            plt.axhline(y=0, color='black', linestyle='-', linewidth=2, label="Eje X")
            plt.axvline(x=0, color='black', linestyle='--', linewidth=2, label="Eje Y")
            plt.plot(raiz_aproximada, f_lambda(raiz_aproximada), 'o', color='red', label=f"Raíz: {raiz_aproximada:.5f}")
            plt.title("Gráfica del método de Bisección con Raíz")
            plt.xlabel("x")
            plt.ylabel("f(x)")
            plt.legend()
            plt.grid()

            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png')
            plt.close()
            img_buffer.seek(0)

            img_data = base64.b64encode(img_buffer.read()).decode('utf-8')

            return render_template('biseccion_result.html', raiz_aproximada=raiz_aproximada, img_data=img_data)
        
        except SympifyError:
            return 'Error al interpretar la función ingresada. Inténtalo de nuevo.', 400
        except ValueError:
            return 'Límites no válidos. Deben ser números.', 400
    else:
        return render_template('biseccion_form.html')

if __name__ == '__main__':
    app.run(debug=True)