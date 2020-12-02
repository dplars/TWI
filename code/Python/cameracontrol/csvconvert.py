import pandas as pd
import numpy as np


df = pd.read_csv("/Users/larsdepauw/Documents/Lars.nosync/Documents/School/1Ma ing/Masterproef/TWI/code/Vision/Datasets/labels/MetingenMicroscoop_TomJacobs.csv", delimiter=';')

print(df.head())
columns = ["bn", "pn", "bullet", "foldername", "imgname", "value"]

data = []
for index,row in df.iterrows():
    bnr = '{:03d}'.format(10+int(row[0]))
    pnr = '{:03d}'.format(int(row[1]))
    foldername = 'batch_'+bnr+'_plate_'+pnr
    bullet = 0
    bulletstr1 = 'nb'
    newrow1 = [bnr,pnr , bullet, foldername, 'b_'+bnr+'_p_'+pnr+'_l_000_'+bulletstr1+'.png', float(row[2])]
    data.append(newrow1)


    bullet = 1
    bulletstr2 = 'b'
    newrow2 = [bnr, pnr, bullet, foldername, 'b_'+bnr+'_p_'+pnr+'_l_000_'+bulletstr2+'.png', float(row[3])]
    data.append(newrow2)

newdf = pd.DataFrame(data=data, columns=columns)
print(newdf.head())

newdf.to_csv(path_or_buf="/Users/larsdepauw/Documents/Lars.nosync/Documents/School/1Ma ing/Masterproef/TWI/code/Vision/Datasets/labels/MetingenMicroscoop_TomJacobs_converted.csv",sep=';', columns=columns)