from flask import Flask, request, render_template
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def jacobi(A, b, x0, tol=1e-10, max_iterations=100):
    D = np.diag(A)
    R = A - np.diagflat(D)
    x = x0
    iter_count = 0
    history = [x0.copy()]

    for i in range(max_iterations):
        x_new = (b - np.dot(R, x)) / D
        history.append(x_new.copy())
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new, iter_count, history
        x = x_new
        iter_count += 1

    return x, iter_count, history

@app.route('/jacobi', methods=['GET', 'POST'])
def metodo_jacobi():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            matriz_a_str = request.form['matriz_a']
            vector_b_str = request.form['vector_b']
            x0_str = request.form['x0']

            # Convertir las entradas en arrays de NumPy
            A = np.array(eval(matriz_a_str))
            b = np.array(eval(vector_b_str))
            x0 = np.array(eval(x0_str))

            # Validar las dimensiones de la matriz y los vectores
            assert A.shape[0] == A.shape[1], "La matriz A debe ser cuadrada"
            assert A.shape[0] == b.size == x0.size, "Las dimensiones de A, b y x0 deben coincidir"

            # Método de Jacobi
            solucion, iteraciones, history = jacobi(A, b, x0)

            # Generar gráfica de convergencia
            plt.figure()
            for i in range(len(x0)):
                plt.plot([h[i] for h in history], label=f'x{i}')
            plt.xlabel('Iteraciones')
            plt.ylabel('Valor de x')
            plt.title('Convergencia del Método de Jacobi')
            plt.legend()
            plt.grid(True)

            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png')
            plt.close()
            img_buffer.seek(0)
            img_data = base64.b64encode(img_buffer.getvalue()).decode()

            return render_template('jacobi_result.html', solucion=solucion, iteraciones=iteraciones, img_data=img_data)
        
        except Exception as e:
            return f"Error: {str(e)}", 400

    else:
        return render_template('jacobi_form.html')

if __name__ == '__main__':
    app.run(debug=True)