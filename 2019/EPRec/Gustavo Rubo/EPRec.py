"""
14/07/2019

Exercício Programa Recuperação - MAP3121

Feito por:
Gustavo Marangoni Rubo NUSPº 4584080

"""

import numpy as np
import math
import matplotlib.pyplot as plt

#configurando as opções de impressão de matrizes
np.set_printoptions(precision=5)
np.set_printoptions(suppress=True)
np.set_printoptions(edgeitems=5)
np.set_printoptions(linewidth=80)

def Simpson1(f, a, b):
	return ((b-a)/6)*(f(a) + 4*f((a+b)/2) + f(b))

def Simpson2(f, a, b):
	h = (b - a) / 4
	soma = f(a) + 4 * f(a + h) + 2 * f(a + 2*h) + 4 * f(a + 3*h) + f(a + 4*h)

	return (h/3)*soma

def acha_pontos(f, a, b, e):
	return acha_pontos_recursiva(f, a, b, a, b, e, [a])	

def acha_pontos_recursiva(f, a, b, xi, xj, e, pontos):
	s1 = Simpson1(f, xi, xj)
	s2 = Simpson2(f, xi, xj)

	if (abs(s1 - s2) < 15*e*(xj - xi)/(b - a)):
		pontos.append(xj)
		return (pontos)
	else:
		pontos = acha_pontos_recursiva(f, a, b, xi, (xi + xj)/2, e, pontos)
		pontos = acha_pontos_recursiva(f, a, b, (xi + xj)/2, xj, e, pontos)
	return pontos

testes = [{
	"f": lambda x : (x + 1)*((x - 0.8)**7),
	"a": -1.5,
	"b": 1.5,
	"e": 1e-6
	}, {
	"f": lambda x : 25*math.e**(-(25*(x-0.5))**2),
	"a": 0,
	"b": 1,
	"e": 1e-6
}]

for i in range(0, len(testes)):
	print("Executando teste " + str(i + 1) + " de " + str(len(testes)))
	print("Extremos: " + str(testes[i]["a"]) + ", " + str(testes[i]["b"]))
	print("Precisão: " + str(testes[i]["e"]))

	pontos = acha_pontos(testes[i]["f"], testes[i]["a"], testes[i]["b"], testes[i]["e"])

	print ("Intervalos: " + str(len(pontos) - 1	))
	print ("Pontos: ")
	print (np.matrix(pontos))

	t = np.arange(testes[i]["a"], testes[i]["b"], (testes[i]["b"] - testes[i]["a"])/1e2)
	plt.plot(t, testes[i]["f"](t))
	for p in pontos:
		plt.axvline(x=p, linewidth=.7, color='r', alpha=.3)
	plt.show()