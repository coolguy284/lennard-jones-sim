% Clear vars
clear
clc
close all

% Constants
initial_cols = 1;
particle_state = 6;
time_delay = 0.01;
bound_limits = [-3, 3];

% Load in table
recorded_states = readtable('data/calculations_05_lennard_jones_7x7x7_coarse.csv');

% Get rows and cols of table for later
[rows, cols] = size(recorded_states);

% Rescale values in table to sane scale
recorded_states{:,1} = recorded_states{:,1} .* 1e8;
recorded_states{:,initial_cols + 1:cols} = ...
    recorded_states{:,initial_cols + 1:cols} .* 1e10;

% mode options
% 'print'
% 'plot'
mode = 'plot';

for row = 1:10:rows
    for col = initial_cols + 1:particle_state:cols
        switch mode
            case 'print'
                fprintf('%f %f %f\n', ...
                    recorded_states{row,col}, ...
                    recorded_states{row,col+1}, ...
                    recorded_states{row,col+2});
            case 'plot'
                x_positions = recorded_states{row,initial_cols + 1:particle_state:cols};
                y_positions = recorded_states{row,initial_cols + 2:particle_state:cols};
                z_positions = recorded_states{row,initial_cols + 3:particle_state:cols};
                plot3(x_positions, y_positions, z_positions, 'o');
                title(sprintf('Time: %f', recorded_states{row,1}));
                xlim(bound_limits);
                ylim(bound_limits);
                zlim(bound_limits);
        end
    end

    pause(time_delay);
end
