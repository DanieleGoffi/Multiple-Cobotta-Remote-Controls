import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

# Definizione della matrice di trasformazione DH
def dh_matrix(theta, d, a, alpha):
    theta = np.radians(theta)
    alpha = np.radians(alpha)
    return np.array([
        [np.cos(theta), -np.sin(theta) * np.cos(alpha), np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
        [np.sin(theta), np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
        [0, np.sin(alpha), np.cos(alpha), d],
        [0, 0, 0, 1]
    ])

# Parametri DH del Cobotta (approssimati, sostituisci con i valori esatti)
DH_PARAMS = [
    (0, 100, 0, -90),   # Theta1, d1, a1, alpha1
    (0, 0, 250, 0),    # Theta2, d2, a2, alpha2
    (0, 0, 160, 0),    # Theta3, d3, a3, alpha3
    (0, 0, 0, -90),    # Theta4, d4, a4, alpha4
    (0, 130, 0, 90),   # Theta5, d5, a5, alpha5
    (0, 50, 0, 0)      # Theta6, d6, a6, alpha6
]

# Limiti dei giunti (in gradi)
JOINT_LIMITS = [
    (-90, 90),  # Giunto 1
    (-90, 90),  # Giunto 2
    (-90, 90),  # Giunto 3
    (-180, 180),# Giunto 4
    (-90, 90),  # Giunto 5
    (-180, 180) # Giunto 6
]

# Generazione dei punti nello spazio
num_samples = 7  # Maggiore = più dettagliato ma più lento
points = []

def forward_kinematics(thetas):
    T = np.eye(4)
    for i in range(6):
        T = T @ dh_matrix(thetas[i], *DH_PARAMS[i][1:])
    return T[:3, 3]  # Estrai solo x, y, z

# Inizio timing
t_start = time.time()

# Campioniamo diversi angoli
angles = [np.linspace(lim[0], lim[1], num_samples) for lim in JOINT_LIMITS]
for theta1 in angles[0]:
    for theta2 in angles[1]:
        for theta3 in angles[2]:
            for theta4 in angles[3]:
                for theta5 in angles[4]:
                    for theta6 in angles[5]:
                        xyz = forward_kinematics([theta1, theta2, theta3, theta4, theta5, theta6])
                        points.append(xyz)

# Fine timing
t_end = time.time()
print(f"Tempo di calcolo: {t_end - t_start:.2f} secondi")

# Convertiamo in array numpy
points = np.array(points)

# Plot 3D
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=1, c='b', alpha=0.5)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Volume di lavoro del Cobotta")
plt.show()
