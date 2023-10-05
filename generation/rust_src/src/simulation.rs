use crate::classes::Particle;
use crate::classes::SimulationParams;

pub fn populate_particles_list(simulation_params_obj: &SimulationParams) -> Vec<Particle> {
  let mut particles = Vec::<Particle>::new();
  
  let particle_spacing = simulation_params_obj.particle_radius * 2.0;
  
  match simulation_params_obj.particle_configuration {
    1 => {
      let x_span = 2;
      let y_span = 2;
      let z_span = 2;
      
      for i in -x_span / 2..=x_span / 2 {
        for j in -y_span / 2..=y_span / 2 {
          for k in -z_span / 2..=z_span / 2 {
            let x = i as f64 * particle_spacing;
            let y = j as f64 * particle_spacing;
            let z = k as f64 * particle_spacing;
            
            particles.push(
              Particle {
                x, y, z,
                dx: 0.0, dy: 0.0, dz: 0.0,
              }
            );
          }
        }
      }
    }
    2 => {
      let x_span = 2;
      let y_span = 2;
      let z_span = 2;
      
      for i in -x_span / 2..=x_span / 2 {
        for j in -y_span / 2..=y_span / 2 {
          for k in -z_span / 2..=z_span / 2 {
            let x = i as f64 * particle_spacing;
            let y = j as f64 * particle_spacing;
            let z = k as f64 * particle_spacing;
            
            particles.push(
              Particle {
                x, y, z,
                dx: particle_spacing / simulation_params_obj.time_step * 0.05,
                dy: 0.0,
                dz: 0.0,
              }
            );
          }
        }
      }
    }
    3 => {
      let x_span = 6;
      let y_span = 6;
      let z_span = 6;
      
      for i in -x_span / 2..=x_span / 2 {
        for j in -y_span / 2..=y_span / 2 {
          for k in -z_span / 2..=z_span / 2 {
            let x = i as f64 * particle_spacing;
            let y = j as f64 * particle_spacing;
            let z = k as f64 * particle_spacing;
            
            particles.push(
              Particle {
                x, y, z,
                dx: 0.0, dy: 0.0, dz: 0.0,
              }
            );
          }
        }
      }
    }
    _ => {
      panic!("Invalid simulation type {}", simulation_params_obj.particle_configuration);
    }
  }
  
  particles
}

pub fn simulate_tick(particles: &Vec<Particle>, simulation_params_obj: &SimulationParams) -> Vec<Particle> {
  // make array for simulation output
  let mut new_particles = particles.to_vec();
  
  // calculate forces
  for i in 0..particles.len() {
    let particle_obj = &particles[i];
    
    // for every particle in front of this particle
    for j in i + 1..particles.len() {
      let particle_two_obj = &particles[j];
      
      // calculate distance to particle
      let distance_squared = particle_obj.distance_to_squared(&particle_two_obj);
      let distance = f64::sqrt(distance_squared);
      
      // calculate strength of gravitational force
      let gravity_strength = if distance_squared != 0.0 {
        simulation_params_obj.grav_constant * simulation_params_obj.particle_mass * simulation_params_obj.particle_mass / distance_squared
      } else {
        0.0
      };
      
      // calculate strength of lennard jones force
      // potential energy is 4 * lennard_jones_well_depth * ((particle_radius / distance) ^ 12 - (particle_radius / distance) ^ 6)
      // force is -1 * 4 * lennard_jones_well_depth * (12 * (particle_radius / distance) ^ 11 * (-particle_radius / distance^2) - 6 * (particle_radius / distance) ^ 5 * (-particle_radius / distance^2))
      let rescaled_distance = simulation_params_obj.particle_radius / distance;
      let rescaled_distance_d_dx = -simulation_params_obj.particle_radius / distance * distance;
      
      let lennard_jones_strength = -1.0 * 4.0 * simulation_params_obj.lennard_jones_well_depth * (12.0 * f64::powf(rescaled_distance, 11.0) * rescaled_distance_d_dx - 6.0 * f64::powf(rescaled_distance, 5.0) * rescaled_distance_d_dx);
      
      // calculate total radial force (negative is towards, positive is away)
      let radial_force = -gravity_strength + lennard_jones_strength;
      
      // calculate radial force
      let particle_one_accel = radial_force / simulation_params_obj.particle_mass;
      let particle_two_accel = radial_force / simulation_params_obj.particle_mass;
      
      let particle_one_accel_vector = particle_obj.vector_away_from_other(&particle_two_obj, particle_one_accel);
      let particle_two_accel_vector = particle_two_obj.vector_away_from_other(&particle_obj, particle_two_accel);
      
      // apply radial force
      new_particles[i] = new_particles[i].apply_acceleration(particle_one_accel_vector.0, particle_one_accel_vector.1, particle_one_accel_vector.2, simulation_params_obj.time_step);
      new_particles[j] = new_particles[j].apply_acceleration(particle_two_accel_vector.0, particle_two_accel_vector.1, particle_two_accel_vector.2, simulation_params_obj.time_step);
    }
  }
  
  // apply velocity
  for i in 0..new_particles.len() {
    let particle_obj = &new_particles[i];
    
    new_particles[i] = particle_obj.apply_own_velocity(simulation_params_obj.time_step);
  }
  
  // apply linear damping
  if simulation_params_obj.linear_damping_strength != 1.0 {
    for i in 0..new_particles.len() {
      let particle_obj = &new_particles[i];
      
      new_particles[i] = Particle {
        x: particle_obj.x,
        y: particle_obj.y,
        z: particle_obj.z,
        dx: particle_obj.dx * f64::powf(simulation_params_obj.linear_damping_strength, simulation_params_obj.time_step * 1e9),
        dy: particle_obj.dy * f64::powf(simulation_params_obj.linear_damping_strength, simulation_params_obj.time_step * 1e9),
        dz: particle_obj.dz * f64::powf(simulation_params_obj.linear_damping_strength, simulation_params_obj.time_step * 1e9),
      };
    }
  }
  
  new_particles
}
