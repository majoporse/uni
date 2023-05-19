package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;

/** This plugin applies the linear stretch on a given 8-bit grayscale image. */
public class My_LinearStretch implements PlugInFilter 
{
	public int setup(String arg, ImagePlus im) 
	{
		// this plugin accepts 8-bit grayscale images only
		return DOES_8G; 
	}

	public void run(ImageProcessor ip) 
	{
		// WRITE YOUR CODE HERe
		int max = ip.getPixelCount();
		double low = ip.get(0);
		double high = ip.get(0);
		for (int i = 0; i < max; ++i){
			int cur = ip.get(i);
			if (cur < low){low = cur;}
			if (cur > high){high = cur;}
		}

		
		if (high == low){
			return;
		}

		double ratio = 255.0 / (high - low);

		for (int i = 0; i < max; ++i){
			int newPixel = (int) ( Math.round( (double) (ip.get(i) - low) * ratio) );
			ip.set(i, newPixel);
		}
		//IJ.showMessage("NOT IMPLEMENTED!");
	}

}
