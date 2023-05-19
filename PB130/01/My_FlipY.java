package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;

/** This plugin flips a given image vertically. */
public class My_FlipY implements PlugInFilter 
{
	public int setup(String arg, ImagePlus im) 
	{
		// this plugin accepts all supported image types
		return DOES_ALL; 
	}

	public void run(ImageProcessor ip) 
	{
		int width = ip.getWidth();
		int height = ip.getHeight() - 1;

		for (int y = 0; y <= ( height / 2 ); ++y){

			for (int x = 0; x < width; ++x){

				int oval = ip.get(x,height - y);

				ip.set(x,height - y,ip.get(x,y));
				ip.set(x,y,oval);
			}
			
		}
		// IJ.showMessage("NOT IMPLEMENTED!");
	}

}
