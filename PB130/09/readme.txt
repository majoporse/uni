%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%       PB130 - Introduction to Digital Image Processing, Autumn 2022
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Exercise 09 - Image thresholding
% 
% prepared by:
% 
% Martin Maska <xmaska@fi.muni.cz>
% David Svoboda <svoboda@fi.muni.cz>
% Petr Matula <pem@fi.muni.cz>
%
% Aim: - To get familiar with basic image thresholding routines
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Built-in image thresholding routines in ImageJ
==============================================

- Open an 8-bit grayscale image from the "images" folder (e.g., "rice.tif" or "pisa.tif") 
- Via "Image -> Adjust -> Threshold", try to apply different image thresholding routines on the opened image
- Open the "shapes.tif" image and try to segment the circle without the square inside it


Implementation of ImageJ plugins
================================

- Back up and delete all files under "plugins/PB130"
- Copy the content of the "09.zip" archive to the "plugins/PB130" folder
- Open the java files in your favourite text editor and complete the "run()" methods in the following order: 
	- My_GradientThresholding (gradient thresholding of a given 8-bit grayscale image)
	- My_UnimodalThresholding (unimodal thresholding of a given 8-bit grayscale image using the triangle method)	
- Study how the implemented routines behave on images in the "images" folder


Validation of completed ImageJ plugins
======================================

- Validate both plugins by compiling and running the "UnitTests_09" plugin located under "PB130"


Submission of completed ImageJ plugins
======================================

- The list of files to be submitted and the homework vault link are given in the interactive syllabus
- Before submission, carefully check that your code neither contains clumsy constructions nor typical errors as listed in the interactive syllabus
