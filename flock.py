# ── flock.py ──────────────────────────────────────────────────────────────────
import random
import config
from mathutils import Vector


class Agent:
    def __init__(self, position, velocity):
        self.position  = Vector(position)
        self.velocity  = Vector(velocity)
        self.radius    = config.AGENT_RADIUS
        self.stiffness = config.AGENT_STIFFNESS

    @property
    def speed(self):
        return self.velocity.length


class Flock:
    def __init__(self, agents, behavior):
        self.agents   = agents
        self.behavior = behavior  # any callable: behavior(flock)

    @property
    def centroid(self):
        if not self.agents:
            return Vector((0, 0, 0))
        total = Vector((0, 0, 0))
        for a in self.agents:
            total += a.position
        return total / len(self.agents)


def init_flock(n_agents, behavior):
    """
    Spawn n agents with randomised positions and velocities.
    behavior — any callable with signature behavior(flock).
    """
    r   = config.SPAWN_RADIUS
    vel = config.BOIDS_INIT_VEL

    agents = []
    for _ in range(n_agents):
        pos = (
            random.uniform(-r, r),
            random.uniform(-r, r),
            random.uniform(-r, r),
        )
        v = (
            random.uniform(-vel, vel),
            random.uniform(-vel, vel),
            random.uniform(-vel, vel),
        )
        agents.append(Agent(pos, v))

    print(f"[flock] {n_agents} agents | behavior: {getattr(behavior, '__name__', type(behavior).__name__)}")
    return Flock(agents, behavior)


def step_flock(flock):
    """Advance one tick — delegate entirely to the attached behavior."""
    flock.behavior(flock)
