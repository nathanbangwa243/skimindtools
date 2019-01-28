#-*-coding: utf-8 -*-

# symbols of set theory
SYMBOL = {
            "INCLUDEMIN": "[",
            "EXCLUDEMIN": "]",
            
            "INCLUDEMAX": "]",
            "EXCLUDEMAX": "["

        }

def createMathematicalInterval(listCommonDataStatus):
    """
        construction des intervalles mathematiques des valeurs
        
        :param listCommonDataStatus: [
                                        {
                                            'data': str(float), # la donnee
                                            'tabset': tuple # tupleObject des ensembles partageant la donnee -> value : str
                                        },
                                        ...
                                    ]

        :return:
                {
                    'setX': [ "[x, y[" , "]x,y]" ],
                    'setY': [ "[x, y[" , "]x,y]" ],
                    'setZ': [ "[x, y[" , "]x,y]" ],
                    ...

                    'setX-setY': [ "[x, y[" , "]x,y]" ],
                    'setZ-setY': [ "[x, y[" , "]x,y]" ],
                    ...
                }
    """
    response =  {}
    # taille de la liste
    lenOfList = len(listCommonDataStatus)

    # indice du dernier element
    lastIndex = lenOfList -1 

    # variables tempons
    min = str() # str : valeur minimale -> ]data or [data
    max = str() # str : valeur maximale -> data[ or data]

    pointer     = None     # POINTE SUR UN ENSEMBLE A LA FOIS
    tmpPointer  = None   # pointeur tempon -> recherche d'un point de changement
    interval    = str()    # sauvegarde temporairement une interval -> []COTEMIN, COTEMAX[]

    # etat de la donnee min doit etre exclue
    #minShouldBeExcluded = False 

    currentIndex = 0 # currentIndex 

    while currentIndex < lastIndex:
        
        # curretnt Tab
        dictCurrentDataStatus  = listCommonDataStatus[currentIndex] # le dictionnaire contenant le status de la donnee courante
        
        # next Tab
        nextIndex               = currentIndex + 1
        dictNextDataStatus  = listCommonDataStatus[nextIndex] # le dictionnaire contenant le status de la donnee suivante
        
        # initialisation du pointeur et definition de l'etat de la data min -> include or exclud
        if len(dictCurrentDataStatus['tabset']) == 1: # : la donnee n'appartient qu'a un seul ensemble
            min     = ''.join((SYMBOL["INCLUDEMIN"], dictCurrentDataStatus['data'])) #  min data include -> [data
            pointer = dictCurrentDataStatus['tabset'][0] # pointer -> l'ensemble unique

        
        else: # currentX != currentY

            if dictCurrentDataStatus['tabset'] == dictNextDataStatus['tabset']: # CurrentMin == NextMin and CurrentMax == NextMax -> CurrentX and CurrentY in dictNextDataStatus['tabset']
                min     = ''.join((SYMBOL["INCLUDEMIN"], dictCurrentDataStatus['data'])) # min include -> [CurrentData
                pointer = "-".join(tuple(dictCurrentDataStatus['tabset'])) # pointer -> currentX-CurrentY : str
            
            elif dictCurrentDataStatus['tabset'] != dictNextDataStatus['tabset']: # currentX not in dictNextDataStatus['tabset'] and currentY not in dictNextDataStatus['tabset'] -> changement complet de tab
                pointer = "-".join(tuple(dictCurrentDataStatus['tabset'])) # pointer -> currentX-CurrentY : str
                min     = "".join((SYMBOL["INCLUDEMIN"], dictCurrentDataStatus['data']))
            
            else: # on pointe vers la d'ensemble qui se trouve aussi parmi la liste des enseambles partageant la donnee suivante
                dictCurrentDataStatus['tabset'] = set(dictCurrentDataStatus['tabset']).intersection(set(dictNextDataStatus['tabset'])) # elements communs a dictCurrentDataStatus['tabset'] et dictNextDataStatus['tabset']
                dictCurrentDataStatus['tabset'] = list(dictCurrentDataStatus['data'])                          # set -> list

                min     = "".join((SYMBOL["EXCLUDEMIN"], dictCurrentDataStatus['data'])) # exclude min -> ]CurrentData
                pointer = "-".join(dictCurrentDataStatus['tabset'])                # pointer ->  
                
        # recherche du point de rupture -> changement de pointeur
        if pointer: # si le pointeur n'est pas vide -> None
            
            tmpPointer = str(pointer) # copy du pointeur

            while pointer == tmpPointer and nextIndex <= lastIndex: # point de changement non trouve' avant le dernier indice inclus
                # listCommonDataStatus[nextIndex]
                dictNextDataStatus  = listCommonDataStatus[nextIndex]
                #dictNextDataStatus['tabset']                       = [nextX, nextY]
            
                # construction du pointeur de verification
                tmpPointer = '-'.join(dictNextDataStatus['tabset']) # pointer -> setX-setY-..-setN : str

                nextIndex += 1 # -> index of the next Tab set [AAAA]

            
            
            # formatage du flag de la donnee max
            if tmpPointer != pointer: # point de changement trouve'
                max      = ''.join((dictNextDataStatus['data'], SYMBOL["EXCLUDEMAX"])) # nextData[
                # on se positionne au point de rupture
                currentIndex = nextIndex - 1 # BECAUSE          [AAAA] n'a pas rompu pas la boucle
            
            else: # tmpPointer == pointer -> currentIndex > lastIndex :dernier indice depasse -> fin de l'algorithme
                max      = "".join((dictNextDataStatus['data'], SYMBOL["INCLUDEMAX"])) #  nextData]
                currentIndex = lastIndex

            # construction de l'interval
            interval = ",".join((min, max))

            if pointer not in response: # si la cle [pointer] n'existe pas dans le dictionnaire
                response[pointer] = []  # on ajoute la dite cle
        
            # on ajoute l'interval a la liste des intervals
            response[pointer].append(interval)

            pointer = None
    
    return response