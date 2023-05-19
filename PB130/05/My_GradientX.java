package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;
import ij.process.FloatProcessor;

/** This plugin approximates the gradient in the x direction using central differences. */
public class My_GradientX implements PlugInFilter 
{
	String title = null;

	public int setup(String arg, ImagePlus im) 
	{
		if (im != null)
		{
			// store the short image title for future use
			title = im.getShortTitle();
			
			// this plugin accepts 8-bit grayscale images only
			return DOES_8G + NO_CHANGES; 
		}
		else
		{
			// no image is open
			IJ.noImage();
			return DONE;
		}
	}

	public void run(ImageProcessor ip) 
	{	
		// size of the input image
		int w = ip.getWidth();
		int h = ip.getHeight();

		// allocate the output image
		FloatProcessor out = new FloatProcessor(w, h);

		// go through the image 'ip' and apply the central difference operator in the x direction
		// skip pixels in which the operator looks outside the image domain
		// store the computed values into the image 'out'
		// to work with floating point values, use getf()/setf() methods of the 'ImageProcessor' class
		// WRITE YOUR CODE HERE
		for(int y = 0; y < h; ++y){
			for (int x = 1; x < w - 1; ++x){

				out.setf(x, y, (ip.getf(x + 1, y) - ip.getf(x - 1, y)) / 2f);

			}
			
		}
		// IJ.showMessage("NOT IMPLEMENTED!");		
		// NO CHANGES NEEDED AFTER THIS LINE

		// show the output image
		ImagePlus outImg = new ImagePlus("My gradientX of " + title, out);
		outImg.show();
	}

}
