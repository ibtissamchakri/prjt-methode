import numpy as np
import matplotlib.pyplot as plt

# --- 1. Paramètres de la Simulation ---

# Nombre de points INTERNES sur un côté de la grille.
# Pour une grille de 4x4 inconnues.
N = 100

# Le domaine est un carré de [0,1] x [0,1]
# h est le pas de discrétisation
h = 1.0 / (N + 1)

# Coordonnées des points de la grille (incluant les bords)
x = np.linspace(0, 1, N + 2)
y = np.linspace(0, 1, N + 2)
X, Y = np.meshgrid(x, y)

# --- 2. Définition de la source f(x,y) ---
# On pr..............end une source constante pour la simplicité.
# f est évaluée sur les points INTERNES de la grille.
F_source = np.full((N, N), 100.0)

# --- 3. Construction de la Matrice A et du Vecteur F ---
# Le système linéaire à résoudre est AU = F

# Le nombre total d'inconnues est N*N = 16
taille_matrice = N * N
A = np.zeros((taille_matrice, taille_matrice))
F = np.zeros(taille_matrice)

# Boucle sur tous les points INTERNES (i,j) de la grille
# i (colonnes) et j (lignes) vont de 0 à N-1
for j in range(N):
    for i in range(N):
        # Conversion des indices 2D (i,j) en indice 1D k
        # On parcourt la grille ligne par ligne.
        k = i + j * N

        # Terme diagonal (4 * u_ij)
        A[k, k] = 4

        # Voisin de droite (u_{i+1,j})
        if i < N - 1:
            A[k, k + 1] = -1

        # Voisin de gauche (u_{i-1,j})
        if i > 0:
            A[k, k - 1] = -1

        # Voisin du dessus (u_{i,j+1})
        if j < N - 1:
            A[k, k + N] = -1
            
        # Voisin du dessous (u_{i,j-1})
        if j > 0:
            A[k, k - N] = -1
            
        # Construction du second membre F
        # F_k = h^2 * f(x_i, y_j)
        F[k] = h**2 * F_source[j, i] # Note: F_source[j,i] pour correspondre au parcours

# --- 4. Résolution du Système et Visualisation ---

print(f"Discrétisation avec N={N}, taille de la matrice A: {A.shape}")
print("Résolution du système linéaire AU = F...")
# Résout le système. U_flat est un vecteur de 16 valeurs.
U_flat = np.linalg.solve(A, F)
print("Résolution terminée.")

# On remet le vecteur solution en forme de grille 2D (4x4)
U_grid = U_flat.reshape((N, N))

# On crée la carte de température complète en ajoutant les bords (u=0)
# np.pad ajoute des '0' tout autour de notre grille de résultats.
U_complete = np.pad(U_grid, pad_width=1, mode='constant', constant_values=0)

# Affichage du résultat
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Surface 3D
ax.plot_surface(X, Y, U_complete, cmap='viridis')

ax.set_title(f"Solution u(x,y) pour N={N}")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("u(x,y)")
plt.show()

# Affichage 2D
plt.figure(figsize=(7, 6))
plt.pcolormesh(X, Y, U_complete, cmap='hot', shading='auto')
plt.colorbar(label="Valeur de u(x,y)")
plt.title(f"Carte de la solution u(x,y) pour N={N}")
plt.xlabel("x")
plt.ylabel("y")
plt.axis('equal')
plt.show()
