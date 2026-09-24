import matplotlib.pyplot as plt

meshSize = []
cD = []
flag = 0

while flag == 0:

    m = float(input("\n Insert the Mesh size: "))
    dragcoeff = float(input("\n Insert the corresponding value of cD: "))
    meshSize.append(m)
    cD.append(dragcoeff)
    procede = input("\n Do you want to insert other data? [Y/n]: ")

    if procede == 'y' or procede == 'Y':
        print("\n \n")
        print("\n Let's continue...")
        flag = 0
    else: 
        print("\n \n")
        print("\n Let's plot the data...")
        flag = 1 

print(f"\n These are the Mesh sizes: {meshSize}")
print(f"\n These are the drag coefficient: {cD} ")

fig, ax = plt.subplots(figsize = (7,5))
ax.plot(meshSize, cD, 'o-', color = 'red', label = '$c_D$')
ax.set_xlabel('Mesh Size', fontsize = 12)
ax.set_ylabel('Drag Coefficient ($c_D$)', fontsize = 12)
ax.set_title('Grid convergence analysis for a Cybertruck\nin standard configuration', fontsize = 14, fontweight = 'bold')
plt.grid(True)
plt.legend(fontsize = 12)
plt.tight_layout()
plt.show()

Err = []
for i in range(len(cD)-1):
    e =( (cD[i+1] - cD[i])/cD[i+1] ) *100
    Err.append(e)
    print('\n'+"-"*40)
    print(f"\n Error between {meshSize[i+1]} and {meshSize[i]} is equal to: {Err[i]}%")
    print("\n" + "-"*40)


