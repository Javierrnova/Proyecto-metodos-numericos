from flask import Flask, request, render_template
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def gauss_seidel(A, b, x0, tol=1e-10, max_iterations=100):
    n = len(x0)
    x = x0.copy().astype(float)
    history = [x0.copy().astype(float)]

    for iter_count in range(max_iterations):
        x_new = x.copy()
        for i in range(n):
            sum1 = np.dot(A[i, :i], x_new[:i])
            sum2 = np.dot(A[i, i+1:], x[i+1:])
            x_new[i] = (b[i] - sum1 - sum2) / A[i, i]
        history.append(x_new.copy())
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new, iter_count + 1, history
        x = x_new

    return x, max_iterations, history

@app.route('/gauss_seidel', methods=['GET', 'POST'])
def metodo_gauss_seidel():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            matriz_a_str = request.form['matriz_a']
            vector_b_str = request.form['vector_b']
            x0_str = request.form['x0']

            # Convertir las entradas en arrays de NumPy
            A = np.array(eval(matriz_a_str), dtype=float)
            b = np.array(eval(vector_b_str), dtype=float)
            x0 = np.array(eval(x0_str), dtype=float)

            # Validar las dimensiones de la matriz y los vectores
            assert A.shape[0] == A.shape[1], "La matriz A debe ser cuadrada"
            assert A.shape[0] == b.size == x0.size, "Las dimensiones de A, b y x0 deben coincidir"

            # Método de Gauss-Seidel
            solucion, iteraciones, history = gauss_seidel(A, b, x0)

            # Generar gráfica de convergencia
            plt.figure()
            for i in range(len(x0)):
                plt.plot([h[i] for h in history], label=f'x{i}')
            plt.xlabel('Iteraciones')
            plt.ylabel('Valor de x')
            plt.title('Convergencia del Método de Gauss-Seidel')
            plt.legend()
            plt.grid(True)

            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png')
            plt.close()
            img_buffer.seek(0)
            img_data = base64.b64encode(img_buffer.getvalue()).decode()

            # Convertir la solución a una lista de cadenas para mantener los decimales
            solucion = [f'{val:.10f}' for val in solucion]

            return render_template('gauss_seidel_result.html', solucion=solucion, iteraciones=iteraciones, img_data=img_data)
        
        except Exception as e:
            return f"Error: {str(e)}", 400

    else:
        return render_template('gauss_seidel_form.html')

if __name__ == '__main__':
    app.run(debug=True)