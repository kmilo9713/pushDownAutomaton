from pila import Pila

def extraerExpresion(cadena):
	divido = cadena.split("/")
	leer = divido[0]
	saca = divido[1]
	mete = divido[2]

	return leer, saca,  mete

class PDA:
	def __init__(self, estadoInicial, estadoAceptacion, simboloInicial):
		self.estadoInicial = estadoInicial
		self.estadoFinal = estadoAceptacion
		self.edges = None
		self.pila = Pila()
		self.proceso = [] # 1 para meter, 0 para sacar
		
		if simboloInicial != None:
			self.pila.apilar(simboloInicial)
			self.proceso.append([simboloInicial, 1, "", ""])
			print(self.pila.verTope())

	def setEdges(self, edges):
		self.edges = edges

	def buscarNodo(self, nodo):

		caminos = []#Lista de caminos

		#Saco los posibles caminos de un punto a otro
		for w in self.edges:
			divido = w[0].split("-")
			origen = divido[0]

			if origen == nodo:
				caminos.append(w)

		return caminos

	def __caminosPosibles(self, letra, caminos):

		caminosPosibles = []

		for x in caminos:
			for i in x:

				if "-" in i:
					caminosPosibles.append(i)
				else:
					leo, saco, meto = extraerExpresion(i)
					if leo == letra or leo == "λ":
							caminosPosibles.append(i)

		return caminosPosibles

	def evaluarCadena(self, cadena, actual, i, pila, proceso):

		if self.edges != None:
			
			caminosTomados = []
			cantidadCaminos = 0

			if (cadena == "" or cadena == "λ") and actual == self.estadoFinal:
				return True, pila, proceso

			if cadena != "":
				letra = cadena[0]

			else:
				cadena = letra = "λ"

			actual = actual.lower()#Nodo donde se encuentra

			caminosEncontrados = self.buscarNodo(actual)
			#Recorro todos los posibles caminos si los hay

			if caminosEncontrados != []:

				caminosEncontrados = self.__caminosPosibles(letra, caminosEncontrados)
				
				encontroCamino = False

				ver = origen = destino = None
				print(caminosEncontrados)
				retorno = False

				for w in caminosEncontrados:
					
					if "-" in w:
						ver = w
						#Divido el string para saber Nodo origen a nodo destino
						divido = ver.split("-")
						origen = divido[0]
						destino = divido[1]
					else:
						print("Iteracion: ", i, "Camino tomado: ", w)

					#Recorro cada regla para sacar leo/saco/meto para evaluar

					if "-" not in w:
						leo, saco, meto = extraerExpresion(w)
						if leo == letra or leo == "λ":
							if saco == pila.verTope():
								#Meto valores en la pila
								#Si el leo y saco estan bien
								encontroCamino = True
								
								proceso.append([pila.sacarPila(), 0, w, ver])

								for x in meto:
									if x != "λ":
										pila.apilar(x)
										proceso.append([x, 1, w, ver])

								if leo == "λ":
									retorno, pila, proceso = self.evaluarCadena(cadena, destino, i+1, pila, proceso)
								else:
									cadena = cadena[1:]
									retorno, pila, proceso = self.evaluarCadena(cadena, destino, i+1, pila, proceso)

						if retorno == True:
							return retorno, pila, proceso

				if encontroCamino == False:
					return False, pila, proceso

				return retorno, pila, proceso

			else:
				return False, pila, proceso


automata1 = PDA("p", "r", "#")
#  Transiciones grafo 1 --- REGLAS CON ESTE AUTOMATA YA ESTA BUENO

label_PtoP = ["p-p","b/b/bb", "a/b/ba", "b/a/ab", "a/a/aa", "b/#/#b", "a/#/#a"]
label_PtoQ = ["p-q","c/#/#", "c/b/b", "c/a/a"]
label_QtoQ = ["q-q","b/b/λ", "a/a/λ"]
label_QtoR = ["q-r","λ/#/#"]

#Transiciones grafo 2 

label_PtoP = ["p-p","b/b/bb", "a/b/ba", "b/a/ab", "a/a/aa", "b/#/#b", "a/#/#a"]
label_PtoQ = ["p-q","b/b/λ", "a/a/λ"]
label_QtoQ = ["q-q","b/b/λ", "a/a/λ"]
label_QtoR = ["q-r","λ/#/#"]

edges1 = [label_PtoQ, label_PtoP, label_QtoR, label_QtoQ]

automata1.setEdges(edges1)
resultado, pila, proceso = automata1.evaluarCadena("aabbbbaa", automata1.estadoInicial, 0, automata1.pila, automata1.proceso)
print("RESULTADO: ", resultado, " tope PILA: ", pila.verTope(), " \nProceso:", proceso)