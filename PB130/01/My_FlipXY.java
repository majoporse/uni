package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;

/** This plugin flips a given image horizontally as well as vertically in a single image pass. */
public class My_FlipXY implements PlugInFilter 
{
	public int setup(String arg, ImagePlus im) 
	{
		// this plugin accepts all supported image types
		return DOES_ALL; 
	}

	public void run(ImageProcessor ip) 
	{
		int width = ip.getWidth();
		int height = ip.getHeight();
		int max = width * height;
		for (int i = 0; i < max / 2; ++i){

			int cur = ip.get(i);
			ip.set(i, ip.get(max - i - 1));
			ip.set(max - i - 1, cur);

		}

		//IJ.showMessage("NOT IMPLEMENTED!");
	}

}
