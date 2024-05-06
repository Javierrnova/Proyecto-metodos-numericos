import numpy as np
import matplotlib.pyplot as plt

# Definición de la función cúbica
def f(x):
    return x**3 + 2*x**2 + 10*x - 20

# Método de bisección para encontrar la raíz
def biseccion(func, a, b, tol=1e-5, max_iter=100):
    # Verificar que el intervalo contiene una raíz
    if func(a) * func(b) >= 0:
        raise ValueError("El intervalo no contiene una raíz.")

    c_values = []
    for _ in range(max_iter):
        c = (a + b) / 2
        c_values.append(c)

        # Verificar criterio de convergencia
        if func(c) == 0 or (b - a) / 2 < tol:
            return c, c_values
        
        # Determinar el intervalo con la raíz
        if func(a) * func(c) < 0:
            b = c
        else:
            a = c
    
    raise ValueError("No se encontró la raíz después de máximo número de iteraciones.")

# Valores iniciales para el intervalo
a = 1.0
b = 2.0

# Encontrar la raíz usando el método de bisección
try:
    root, c_values = biseccion(f, a, b)
except ValueError as e:
    print("Error:", e)
    root = None
    c_values = []

# Graficar la función con la línea que representa el eje X
x = np.linspace(1, 3, 100)
plt.figure()
plt.plot(x, f(x), label="f(x)")

# Añadir la línea horizontal que representa el eje X
plt.axhline(y=0, color='black', linestyle='-', linewidth=2, label='Eje X')

# Graficar el punto de la raíz y las líneas del proceso de bisección
if root is not None:
    plt.plot(root, f(root), 'o', label=f'Raíz: {root:.5f}', color='red')
    for c in c_values:
        plt.axvline(x=c, color='gray', linestyle='--', linewidth=1)

plt.title("Método de Bisección")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid()
plt.show()