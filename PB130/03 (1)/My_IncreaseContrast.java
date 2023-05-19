package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;

/** This plugin increases the contrast of a given 8-bit grayscale image by 50%. */
public class My_IncreaseContrast implements PlugInFilter 
{
	public int setup(String arg, ImagePlus im) 
	{
		// this plugin accepts 8-bit grayscale images only
		return DOES_8G; 
	}

	public void run(ImageProcessor ip) 
	{
		// WRITE YOUR CODE HERE
		int max = ip.getPixelCount();
		for (int i = 0; i < max; ++i){
			int novy = (int) ((float) ip.get(i) * 1.5 + 0.5);
			if (novy > 255) {novy = 255;}
			ip.set(i, novy);
		}
		//IJ.showMessage("NOT IMPLEMENTED!");
	}

}
