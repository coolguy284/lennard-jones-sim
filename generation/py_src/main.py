import sys
from math import floor
from os import chdir
from os.path import exists

# simulation modeled after helium atom
# radius = 140 pm (van der walls), 28 pm (covalent); 40 pm is the value we're going with, so 40e-12 m
# mass = 4.002 602 mass units; one dalton (atomic mass unit) is 1.660 539 066 60e-27; so mass is 6.646476989051294e-27 kg
# constants defined in perform_simulation_run

# change directory to program's path
chdir(sys.path[0])

testing = False

# particles objects go here
particles = None

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
      -(other.x - self.x) * multiplication_const,
      -(other.y - self.y) * multiplication_const,
      -(other.z - self.z) * multiplication_const
    )
  
  def apply_velocity(self, dx, dy, dz, time_step):
    return particle(
      self.x + self.dx * time_step,
      self.y + self.dy * time_step,
      self.z + self.dz * time_step,
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

def populate_particles_list(simulation_params_obj):
  particles = []
  
  particle_spacing = simulation_params_obj.particle_radius * 2

  if simulation_params_obj.particle_configuration == 1:
    x_span = 2
    y_span = 2
    z_span = 2
    
    for i in range(floor(-x_span / 2), floor(x_span / 2) + 1):
      for j in range(floor(-y_span / 2), floor(y_span / 2) + 1):
        for k in range(floor(-z_span / 2), floor(z_span / 2) + 1):
          x = i * particle_spacing
          y = j * particle_spacing
          z = k * particle_spacing
          
          particles.append(particle(x, y, z, 0, 0, 0))
  elif simulation_params_obj.particle_configuration == 2:
    x_span = 2
    y_span = 2
    z_span = 2
    
    for i in range(floor(-x_span / 2), floor(x_span / 2) + 1):
      for j in range(floor(-y_span / 2), floor(y_span / 2) + 1):
        for k in range(floor(-z_span / 2), floor(z_span / 2) + 1):
          x = i * particle_spacing
          y = j * particle_spacing
          z = k * particle_spacing
          
          particles.append(particle(x, y, z, particle_spacing / simulation_params_obj.time_step * 0.05, 0, 0))
  elif simulation_params_obj.particle_configuration == 3:
    x_span = 6
    y_span = 6
    z_span = 6
    
    for i in range(floor(-x_span / 2), floor(x_span / 2) + 1):
      for j in range(floor(-y_span / 2), floor(y_span / 2) + 1):
        for k in range(floor(-z_span / 2), floor(z_span / 2) + 1):
          x = i * particle_spacing
          y = j * particle_spacing
          z = k * particle_spacing
          
          particles.append(particle(x, y, z, 0, 0, 0))
  
  return tuple(particles)

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
    'linear_damping_strength',
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
    linear_damping_strength,
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
    self.linear_damping_strength = linear_damping_strength
    self.time_step = time_step
    self.num_steps = num_steps
    self.particle_configuration = particle_configuration
    self.csv_file_skip_steps = csv_file_skip_steps
    self.status_update_skip_steps = status_update_skip_steps

def simulate_tick(particles, simulation_params_obj):
  # convert to list
  new_particles = list(particles)
  
  # calculate forces
  for i in range(len(particles)):
    particle_obj = particles[i]
    
    # for every other particle in front of this particle
    for j in range(i + 1, len(particles)):
      # calculate distance to particle
      particle_two_obj = particles[j]
      
      distance_squared = particle_obj.distance_to_squared(particle_two_obj)
      distance = distance_squared ** 0.5
      
      # calculate strength of gravitational force
      gravity_strength = simulation_params_obj.grav_constant * simulation_params_obj.particle_mass * simulation_params_obj.particle_mass / distance_squared if distance_squared != 0 else 0
      
      # calculate strength of lennard jones force
      # potential energy is 4 * lennard_jones_well_depth * ((particle_radius / distance) ^ 12 - (particle_radius / distance) ^ 6)
      # force is -1 * 4 * lennard_jones_well_depth * (12 * (particle_radius / distance) ^ 11 * (-particle_radius / distance^2) - 6 * (particle_radius / distance) ^ 5 * (-particle_radius / distance^2))
      rescaled_distance = simulation_params_obj.particle_radius / distance
      rescaled_distance_d_dx = -simulation_params_obj.particle_radius / distance ** 2
      
      lennard_jones_strength = -1 * 4 * simulation_params_obj.lennard_jones_well_depth * (12 * rescaled_distance ** 11 * rescaled_distance_d_dx - 6 * rescaled_distance ** 5 * rescaled_distance_d_dx)
      
      # calculate total radial force (negative is towards, positive is away)
      radial_force = -gravity_strength + lennard_jones_strength
      
      # calculate radial force
      particle_one_accel = radial_force / simulation_params_obj.particle_mass
      particle_two_accel = radial_force / simulation_params_obj.particle_mass
      
      particle_one_accel_vector = particle_obj.vector_away_from_other(particle_two_obj, particle_one_accel)
      particle_two_accel_vector = particle_two_obj.vector_away_from_other(particle_obj, particle_two_accel)
      
      # apply radial force
      new_particles[i] = new_particles[i].apply_acceleration(*particle_one_accel_vector, simulation_params_obj.time_step)
      new_particles[j] = new_particles[j].apply_acceleration(*particle_two_accel_vector, simulation_params_obj.time_step)
  
  # apply velocity
  for i in range(len(new_particles)):
    particle_obj = new_particles[i]
    
    new_particles[i] = particle_obj.apply_own_velocity(simulation_params_obj.time_step)
  
  # apply linear damping
  if simulation_params_obj.linear_damping_strength != 1:
    # apply velocity
    for i in range(len(new_particles)):
      particle_obj = new_particles[i]
      
      new_particles[i] = particle(
        particle_obj.x,
        particle_obj.y,
        particle_obj.z,
        particle_obj.dx * simulation_params_obj.linear_damping_strength ** (simulation_params_obj.time_step * 1e9),
        particle_obj.dy * simulation_params_obj.linear_damping_strength ** (simulation_params_obj.time_step * 1e9),
        particle_obj.dz * simulation_params_obj.linear_damping_strength ** (simulation_params_obj.time_step * 1e9),
      )
  
  # convert back to tuple
  return tuple(new_particles)

def get_particle_string(recorded_states):
  # figure out column headers
  
  num_particles = len(recorded_states[0].particles)
  
  headers = ['time']
  
  for i in range(1, num_particles + 1):
    headers.append(f'p{i}_x')
    headers.append(f'p{i}_y')
    headers.append(f'p{i}_z')
    headers.append(f'p{i}_dx')
    headers.append(f'p{i}_dy')
    headers.append(f'p{i}_dz')
  
  # create var for each line of file
  
  file_lines = []
  
  file_lines.append(','.join(headers))
  
  # add each state to file lines
  
  for state in recorded_states:
    file_line = []
    
    file_line.append(str(state.time))
    
    for particle_obj in state.particles:
      file_line.append(str(particle_obj.x))
      file_line.append(str(particle_obj.y))
      file_line.append(str(particle_obj.z))
      file_line.append(str(particle_obj.dx))
      file_line.append(str(particle_obj.dy))
      file_line.append(str(particle_obj.dz))
    
    file_lines.append(','.join(file_line))
  
  return '\n'.join(file_lines)

if testing:
  particle_one = particle(0, 0, 0, 0, 0, 0)
  particle_two = particle(0.1, 0.1, 0.1, 0, 0, 0)
  print(particle_one.distance_to(particle_two))
  print(particle_one.vector_away_from_other(particle_two, 2.0))
  exit()

def perform_simulation_run(run_number, file_name, force_rerun = False):
  file_name_extended = f'{run_number:0>2}_{file_name}'
  full_file_path = f'../../data/calculations_{file_name_extended}.csv'
  
  print(f'Simulating run {file_name_extended}...')
  
  # assume already calculated if file already exists
  if not force_rerun and exists(full_file_path):
    print('Path already exists, not calculating.')
    print()
    return
  
  # constants defined here
  particle_radius = 40e-12
  particle_mass = 6.646476989051294e-27 # 1.66053906660e-27 * 4.002602
  grav_constant = 0 # normally 6.67408e-11
  lennard_jones_well_depth = 1e-32
  linear_damping_strength = 0.95 # this is basically multiplied by the velocity every nanosecond
  time_step = 1e-9
  num_steps = 1000
  
  if run_number == 1:
    simulation_params_obj = simulation_params(
      particle_radius = particle_radius,
      particle_mass = particle_mass,
      grav_constant = 0,
      lennard_jones_well_depth = 0,
      linear_damping_strength = 0,
      time_step = time_step,
      num_steps = num_steps,
      particle_configuration = 2,
      csv_file_skip_steps = 10,
      status_update_skip_steps = 100,
    )
  elif run_number == 2:
    simulation_params_obj = simulation_params(
      particle_radius = particle_radius,
      particle_mass = particle_mass,
      grav_constant = grav_constant,
      lennard_jones_well_depth = lennard_jones_well_depth,
      linear_damping_strength = linear_damping_strength,
      time_step = time_step,
      num_steps = num_steps,
      particle_configuration = 1,
      csv_file_skip_steps = 10,
      status_update_skip_steps = 100,
    )
  elif run_number == 3:
    simulation_params_obj = simulation_params(
      particle_radius = particle_radius,
      particle_mass = particle_mass,
      grav_constant = grav_constant,
      lennard_jones_well_depth = lennard_jones_well_depth,
      linear_damping_strength = linear_damping_strength,
      time_step = time_step,
      num_steps = num_steps,
      particle_configuration = 1,
      csv_file_skip_steps = 10,
      status_update_skip_steps = 100,
    )
  elif run_number == 4:
    simulation_params_obj = simulation_params(
      particle_radius = particle_radius,
      particle_mass = particle_mass,
      grav_constant = grav_constant,
      lennard_jones_well_depth = lennard_jones_well_depth,
      linear_damping_strength = linear_damping_strength,
      time_step = time_step,
      num_steps = num_steps,
      particle_configuration = 3,
      csv_file_skip_steps = 10,
      status_update_skip_steps = 10,
    )
  elif run_number == 5:
    simulation_params_obj = simulation_params(
      particle_radius = particle_radius,
      particle_mass = particle_mass,
      grav_constant = grav_constant,
      lennard_jones_well_depth = lennard_jones_well_depth,
      linear_damping_strength = linear_damping_strength,
      time_step = time_step * 3,
      num_steps = num_steps,
      particle_configuration = 3,
      csv_file_skip_steps = 10,
      status_update_skip_steps = 10,
    )

  print('Creating particles...')

  particles = populate_particles_list(simulation_params_obj)

  recorded_states = [
    # array of systemstate objects will get put here
  ]

  print('Recording initial state...')

  recorded_states.append(system_state(0, particles))

  print('Calculating...')

  for i in range(1, simulation_params_obj.num_steps // simulation_params_obj.csv_file_skip_steps + 1):
    current_time = simulation_params_obj.time_step * i
    for _ in range(simulation_params_obj.csv_file_skip_steps):
      particles = simulate_tick(particles, simulation_params_obj)
    recorded_states.append(system_state(current_time, particles))
    if i % (simulation_params_obj.status_update_skip_steps // simulation_params_obj.csv_file_skip_steps) == 0:
      print(f'Calculated state {i * simulation_params_obj.csv_file_skip_steps}/{simulation_params_obj.num_steps}')

  print('Saving to csv file...')

  particle_string = get_particle_string(recorded_states)

  with open(full_file_path, 'w') as f:
    f.write(particle_string)
  
  print()

perform_simulation_run(1, 'moving_right')
perform_simulation_run(2, 'gravity')
perform_simulation_run(3, 'lennard_jones_3x3x3')
perform_simulation_run(4, 'lennard_jones_7x7x7')
perform_simulation_run(5, 'lennard_jones_7x7x7_coarse', force_rerun = True)
