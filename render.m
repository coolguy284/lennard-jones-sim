% Clear vars
clear
clc
close all

% Constants
initial_cols = 1;

% Load in table
recorded_states = readtable('calculations_1.csv');

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

for row = 1:1:1
    for col = initial_cols + 1:3:cols
        switch mode
            case 'print'
                fprintf('%f %f %f\n', ...
                    recorded_states{row,col}, ...
                    recorded_states{row,col+1}, ...
                    recorded_states{row,col+2});
            case 'plot'
                x_positions = recorded_states{row,initial_cols + 1:3:cols};
                y_positions = recorded_states{row,initial_cols + 2:3:cols};
                z_positions = recorded_states{row,initial_cols + 3:3:cols};
                plot3(x_positions, y_positions, z_positions, 'o');
        end
    end
end
