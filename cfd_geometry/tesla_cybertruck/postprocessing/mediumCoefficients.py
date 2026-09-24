from numpy import *
import pandas as pd

df = pd.read_csv(
    'forceCoeffs/0/forceCoeffs.dat', sep = "\s+", skiprows = 9,
    names = ['Time', 'CL', 'CD', 'CM', 'CL (f)', 'CL (r)']
)

meanCD = df.loc[-1000:, 'CD'].mean()

print(f"The mean drag coefficient is: {meanCD}")
