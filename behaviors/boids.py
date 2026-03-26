# ── behaviors/boids.py ────────────────────────────────────────────────────────
# Pure function — no state needed.
# Usage: pass boids directly to init_flock(n, boids)
import config
from mathutils import Vector


def boids(flock):
    """
    Classic Reynolds boids — separation, alignment, cohesion.
    Callable signature: boids(flock) -> None
    """
    agents       = flock.agents
    new_velocities = []

    for agent in agents:
        neighbors = [
            a for a in agents
            if a is not agent
            and (a.position - agent.position).length < config.BOIDS_NEIGHBOR_RADIUS
        ]

        sep = _separation(agent, neighbors)
        aln = _alignment(agent, neighbors)
        coh = _cohesion(agent, neighbors)

        vel = (
            agent.velocity
            + sep * config.BOIDS_W_SEPARATION
            + aln * config.BOIDS_W_ALIGNMENT
            + coh * config.BOIDS_W_COHESION
        )

        if vel.length > config.BOIDS_MAX_SPEED:
            vel = vel.normalized() * config.BOIDS_MAX_SPEED

        new_velocities.append(vel)

    for agent, vel in zip(agents, new_velocities):
        agent.velocity  = vel
        agent.position += vel


def _separation(agent, neighbors):
    steer = Vector((0, 0, 0))
    close = [n for n in neighbors if (n.position - agent.position).length < config.BOIDS_SEPARATION_RADIUS]
    for n in close:
        diff = agent.position - n.position
        if diff.length > 0:
            steer += diff.normalized() / diff.length
    return steer


def _alignment(agent, neighbors):
    if not neighbors:
        return Vector((0, 0, 0))
    avg = Vector((0, 0, 0))
    for n in neighbors:
        avg += n.velocity
    avg /= len(neighbors)
    return (avg - agent.velocity) * config.BOIDS_ALIGNMENT_SCALE


def _cohesion(agent, neighbors):
    if not neighbors:
        return Vector((0, 0, 0))
    center = Vector((0, 0, 0))
    for n in neighbors:
        center += n.position
    center /= len(neighbors)
    return (center - agent.position) * config.BOIDS_COHESION_SCALE
