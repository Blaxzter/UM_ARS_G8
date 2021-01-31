# ---PARTICLE consts
MAX_POS = 10000     # Maximum value of the position for both X and Y throughout the whole simulation
MIN_POS = 0         # Minimum value of the position for both X and Y throughout the whole simulation
MAX_VEL = 1         # Maximum value of the velocity for both X and Y for the initialization
MIN_VEL = 0.1       # Minimum value of the velocity for both X and Y for the initialization
W = 0.5             # Factor for the current velocity (> means exploitation, < means exploration)
C1 = 2              # Factor for the cognitive velocity (>C2 means exploitation, <C2 means exploration)
C2 = 2              # Factor for the cognitive velocity (>C1 means exploration, <C1 means exploitation)

# ---PSO consts
N_PARTICLES = 100   # Number of particles used for the simulation
N_ITERATIONS = 10   # Number of iterations used for the PSO
