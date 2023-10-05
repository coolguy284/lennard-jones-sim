class particle:
  __slots__ = 'x', 'y', 'z', 'dx', 'dy', 'dz'
  
  def __init__(self, *args):
    if len(args) == 6:
      self.x = args[0]; self.y = args[1]; self.z = args[2]
      self.dx = args[3]; self.dy = args[4]; self.dz = args[5]
    elif len(args) == 1:
      self.x = args[0].x; self.y = args[0].y; self.z = args[0].z
      self.dx = args[0].dx; self.dy = args[0].dy; self.dz = args[0].dz
  
  def distance_to_squared(self, other):
    return (other.x - self.x) ** 2 + (other.y - self.y) ** 2 + (other.z - self.z) ** 2
  
  def distance_to(self, other):
    return self.distance_to_squared(other) ** 0.5
  
  def vector_away_from_other(self, other, length):
    # multiply difference between the 2 particles' positions, by 1 / distance, then by length
    
    # calculate this multiplication constant
    distance = self.distance_to(other)
    multiplication_const = 1 / distance * length if distance != 0 else 0
    
    return (
      (self.x - other.x) * multiplication_const,
      (self.y - other.y) * multiplication_const,
      (self.z - other.z) * multiplication_const
    )
  
  def apply_velocity(self, dx, dy, dz, time_step):
    return particle(
      self.x + dx * time_step,
      self.y + dy * time_step,
      self.z + dz * time_step,
      self.dx,
      self.dy,
      self.dz
    )
  
  def apply_own_velocity(self, time_step):
    return self.apply_velocity(self.dx, self.dy, self.dz, time_step)
  
  def apply_acceleration(self, ddx, ddy, ddz, time_step):
    return particle(
      self.x,
      self.y,
      self.z,
      self.dx + ddx * time_step,
      self.dy + ddy * time_step,
      self.dz + ddz * time_step,
    )

class system_state:
  __slots__ = 'time', 'particles'
  
  def __init__(self, time, particles):
    self.time = time
    self.particles = particles

class simulation_params:
  __slots__ = (
    'particle_radius',
    'particle_mass',
    'grav_constant',
    'lennard_jones_well_depth',
    'linear_damping_multiplier',
    'time_step',
    'num_steps',
    'particle_configuration',
    'csv_file_skip_steps',
    'status_update_skip_steps',
  )
  
  def __init__(
    self,
    particle_radius,
    particle_mass,
    grav_constant,
    lennard_jones_well_depth,
    linear_damping_multiplier,
    time_step,
    num_steps,
    particle_configuration,
    csv_file_skip_steps,
    status_update_skip_steps
  ):
    self.particle_radius = particle_radius
    self.particle_mass = particle_mass
    self.grav_constant = grav_constant
    self.lennard_jones_well_depth = lennard_jones_well_depth
    self.linear_damping_multiplier = linear_damping_multiplier
    self.time_step = time_step
    self.num_steps = num_steps
    self.particle_configuration = particle_configuration
    self.csv_file_skip_steps = csv_file_skip_steps
    self.status_update_skip_steps = status_update_skip_steps
