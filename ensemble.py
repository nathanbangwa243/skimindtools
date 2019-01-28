#-*-coding: utf-8 -*-

# tools ->
from .setheory import createIntervalOfSet  # 

import numpy as np

class Research(object):
    """
        classe singleton -> permet de chercher un element dans une liste en fouillant dans les sous-listes
        si l'element se trouve dans un intervalle donne'.

        O(n) = c + log(n) -> logarithmic complexity : time of search. - with  c < 3 and n = len(listData)
    """

    researchObject = None

    def __new__(cls, *args, **kwargs):
        if not cls.researchObject:
            cls.researchObject = super(Research, cls).__new__(cls, *args, **kwargs)

        return cls.researchObject

    def valeuInListData(self, value, listData):
        """
        verifie si une valeur figure dans une intervalle des valeurs de la liste [listData]

        :param listData: list
                        [[min1, max1], [min2, max2]]
        
        :return: bool
                True  -> if valeu >= minx and valeu <= maxx
                False -> else 
        """

        maxIndex = len(listData) - 1 # index max
        minIndex = 0    # by default for init

        middleIndex = (minIndex + maxIndex) // 2 # middle index in listData

        if value < listData[minIndex][0] or value > listData[maxIndex][1]: # valeu cannot be found in listData
            return False

        while(maxIndex - minIndex > 1): 

            if value >= listData[middleIndex][0]: # valeu can be found in listData[middleIndex:] goto --->
                minIndex = middleIndex              # exclusion of [:middleIndex]
            
            else:   # valeu can be found in listData[:middleIndex] goto <----
                maxIndex = middleIndex - 1 # # exclusion of listData[middleIndex:]

            middleIndex = (minIndex + maxIndex) // 2    # update middle index in listData
        
        if minIndex == maxIndex:    # un seul indice a verifier
            listData = [listData[minIndex]]
        
        else:   # une intervalle d'indices < 2 a verifier
            listData = listData[minIndex:maxIndex+1] # maxIndex Included
        
        if [True for min, max in listData if value >= min and value <= max] :
            return True # valeu exist in listData
        
        return False    # valeu not found


class MathSetClassifier(object):
    """
        Permet de construire un datasets decisionnel 
        en se basant sur la theorie des ensembles mathematiques
    """

    def __init__(self, serialConst=None):
        """
            :param serialConst: str
                            constant of serialization of mathematicals sets
                            definit la plage d'exclusion d'une donnee

                            for exemple : serialConst = '5'
                                        if ]min, max[ => ]10.5, 20.55[ = class
                                            minSerialConst = 0.5
                                            maxSerialConst = 0.05
                                        
                                        then 
                                            class = [min + minSerialConst, max - maxSerialConst]
                                            class = [11, 20.5]
        """

        self.serialConst = serialConst
        self._datasets = dict() # dictionnary of data datasets {class : []}

        self.research = Research()
    
    @property
    def datasets(self):
        return self._datasets
    
    def formatDatas(self, data, label):
        """
            preparation des donnees pour le traitement
            :before action:
                self._datasets = {}
            :after action:
                self._datasets = {classe : [data]}
            
            :return: self
        """
        # raz
        self._datasets = dict()

        for index, classe in enumerate(label):
            if classe not in self._datasets:
                self._datasets[classe] = []
            
            self._datasets[classe].append(data[index])
        
        return self


    def fit(self, X, y, dataowner=False):
        """
            application de la theorie des ensembles mathematiques aux donnees 
            afin de trouver des intervalles de valeurs propre a un ensemble 
            ou a une combinaison des ensembles

            :param X:  array-like (list)
                            The training input samples
                            shape = [n_samples]
                            dtype = (real number). use numpy.float32
            
            :param y: array-like (list)
                            shape = [n_samples]
                            The target values (class labels) as integers or strings.

                                
            :param dataowner: bool
                                True ->     une donnee ne doit appartenir qu'a un seul ensemble (classe)
                                False ->    une donnee peut appartenir a plusieurs ensembles (classes)
            
            :return : self (object)
                        
        """

        # check inputs
        if len(X) != len(y):
            msg = "Number of labels={} does not match number of samples={}".format(len(y), len(X))
            raise ValueError(msg)

        # preparation
        self.formatDatas(X, y)

        if self.serialConst: # serialConst are not None
            self._datasets = createIntervalOfSet(listOfSets=self._datasets, dataowner=dataowner, serialConst=self.serialConst) # construction of interval

        else:   # use a default value of the serialConst
            self._datasets = createIntervalOfSet(listOfSets=self._datasets, dataowner=dataowner)  # construction of interval
        
        return self
    
    def predict(self, X, xset=True):
        """
            :param X: list
                            contient les entrees a classifier
                            dtype = (real number)
            
            :param xset: bool
                        True : la prediction peut avoir plusieurs classes possibles
                        False : une entree ne peut avoir qu'une seule classe
            
            :return: list
                    class : si la donnee appartient a au moins un ensemble
                    None   : si la donnee n'appartient a aucun des ensembles
        """

        response = list()

        if self._datasets:
            for index, target in enumerate(X): # loop sur chaque donnee de l'entree
                try:
                    target = float(target)
                except:
                    raise ValueError("value should be numeric : [{}] index {}".format(X[index], index))
                
                for classe, listData in self._datasets.items(): # loop sur les classes
                    if not xset and '-' in classe or classe == 'all': # classe composite exclue
                        continue

                    if self.research.valeuInListData(value=target, listData=listData):
                        response.append(classe)
                        break
                
                else: # aucune classe trouvee
                    response.append(None)
        
        return np.array(response)