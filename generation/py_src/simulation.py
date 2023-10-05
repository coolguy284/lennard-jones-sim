from math import floor

from classes import *

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

def simulate_tick(particles, simulation_params_obj):
  # convert to list
  new_particles = list(particles)
  
  # calculate forces
  if simulation_params_obj.grav_constant != 0 or simulation_params.lennard_jones_well_depth != 0:
    for i in range(len(particles)):
      particle_obj = particles[i]
      
      # for every particle in front of this particle
      for j in range(i + 1, len(particles)):
        particle_two_obj = particles[j]
        
        # calculate distance to particle
        distance_squared = particle_obj.distance_to_squared(particle_two_obj)
        distance = distance_squared ** 0.5
        
        # only calculate force if distance is not zero
        if distance_squared != 0.0:
          # calculate strength of gravitational force
          if simulation_params_obj.grav_constant != 0:
            gravity_strength = simulation_params_obj.grav_constant * simulation_params_obj.particle_mass * simulation_params_obj.particle_mass / distance_squared
          else:
            gravity_strength = 0
          
          # calculate strength of lennard jones force
          # potential energy is 4 * lennard_jones_well_depth * ((particle_radius / distance) ^ 12 - (particle_radius / distance) ^ 6)
          # force is -1 * 4 * lennard_jones_well_depth * (12 * (particle_radius / distance) ^ 11 * (-particle_radius / distance^2) - 6 * (particle_radius / distance) ^ 5 * (-particle_radius / distance^2))
          if simulation_params_obj.lennard_jones_well_depth != 0:
            rescaled_distance = simulation_params_obj.particle_radius / distance
            rescaled_distance_d_dx = -simulation_params_obj.particle_radius / distance ** 2
            
            lennard_jones_strength = -1 * 4 * simulation_params_obj.lennard_jones_well_depth * (12 * rescaled_distance ** 11 * rescaled_distance_d_dx - 6 * rescaled_distance ** 5 * rescaled_distance_d_dx)
          else:
            lennard_jones_strength = 0
          
          # calculate total radial force (negative is towards, positive is away)
          radial_force = -gravity_strength + lennard_jones_strength
        else:
          radial_force = 0
        
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
  if simulation_params_obj.linear_damping_multiplier != 1:
    for i in range(len(new_particles)):
      particle_obj = new_particles[i]
      
      new_particles[i] = particle(
        particle_obj.x,
        particle_obj.y,
        particle_obj.z,
        particle_obj.dx * simulation_params_obj.linear_damping_multiplier ** (simulation_params_obj.time_step * 1e9),
        particle_obj.dy * simulation_params_obj.linear_damping_multiplier ** (simulation_params_obj.time_step * 1e9),
        particle_obj.dz * simulation_params_obj.linear_damping_multiplier ** (simulation_params_obj.time_step * 1e9),
      )
  
  # convert back to tuple
  return tuple(new_particles)
