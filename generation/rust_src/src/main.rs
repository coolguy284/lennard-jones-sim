pub mod classes;
pub mod simulation;

use crate::classes::SystemState;

// simulation modeled after helium atom
// radius = 140 pm (van der walls), 28 pm (covalent); 40 pm is the value we're going with, so 40e-12 m
// mass = 4.002 602 mass units; one dalton (atomic mass unit) is 1.660 539 066 60e-27; so mass is 6.646476989051294e-27 kg
// constants defined in perform_simulation_run

fn get_particle_string(recorded_states: Vec<SystemState>) -> String {
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
    
    for particle_obj in state.particles {
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
  let full_file_path = format!("../../../../data/calculations_{}.csv", file_name_extended);
  
  println!("Simulating run {}...", file_name_extended);
}

fn main() {
  println!("Hello, world!");
}
