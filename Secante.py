from flask import Flask, request, render_template
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from sympy.core.sympify import SympifyError

app = Flask(__name__)

@app.route('/secante', methods=['GET', 'POST'])
def metodo_secante():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            funcion_f_str = request.form['funcion_f']
            x0_str = request.form['x0']
            x1_str = request.form['x1']
            
            # Convertir la función a expresión simbólica y validar los valores iniciales
            f = sp.sympify(funcion_f_str)
            x = sp.symbols('x')
            x0 = float(x0_str)
            x1 = float(x1_str)
            
            # Método de la secante
            f_lambda = sp.lambdify(x, f, 'numpy')
            n_iter = 0
            max_iter = 10
            tol = 1e-6
            
            secante_x_vals = []
            secante_y_vals = []
            
            while n_iter < max_iter:
                f_x0 = f_lambda(x0)
                f_x1 = f_lambda(x1)
                if abs(f_x1) < tol:
                    break
                if f_x0 == f_x1:
                    return "Error: Divisor cero. No se puede continuar."
                x_new = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
                if abs(x_new - x1) < tol:
                    break
                
                secante_x_vals.append([x0, x1])
                secante_y_vals.append([f_x0, f_x1])
                
                x0, x1 = x1, x_new
                n_iter += 1
            
            raiz_aproximada = x_new
            
            x_vals = np.linspace(raiz_aproximada - 2, raiz_aproximada + 2, 100)
            y_vals = f_lambda(x_vals)
            plt.figure()
            plt.plot(x_vals, y_vals, label="f(x)")
            plt.axhline(y=0, color='black', linestyle='-', linewidth=2, label="Eje X")
            plt.axvline(x=0, color='black', linestyle='--', linewidth=2, label="Eje Y")
            plt.plot(raiz_aproximada, f_lambda(raiz_aproximada), 'o', color='red', label=f"Raíz: {raiz_aproximada:.5f}")
            
            for sec_x_vals, sec_y_vals in zip(secante_x_vals, secante_y_vals):
                plt

                plt.plot(sec_x_vals, sec_y_vals, 'g--', alpha=0.5, label="Línea secante")
                
            plt.title("Gráfica del Método de la Secante con Raíz")
            plt.xlabel("x")
            plt.ylabel("f(x)")
            plt.legend()
            plt.grid()
            
            plt.ylim(bottom=min(y_vals) - 1, top=max(y_vals) + 1)
            
            function_str = f"$f(x) = {sp.latex(f)}$"
            plt.text(0.5, 0.95, function_str, ha='center', va='center', transform=plt.gca().transAxes, fontsize=10, bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=0.5'))
            
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png')
            plt.close()
            img_buffer.seek(0)
            
            img_data = base64.b64encode(img_buffer.getvalue()).decode()
            
            return render_template('secante_result.html', raiz_aproximada=raiz_aproximada, img_data=img_data)
        
        except SympifyError:
            return 'Error al interpretar la función ingresada. Inténtalo de nuevo.', 400
        except ValueError:
            return 'Valores iniciales no válidos. Inténtalo de nuevo.', 400
    else:
        return render_template('secante_form.html')

if __name__ == '__main__':
    app.run(debug=True)