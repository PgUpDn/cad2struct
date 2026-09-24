import matplotlib.pyplot as plt 
import numpy as np

dimensions = {
    'Length': 5700,
    'Width_base':2000,
    'Width_up':1200,
    'Height':1750 
}

Cds = {
    'Base':0.312,
    'OpenBox':0.375,
    'RoofRack':0.337,
    'RoofBox':0.408
}

coefficient = {
    'Base':0.815,
    'OpenBox':0.815,
    'RoofRack':0.815, 
    'RoofBox':0.780
}

Areas = {
    'Base':3.346,
    'OpenBox':3.346,
    'RoofRack':3.346,
    'RoofBox':4.083
}

#Constants
rho = 1.225 #[Kg/m^3]
v_km = np.linspace(100, 150, 20)
v = v_km/3.6
eta = 0.9
E_battery = 123000 #[Wh] nominal maximum capacity of the cybertruck

ranges = {}

fig, ax = plt.subplots(figsize = (10,6))

for config in Cds.keys():

    Cd = Cds[config]
    Ar = Areas[config] #value of the rough estimate of the area
    K = coefficient[config]

    Ax = Ar * K #real value of the frontal area

    Pcd = (0.5 * rho * Ax * Cd * v**3) / eta #[W]
    P = Pcd / 1000 #[KW]

    Consumption = Pcd/v_km

    range = E_battery / Consumption
    ranges[config] = range

    ax.plot(v_km, range, 'o-', label = f"{config}($C_D$ = {Cd}, $A_x$ = {Ax:.3f} $m^2$)", linewidth = 2)
 

ax.set_xlabel('Velocity (km/h)', fontweight='bold')
ax.set_ylabel('Estimated autonomy (km)', fontweight='bold')
ax.set_title('Estimate of the impact of drag\non Tesla CyberTruck autonomy', fontsize=14, fontweight='bold')
ax.grid(True, alpha = 0.3)
ax.legend(fontsize = 'large')

plt.tight_layout()
plt.show()

print("\n" + "="*85)
print(f"{'SPEED':<10} | {'CONFIG':<10} | {'RANGE [km]':<12} | {'DELTA [km]':<12} | {'DELTA [%]':<10}")
print("="*85)

base_range = ranges['Base']

for i, vel in enumerate(v_km):
    base_val = base_range[i]
    print("\n")
    print(f"{vel:>3.0f} km/h   | {'Base':<10} | {base_val:>10.2f} | {'-':>12} | {'-':>10}")
    for config in Cds.keys():
        if config == 'Base': continue
        
        current_val = ranges[config][i]
        delta_km = current_val - base_val
        delta_perc = (delta_km / base_val) * 100
        
        print(f"{'':<10} | {config:<10} | {current_val:>10.2f} | {delta_km:>12.2f} | {delta_perc:>9.2f}%")
    print("-" * 85)
