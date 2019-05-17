% Test code to illustrate simple radar processing
% Performs following:
% Creates data (signal + noise) for a 4 aperture antenna, with each aperture
% Multiplies signal for each aperture by appropriate phase due to angle of
% arrival
% Once data has been created, performs following processing:
% - pulse compression; keeps only valid data, i.e. data for which full pulse
%   code has multiplied the signal
% - corner turn (transpose)
% - multiplies by Doppler window
% - Fourier transform (via FFT)
% - FFT shift (brings 0 frequency to center of range/Doppler map)
% - Forms sum channel RDM by summing over apertures
% - finds peak of RDM
% - using voltages from each aperture at peak of RDM, forms monopulse angle estimate

%% Define basic parameters
pulseCode = [1,-1,1,-1,1,1,-1,-1,1,1,1,1,1];   % pulse compression code, must be nChips X 1 (not checked)
nPulses = 128;              % number of pulses transmitted
dutyFactor = 0.25;           % fraction of time transmitter is on
targetOffset = 30;          % offset of received pulse from beginning of
                            % transmit pulse (this many samples prior to pulse)
phaseShiftPerPulse = pi/63; % phase shift per pulse (radians)
noisePowerdB = 0;           % noise power (in dB) relative to unit amplitude, each sample
singleChannelSNR_dB = 20;   % signal power(in dB) relative to unit amplitude
                            % for 1 channel, prior to pulse compression and
                            % Doppler processing
winstring = 'hanning';      % Doppler window (for Doppler sidelobe suppression)
applyWindow = 'y';          % if 'y', apply window; otherwise, do not window
fc = 30e9;                  % frequency (Hz.)
diamAnt = 2*2.2492;         % antenna diameter (cm) (2 * radius to phase centers); 
                            % this value gives rho = 10 for fc = 30e9
thetaTargetDeg = 0;         % target pitch (degrees)
psiTargetDeg = 0;           % target yaw (degrees)
%% Miscellaneous parameters
J = 10;                 % state for random # generator 
c = 2.99792458e10;      % exact speed of light (cm/sec)
% "switch" parameters for debugging purposes. Usually set to 'y'
addSignal = 'y';            % if 'y', add signal; otherwise, do not add signal
addNoise = 'y';             % if 'y' add noise, otherwise do not add noise
excludeDopplerBins = 8;     % exclude this many bins on either side of peak for noise estimation
%% Display Parameters
diagnosticPlot = 'n';       % 'y' for diagnostic plots, 'n' for no diagnostic plots
nPulsesToPlot = 5;          % number of pulses to plot for diagnostic purposes
%% initialize
nChips = length(pulseCode);   % number of pulse code samples per
                              % transmitted pulse
nSamplesPerPulse = ceil(nChips/dutyFactor); % calculate samples per PRI
nSamplesTotal = nPulses*nSamplesPerPulse;
thetaTarget = thetaTargetDeg * pi/180;       % target pitch in radians
psiTarget = psiTargetDeg * pi/180;           % target yaw in radians
phaseShiftPerSample = phaseShiftPerPulse/nSamplesPerPulse;
wl = c/fc;                                   % wavelength (cm)
rho = diamAnt*pi/(sqrt(2)*wl);               % 2*pi*d/wavelength
rAperture = wl*rho/(sqrt(2)*pi);             % radius of circle apertures lie on
rng(J,'twister')                             % set seed of random number generator
% create Doppler window
window = getWindow(nPulses, winstring);      % Calculate Doppler window
% replicate window so it can be applied to all samples and pulses at once
bigWindow = repmat(window, 1, nSamplesPerPulse-nChips+1);
 % transpose window to correct shape for window application
bigWindow = transpose(bigWindow);           
% calculate expected sum Channel SNR
singleChannelSNR = 10^(singleChannelSNR_dB/10);
FFTGain = nPulses;
sumChannelGain = 4;
windowingLoss = sum(window)^2/nPulses^2;
pulseCompressionGain = nChips;
processingGain = sumChannelGain*FFTGain*pulseCompressionGain*windowingLoss;
expectedSNR_dB = singleChannelSNR_dB + 10*log10(processingGain);
expectedNoise_dB = noisePowerdB + 10*log10(sumChannelGain*FFTGain*pulseCompressionGain);
%% Error checking
% end of transmitted signal must be before next pulse
if ~(nChips + targetOffset <= nSamplesPerPulse-1)
   error('end of transmitted pulse past beginning of next pulse')
end
%% Create phase for each of the 4 apertures 
% unit vector in target signal propagation direction
kHatTarget = [-sin(thetaTarget); -cos(thetaTarget)*sin(psiTarget)];

% aperture locations
% thetaAperture = (2*pi/nApertures*(0:nApertures-1))';
thetaAperture = pi/180*[45 135 225 315]' ;
apertureLoc = rAperture*[cos(thetaAperture) sin(thetaAperture)];

% compute phase at each aperture due to angle of arrival
 aperturePhasesTgt= exp(-2* pi * 1i * apertureLoc * kHatTarget /wl);

%% Create the signal for 1 aperture (without phase shift due to angle of arrival)
% create first pulse, then replicate nPulses times
firstPulse = zeros(1, nSamplesPerPulse);
firstPulse(1+targetOffset: targetOffset + nChips) = pulseCode;
% replicate first pulse nPulses times
signal = repmat(firstPulse, 1, nPulses);
if strcmp(diagnosticPlot,'y') % diagnostic plot of signal vs. index
   figure
   plot(signal(1:3*nSamplesPerPulse),'x')
   title(sprintf('First %d pulses, no phase shift, no noise', nPulsesToPlot))
end
% multiply signal by phase shift due to motion (Doppler shift)
idx = 0:nSamplesTotal-1;
signal = signal.*exp(idx*1i*phaseShiftPerSample);
if strcmp(diagnosticPlot,'y') % diagnostic plot of signal vs. index
   shortIndex = 1:nPulsesToPlot*nSamplesPerPulse;
   figure
   plot(shortIndex, real(signal(1, shortIndex)),'rx', ...
      shortIndex, imag(signal(1, shortIndex)),'bo')
   legend('Real Part','Imag Part')
   title(sprintf('First %d pulses, with phase shift due to motion, no noise', nPulsesToPlot))
end

% multiply signal by appropriate phase shift due to angle of arrival and by
% appropriate factor to give single
signal = sqrt(singleChannelSNR)*repmat(signal,4,1) .* repmat(aperturePhasesTgt,1, nSamplesTotal);

% create noise for each channel
if strcmp(addNoise,'y')
   noise = 10^(noisePowerdB/20)*crandn(4, nSamplesTotal);  % receiver noise (4 channels)
else
   noise = 0;
end
% add noise to signal
if strcmp(addSignal,'y')
   data = noise + signal;
else
   data = noise;
end

if strcmp(diagnosticPlot,'y') % diagnostic plot of signal vs. index
   figure
   plot(shortIndex, real(data(1, shortIndex)),'rx', ...
      shortIndex, imag(data(1, shortIndex)),'bo')
   legend('Real Part','Imag Part')
   title(sprintf('First %d pulses, with phase shift due to motion and noise',nPulsesToPlot))
end

% For each aperture, reshape data so that it is stored as nPulses X nSamplesPerPulse matrix,
% i.e. first pulse in first row, second pulse in second row, etc.
fullData = zeros(4, nPulses, nSamplesPerPulse);
for ap = 1:4
   fullData(ap,:,:) = transpose(reshape(data(ap,:), nSamplesPerPulse, nPulses));
end
if strcmp(diagnosticPlot,'y') % diagnostic plot of signal vs. index
   figure
   imagesc(squeeze(abs(fullData(1,:,:))))
   colorbar
   title('Aperture 1 data')
   xlabel('Sample')
   ylabel('Pulse')
end


%% Process the Data

% pulse compress the data, one aperture at a time
dataPC = zeros(4, nPulses, nSamplesPerPulse-nChips+1);
for ap = 1:4
   dataPC(ap,:,:) = conv2(squeeze(fullData(ap,:,:)), conj(fliplr(pulseCode)),'valid'); % need to 'flip'
% pulseCode left to right because we are doing correlation, not convoluion
end
if strcmp(diagnosticPlot,'y') % diagnostic plot of pulse-compressed data, channel 1
   figure
   imagesc(squeeze(abs(dataPC(1,:,:))))
   colorbar
   title('Pulse Compressed Data')
end

% corner turn, one aperture at a time
% first create dataCT with correct size
dataCT = zeros(4, nSamplesPerPulse-nChips+1, nPulses);
for ap = 1:4
   dataCT(ap,:,:) = transpose(squeeze(dataPC(ap,:,:)));  % .' performs transpose with complex conjugation
end

% Multiply by Dopper Window, one aperture at a time, if applyWindow = 'y'
if strcmp(applyWindow,'y')   % then apply window
   windowedData = zeros(4, nSamplesPerPulse-nChips+1, nPulses);
   for ap = 1:4
      windowedData(ap,:,:) = squeeze(dataCT(ap,:,:)).*bigWindow;
   end
else                           % do not apply window
   windowedData = dataCT;
end
% FFT in pulse direction
dataFFT = fft(windowedData, nPulses, 3);
% Use fftshift to put frequency = 0 in middle of Doppler
% axis. 
dataFFTShift = fftshift(dataFFT, 3);
% create sum channel range Doppler map RDM
RDM = squeeze(sum(dataFFTShift)); % sum over apertures

% find range/Doppler cell with maximum absolute value
maxRDM = max(abs(RDM(:)));
[r,d] = find(abs(RDM)==maxRDM);

% find voltages for each quadrant at [r,d]
maxVoltage = dataFFTShift(:, r, d);

% combine quadrant data into sum, delta el, delta az channels
channelCombiner = [1, 1, 1, 1; 1, 1, -1, -1; 1, -1, -1, 1];
sumDD = channelCombiner*maxVoltage;   % sumDD = [sum channel, delta elevation, delta azimuth]

% calculate monopulse angle estimates from sumDD
deltaAzOverSum = sumDD(3)/sumDD(1);
deltaElOverSum = sumDD(2)/sumDD(1);
thetaMono = asin(((1/rho)*atan(imag(deltaAzOverSum))));
psiMono = asin(1/(rho*cos(thetaMono))*atan(imag(deltaElOverSum)));
thetaMonoDeg = 180/pi*thetaMono;
psiMonoDeg = 180/pi*(psiMono);


%% Some diagnostics
% estimate mean noise power
RDML= RDM(:, 1:d-excludeDopplerBins);
RDMR = RDM(:, d+excludeDopplerBins:end);
noiseRDM = [RDML RDMR];
measuredNoisePower_dB = 10*log10(mean(abs(noiseRDM(:)).^2));

%% Display some results
fprintf('monopulse theta (degrees): %4.2f [%4.2f]\n', thetaMonoDeg, thetaTargetDeg)
fprintf('monopulse psi (degrees): %4.2f [%4.2f]\n', psiMonoDeg, psiTargetDeg)
fprintf('SNR (analytic noise): %4.2f dB \n', 20*(log10(maxRDM))- expectedNoise_dB);
fprintf('SNR (measured noise):  %4.2f dB \n', 20*(log10(maxRDM))- measuredNoisePower_dB);
fprintf('Measured Noise: %4.2f dB [%4.2f]\n', measuredNoisePower_dB, expectedNoise_dB);
if strcmp(applyWindow,'y')
   titleStr = sprintf('Sum Channel Range-Doppler Map [dB], %s window', winstring);
else
   titleStr = 'Sum Channel Range-Doppler Map [dB]';
end

% Display image of range-Doppler Map

figure
imagesc(10*log10(abs(RDM).^2))

xlabel('Doppler Frequency')
ylabel('Range')
title(titleStr)
colorbar

% Display surface plot  of range-Doppler Map

figure
surf(10*log10(abs(RDM).^2))
rotate3d on
ylabel('Range')
title(titleStr)
colorbar





