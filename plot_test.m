% Initial Plot Verification Script
% This script generates a simple 3D plot to verify graphical output.

disp('Generating test plot...');

% Create data for plotting
[X, Y] = meshgrid(-2:0.1:2);
Z = X .* exp(-X.^2 - Y.^2);

% Create figure
figure('Name', 'Antigravity Plot Test', 'NumberTitle', 'off');
surf(X, Y, Z);

% Add labels and title
title('3D Surface Plot Test: Gaussian Form');
xlabel('X-axis');
ylabel('Y-axis');
zlabel('Z-axis');
colorbar;

% Improve view
view(45, 30);
grid on;

disp('Plot generated successfully! Check for a new figure window.');
