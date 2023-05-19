%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%       PB130 - Introduction to Digital Image Processing, Autumn 2022
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Exercise 08 - Mathematical morphology
% 
% prepared by:
% 
% Martin Maska <xmaska@fi.muni.cz>
% David Svoboda <svoboda@fi.muni.cz>
% Petr Matula <pem@fi.muni.cz>
%
% Aim: - To get familiar with basic mathematical morphology concepts
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Built-in mathematical morphology in ImageJ
==============================================

- You may find useful the following menu commands:
	- "Process -> Filters -> Minimum" - erosion operator with a disk structuring element
	- "Process -> Filters -> Maximum" - dilation operator with a disk structuring element
	- "Process -> Image Calculator"	- basic arithmetical operations over images
	- "Image -> Duplicate" - duplicate a given image

- Open the "black_point.tif", "white_point.tif", and "t.tif" images from the "images" folder and study the behavior of the erosion, dilation, opening, and closing operators with disk structuring elements of different sizes 
- Open the "wheel.tif" image from the "images" folder and extract individual cogs
- Open the "rice.tif" image from the "images" folder and remove its unevenly illuminated background using a white top-hat filter
- Via "Process -> Binary -> Outline", compute the boundary of objects in an opened binary image (e.g., "t.tif" or "wheel.tif" from the "images" folder)   
- Via "Process -> Binary -> Skeletonize", compute the skeleton of objects in an opened binary image (e.g., "t.tif" or "wheel.tif" from the "images" folder)


Implementation of ImageJ plugins
================================

- Back up and delete all files under "plugins/PB130"
- Copy the content of the "08.zip" archive to the "plugins/PB130" folder
- Open the java files in your favourite text editor and complete them in the following order: 
	- My_BinaryMorphology (apply basic morphological operators to a given binary image)
	- My_BinaryHoleFilling (fill holes in a given binary image by emulating morphological reconstruction via flood filling)


Validation of completed ImageJ plugins
======================================

- Validate both plugins by compiling and running the "UnitTests_08" plugin located under "PB130"


Submission of completed ImageJ plugins
======================================

- The list of files to be submitted and the homework vault link are given in the interactive syllabus
- Before submission, carefully check that your code neither contains clumsy constructions nor typical errors as listed in the interactive syllabus