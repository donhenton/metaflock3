# ── behaviors/lavalamp.py ─────────────────────────────────────────────────────
# Callable object — needs internal state (frame counter, per-agent phase).
# From the outside it looks identical to calling boids:
#   init_flock(n, LavaLamp())
import math
import random
import config
from mathutils import Vector


class LavaLamp:
    """
    Lava lamp simulation.
    Agents rise and fall independently on phase-offset sine waves,
    constrained to a vertical column. Oblivious to each other —
    the metaball field handles all visual merging.

    Callable signature: instance(flock) -> None
    """

    def __init__(self):
        self.frame = 0

    def __call__(self, flock):
        self.frame += 1

        for agent in flock.agents:
            # inject phase on first encounter
            if not hasattr(agent, 'phase'):
                agent.phase = random.uniform(0, 2 * math.pi)

            # vertical oscillation — each agent on its own sine phase
            vertical = math.sin(self.frame * config.LAVA_FREQ + agent.phase) * config.LAVA_RISE_SPEED

            # subtle horizontal drift
            drift_x = random.uniform(-config.LAVA_DRIFT_SPEED, config.LAVA_DRIFT_SPEED)
            drift_y = random.uniform(-config.LAVA_DRIFT_SPEED, config.LAVA_DRIFT_SPEED)

            # wall pull — nudge back toward centre if too far out
            wall_x = -agent.position.x * config.LAVA_WALL_PULL if abs(agent.position.x) > config.LAVA_WALL_RADIUS else 0.0
            wall_y = -agent.position.y * config.LAVA_WALL_PULL if abs(agent.position.y) > config.LAVA_WALL_RADIUS else 0.0

            agent.velocity  = Vector((drift_x + wall_x, drift_y + wall_y, vertical))
            agent.position += agent.velocity

            # soft clamp vertical range
            agent.position.z = max(-config.LAVA_VERTICAL_RANGE, min(config.LAVA_VERTICAL_RANGE, agent.position.z))
