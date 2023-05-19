%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%       PB130 - Introduction to Digital Image Processing, Autumn 2022
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Exercise 01 - ImageJ and digital image representation
% 
% prepared by:
% 
% Martin Maska <xmaska@fi.muni.cz>
% David Svoboda <svoboda@fi.muni.cz>
% Petr Matula <pem@fi.muni.cz>
%
% Aims: - To get familiar with the ImageJ environment
%	- To implement simple ImageJ plugins
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

First steps with ImageJ
=======================

- Create a folder named "PB130" under "ImageJ/plugins" and copy the content of the "01.zip" archive there
- Via "File -> Open...", open a few sample images from "PB130/images" (e.g., leaf.jpg, rotated_leaf.jpg, or tree_rings.tif)
- What is the size and bit-depth of these images?
- Via "Image -> Color -> Split Channels", extract individual channels from an RGB image
- Via "Image -> Type", convert an RGB image into a grayscale one
- Try other functions under the "Image" menu (e.g., zooming in/out, scaling, flipping) 


Compilation of the first simple ImageJ plugin
=============================================

- Compile the "Complete_AddLineGrid.java" file via "Plugins -> Compile and Run"
- Refresh the content of menus via "Help -> Refresh Menus"
- Run the plugin via "Plugins -> PB130 -> Complete_AddLineGrid" over an opened 8-bit grayscale image (e.g., "Tree Rings")
- Open the java file in your favourite text editor and study the plugin structure and implementation


Implementation of ImageJ plugins
================================

- Open the My*.java files in your favorite text editor and complete the "run()" methods in the following order: 
	- My_MinMax (find the minimum and maximum intensity within a given 8-bit grayscale image)
	- My_FlipX (flip a given image horizontally)
	- My_FlipY (flip a given image vertically)
	- My_FlipXY (flip a given image horizontally as well as vertically in a single image pass)


Validation of completed ImageJ plugins
======================================

- Validate the "My_MinMax" plugin by comparing its output for all 8-bit images under "PB130/images" with the values reported in a particular histogram window (Ctrl+H)
- Validate the remaining plugins by compiling and running the "UnitTests_01" plugin located under "PB130"


Submission of completed ImageJ plugins
======================================

- The list of files to be submitted and the homework vault link are given in the interactive syllabus
- Before submission, carefully check that your code neither contains clumsy constructions nor typical errors as listed in the interactive syllabus