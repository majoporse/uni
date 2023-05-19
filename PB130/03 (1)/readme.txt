%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%       PB130 - Introduction to Digital Image Processing, Autumn 2022
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Exercise 03 - Point transforms
% 
% prepared by:
% 
% Martin Maska <xmaska@fi.muni.cz>
% David Svoboda <svoboda@fi.muni.cz>
% Petr Matula <pem@fi.muni.cz>
%
% Aim: - To get familiar with basic point transforms
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Built-in point transforms in ImageJ
===================================

- Open an 8-bit grayscale image (e.g., "tree_rings.tif" from the "images" folder)
- Via "Process -> Math", increase/decrease the brightness (Add/Subtract) and contrast (Multiply/Divide) of an opened image
- Via "Process -> Math -> Gamma", apply a gamma correction to an opened image
- What happens with the intensity histogram after applying these transforms? Press Ctrl+H to open the histogram window
- Are the elementwise addition, multiplication, and minimum of two images point transforms? If so, are they position-dependent or position-independent?


Implementation of ImageJ plugins
================================

- Back up and delete all files under "plugins/PB130"
- Copy the content of the "03.zip" archive to the "plugins/PB130" folder
- Open the java files in your favorite text editor and complete the "run()" methods in the following order: 
	- My_Inversion (invert a given 8-bit grayscale image)
	- My_IncreaseBrightness (increase the brightness of a given 8-bit grayscale image by 30; Warning: beware of image data type overflows)
	- My_IncreaseContrast (increase the contrast of a given 8-bit grayscale image by 50%; Warning: beware of image data type overflows)
	- My_LinearStretch (apply linear stretching on a given 8-bit grayscale image; Warning: do not modify constant images)
	- My_GammaCorrection (apply a gamma correction to a given 8-bit grayscale image)
- Study how the implemented point transforms modify the intesity histogram of an image (e.g., "tree_rings.tif" from the "images" folder)


Validation of completed ImageJ plugins
======================================

- Validate all the five plugins by compiling and running the "UnitTests_02" plugin located under "PB130"


Submission of completed ImageJ plugins
======================================

- The list of files to be submitted and the homework vault link are given in the interactive syllabus
- Before submission, carefully check that your code neither contains clumsy constructions nor typical errors as listed in the interactive syllabus
