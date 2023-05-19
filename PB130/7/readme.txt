%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%       PB130 - Introduction to Digital Image Processing, Autumn 2022
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Exercise 07 - Distance transform and region labeling
% 
% prepared by:
% 
% Martin Maska <xmaska@fi.muni.cz>
% David Svoboda <svoboda@fi.muni.cz>
% Petr Matula <pem@fi.muni.cz>
%
% Aim: - To get familiar with basic distance transform and region labeling routines 
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Implementation of ImageJ plugins
================================

- Back up and delete all files under "plugins/PB130"
- Copy the content of the "07.zip" archive to the "plugins/PB130" folder
- Open the java files in your favourite text editor and complete them in the following order: 
	- My_ChessboardDistanceTransform (compute the chessboard (D8) distance transform for the foreground of a given binary image) 	
	- My_RegionLabeling (label 4-connected foreground regions in a given binary image using a breadth-first flood filling routine)
- Study how the implemented routines behave on the images in the "images" folder 


Validation of completed ImageJ plugins
======================================

- Validate both plugins by compiling and running the "UnitTests_07" plugin located under "PB130"


Submission of completed ImageJ plugins
======================================

- The list of files to be submitted and the homework vault link are given in the interactive syllabus
- Before submission, carefully check that your code neither contains clumsy constructions nor typical errors as listed in the interactive syllabus