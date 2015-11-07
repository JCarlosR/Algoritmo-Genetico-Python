#coding:windows-1252

# Permite escribir usando tildes
from __future__ import unicode_literals
# Permite generar aleatorios
import random


# Variables globales definidas inicialmente
M = 6
A = 11
B = 7
limInferior = 1
probC = 0.5
probM = 0.35
iteraciones = 20

# Variables globales por definir
longC = 0
longC_X = 0
longC_Y = 0

# Variables que permiten encontrar el óptimo global
desviaciones = []
mejoresCromosomas = []





# Genera dos poblaciones, evitando el par (1, 1)
def generarPoblacion(pX, pY):
	i = 0
	while i < M:
		pX += [ random.randrange(limInferior, B/2) ]
		pY += [ random.randrange(limInferior, A/2) ]
		# Basta que uno sea diferente de 1 para continuar
		if pX[i] == 1 and pY[i] == 1:
			pX.pop()
			pY.pop()
		else:
			i += 1



# Cálculo de la longitud de cromosoma
def calcularLongitud():
	global longC
	global longC_X
	global longC_Y

	longC_X = len(toBinary(B/2))
	longC_Y = len(toBinary(A/2))
	longC = longC_X + longC_Y


# Devuelve el área no utilizada luego de los cortes
def evaluar(x, y):
	
	# Longitud sobrante en la Altura
	Sa = A % y
	# Longitud sobrante en la Base
	Sb = B % x
	# Lo que desea calcular
	sobranteTotal = 0

	# Se usará _A y _B para calcular el área sobrante del sobrante
	# Importante para no alterar el valor original de A y B

	# Según la forma del retazo se intenta hacer más cortes
	if x > y:
		# El sobrante es el bloque 1
		B1 = (B - Sb) * Sa
		# Reasignación de A y B
		_B = A
		_A = Sb
		# Calculamos las sobras de las sobras
		Sa = _A % y
		Sb = _B % x
		sobranteMenor = _B * Sa + (_A - Sa) * Sb
		# El total es
		sobranteTotal = sobranteMenor + B1
	elif y > x:
		# El sobrante es el bloque 3
		B3 = (A - Sa) * Sb
		# Reasignación de A y B
		_A = B
		_B = Sa
		# Calculamos las sobras de las sobras
		Sa = _A % y
		Sb = _B % x
		sobranteMenor = _B * Sa + (_A - Sa) * Sb
		# El total es
		sobranteTotal = sobranteMenor + B3
	else:
		sobranteTotal = B * Sa + (A - Sa) * Sb

	return sobranteTotal


# Devuelve en un arreglo la conversión a binario
def toBinary(n, longitud=0):
	arreglo = []

	while n >= 2:
		arreglo += [ n % 2 ]
		n = n / 2

	arreglo += [ n ]

	if longitud == 0:
		relleno = []
	else: 
		relleno = [0] * (longitud-len(arreglo))
	return arreglo + relleno



# Cruza la cantidad de genes indicada entre los cromosomas
def cruzar(cromosoma1, cromosoma2, genes):
	for i in range(genes):
		temporal = cromosoma1[i]
		cromosoma1[i] = cromosoma2[i]
		cromosoma2[i] = temporal


# Devuelve en decimal la conversión de un arreglo binario
def toDecimal(cromosoma):
	resultado = 0
	for i in range(len(cromosoma)):
		resultado += cromosoma[i] * pow(2, i)
	return resultado


# Clase para manejar los intervalos
class Intervalo:

    def __init__(self, min, max):
        self.min = min
        self.max = max

    def pertenece(self, valor):
        return self.min<=valor and valor<=self.max

    def toString(self):
    	return '[' + '{:.2f}'.format(self.min) + ' - ' + '{:.2f}'.format(self.max) + ']'


# Imprime un cromosoma con formato adecuado
def imprimirCromosoma(cromosoma):
	cadena = ''
	for gen in cromosoma:
		cadena = str(gen) + cadena
	
	numCeros = longC - len(cromosoma)
	ceros = '0' * numCeros

	print ceros, cadena


# Imprimir matriz con título
def imprimirMt(matriz):
	for fila in matriz:
		imprimirCromosoma(fila)


# Función principal
def main():	
	print "Bienvenido - Algoritmo genético de 2 variables"

	# Calculamos la longitud de cromosoma total
	calcularLongitud()

	# Para cálculos posteriores
	cromosomas = []
	evaluaciones = []
	columnaK = []
	desviaciones = []
	mejoresCromosomas = []
	aleatorios = []
	seleccion = []
	posicionesCruce = []
	cruzamiento = []
	mutacion = []

	# Primera población de individuos X e Y
	poblacionX = []
	poblacionY = []

	generarPoblacion(poblacionX, poblacionY)

	for ite in range(iteraciones):

		print "Población X:", poblacionX
		print "Población Y:", poblacionY

		print 'Longitud de X: ', longC_X
		print 'Longitud de Y: ', longC_Y
		print 'Longitud total: ', longC

		# Convertimos la primera población a cromosomas
		for i in range(M):
			# Se antepone Y y luego X, porque al imprimir se gira
			cromosomas += [ toBinary(poblacionY[i], longC_Y) + toBinary(poblacionX[i], longC_X) ]
		print 'Cromosomas: '
		imprimirMt(cromosomas)

		# Evaluamos
		sumaEvaluaciones = 0
		for i in range(M):
			evaluacion = evaluar(poblacionX[i], poblacionY[i])
			evaluaciones += [ evaluacion ]
			sumaEvaluaciones += evaluacion
		print 'Evaluaciones: ', evaluaciones

		# Promedio de las evaluaciones (para la desviación estándar)
		promedio = sumaEvaluaciones / M

		##################################################
		
		##### Desviación estándar
		# Suma de cuadrados
		sumaCuadrados = 0
		for e in evaluaciones:
			sumaCuadrados += pow(e - promedio, 2)

		interno = sumaCuadrados / (M-1)
		dS = pow(interno, 0.5)

		# Guardamos la ds de la iteración actual
		desviaciones += [ dS ]

		#### Mejor individuo
		# Posición del mejor cromosoma
		minIndex = evaluaciones.index(min(evaluaciones))
		# Guardamos el mejor cromosoma de la iteración actual
		mejoresCromosomas += [ cromosomas[minIndex] ]

		##################################################

		# Cálculo de la columna K
		for e in evaluaciones:
			columnaK += [ float(e) / sumaEvaluaciones ]
		print 'Columna K: ', columnaK

		# Definición de los intervalos
		intervalos = [ Intervalo(0, columnaK[0]) ]
		inferior = columnaK[0] + 0.01
		for i in range(1, M):
			superior = intervalos[i-1].max + columnaK[i]
			intervalos += [ Intervalo(inferior, superior) ]
			inferior = superior + 0.01

		# Listado de intervalos
		print 'Intervalos: '
		for intervalo in intervalos:
			print intervalo.toString()	

		# Aleatorios para la selección
		for i in range(M):
			aleatorios += [ random.uniform(0, 1) ]
		

		# Selección
		for i in range(M):
			seleccion += [0]
			for j in range(M):
				if intervalos[i].pertenece( aleatorios[j] ):
					seleccion[i] += 1
	 
		print 'Selección: ', seleccion

		# Reproducción
		reproduccion = cromosomas[:]
		for i in range(len(seleccion)):
			for j in range(seleccion[i]-1):
				for k in range(M):
					if seleccion[k] == 0:
						reproduccion[k] = cromosomas[i]
						seleccion[k] += 1
						break

		print 'Reproducción: '
		imprimirMt(reproduccion)


		# Punto de cruce
		ptoCruce = random.randrange(1, longC-1)

		# Elegidos para cruzarse
		for i in range(M):
			if random.uniform(0, 1) <= probC:
				posicionesCruce += [i]
				print 'Fila escogida para el cruzamiento: ', i


		# Cruzamiento
		cruzamiento = reproduccion[:]
		genesCruzar = longC - ptoCruce
		print 'Genes a cruzar: ', genesCruzar
			

		for i in range(0, len(posicionesCruce), 2):
			if i+1 < len(posicionesCruce):
				print 'Se cruzarán los cromosomas ', posicionesCruce[i], 'con ', posicionesCruce[i+1]
				cruzar(cruzamiento[posicionesCruce[i]], cruzamiento[posicionesCruce[i+1]], genesCruzar)

		print 'Cruzamiento: '
		imprimirMt(cruzamiento)


		# Mutación
		mutacion = cruzamiento[:]

		for i in range(M):
			for j in range(len(cruzamiento[i])):
				if random.uniform(0, 1) <= probM:
					mutacion[i][j] = 1 if cruzamiento[i][j] == 0 else 0
					print 'Mutó el cromosoma ', i, ' su gen ', j

		print 'Mutación: '
		imprimirMt(mutacion)
		
		print 'Fin de la iteracion ', ite



		# Luego de la mutación se corrigen los valores imposibles
		i = 0
		while i < M:
			print 'Parte corresponde al x: ', mutacion[i][longC_Y:]
			poblacionX[i] = toDecimal(mutacion[i][longC_Y:])
			print 'Elem x de la mutacion en decimal es ', poblacionX[i]
			if poblacionX[i] < 1 or poblacionX[i] > B/2:
				poblacionX[i] = random.randrange(limInferior, B/2)
				print 'Este elem x se cambio por ', poblacionX[i]

			print 'Parte corresponde al y: ', mutacion[i][:longC_Y]
			poblacionY[i] = toDecimal(mutacion[i][:longC_Y])
			print 'Elem y de la mutacion en decimal es ', poblacionY[i]
			if poblacionY[i] < 1 or poblacionY[i] > A/2:
				poblacionY[i] = random.randrange(limInferior, A/2)
				print 'Este elem y se cambio por ', poblacionY[i]

			if poblacionX[i] == 1 and poblacionY[i] == 1:
				x = random.randrange(limInferior, B/2)
				y = random.randrange(limInferior, A/2)
				mutacion[i] = toBinary(y) + toBinary(x)
			else:
				i = i + 1


		cromosomas[:] = []
		evaluaciones[:] = []
		columnaK[:] = []
		intervalos[:] = []
		aleatorios[:] = []
		seleccion[:] = []
		reproduccion[:] = []
		posicionesCruce[:] = []
		cruzamiento[:] = []
		mutacion[:] = []

		raw_input('Presione <ENTER> para continuar')


	raw_input('Presione <ENTER> para ver resultados')

	menorDS = 0;
	for i in range(1, M):
		if desviaciones[i] < desviaciones[menorDS]:
			menorDS = i;

	print 'La mejor población es la población: ', menorDS
	print 'El mejor cromosoma de la mejor generación es: ', mejoresCromosomas[menorDS]

	print 'Parte X: ', mejoresCromosomas[menorDS][longC_Y:]
	print 'Valor X: ', toDecimal(mejoresCromosomas[menorDS][longC_Y:])

	print 'Parte Y: ', mejoresCromosomas[menorDS][:longC_Y]
	print 'Valor Y: ', toDecimal(mejoresCromosomas[menorDS][:longC_Y])
	

# Sección de test
def test():
	intervalo = Intervalo(0.2,0.6)
	print intervalo.pertenece(0.1)

main()