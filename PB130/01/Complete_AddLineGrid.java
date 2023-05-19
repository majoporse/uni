package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;

/** This plugin adds a regular grid of lines over a given 8-bit grayscale image. The distance between the lines is set to 20 pixels in each axis. */
public class Complete_AddLineGrid implements PlugInFilter 
{
	public int setup(String arg, ImagePlus im) 
	{
		// this plugin accepts 8-bit grayscale images only
		return DOES_8G; 
	}

	public void run(ImageProcessor ip) 
	{
		int w = ip.getWidth();
		int h = ip.getHeight();

		// add horizontal lines
		for (int y = 0; y < h; y += 20)
		{
			for (int x = 0; x < w; ++x) 
			{
				ip.set(x, y, 255);
			}
		}

		// add vertical lines
		for (int x = 0; x < w; x += 20)
		{
			for (int y = 0; y < h; ++y) 
			{
				ip.set(x, y, 255);
			}
		}
	}

}
