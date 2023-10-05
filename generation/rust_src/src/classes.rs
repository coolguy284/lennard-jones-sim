#[derive(Clone)]
pub struct Particle {
  pub x: f64,
  pub y: f64,
  pub z: f64,
  pub dx: f64,
  pub dy: f64,
  pub dz: f64,
}

impl Particle {
  pub fn from_coords(
    x: f64, y: f64, z: f64,
    dx: f64, dy: f64, dz: f64
  ) -> Particle {
    Particle {
      x,
      y,
      z,
      dx,
      dy,
      dz,
    }
  }
  
  pub fn from_particle(particle_obj: &Particle) -> Particle {
    Particle {
      x: particle_obj.x,
      y: particle_obj.y,
      z: particle_obj.z,
      dx: particle_obj.dx,
      dy: particle_obj.dy,
      dz: particle_obj.dz,
    }
  }
  
  pub fn distance_to_squared(&self, other: &Particle) -> f64 {
    let delta_x = other.x - self.x;
    let delta_y = other.y - self.y;
    let delta_z = other.z - self.z;
    
    delta_x * delta_x + delta_y * delta_y + delta_z * delta_z
  }
  
  pub fn distance_to(&self, other: &Particle) -> f64 {
    f64::sqrt(self.distance_to_squared(other))
  }
  
  pub fn vector_away_from_other(&self, other: &Particle, length: f64) -> (f64, f64, f64) {
    // multiply difference between the 2 particles' positions, by 1 / distance, then by length
    
    // calculate this multiplication constant
    let distance = self.distance_to(other);
    let multiplication_const = if distance != 0.0 {
      1.0 / distance * length
    } else {
      0.0
    };
    
    (
      (self.x - other.x) * multiplication_const,
      (self.y - other.y) * multiplication_const,
      (self.z - other.z) * multiplication_const
    )
  }
  
  pub fn apply_velocity(
    &self,
    dx: f64, dy: f64, dz: f64,
    time_step: f64,
  ) -> Particle {
    Particle {
      x: self.x + dx * time_step,
      y: self.y + dy * time_step,
      z: self.z + dz * time_step,
      dx: self.dx,
      dy: self.dy,
      dz: self.dz,
    }
  }
  
  pub fn apply_own_velocity(&self, time_step: f64) -> Particle {
    self.apply_velocity(self.dx, self.dy, self.dz, time_step)
  }
  
  pub fn apply_acceleration(&self, ddx: f64, ddy: f64, ddz: f64, time_step: f64) -> Particle {
    Particle {
      x: self.x,
      y: self.y,
      z: self.z,
      dx: self.dx + ddx * time_step,
      dy: self.dy + ddy * time_step,
      dz: self.dz + ddz * time_step,
    }
  }
}

pub struct SystemState {
  pub time: f64,
  pub particles: Vec<Particle>,
}

pub struct SimulationParams {
  pub particle_radius: f64,
  pub particle_mass: f64,
  pub grav_constant: f64,
  pub lennard_jones_well_depth: f64,
  pub linear_damping_multiplier: f64,
  pub time_step: f64,
  pub num_steps: u64,
  pub particle_configuration: u8,
  pub csv_file_skip_steps: u64,
  pub status_update_skip_steps: u64,
}
