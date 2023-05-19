package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;

/** This plugin flips a given image horizontally. */
public class My_FlipX implements PlugInFilter 
{
	public int setup(String arg, ImagePlus im) 
	{
		// this plugin accepts all supported image types
		return DOES_ALL; 
	}

	public void run(ImageProcessor ip) 
	{
		int width = ip.getWidth() - 1;
		int height = ip.getHeight();

		for (int y = 0; y < height; ++y){

			for (int x = 0; x <= (width / 2); ++x){

				int oval = ip.get(width - x, y);

				ip.set(width - x, y, ip.get(x,y));
				ip.set(x, y, oval);
			}
			
		}
		// IJ.showMessage("NOT IMPLEMENTED!");
	}

}
