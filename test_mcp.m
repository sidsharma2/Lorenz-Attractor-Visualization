% Test MATLAB MCP Integration
disp('Hello from Antigravity!');
disp(['Current Directory: ', pwd]);
disp('Running a simple matrix operation...');
A = magic(5);
disp('Magic Square of size 5:');
disp(A);
disp(['Sum of columns: ', num2str(sum(A))]);

% Check for toolboxes
disp('Checking for Signal Processing Toolbox...');
if license('test', 'signal_toolbox')
    disp('Signal Processing Toolbox is available.');
else
    disp('Signal Processing Toolbox is NOT available.');
end
