import pandas as pd
import numpy as np
import time
from tkinter import filedialog

def export_data(data):
    #Define the function
    def save_file():
        return filedialog.askdirectory()
    save_path = save_file()
    
    file_prefix = time.strftime('%x %X')
    file_prefix = file_prefix.replace('/','_')
    file_prefix = file_prefix.replace(' ', '__')
    file_prefix = file_prefix.replace(':','-')

    for i,d in enumerate(data[1]):
        d[2] = np.delete(d[2], -1, 0)
        airfoil_data = np.vstack([d[1], np.flipud(d[2])])
        df = pd.DataFrame(airfoil_data, columns=['x','y','z'])
        file_name = file_prefix + '_' + d[0]
        file_name = file_name.replace(' ', '_')
        np.savetxt(save_path + '\\' + file_name+'.txt', df.values, fmt='%1.6f', delimiter='\t')

    if data[0] == 'All':
        for i,g in enumerate(data[2]):
            df = pd.DataFrame(g, columns=['x','y','z'])
            file_name = file_prefix + '_' + 'guideline'+str(i)
            file_name = file_name.replace(' ', '_')
            np.savetxt(save_path + '\\' + file_name+'.txt', df.values, fmt='%1.6f', delimiter='\t')
        # df = pd.DataFrame()
        # file_name = file_prefix + '_' + data[0]
        # file_name = file_name.replace(' ', '_')
        # np.savetxt(save_path + "\\"+ file_name, df.values, fmt='%1.6f', delimiter='\t')

    # win.mainloop()
    # name = data[0]
    # surface = data[1]
    # df = pd.DataFrame(surface, columns=['x','y','z'])
    # file_name = time.strftime('%x') + '_' + name + '.txt'
    # file_name = file_name.replace('/','_')
    # file_name = file_name.replace(' ','_')
    # np.savetxt(file_name, df.values, fmt='%1.6f', delimiter='\t')
    return