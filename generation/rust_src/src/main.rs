pub mod classes;
pub mod simulation;

use std::env;
use std::fs;
use std::path::Path;
use crate::classes::SimulationParams;
use crate::classes::SystemState;
use crate::simulation::populate_particles_list;
use crate::simulation::simulate_tick;

// simulation modeled after helium atom
// radius = 140 pm (van der walls), 28 pm (covalent); 40 pm is the value we're going with, so 40e-12 m
// mass = 4.002 602 mass units; one dalton (atomic mass unit) is 1.660 539 066 60e-27; so mass is 6.646476989051294e-27 kg
// constants defined in perform_simulation_run

fn get_particle_string(recorded_states: &Vec<SystemState>) -> String {
  // figure out column headers
  
  let num_particles = recorded_states[0].particles.len();
  
  let mut headers = vec!["time".to_string()];
  
  for i in 1..num_particles + 1 {
    headers.push(format!("p{}_x", i));
    headers.push(format!("p{}_y", i));
    headers.push(format!("p{}_z", i));
    headers.push(format!("p{}_dx", i));
    headers.push(format!("p{}_dy", i));
    headers.push(format!("p{}_dz", i));
  }
  
  // create var for each line of file
  
  let mut file_lines = Vec::<String>::new();
  
  file_lines.push(headers.join(","));
  
  // add each state to file lines
  
  for state in recorded_states {
    let mut file_line = Vec::<String>::new();
    
    file_line.push(format!("{}", state.time));
    
    for particle_obj in &state.particles {
      file_line.push(format!("{}", particle_obj.x));
      file_line.push(format!("{}", particle_obj.y));
      file_line.push(format!("{}", particle_obj.z));
      file_line.push(format!("{}", particle_obj.dx));
      file_line.push(format!("{}", particle_obj.dy));
      file_line.push(format!("{}", particle_obj.dz));
    }
    
    file_lines.push(file_line.join(","));
  }
  
  file_lines.join("\n")
}

fn perform_simulation_run(run_number: u64, file_name: String, force_rerun: Option<bool>) {
  let file_name_extended = format!("{:0>2}_{}", run_number, file_name);
  let full_file_path_string = format!("../../../../data/calculations_{}.csv", file_name_extended);
  let full_file_path = Path::new(full_file_path_string.as_str());
  
  println!("Simulating run {}...", file_name_extended);
  
  // assume already calculated if file already exists
  if !force_rerun.unwrap_or(false) && full_file_path.exists() {
    println!("Path already exists, not calculating.");
    println!();
    return
  }
  
  // constants defined here
  let particle_radius = 40e-12;
  let particle_mass = 6.646476989051294e-27; // 1.66053906660e-27 * 4.002602
  let grav_constant = 1e8; // normally 6.67408e-11
  let lennard_jones_well_depth = 1e-32;
  //let linear_damping_strength = 0.95; // this is basically multiplied by the velocity every nanosecond
  let time_step = 1e-9;
  let num_steps = 1000u64;
  
  let simulation_params_obj = match run_number {
    1 => {
      SimulationParams {
        particle_radius,
        particle_mass,
        grav_constant: 0.0,
        lennard_jones_well_depth: 0.0,
        linear_damping_strength: 0.0,
        time_step,
        num_steps,
        particle_configuration: 2,
        csv_file_skip_steps: 10,
        status_update_skip_steps: 100,
      }
    }
    2 => {
      SimulationParams {
        particle_radius,
        particle_mass,
        grav_constant,
        lennard_jones_well_depth,
        linear_damping_strength: 0.95,
        time_step,
        num_steps,
        particle_configuration: 1,
        csv_file_skip_steps: 10,
        status_update_skip_steps: 100,
      }
    }
    3 => {
      SimulationParams {
        particle_radius,
        particle_mass,
        grav_constant,
        lennard_jones_well_depth,
        linear_damping_strength: 0.95,
        time_step,
        num_steps,
        particle_configuration: 1,
        csv_file_skip_steps: 10,
        status_update_skip_steps: 100,
      }
    }
    4 => {
      SimulationParams {
        particle_radius,
        particle_mass,
        grav_constant,
        lennard_jones_well_depth,
        linear_damping_strength: 0.95,
        time_step,
        num_steps,
        particle_configuration: 3,
        csv_file_skip_steps: 10,
        status_update_skip_steps: 10,
      }
    }
    5 => {
      SimulationParams {
        particle_radius,
        particle_mass,
        grav_constant,
        lennard_jones_well_depth,
        linear_damping_strength: 0.95,
        time_step: time_step * 3.0,
        num_steps,
        particle_configuration: 3,
        csv_file_skip_steps: 10,
        status_update_skip_steps: 10,
      }
    }
    6 => {
      SimulationParams {
        particle_radius,
        particle_mass,
        grav_constant,
        lennard_jones_well_depth,
        linear_damping_strength: 0.95,
        time_step,
        num_steps: num_steps * 60,
        particle_configuration: 3,
        csv_file_skip_steps: 10,
        status_update_skip_steps: 10,
      }
    }
    7 => {
      SimulationParams {
        particle_radius,
        particle_mass,
        grav_constant,
        lennard_jones_well_depth,
        linear_damping_strength: 0.997,
        time_step,
        num_steps: num_steps * 60,
        particle_configuration: 3,
        csv_file_skip_steps: 10,
        status_update_skip_steps: 10,
      }
    }
    8 => {
      SimulationParams {
        particle_radius,
        particle_mass,
        grav_constant,
        lennard_jones_well_depth,
        linear_damping_strength: 1.0,
        time_step,
        num_steps: num_steps * 60,
        particle_configuration: 3,
        csv_file_skip_steps: 10,
        status_update_skip_steps: 10,
      }
    }
    _ => {
      panic!("Run number {} invalid", run_number);
    }
  };
  
  println!("Creating particles...");
  
  let mut particles = populate_particles_list(&simulation_params_obj);
  
  let mut recorded_states = Vec::<SystemState>::new();
  
  println!("Recording initial state...");
  
  recorded_states.push(
    SystemState {
      time: 0.0,
      particles: particles.clone(),
    }
  );
  
  println!("Calculating...");
  
  for i in 1..=simulation_params_obj.num_steps / simulation_params_obj.csv_file_skip_steps {
    let current_time = simulation_params_obj.time_step * i as f64;
    for _ in 0..simulation_params_obj.csv_file_skip_steps {
      particles = simulate_tick(&particles, &simulation_params_obj);
    }
    recorded_states.push(
      SystemState {
        time: current_time,
        particles: particles.clone(),
      }
    );
    if i % (simulation_params_obj.status_update_skip_steps / simulation_params_obj.csv_file_skip_steps) == 0 {
      println!("Calculated state {}/{}", i * simulation_params_obj.csv_file_skip_steps, simulation_params_obj.num_steps);
    }
  }
  
  println!("Saving to csv file...");
  
  let particle_string = get_particle_string(&recorded_states);
  
  fs::write(full_file_path, particle_string).unwrap();
  
  println!();
}

fn main() {
  let testing = false;
  
  if testing {
    use crate::classes::Particle;
    let particle_one = Particle::from_coords(0.0, 0.0, 0.0, 0.0, 0.0, 0.0);
    let particle_two = Particle::from_coords(0.1, 0.1, 0.1, 0.0, 0.0, 0.0);
    println!("{}", particle_one.distance_to(&particle_two));
    println!("{:?}", particle_one.vector_away_from_other(&particle_two, 2.0));
    panic!();
  }
  
  // change directory to program's path
  
  let mut program_dir_buf = env::current_exe().unwrap();
  program_dir_buf.pop(); // get parent dir of program path
  let program_dir_os_string = program_dir_buf.into_os_string();
  env::set_current_dir(Path::new(&program_dir_os_string)).unwrap();
  
  println!("Lennard Jones Simulator -- Rust Version");
  println!();
  
  perform_simulation_run(1, "moving_right".to_string(), None);
  perform_simulation_run(2, "gravity".to_string(), None);
  perform_simulation_run(3, "lennard_jones_3x3x3".to_string(), None);
  perform_simulation_run(4, "lennard_jones_7x7x7".to_string(), None);
  perform_simulation_run(5, "lennard_jones_7x7x7_coarse".to_string(), None);
  perform_simulation_run(6, "lennard_jones_7x7x7_long".to_string(), None);
  perform_simulation_run(7, "lennard_jones_7x7x7_long_lightdamped".to_string(), None);
  perform_simulation_run(8, "lennard_jones_7x7x7_long_undamped".to_string(), None);
}
