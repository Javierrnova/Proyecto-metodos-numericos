import numpy as np
from matplotlib import pyplot as plt

# Función que queremos resolver
def f(x):
    return x**2 - 2*x - 5

# Nueva función iterativa para punto fijo
def g(x):
    return np.sqrt(2*x + 5)  # Reorganizada para el método de punto fijo

# Valor inicial para la iteración
xi = 2.0  # Ajusta el valor inicial para lograr la convergencia

# Lista para rastrear iteraciones
iteraciones = []

# Método de punto fijo
while True:
    xn = g(xi)
    # Guardar las iteraciones
    iteraciones.append(xn)
    
    # Criterio de convergencia
    if abs(xn - xi) / xn < 0.00001:
        break
    
    xi = xn

# Mostrar el resultado de la raíz aproximada
print("Valor de la raíz aproximada =", xn)

# Graficar la función y las iteraciones
x = np.linspace(-2, 6, 100)  # Ajusta el rango de valores para graficar
plt.figure()
plt.plot(x, f(x), label="f(x)")

# Línea horizontal para representar el eje X
plt.axhline(y=0, color='black', linestyle='-', linewidth=2, label="Eje X")

plt.axvline(x=0, color='black', linestyle='--', linewidth=2, label="Eje Y")

# Resaltar el punto de la raíz
plt.plot(xn, f(xn), 'o', color='red', label=f"Raíz: {xn:.5f}")

# Configuración del gráfico
plt.title("Método de Punto Fijo para Encontrar Raíz")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid()
plt.show()
