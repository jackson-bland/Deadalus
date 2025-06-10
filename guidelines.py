import numpy as np
from calculations import *

def guideline_creator(airfoils, resolution):
    guideline_list = [np.zeros((len(airfoils),3)),np.zeros((len(airfoils),3)),np.zeros((len(airfoils),3)),np.zeros((len(airfoils),3))]
    # get guidelines, # of guidelines = 4
    for i,a in enumerate(airfoils):
        LE = a[2][0]
        TE = a[2][-1]
        UM = a[2][resolution//2]
        LM = a[3][resolution//2]
        guideline_list[0][i] = LE
        guideline_list[1][i] = TE
        guideline_list[2][i] = UM
        guideline_list[3][i] = LM
    return guideline_list