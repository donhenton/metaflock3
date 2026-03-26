# ── config.py ─────────────────────────────────────────────────────────────────
# All tuneable constants in one place. Change here, nowhere else.

# ── simulation ────────────────────────────────────────────────────────────────
N_AGENTS      = 12
SPAWN_RADIUS  = 2.5

# ── animation ─────────────────────────────────────────────────────────────────
FPS           = 24
FRAME_START   = 1
FRAME_END     = 180

# ── camera ────────────────────────────────────────────────────────────────────
CAM_LOCATION  = (12, -12, 7)
CAM_LERP      = 0.04      # 0.0 = locked, 1.0 = instant snap, 0.04 = lazy drift

# ── light ─────────────────────────────────────────────────────────────────────
LIGHT_TYPE    = "POINT"
LIGHT_LOCATION = (6, 4, 10)
LIGHT_ENERGY  = 600

# ── metaballs ─────────────────────────────────────────────────────────────────
MB_THRESHOLD  = 0.35
MB_RESOLUTION = 0.3
AGENT_RADIUS  = 1.0
AGENT_STIFFNESS = 0.6

# ── boids ─────────────────────────────────────────────────────────────────────
BOIDS_MAX_SPEED        = 0.9
BOIDS_NEIGHBOR_RADIUS  = 3.5
BOIDS_SEPARATION_RADIUS = 1.2
BOIDS_W_SEPARATION     = 2.5
BOIDS_W_ALIGNMENT      = 2.0
BOIDS_W_COHESION       = 3.0
BOIDS_COHESION_SCALE   = 0.05
BOIDS_ALIGNMENT_SCALE  = 0.3
BOIDS_INIT_VEL         = 1.5   # ±range for random starting velocity

# ── lava lamp ─────────────────────────────────────────────────────────────────
LAVA_RISE_SPEED     = 0.015
LAVA_DRIFT_SPEED    = 0.003
LAVA_WALL_PULL      = 0.02
LAVA_WALL_RADIUS    = 2.5
LAVA_VERTICAL_RANGE = 3.0
LAVA_FREQ           = 0.04    # sine oscillation frequency

# ── world background ──────────────────────────────────────────────────────────
WORLD_NOISE_SCALE    = 4.0
WORLD_WAVE_DISTORTION = 8.0
WORLD_DARKNESS       = 0.15

# ── reference objects ─────────────────────────────────────────────────────────
FLOOR_SIZE      = 14.0
FLOOR_Z         = -4.0
MONOLITH_COUNT  = 4
