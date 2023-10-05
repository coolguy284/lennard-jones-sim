import sys
from os import chdir
from os.path import exists

from classes import *
from simulation import *

# simulation modeled after helium atom
# radius = 140 pm (van der walls), 28 pm (covalent); 40 pm is the value we're going with, so 40e-12 m
# mass = 4.002 602 mass units; one dalton (atomic mass unit) is 1.660 539 066 60e-27; so mass is 6.646476989051294e-27 kg
# constants defined in perform_simulation_run

testing = False

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
  grav_constant = 1e8 # normally 6.67408e-11
  lennard_jones_well_depth = 1e-32
  #linear_damping_multiplier = 0.95 # this is basically multiplied by the velocity every nanosecond
  time_step = 1e-9
  num_steps = 1000
  
  if run_number == 1:
    simulation_params_obj = simulation_params(
      particle_radius = particle_radius,
      particle_mass = particle_mass,
      grav_constant = 0,
      lennard_jones_well_depth = 0,
      linear_damping_multiplier = 0,
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
      linear_damping_multiplier = 0.95,
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
      linear_damping_multiplier = 0.95,
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
      linear_damping_multiplier = 0.95,
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
      linear_damping_multiplier = 0.95,
      time_step = time_step * 3,
      num_steps = num_steps,
      particle_configuration = 3,
      csv_file_skip_steps = 10,
      status_update_skip_steps = 10,
    )
  elif run_number == 6:
    simulation_params_obj = simulation_params(
      particle_radius = particle_radius,
      particle_mass = particle_mass,
      grav_constant = grav_constant,
      lennard_jones_well_depth = lennard_jones_well_depth,
      linear_damping_multiplier = 0.95,
      time_step = time_step,
      num_steps = num_steps * 60,
      particle_configuration = 3,
      csv_file_skip_steps = 10,
      status_update_skip_steps = 10,
    )
  elif run_number == 7:
    simulation_params_obj = simulation_params(
      particle_radius = particle_radius,
      particle_mass = particle_mass,
      grav_constant = grav_constant,
      lennard_jones_well_depth = lennard_jones_well_depth,
      linear_damping_multiplier = 0.997,
      time_step = time_step,
      num_steps = num_steps * 60,
      particle_configuration = 3,
      csv_file_skip_steps = 10,
      status_update_skip_steps = 10,
    )
  elif run_number == 8:
    simulation_params_obj = simulation_params(
      particle_radius = particle_radius,
      particle_mass = particle_mass,
      grav_constant = grav_constant,
      lennard_jones_well_depth = lennard_jones_well_depth,
      linear_damping_multiplier = 1,
      time_step = time_step,
      num_steps = num_steps * 60,
      particle_configuration = 3,
      csv_file_skip_steps = 10,
      status_update_skip_steps = 10,
    )
  elif run_number == 9:
    simulation_params_obj = simulation_params(
      particle_radius = particle_radius,
      particle_mass = particle_mass,
      grav_constant = grav_constant,
      lennard_jones_well_depth = lennard_jones_well_depth,
      linear_damping_multiplier = 1,
      time_step = time_step / 10,
      num_steps = num_steps * 200,
      particle_configuration = 3,
      csv_file_skip_steps = 100,
      status_update_skip_steps = 100,
    )
  elif run_number == 10:
    simulation_params_obj = simulation_params(
      particle_radius = particle_radius,
      particle_mass = particle_mass,
      grav_constant = grav_constant,
      lennard_jones_well_depth = lennard_jones_well_depth,
      linear_damping_multiplier = 0.997,
      time_step = time_step / 10,
      num_steps = num_steps * 200,
      particle_configuration = 3,
      csv_file_skip_steps = 100,
      status_update_skip_steps = 100,
    )
  elif run_number == 11:
    simulation_params_obj = simulation_params(
      particle_radius = particle_radius,
      particle_mass = particle_mass,
      grav_constant = grav_constant,
      lennard_jones_well_depth = lennard_jones_well_depth,
      linear_damping_multiplier = 0.9998,
      time_step = time_step / 10,
      num_steps = num_steps * 250,
      particle_configuration = 3,
      csv_file_skip_steps = 20,
      status_update_skip_steps = 100,
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

if testing:
  particle_one = particle(0, 0, 0, 0, 0, 0)
  particle_two = particle(0.1, 0.1, 0.1, 0, 0, 0)
  print(particle_one.distance_to(particle_two))
  print(particle_one.vector_away_from_other(particle_two, 2.0))
  exit()

# change directory to program's path
chdir(sys.path[0])

print('Lennard Jones Simulator -- Python Version')
print()

perform_simulation_run(1, 'moving_right')
perform_simulation_run(2, 'gravity')
perform_simulation_run(3, 'lennard_jones_3x3x3')
perform_simulation_run(4, 'lennard_jones_7x7x7')
perform_simulation_run(5, 'lennard_jones_7x7x7_coarse')
perform_simulation_run(6, 'lennard_jones_7x7x7_long')
perform_simulation_run(7, 'lennard_jones_7x7x7_long_lightdamped')
perform_simulation_run(8, 'lennard_jones_7x7x7_long_undamped')
perform_simulation_run(9, 'lennard_jones_7x7x7_long_undamped_accurate')
perform_simulation_run(10, 'lennard_jones_7x7x7_long_lightdamped_accurate')
perform_simulation_run(11, 'lennard_jones_7x7x7_long_verylightdamped_accurate')
