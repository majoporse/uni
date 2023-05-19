package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;
import ij.process.ByteProcessor;

/** This plugin computes and displays the intensity histogram of a given 16-bit grayscale image, which consists of 512 bins. */
public class My_BinnedHistogram implements PlugInFilter 
{	
	String title = null;
	
	public int setup(String arg, ImagePlus im) 
	{
		if (im != null)
		{
			// store the short image title for future use
			title = im.getShortTitle();
			
			// this plugin accepts 16-bit grayscale images only
			return DOES_16 + NO_CHANGES; 
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
		// histogram array with 512 bins
		int[] hist = new int[512];

		// compute the intensity histogram
		// WRITE YOUR CODE HERE
		
		int bucket = 128;
		int max = ip.getPixelCount();
		for (int i = 0; i < max; ++i){
			hist[ip.get(i) / bucket] += 1;
		}


		//IJ.showMessage("NOT IMPLEMENTED!");		
		// NO CHANGES NEEDED AFTER THIS LINE		
		
		// show the intensity histogram as a new image
		int histImgHeight = 130;
		ImageProcessor histIp = new ByteProcessor(hist.length, histImgHeight);
		histIp.setValue(255);
		histIp.fill();
		
		int histMax = hist[0];
		for (int i = 1; i < hist.length; ++i)
		{
			if (hist[i] > histMax)
			{
				histMax = hist[i];
			}
		}

		if (histMax == 0)
		{
			IJ.error("Empty histogram!");
			return;
		}

		int start = 0;
		for (int i = 0; i < hist.length; ++i)
		{
			start = histImgHeight - (int)((double) hist[i] / histMax * histImgHeight);

			for (int y = start; y < histImgHeight; ++y)
			{
				histIp.set(i, y, 0);	
			}
		}

		ImagePlus histImg = new ImagePlus("My binned histogram of " + title, histIp);
		histImg.show();
	}

}
