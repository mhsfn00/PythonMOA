import time
import sys

time_start = time.time() # Começa medida de tempo.

arrValor = [] # Valores.
arrPeso = [] # Pesos.
arrQuo = [] # Valor/Peso.
arrInBag = [] # 0: Não está na mochila | 1: Está na mochila.

instancesFile = sys.argv[1] # Passar o arquivo com as instancias
                            # como segundo argumento da chamada
                            # python 01knap.py instancia.txt.

def readFromFile (): # Função para ler as instancias do arquivo txt, faz alterações nos arranjos arrValor, arrPeso, arrQuo e arrInBag.
    file1 = open (instancesFile)
    tmpItems, tmpPeso = file1.readline().split() # Primeira linha do arquivo txt tem a quantidade de items e o peso máximo da mochia.
    qtdItems = int (tmpItems)
    pesoMax = int (tmpPeso)
    for line in file1: # Para todas as linhas apartir da segunda, le um valor e um peso (representando cada item) e os salva nos
        tmpValor, tmpPeso = line.split() # arranjos globais arrValor, arrPeso.
        valor = int (tmpValor)
        peso = int (tmpPeso)
        quo = float(valor/peso)
        arrValor.append (valor)
        arrPeso.append (peso)
        arrQuo.append (quo) # arrQuo recebe valor/peso de cada item.
        arrInBag.append (0) # arrInBag é inicializado com 0 em todos os índices (indicando que todos os itens estão fora da mochila).
    file1.close()
    return (qtdItems, pesoMax) # Retorna a quantidade de itens e o peso máximo da mochila.

qtdItems, pesoMax = readFromFile () # Chama a função para ler as informações do arquivo txt.
                                    # Recebe a quantidade de items e o peso máximo da mochila (primeira linha do arquivo txt).

def greedyKnap (itemQtt, maxWeight): # Algoritmo guloso, coloca o item de menor peso disponível na mochila, repete até
    bagValue = 0                    # encher a mochila.
    bagLightest = []                
    lightestWeight = 0
    lightestIndex = 0

    while True:
        lightestWeight = float('inf')
        for object in range (0, len(arrPeso)): # Encontra o objeto com o menor peso fora da mochila.
            if arrPeso[object] < lightestWeight and arrInBag[object] == 0:
                lightestWeight = arrPeso[object]
                lightestIndex = object

        maxWeight = maxWeight - arrPeso[lightestIndex]
        if maxWeight < 0: # Checagem para o caso em que o último item colocado ultrapassa o peso máximo da mochila.
            maxWeight = maxWeight + arrPeso[lightestIndex]
            break

        bagLightest.append(lightestIndex)
        arrInBag[lightestIndex] = 1 # Essa parte "marca" os items que foram colocados na mochila.
        itemQtt = itemQtt - 1
        bagValue = bagValue + arrValor[lightestIndex]

        if maxWeight == 0 or itemQtt == 0:
            break
                                        # Após a execução, o arranjo global arrInBag representa a solução obtida, com 0 nos índices
                                        # dos items que não foram colocados na mochila e 1 nos índices dos items que foram colocados 
                                        # na mochila.

    return bagValue, maxWeight, bagLightest # Retorna o valor da mochila com os items adicionados (bagValue), o peso restante (maxWeight)
                                            # e o arranjo (bagLightest) que representa os items adicionados a mochila.

def VNS (bagValue, remWeight, bagLightest): # Algoritmo utilizando a heurística VNS (Variable Neighborhood Search)
    # Essa função remove um item da mochila e adiciona um item que estava fora. A seleção e a adição de items e feita
    # de acordo com o parâmetro Quo (valor/peso).
    # Aqui são considerados vizinhos de primeiro nível as soluções que removem um item, segundo nível as soluções que removem dois items
    # e assim por diante. Vale citar que somente as soluções viáveis (as que respeitam o peso máximo da mochila) são consideradas. 

    maxLevel = round (0.2 * qtdItems) # Nível máximo é 20% da quantidade de instâncias.
    Quo = None # Usado durante a função como o valor de um item dividido pelo peso desse mesmo item.
    smallestQuo = None # Menor quocience valor/peso calculado até o momento.
    smallestIndex = None # Índice do menor quociente calculado até o momento (Esse índice server para os arranjos globais arrPeso, arrValor, ...).
    bestValue = bagValue
    currLevel = 0

    while currLevel <= maxLevel: # Verifica se o nível atual é menor ou igual ao nível máximo (caso falso finaliza a execução).

        smallestQuo = float('inf')
        for inBag in range (0, len(bagLightest)): # Busca o item da mochila com o menor parametro Quo(valor/peso).
            Quo = arrValor[bagLightest[inBag]] / arrPeso[bagLightest[inBag]]
            if Quo < smallestQuo:
                smallestQuo = Quo
                smallestIndex = bagLightest[inBag]
                bagLightestIndex = inBag

        bagValue = bagValue - arrValor[smallestIndex] # Remove o item com o menor parâmetro Quo.
        remWeight = remWeight + arrPeso[smallestIndex] 
        bagLightest.remove(bagLightest[bagLightestIndex]) 

        biggestQuo = 0
        for notInBag in range (0, len(arrValor)): # Busca o item com maior parâmetro Quo fora da mochila.
            if arrInBag[notInBag] == 0:
                Quo = arrValor[notInBag] / arrPeso[notInBag]
                if Quo > biggestQuo:
                    biggestQuo = Quo
                    biggestQuoIndex = notInBag

                    

        if remWeight >= arrPeso[biggestQuoIndex]: # Verifica se o item com maior Quo pode ser adicionado após a remoção do item com
            remWeight = remWeight - arrPeso[biggestQuoIndex] # menor Quo. Caso seja possível tem-se uma solução vizinha de primeiro
            bagValue = bagValue + arrValor[biggestQuoIndex] # nível, caso contrário aumenta o nível.
            arrInBag[biggestQuoIndex] = 1
            bagLightest.append(biggestQuoIndex)

        if bagValue >= bestValue: # Atualiza melhor valor obtido quando necessário.
            bestValue = bagValue
        else:
            currLevel = currLevel + 1 # Aumenta o nível quando o valor atual não é melhor que o melhor valor atual.

    bagLightest.append(smallestIndex)   
    return bestValue, remWeight-arrPeso[smallestIndex], bagLightest


def arrSum (itensInBag): # Soma o valor total dos itens no array passado como argumento.
    total = 0
    for _ in range (0, len(itensInBag)):
        total = total + arrValor[itensInBag[_]]
    return total

bagValue, remWeight, bagLightest = greedyKnap (qtdItems, pesoMax)
totalSum = arrSum (bagLightest)
print ("Valor guloso:",bagValue)
print ("Capacidade restante:",remWeight)
print ("\n")

bestValue, bestRemWeight, bestBagLightest = VNS (bagValue, remWeight, bagLightest)
totalSum = arrSum (bestBagLightest)
print ("Valor guloso + melhoramento:",bestValue)
print ("Capacidade restante:",bestRemWeight)

time_end = time.time() #Termina medida de tempo
print (round(time_end - time_start, 2), "sec")