% Clear vars
%clear
clc
close all

% Constants
initial_cols = 1;
particle_state_length = 6;
time_delay = 0.01;
bound_limits = [-3, 3];

% Load in table
if ~exist('recorded_states', 'var')
    recorded_states = readtable('data/calculations_06_lennard_jones_7x7x7_long.csv');
    
    % Get rows and cols of table for later
    [rows, cols] = size(recorded_states);
    
    % Rescale values in table to sane scale
    recorded_states{:,1} = recorded_states{:,1} .* 1e8;
    recorded_states{:,initial_cols + 1:cols} = ...
        recorded_states{:,initial_cols + 1:cols} .* 1e10;
end

% mode options
% 'print'
% 'plot'
mode = 'plot';

for row = 1:1:rows
    switch mode
        case 'print'
            for col = initial_cols + 1:particle_state_length:cols
                fprintf('%f %f %f\n', ...
                    recorded_states{row,col}, ...
                    recorded_states{row,col+1}, ...
                    recorded_states{row,col+2});
            end
        case 'plot'
            x_positions = recorded_states{row,initial_cols + 1:particle_state_length:cols};
            y_positions = recorded_states{row,initial_cols + 2:particle_state_length:cols};
            z_positions = recorded_states{row,initial_cols + 3:particle_state_length:cols};
            plot3(x_positions, y_positions, z_positions, 'o');
            title('Movement of Lennard-Jones Particles in 7x7x7 "crystal"');
            xlim(bound_limits);
            ylim(bound_limits);
            zlim(bound_limits);
            xlabel('x-coord (m * 10^{-10})');
            ylabel('y-coord (m * 10^{-10})');
            zlabel('z-coord (m * 10^{-10})');
            delete(findall(gcf, 'type', 'annotation'));
            annotation('textbox', ...
                [0, 0, .4, .1], ...
                'String', ...
                sprintf('Time: %f (s * 10^{-8})', recorded_states{row,1}), ...
                'EdgeColor', ...
                'none');
    end
    pause(time_delay);
end
