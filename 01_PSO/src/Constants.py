# ---PARTICLE consts
MAX_POS = 5           # Maximum value of the position for both X and Y throughout the whole simulation
MIN_POS = -5           # Minimum value of the position for both X and Y throughout the whole simulation
MAX_VEL = 1             # Maximum value of the velocity for both X and Y for the initialization
MIN_VEL = -1           # Minimum value of the velocity for both X and Y for the initialization
SPEED = 0.05
W = 0.4                 # Factor for the current velocity (> means exploitation, < means exploration)
C1 = 2                  # Factor for the cognitive velocity (>C2 means exploitation, <C2 means exploration)
C2 = 2                  # Factor for the cognitive velocity (>C1 means exploration, <C1 means exploitation)

# ---PSO consts

DIMENSION = 2

N_PARTICLES = 20       # Number of particles used for the simulation
N_ITERATIONS = 1000     # Number of iterations used for the PSO
