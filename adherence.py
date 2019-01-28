


def findAllCommonData(metadata):
    """
        trouve les donnees partagees et -->
        ...--> renvoit un dictionnaire ->  {key : value} with key : donnee partagee, value: liste des ensembles partageant la donnee

        :param metadata: {
                        set1: [data],
                        set2: [data],
                        set3: [data]
                    } # or

                    [set1, set2, set3, ..., setn] or (set1, set2, set3, ..., setn) # with type(setx) in [list, tuple]

    :return: dict
            {
                data : [setx, sety, ..., setN] 
                ...
            }
            
            None if no any common data
    """
    response =  dict()

    if type(metadata) != dict:  # si on a pas un dictionnaire a l'entree
        metadata = dict(enumerate(metadata)) # on transforme la list(tuple) en dictionnaire
                                                # {index: value}

    listOfUniqueData = list()   # liste des donnees non redondant

    for dataList in metadata.values():  # loop -> all set
        # on trie les elements qui ne figurent pas dans la liste des donnees sans redondances
        dataList = [data for data in dataList if data not in listOfUniqueData]

        if dataList:  # si la liste n'est pas vide
            listOfUniqueData.extend(dataList)   # on ajoute les elements a la liste sans redondance
    
    for data in listOfUniqueData:
        # la liste des ensembles partageant la donnee
        listOfSets = [key for key in metadata if data in metadata[key]]

        if len(listOfSets) >= 2:    # s'il y a au moins 2 ensembles qui partagent la donnee
            response[data] = listOfSets   # on ajoute la donnee et la liste de ses propriataires
    
    return response

def findOwnerOfData(commonData, metadata):
    """
    theorem : une donnee partagee entre n ensembles ne peut appartenir qu'a un seul
                de ces n ensembles suivant la frequence d'apparition de la donnee dans les n ensembles
                si la donnee a une meme frequence dans au moins deux des ensembles, elle est dite non partageable
                et est exclue -> elle n'appartient a aucun de ces ensembles 

    la fonction cherche un ensemble (element key) auquel appartient une donnee 

    :param metadata: {
                        set1: [data],
                        set2: [data],
                        set3: [data]
                    } # or

                    [set1, set2, set3, ..., setn] or (set1, set2, set3, ..., setn) # with type(setx) in [list, tuple]

    :return: type -> function of metadata.keys()
            response in metadata.keys() or None if the commonData has not an owner
    """
    response =  None # by deaault : la donnee n'appartient a aucun des ensembles

    if type(metadata) != dict:  # si on a pas un dictionnaire a l'entree
        metadata = dict(enumerate(metadata)) # on transforme la list(tuple) en dictionnaire
                                                # {index: value}

    # liste des cles(sets) partageants la donnee
    setListKey = [setKey for setKey, dataList in metadata.items() if commonData in dataList]

    if setListKey: # si la donnee est presente dans au moins l'un des ensembles
        if len(setListKey) == 1: # si la donnee n'appartient qu'a un seul ensemble
            return setListKey[0]    # on renvoit l'id de l'ensemble proprietaire
        
        else:   # si la donnee est partagee entre au moins 2 ensembles
            # liste des frequences d'apparition de la donnee dans les ensembles cibles
            commonDataFrequency = [list(metadata[setKey]).count(commonData) for setKey in setListKey]

            # la copie de la liste des frequences
            copyList = list(commonDataFrequency)
            copyList.sort() # tri croissant

            if copyList[-1] > copyList[-2]: # si la plus grande frequence est strictement superieur aux autres
                indexOfFrequency = commonDataFrequency.index(copyList[-1])  # on recupere l'indice de la frequence

                return setListKey[indexOfFrequency] # on renvoi l'id de l'ensemble

    
    return response


def commonDataExlusion(metadata):
    """
    theorem : une donnee partagee entre n ensembles ne peut appartenir qu'a un seul
                de ces n ensembles suivant la frequence d'apparition de la donnee dans les n ensembles
                si la donnee a une meme frequence dans au moins deux des ensembles, elle est dite non partageable
                et est exclue -> elle n'appartient a aucun de ces ensembles 

    :param metadata: {
                        set1: [data],
                        set2: [data],
                        set3: [data]
                    } # or

                    [set1, set2, set3, ..., setn] or (set1, set2, set3, ..., setn) # with type(setx) in [list, tuple]
    
    :return: metadata # avec l'application du theorem
    """

    typeMetaIsNotDict = False

    if type(metadata) != dict:
        typeMetaIsNotDict = True
        metadata = dict(enumerate(metadata))

    response = metadata   # une copie de cles de l'entree

    # dictionnaires des donnees partagees
    dictOfCommonData = findAllCommonData(metadata=metadata)

    if dictOfCommonData:    # s'il existe des donnees partagees
        for commonData, listOfSets in dictOfCommonData.items(): # loop -> commonData
            # on cherche l'ensemble proprietaire de la donnee
            setOwner = findOwnerOfData(commonData=commonData, metadata=metadata)   
            
            if setOwner != None:    # si la donnee a un proprietaire propre : != None pour eviter que la cle 0 soit ignoree
                listOfSets.remove(setOwner) # on ecarte l'ensemble proprietaire

            for setKey in listOfSets:
                # suppression de la donnee dans les ensembles declare's non proprietaires
                response[setKey] = [data for data in response[setKey] if data != commonData]
    
    else:   # s'il y a aucune donnee partagee
        response =  metadata
    
    if typeMetaIsNotDict:   # si a l'entree on a pas un dictionnaire
        listKeys = response.keys()
        listKeys = list(listKeys)
        listKeys.sort()
        # on reconstitue le type d'entree
        response = [response[setKey] for setKey in listKeys]
    
    return response
