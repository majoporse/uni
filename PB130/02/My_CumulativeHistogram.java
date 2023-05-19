package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;
import ij.process.ByteProcessor;

/** This plugin computes and displays the cumulative histogram of a given 8-bit grayscale image. */
public class My_CumulativeHistogram implements PlugInFilter 
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
		// compute the intensity histogram
		int[] hist = ip.getHistogram();

		// compute the cumulative histogram in-place
		// it must be stored in the original array "hist"
		// WRITE YOUR CODE HERE

		for (int i = 1; i < hist.length; ++i){
			hist[i] += hist[i - 1];
		}

		// IJ.showMessage("NOT IMPLEMENTED!");		
		// NO CHANGES NEEDED AFTER THIS LINE		
		
		// show the cumulative histogram as a new image
		int histImgHeight = 130;
		ImageProcessor histIp = new ByteProcessor(hist.length, histImgHeight);
		histIp.setValue(255);
		histIp.fill();
		
		int start = 0;
		int num = ip.getPixelCount();

		for (int i = 0; i < hist.length; ++i)
		{
			start = histImgHeight - (int)((double) hist[i] / num  * histImgHeight);

			for (int y = start; y < histImgHeight; ++y)
			{
				histIp.set(i, y, 0);	
			}
		}

		ImagePlus histImg = new ImagePlus("My cumulative histogram of " + title, histIp);
		histImg.show();
	}

}
