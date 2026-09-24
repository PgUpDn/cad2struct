#Cd_standar = 0.312
#Cd_roofrack = 0.337
#Cd_open = 0.375
#Cd_box = 0.408

import matplotlib.pyplot as plt
import numpy as np

N = 4                                                   #number of configurations

Base = np.ones(4) * 0.312                               #Cd values of the baseline configuration
RoofRack = [0, 0, (0.337-0.312), (0.337-0.312)]         #Cd values of the Roof Rack configuration 
RoofBox = [0, 0, 0, (0.408-0.337)]                      #Cd values of the Roof Box configuaration 
OpenBox = [0, (0.375-0.312), 0, 0]                      #Cd values of the Open Box configuration 

barwidth = 0.25                                         #width of the bar of the plot

b0 = np.arange(len(Base))
b1 = []
b2 = []
b3 = []

for x in b0:
    b1.append(x + barwidth)                             #with this cycle we defien the position of the bar in order to not superimpose them 

for x in b1:
    b2.append(x + barwidth)

fig, ax = plt.subplots(figsize = (10,6))

ax.bar(b0, Base, width = barwidth, edgecolor = 'grey', label = 'Baseline')
ax.bar(b1, RoofRack, width = barwidth, edgecolor = 'grey', label = 'Roof Rack')
ax.bar(b2, RoofBox, width = barwidth, edgecolor = 'grey', label = 'Roof Box')
ax.bar(b1, OpenBox, width = barwidth, edgecolor = 'grey', label = 'Open Box')

ax.set_ylabel('Drag Coefficient ($C_D$)', fontsize = 12, fontweight = 'bold')
ax.set_xticks([r + barwidth for r in range(len(b0))], 
              ['Baseline', 'Roof Rack', 'Roof Box', 'Open Box'])
ax.set_xlabel('Configuration', fontsize = 12, fontweight = 'bold')
ax.set_title('Drag breakdown', fontsize = 14, fontweight = 'bold')

ax.grid(True, linestyle='--', alpha = 0.5)
plt.legend()
plt.tight_layout()
plt.show()

level2 = Base + RoofRack
level3 = Base + RoofRack + RoofBox

fig, ax1 = plt.subplots(figsize = (10,6))

p1 = ax1.bar(b0, Base, width = 0.6, edgecolor = 'grey', label = 'Baseline', align = 'center')

p4 = ax1.bar(b0, OpenBox, width = 0.6, bottom = level3,  edgecolor = 'grey', label = 'Open Box', align = 'center')

p2 = ax1.bar(b0, RoofRack, width = 0.6, bottom = Base,  edgecolor = 'grey', label = 'Roof Rack', align = 'center')

p3 = ax1.bar(b0, RoofBox, width = 0.6, bottom = level2, edgecolor = 'grey', label = 'Roof Box', align = 'center')

containers = [p1, p4, p2, p3]

for c in containers:
    
    labels_locali = [f'{v:.3f}' if v > 0 else "" for v in c.datavalues]
    
    ax1.bar_label(c, labels=labels_locali, label_type='center', 
                 fontsize=9, color='white', fontweight='bold')

totali = Base + RoofRack+ RoofBox + OpenBox
labels_totali = [f'{val:.3f}' for val in totali]
ax1.bar_label(p4, labels=labels_totali, padding=8, fontweight='bold', fontsize=11, color='black')
ax1.set_ylabel('Drag Coefficient ($C_D$)', fontsize = 12, fontweight = 'bold')
ax1.set_xticks(b0, 
              ['Baseline', 'Open Box', 'Roof Rack', 'Roof Box'])
ax1.set_xlabel('Configuration', fontsize = 12, fontweight = 'bold')
ax1.set_title('Drag breakdown', fontsize = 14, fontweight = 'bold')
ax1.grid(True, linestyle='--', alpha = 0.5)
ax1.set_ylim(0, 0.55)
plt.legend()
plt.tight_layout()
plt.show()







