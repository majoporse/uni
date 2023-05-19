package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;

/** This plugin displays the minimum and maximum intensities within a given 8-bit grayscale image. */
public class My_MinMax implements PlugInFilter 
{
	public int setup(String arg, ImagePlus im) 
	{
		// this plugin accepts 8-bit grayscale images only
		return DOES_8G + NO_CHANGES; 
	}

	public void run(ImageProcessor ip)
	{
		int min = ip.get(0);
		int max = ip.get(0);

		int height = ip.getHeight();
		int width = ip.getWidth();
		int maximum = height * width;

		for (int y = 0; y < maximum; ++y){

				int cur = ip.get(y);
			
				if (cur > max){ max = cur; }
				if (cur < min){ min = cur; }
		}
		
		IJ.showMessage(String.format("Min: %d Max: %d", min, max));
		//IJ.showMessage("NOT IMPLEMENTED!");	
	}

}
