%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%       PB130 - Introduction to Digital Image Processing, August 2022
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Exercise 04 - Linear filters and convolution
% 
% prepared by:
% 
% Martin Maska <xmaska@fi.muni.cz>
% David Svoboda <svoboda@fi.muni.cz>
% Petr Matula <pem@fi.muni.cz>
%
% Aim: - To get familiar with basic linear filters
%      - To get familiar with the convolution operator and different boundary conditions
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Built-in linear filters in ImageJ
=================================

- Via "File -> Open Samples", open an 8-bit grayscale image (e.g., Boats)
- Via "Process -> Filters -> Convolve", apply basic linear filters on an opened image. The kernels of several common filters (e.g., box, Gaussian, Laplacian, or sharpening filter) can be found in the "kernels" folder. 
- What is the reason for using normalized kernels?
- Several linear filters can also be called directly, without explicitly specifying their kernels:
	- Box filter ("Process -> Filters -> Mean")
	- Gaussian filter ("Process -> Filters -> Gaussian Blur")
	- Sharpening filter ("Process -> Filters -> Unsharp Mask")  	


Convolution
===========

To better understand and practice the computation of convolution, convolve a matrix A = [-2 0 1; 0 4 3; 2 1 -1] with a matrix B = [-1 0 1; 0 3 2] by hand. What is the size of the final matrix?


Implementation of ImageJ plugins
================================

- Back up and delete all files under "plugins/PB130"
- Copy the content of the "04.zip" archive to the "plugins/PB130" folder
- Open the java files in your favourite text editor and complete them in the following order:
	- My_Convolution (convolution of two integer matrices with zero boundary conditions; complete the "doConvolution()" method)
	- My_CyclicConvolution (convolution of two integer matrices with periodic boundary conditions; complete the "getElement()" and "doConvolution()" methods; Warning: accessing pixels outside the matrix domain results in a runtime error; it might be useful to exploit modular arithmetics instead of nested conditional statements)


Validation of completed ImageJ plugins
======================================

- Validate both plugins by visually checking the titles of the predefined message box shown by these plugins


Submission of completed ImageJ plugins
======================================

- The list of files to be submitted and the homework vault link are given in the interactive syllabus
- Before submission, carefully check that your code neither contains clumsy constructions nor typical errors as listed in the interactive syllabus
