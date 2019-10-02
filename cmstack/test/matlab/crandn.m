function randout=crandn(n,m)
% returns an (n by m) matrix of Gaussian random complex numbers, each with
% mean zero and variance 1
%
% INPUT 
%	n,m		integers
%
% OUTPUT	
% 	randout	(n by m) matrix of Gaussian random complex numbers, each with
% mean zero and variance 1
%
% USAGE
%  randout=crandn(n,m);

randout = 1/sqrt(2)*(randn(n,m) + i*randn(n,m));
return
