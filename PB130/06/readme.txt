%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%       PB130 - Introduction to Digital Image Processing, Autumn 2022
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Exercise 06 - Nonlinear filters
% 
% prepared by:
% 
% Martin Maska <xmaska@fi.muni.cz>
% David Svoboda <svoboda@fi.muni.cz>
% Petr Matula <pem@fi.muni.cz>
%
% Aim: - To get familiar with basic nonlinear filters
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Built-in nonlinear filters in ImageJ
====================================

- Open "nuts_bolts.tif" from the "images" folder
- Via "Process -> Filters -> Minimum/Maximum", apply minimum or/and maximum filters to fill the holes inside nuts
- Open an 8-bit grayscale image (e.g., "chessboard.tif" from the "images" folder) and degrade it with a salt and pepper noise
- Via "Process -> Filters -> Median", apply a median filter and compare the result with that of a Gaussian filter
- Open "space.tif" from the "images" folder and correct it for uneven illumination using a median filter
- You may find useful the following menu commands:
	- "Image -> Duplicate" - duplicate a given image
	- "Process -> Image Calculator"	- basic arithmetical operations over images
- Does a change in the order of applied nonlinear filters influence the result? 
- Does a change in the order of applied linear and nonlinear filters influence the result?


Implementation of ImageJ plugins
================================

- Back up and delete all files under "plugins/PB130"
- Copy the content of the "06.zip" archive to the "plugins/PB130" folder
- Open the java files in your favourite text editor and complete the "run()" methods in the following order: 
	- My_MedianFilter (apply median filtering with a square neighborhood on a given 8-bit grayscale image; assure that only the pixels within the original image domain are used)
	- My_AdvancedMedianFilter (apply advanced median filtering with a square neighborhood on a given 8-bit grayscale image corrupted with salt-and-pepper noise; assure that the filter is applied to the noise-corrupted pixels only, working only with the noise-uncorrupted pixels in the neighborhood)


Validation of completed ImageJ plugins
======================================

- Validate both plugins by compiling and running the "UnitTests_06" plugin located under "PB130"


Submission of completed ImageJ plugins
======================================

- The list of files to be submitted and the homework vault link are given in the interactive syllabus
- Before submission, carefully check that your code neither contains clumsy constructions nor typical errors as listed in the interactive syllabus
