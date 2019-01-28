#-*-coding: utf-8 -*-

# tools
#from tools import find_int_in_str

from .tools import find_int_in_str

# MARGE DE DIFFERENTIATION
DEFAULTSERIALCONSTANT = '01'

# signe de la data -> MAX MIN
NEGATIVESIGNE = '-'


def calculConst(value, serialConst=DEFAULTSERIALCONSTANT):
    """
        calcul la valeur de la constante de differenciation adaptee a un nombre donnee'

        :param value: float

        :param serialConst: str -> constant of serialization
                        ex: '01', '00002', ..., 'xxxx'
        return : float
            ex: value = 5.06 -> const = 0.0x with x -> DEFAULTSERIALCONSTANT
    """
    const    = str(float(value)).split('.')      # separation de la partie entiere de la partie flotante
    const[0] = '0'                               # mise a zero de la partie entiere 

    const    = ['0'*len(part) for part in const] # mise a zero de la partie flaotante -> Nieme
    const    = '.'.join(const)                   # reconstitution du nombre flotant
    const    = const[:-1] + str(DEFAULTSERIALCONSTANT)   # formatage de la constante de differenciation adaptee au nombre

    return float(const)

def serializeMathematicalInterval(dictInterval, serialConst=DEFAULTSERIALCONSTANT):
    """
        serialisation des donnees construites sous-formes d'intevalles mathematique
            
                EXCLUDED                    INCLUDED

        IF ]min : min = min + CONST | IF [min : min = min
        IF max[: max = max - CONST  | IF max] : max = max
                    

    :param dictInterval: dict 
                            {
                                key:
                                [
                                    ']min,max[', '[min,max[' 
                                ]
                            }
    :param serialConst: str -> constant of serialization
                        ex: '01', '00002', ..., 'xxxx'
                        
    :return: dict
                {
                    key:
                    [
                        [min, max]
                    ]
                }
    """

    response = {key: [] for key in dictInterval} # object to return

    # signes relatives aux donnees
    signeStatus = {'MIN': '', 'MAX': ''}

    for key, listMathInterval in dictInterval.items():      # loop -> liste des intervalles

        for interstr in listMathInterval:                   # loop -> chaque intervalle
            
            interstr            = interstr.strip()          # on retire les espaces
            
            charMin, charMax    = interstr[0], interstr[-1] # charactere [inclusion, exclusion]
            
            indexComma          = interstr.find(',')        # l'indice de la virgule
            
            # etat de la donnees -> positive or negative
            signeStatus['MIN'], signeStatus['MAX']    = interstr[1], interstr[indexComma+1]

            for keySign, flag in signeStatus.items():       # lopp -> signe of the data
                
                if flag != NEGATIVESIGNE:       # si la data est un nombre negatif
                    signeStatus[keySign] = 1

                else:                           # si la data est un nombre begatif
                    signeStatus[keySign] = -1
                
            # on recupere les valeurs min, max
            minValue, maxValue = [float(value) for value in find_int_in_str(interstr)]

            # restoration de l'integrite des donnees
            minValue *= signeStatus['MIN']
            maxValue *= signeStatus['MAX']

            # adaptation des donnees for -> POST CONDITION
            if charMin == ']': # min exclude
                const       = calculConst(minValue, serialConst=serialConst) # calcul de la constante de la donnee min
                minValue    += const                # adaptation

            if charMax == '[': # max exclude
                
                const       = calculConst(maxValue, serialConst=serialConst) # calcul de la constante de la donnee max
                maxValue    -= const                # adaptation
                

            if maxValue >= minValue: # filtre d'exclusion -> [minValue, maxValue[ with minVlue==maxValue: 
                                    # une donnee inclue et exclue en meme temps est exclue
                response[key].append([minValue, maxValue]) # ajout de la plage


    return response