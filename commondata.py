#-*-coding: utf-8 -*-

#tools

def getSetDetValue(listOfSets):
    """
        retourne un ensemble des valeurs non redondantes (set)

        :param listOfSets: [set1, set2, ..., setn] # set : list of value -> [data, ..., dataN]

        :return: list
                [data] # unique data by order croissant
            with : pourtout valeur, return.count(valeur) == 1
    """
   
    response = []  # contient l'ensemble des matchs
    for data in listOfSets:
        response.extend(data)


    response = list(set(response))  # unique value and transform set -> list
    response.sort()                 # tri croissant

    return response

def sortCommonDataStatus(listOfSets):
    """
        trie la listOfSets et etablit une liste des donnees partagees entre plusieurs enseambles ou non -> data status

        :param listOfSets: [set1, set2, ..., setn] # set : set of data             
        
        :return: [
                    {
                        'data': float, # la donnee
                        'tabset': () # tupleObject des ensembles partageant la donnee
                    },
                    ...
                ]
    """

    setDetValue = getSetDetValue(listOfSets) # donnees uniques des ensembles

    response    = []  # object to return

    dataStatus  = dict() # status de la donnee -> (set1, data1, set2)

    for commonData in setDetValue:
        dataStatus = {}
        setListIndexTmp = [] # liste tempon des indices des sets partageant une donnee
                                # les valeurs sont triees d'une maniere croissante grace a la seconde boucle

        for indexOfSet, SetData in enumerate(listOfSets): # loop

            if commonData in SetData: # si la donnee fait partie de l'ensemble
                setListIndexTmp.append(str(indexOfSet)) # on ajoute l'indice de l'ensemble
        
        lenSetList = len(setListIndexTmp) # nombre d'ensemble partageant une donnee

        if lenSetList == len(listOfSets): # si la donnee est partagee entre tous les ensembles fournies a l'entree
            dataStatus['tabset'] = tuple(['all'])
        
        else: # donnee partagee entre 2 et (nbsets - 1) ensembles ou donnee propre a un seul ensemble
            dataStatus['tabset'] = tuple(setListIndexTmp) # les ensembles concerne's
        
        dataStatus['data'] = str(commonData)
        
        response.append(dataStatus) # ajout du status de la donnee
    
    return response
