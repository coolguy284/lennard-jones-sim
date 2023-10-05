from math import floor

# simulation modeled after helium atom
# radius = 140 pm (van der walls), 28 pm (covalent); 40 pm is the value we're going with, so 40e-12 m
# mass = 4.002 602 mass units; one dalton (atomic mass unit) is 1.660 539 066 60e-27; so mass is 6.646476989051294e-27 kg
particle_radius = 40e-12
particle_mass = 6.646476989051294e-27 # 1.66053906660e-27 * 4.002602
grav_constant = 1 # normally 6.67408e-11
time_step = 1e-9
num_steps = 1000
csv_file_skip_steps = 10
status_update_skip_steps = 100

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
    multiplication_const = 1 / self.distance_to(other) * length
    
    return (
      -(other.x - self.x) * multiplication_const,
      -(other.y - self.y) * multiplication_const,
      -(other.z - self.z) * multiplication_const
    )

def populate_particles_list():
  particles = []
  
  particle_spacing = particle_radius * 2

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
  
  return tuple(particles)

class system_state:
  __slots__ = 'time', 'particles'
  
  def __init__(self, time, particles):
    self.time = time
    self.particles = particles

def simulate_tick(particles, time_step):
  # convert to list
  particles = list(particles)
  
  # calculate forces
  for i in range(len(particles)):
    particle_obj = particles[i]
    
    # for every other particle in front of this particle
    for j in range(i + 1, len(particles)):
      # calculate distance to particle
      particle_two_obj = particles[j]
      
      distance_squared = particle_obj.distance_to_squared(particle_two_obj)
      
      # calculate strength of gravitational force
      gravity_strength = grav_constant * particle_mass * particle_mass / distance_squared
      
      # calculate total radial force (negative is towards, positive is away)
      radial_force = gravity_strength
      
      # calculate radial force
      particle_one_accel = radial_force / particle_mass
      particle_two_accel = radial_force / particle_mass
      
      particle_one_accel_vector = particle_obj.vector_away_from_other(particle_two_obj, particle_one_accel)
      particle_two_accel_vector = particle_two_obj.vector_away_from_other(particle_obj, particle_two_accel)
      
      # apply radial force
      particles[i] = particle(
        particle_obj.x,
        particle_obj.y,
        particle_obj.z,
        particle_obj.dx + particle_one_accel_vector[0],
        particle_obj.dy + particle_one_accel_vector[1],
        particle_obj.dz + particle_one_accel_vector[2],
      )
      particles[j] = particle(
        particle_two_obj.x,
        particle_two_obj.y,
        particle_two_obj.z,
        particle_two_obj.dx + particle_two_accel_vector[0],
        particle_two_obj.dy + particle_two_accel_vector[1],
        particle_two_obj.dz + particle_two_accel_vector[2],
      )
  
  # apply velocity
  for i in range(len(particles)):
    particle_obj = particles[i]
    
    # apply velocity
    particles[i] = particle(
      particle_obj.x + particle_obj.dx * time_step,
      particle_obj.y + particle_obj.dy * time_step,
      particle_obj.z + particle_obj.dz * time_step,
      particle_obj.dx,
      particle_obj.dy,
      particle_obj.dz
    )
  
  # convert back to tuple
  return tuple(particles)

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

print('Creating particles...')

particles = populate_particles_list()

recorded_states = [
  # array of systemstate objects go here
]

print('Saving initial state...')

recorded_states.append(system_state(0, particles))

for i in range(1, num_steps // csv_file_skip_steps + 1):
  if i % (status_update_skip_steps // csv_file_skip_steps) == 0:
    print(f'Calculating state {i * csv_file_skip_steps}...')
  current_time = time_step * i
  for i in range(csv_file_skip_steps):
    particles = simulate_tick(particles, time_step)
  recorded_states.append(system_state(current_time, particles))

print('Saving to csv file...')

particle_string = get_particle_string(recorded_states)

with open('data/calculations_1.csv', 'w') as f:
  f.write(particle_string)
