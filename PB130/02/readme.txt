%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%       PB130 - Introduction to Digital Image Processing, Autumn 2022
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Exercise 2 - Intensity histograms
% 
% prepared by:
% 
% Martin Maska <xmaska@fi.muni.cz>
% David Svoboda <svoboda@fi.muni.cz>
% Petr Matula <pem@fi.muni.cz>
%
% Aim: - To get familiar with intensity histograms
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Built-in intensity histograms in ImageJ
=======================================

- Open an 8-bit grayscale image (e.g., "photo.tif" or "photo2.tif" from the "images" folder)
- Display its intensity histogram (Ctrl+H) in different modes
- Is the intensity histogram unique representation of an image? Analyze the intensity histograms of "chessboard.tif" and "ramp.tif" from the "images" folder
- What operation over two general images of the same size and bit depth corresponds to the summation of their intensity histograms? 
- Open "chessboard.tif" and its three variants (i.e., "noisy_chessboard1.tif", "noisy_chessboard2.tif", and "noisy_chessboard3.tif") corrupted by a different type of noise. Decide which of these variants correspond to the original image corrupted by:
	- impulse noise
	- additive Gaussian noise
	- photon noise


Implementation of ImageJ plugins
================================

- Back up and delete all files under "plugins/PB130"
- Copy the content of the "02.zip" archive to the "plugins/PB130" folder
- Open the java files in your favorite text editor and complete the "run()" methods in the following order: 
	- My_Histogram (compute the intensity histogram of a given 8-bit grayscale image and check whether the image is underexposed/overexposed)
	- My_CumulativeHistogram (compute the cumulative histogram of a given 8-bit grayscale image)
	- My_BinnedHistogram (compute the intensity histogram of a given 16-bit grayscale image (e.g., "lena16b.tif" from the "images" folder), 
	  which consists of 512 bins)
	- My_GaussianNoise (add additive Gaussian noise to a given 8-bit grayscale image; Warning: beware of image data type overflows)


Validation and submission of completed ImageJ plugins
=====================================================

- Validate all the four plugins by compiling and running the "UnitTests_02" plugin located under "PB130"


Submission of completed ImageJ plugins
======================================

- The list of files to be submitted and the homework vault link are given in the interactive syllabus
- Before submission, carefully check that your code neither contains clumsy constructions nor typical errors as listed in the interactive syllabus