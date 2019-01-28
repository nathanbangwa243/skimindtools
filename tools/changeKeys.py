#-*-coding: utf-8 -*-

"""
    changement des cles d'un dictionnaire
"""

def replaceKeys(target, config, sep=' '):
    """
        changement de cles dans un dictionnaire

        :paaram target: dict
                    le dictionnaire cible
                    {
                        lastKey             : value
                        lastKey1 [sep] lastKey2   : value
                    } 
                        # ex : {set1-set2 : 10} # sep = '-'
                
        :param config: dict
                    {
                        lastKey : newKey,
                    }
        
        :param sep: str
                    le caractere de separation des anciennes cles en cas des combinaisons des cles
                    default = ' ' # space

        :return: dict
                {
                    newKey              : value
                    newKey1 [sep] newKey2     : value
                }
    """

    # keys of dict target
    targetKey = target.keys()
    targetKey = list(targetKey)

    newKey     = None

    for lastKey in targetKey: # target keys loop
        # list
        newKey = []

        for key in lastKey.split(sep):
            if key in config:
                newKey.append(str(config[key]))

        # str
        newKey = sep.join(newKey)

        if newKey:
            # value acquire : delete 
            value   = target.pop(lastKey)

            # replace
            target[newKey] = value
    
    return target
