from flask import Flask, request
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from sympy.core.sympify import SympifyError

app = Flask(__name__)

# Página principal con formulario para ingresar los datos
formulario_html = '''
<h1> Método de Newton-Raphson</h1>
<body style="background-color:D9CECB;">
    <form method="post">
        <label>Introduce la función f(x):</label>
        <input type="text" name="funcion_f" placeholder="x**2 - 2*x - 5"><br>
        <h2></h2>
        <label>Introduce el valor inicial (x0):</label>
        <input type="text" name="valor_inicial" placeholder="2"><br>
        <input type="submit" value="Calcular">
    </form>
'''

@app.route('/newton', methods=['GET', 'POST'])
def metodo_newton():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            funcion_f_str = request.form['funcion_f']
            valor_inicial_str = request.form['valor_inicial']
            
            # Convertir la función a expresión simbólica y validar el valor inicial
            f = sp.sympify(funcion_f_str)
            x = sp.symbols('x')
            x0 = float(valor_inicial_str)
            
            # Calcular la derivada de la función
            df = sp.diff(f, x)
            
            # Método de Newton-Raphson
            f_lambda = sp.lambdify(x, f, 'numpy')
            df_lambda = sp.lambdify(x, df, 'numpy')
            n_iter = 0
            max_iter = 10  # Limitar el número de iteraciones para evitar gráficos demasiado complejos
            tol = 1e-6
            
            # Listas para almacenar los datos de las rectas tangentes
            tangents_x_vals = []
            tangents_y_vals = []
            
            while n_iter < max_iter:
                f_value = f_lambda(x0)
                if abs(f_value) < tol:
                    break
                df_value = df_lambda(x0)
                if df_value == 0:
                    return "Error: Derivada igual a cero. No se puede continuar."
                x_new = x0 - f_value / df_value
                if abs(x_new - x0) < tol:
                    break
                
                # Añadir datos de la recta tangente entre los puntos de iteración
                tangent_x_vals = np.linspace(x0, x_new, 100)
                tangent_y_vals = f_lambda(x0) + df_lambda(x0) * (tangent_x_vals - x0)
                tangents_x_vals.append(tangent_x_vals)
                tangents_y_vals.append(tangent_y_vals)
                
                x0 = x_new
                n_iter += 1
            
            # Resultado de la raíz aproximada
            raiz_aproximada = x_new
            
            # Crear la gráfica
            x_vals = np.linspace(raiz_aproximada - 2, raiz_aproximada + 2, 100)
            y_vals = f_lambda(x_vals)
            plt.figure()
            plt.plot(x_vals, y_vals, label="f(x)")
            plt.axhline(y=0, color='black', linestyle='-', linewidth=2, label="Eje X")
            plt.axvline(x=0, color='black', linestyle='--', linewidth=2, label="Eje Y")
            plt.plot(raiz_aproximada, f_lambda(raiz_aproximada), 'o', color='red', label=f"Raíz: {raiz_aproximada:.5f}")
            
            # Añadir todas las rectas tangentes al gráfico
            for tangent_x_vals, tangent_y_vals in zip(tangents_x_vals, tangents_y_vals):
                plt.plot(tangent_x_vals, tangent_y_vals, '-', label="Recta tangente", alpha=0.5)
                
            plt.title("Gráfica del Método de Newton-Raphson con Raíz")
            plt.xlabel("x")
            plt.ylabel("f(x)")
            plt.legend()
            plt.grid()
            
            # Ajustar los límites del eje y para dejar espacio arriba del gráfico
            plt.ylim(bottom=min(y_vals) - 1, top=max(y_vals) + 1)
            
            # Mostrar la función y su derivada fuera del gráfico
            function_str = f"$f(x) = {sp.latex(f)}$"
            derivative_str = f"$F'(x) = {sp.latex(df)}$"
            plt.text(5, -2.9, function_str, ha='center', va='center',  fontsize=10, bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=0.5'))
            plt.text(5, -5.3, derivative_str, ha='center', va='center', fontsize=10, bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=0.5'))
            
            # Guardar la imagen en un buffer de memoria para mostrarla en la web
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png')
            plt.close()
            img_buffer.seek(0)

            # Codificar la imagen en base64 para mostrarla en HTML
            img_data = base64.b64encode(img_buffer.getvalue()).decode()

            return f'''<h3>Raíz aproximada: {raiz_aproximada}</h3>
                        <body style="background-color:#F7E3F1;">
                    <img src="data:image/png;base64,{img_data}" alt="Gráfica de raíz">'''
        
        except SympifyError:
            return 'Error al interpretar la función ingresada. Inténtalo de nuevo.', 400
        except ValueError:
            return 'Valor inicial no válido. Inténtalo de nuevo.', 400
    else:
        return formulario_html

if __name__ == '__main__':
    app.run(debug=True)