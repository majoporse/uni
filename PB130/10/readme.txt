%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%       PB130 - Introduction to Digital Image Processing, Autumn 2022
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Exercise 10 - Region measurements
% 
% prepared by:
% 
% Martin Maska <xmaska@fi.muni.cz>
% David Svoboda <svoboda@fi.muni.cz>
% Petr Matula <pem@fi.muni.cz>
%
% Aim: - To get familiar with basic characteristics of binary regions
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Implementation of ImageJ plugins
================================

- Back up and delete all files under "plugins/PB130"
- Copy the content of the "10.zip" archive to the "plugins/PB130" folder
- Open the java file in your favourite text editor and complete the following methods in the given order:
	- measure (measure the basic properties of individual regions in a given labeled image)
	- centralMoment (compute the central moment of given orders for a given binary region)
	- classifyEcc (classify regions into three categories depending on their eccentricity)


Validation of completed ImageJ plugins
======================================

- Validate the plugin by compiling and running the "UnitTests_10" plugin located under "PB130" and by visually checking individual region properties for the "nuts_bolts.tif" image from the "images" folder with the records shown in "nuts_bolts_properties.png"


Submission of completed ImageJ plugins
======================================

- The list of files to be submitted and the homework vault link are given in the interactive syllabus
- Before submission, carefully check that your code neither contains clumsy constructions nor typical errors as listed in the interactive syllabus