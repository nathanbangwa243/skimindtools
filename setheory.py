#-*-coding: utf-8 -*-

# tools
from .commondata import sortCommonDataStatus         # representation du status de chaque donnee unique des ensambles

from .interval import createMathematicalInterval     # representation des donnees sous-forme d'intervalles mathematiques

from .serialize import serializeMathematicalInterval # representation objet [logique] d'intervalles mathematiques

from .adherence import commonDataExlusion            # classifieur d'une donnee partagee

from .tools.changeKeys import replaceKeys            # gestion des cles depart

# condition d'utilisation -> verification
POSTCONDITION = 'if value >= min and value <= max: ... # interval -> [min, max]'

def createIntervalOfSet(listOfSets, serialConst=None, dataowner=False):
    #print(listOfSets)
    """
        recoit une liste des ensembles et applique la theorie des ensembles mathematiques
        afin de trouver les intervalles des valeurs propres a chaque esnsemble

        :param listOfSets: [set1, set2, ..., setN] --> setX = [data, data1, ..., dataN] or
                           {set1: [], set2: [], ..., setN: []}
        
        :param serialConst: str
                            constant of serialization of mathematicals sets
        
        :param dataowner: bool
                        True: une donnee ne doit appartenir qu'a un seul ensemble
                        False: une donnee peut appartenir a plusieurs ensembles

        :return dict:
                {
                    key:
                    [
                        [min, max]
                    ]
                } # key -> set or combinaison setX-setY-...-setN

    """
    response    = dict()  # object to return
    isDict      = False # si on a un dictionnaire des ensembles a l'entree
    start       = False

    lastNewKeys = dict()    # newkeys par rapport aux anciennes keys: en cas d'un dictionnaire a l'entree

    if listOfSets:
        if type(listOfSets) == list: # si on a une liste des ensembles a l'entree
            start = True             # on active le treatement

        elif type(listOfSets) == dict: # si on a un dictionnaire des ensembles a l'entree
            ancienKeys  = list(listOfSets.keys())   # les clea de depart
            ancienKeys.sort()                       # tri croissant

            listOfSets  = [listOfSets[key] for key in ancienKeys] # adaptation d'element
            isDict      = True  # on active la reconstitution des cles de depart
            start       = True  # on active le treatement

            # dictionnaire de configuration : newKey par rapport aux anciennes keys
            lastNewKeys = {str(newKey) : lastKey for newKey, lastKey in enumerate(ancienKeys)}
        
        if start:
            response = listOfSets

            if dataowner: # classification d'une donnee partagee
                response = commonDataExlusion(metadata=listOfSets)
                
            # representation du status de chaque donnee unique des ensambles
            response = sortCommonDataStatus(listOfSets=response) #[{'data': float, 'tabset': ()}, ...]

            # representation des donnees sous-forme d'intervalles mathematiques
            response = createMathematicalInterval(listCommonDataStatus=response) # {key: [ ']min, max[', ... ], ...}

            
            # representation objet [logique] d'intervalles mathematiques
            if serialConst:
                response = serializeMathematicalInterval(dictInterval=response, serialConst=serialConst)
            else:
                response = serializeMathematicalInterval(dictInterval=response)      # {key: [ [min, max], ... ], ...}

            if isDict: # on reconstitue les cles de l'entree
                response = replaceKeys(target=response, config=lastNewKeys, sep='-')

    return response


