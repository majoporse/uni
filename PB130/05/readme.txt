%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%       PB130 - Introduction to Digital Image Processing, August 2022
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Exercise 5 - Image gradient and difference operators
% 
% prepared by:
% 
% Martin Maska <xmaska@fi.muni.cz>
% David Svoboda <svoboda@fi.muni.cz>
% Petr Matula <pem@fi.muni.cz>
%
% Aim: - To get familiar with image gradient and basic difference operators
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Built-in difference operators in ImageJ
=======================================

- Open an 8-bit grayscale image from the "images" folder (e.g., "ramp.tif" or "chessboard.tif") 
- Via "Process -> Filters -> Convolve", try to apply different difference operators on the opened image and its flipped version
- Why are the edges detected in one direction only?


Implementation of ImageJ plugins
============================================

- Back up and delete all files under "plugins/PB130"
- Copy the content of the "05.zip" archive to the "plugins/PB130" folder
- Open the java files in your favourite text editor and complete the "run()" methods in the following order: 
	- My_GradientX (approximate the gradient in the x direction using central differences)
	- My_GradientY (approximate the gradient in the y direction using central differences)
	- My_GradientMagnitude (approximate the gradient magnitude using central differences)
	- My_GradientOrientation (approximate the gradient orientation using central differences)
	- My_LaplacianZeroCrossing (find the Laplacian zero-crossing of a given 8-bit grayscale image)
- Study how the implemented routines behave on images in the "images" folder


Validation of completed ImageJ plugins
======================================

- Validate all the five plugins by compiling and running the "UnitTests_05" plugin located under "PB130"


Submission of completed ImageJ plugins
======================================

- The list of files to be submitted and the homework vault link are given in the interactive syllabus
- Before submission, carefully check that your code neither contains clumsy constructions nor typical errors as listed in the interactive syllabus
