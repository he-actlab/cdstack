% Test code to illustrate simple radar processing
%% Define basic parameters
pulseCode = [1,-1,1,-1,1,1,-1,-1,1,1,1,1,1];   % pulse compression code, must be nChips X 1 (not checked)
nPulses = 128;              % number of pulses transmitted
dutyFactor = .25;           % fraction of time transmitter is on
targetOffset = 30;          % offset of received pulse from beginning of
                            % transmit pulse (this many samples prior to pulse)
phaseShiftPerPulse = pi/20; % phase shift per pulse (radians)
noisePowerdB = 0;           % noise power (in dB) relative to unit amplitude
signalPowerdB = 20;         % signal power(in dB) relative to unit amplitude
%% Display Parameters
diagnosticPlot = 'n';       % 'y' for diagnostic plots, 'n' for no do diagnostic plots
nPulsesToPlot = 5;          % number of pulses to plot for diagnostic purposes
%% initialize
nChips = length(pulseCode);   % number of pulse code samples per
                              % transmitted pulse
nSamplesPerPulse = ceil(nChips/dutyFactor); % calculate samples per PRI
nSamplesTotal = nPulses*nSamplesPerPulse;
phaseShiftPerSample = phaseShiftPerPulse/nSamplesPerPulse;
%% Error checking
% end of transmitted signal must be before next pulse
if ~(nChips + targetOffset <= nSamplesPerPulse-1)
    error('end of transmitted pulse past beginning of next pulse')
end
%% Create the Data
noise = 10^(noisePowerdB/20)*crandn(1, nSamplesTotal);  % receiver noise
% create first pulse, then replicate nPulses times
firstPulse = zeros(1, nSamplesPerPulse);
firstPulse(1+targetOffset: targetOffset + nChips) = ...
    10^(signalPowerdB/10)*pulseCode;
% replicate first pulse nPulses time
signal = repmat(firstPulse, 1, nPulses);
if strcmp(diagnosticPlot,'y') % diagnostic plot of signal vs. index
      figure
      plot(signal(1:3*nSamplesPerPulse),'x')
      title(sprintf('First %d pulses, no phase shift, no noise', nPulsesToPlot))
end      
% multiply signal by phase shift
idx = 0:nSamplesTotal-1; 
signal = signal.*exp(idx*1i*phaseShiftPerSample);
if strcmp(diagnosticPlot,'y') % diagnostic plot of signal vs. index
   shortIndex = 1:nPulsesToPlot*nSamplesPerPulse;
   figure
   plot(shortIndex, real(signal(shortIndex)),'rx', ...
      shortIndex, imag(signal(shortIndex)),'bo')
   legend('Real Part','Imag Part')
   title(sprintf('First %d pulses, with phase shift, no noise', nPulsesToPlot))
end
% add noise to signal
data = noise + signal;
if strcmp(diagnosticPlot,'y') % diagnostic plot of signal vs. index
   figure
   plot(shortIndex, real(data(shortIndex)),'rx', ...
      shortIndex, imag(data(shortIndex)),'bo')
   legend('Real Part','Imag Part')
   title(sprintf('First %d pulses, with phase shift and noise',nPulsesToPlot))
end

% reshape data so that it is stored as a nPulses X nSamplesPerPulse  matrix,
% i.e. first pulse in first row, second pulse in second row, 

data = transpose(reshape(data, nSamplesPerPulse, nPulses));


%% Complex numbers representation?
%% Extend iterator support
%% control flows/predication


%% Process the Data

% pulse compress the data
dataPC = conv2(data, conj(fliplr(pulseCode)),'same'); % need to 'flip' 
% pulseCode left to right because we are doing correlation, not convoluion

if strcmp(diagnosticPlot,'y') % diagnostic plot of signal vs. index
   figure
   imagesc(abs(dataPC))
   colorbar
   title('Pulse Compressed Data')
end

% corner turn
dataCT = transpose(dataPC);  % .' performs transpose with complex conjugation

% FFT in pulse direction
dataFFT = fft(dataCT, nPulses, 2); 

% form range-Doppler map. Use fftshift to put frequency = 0 in middle of Doppler
% axis. Calculate RDM in dB
RDM = fftshift(dataFFT,2);

%% Display some results

% Display image of range-Doppler Map

figure
imagesc(10*log10(abs(RDM).^2))
xlabel('Doppler Frequency')
ylabel('Range')
title('Range-Doppler Map')
colorbar

% Display surface plot  of range-Doppler Map

figure
surf(10*log10(abs(RDM).^2))
xlabel('Doppler Frequency')
ylabel('Range')
title('Range-Doppler Map')
colorbar






