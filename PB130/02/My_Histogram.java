package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;
import ij.process.ByteProcessor;

/** This plugin computes and displays the intensity histogram of a given 8-bit grayscale image. In addition, it displays the image exposure information. 
    The image is considered underexposed/overexposed if the pixels with the intesity 0/255 cover more than 10% of the total image area. */
public class My_Histogram implements PlugInFilter 
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
		// histogram array
		int[] hist = new int[256];
		
		// compute the intensity histogram
		// WRITE YOUR CODE HERE

		int maximum = ip.getHeight() * ip.getWidth();

		for (int i = 0; i < maximum; ++i){
			hist[ip.get(i)] += 1;
		}

		// IJ.showMessage("NOT IMPLEMENTED!");		

		// decide whether the image is underexposed/overexposed or not
		boolean uexp = hist[0] > maximum / 10;
		boolean oexp = hist[255] > maximum / 10;
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

		ImagePlus histImg = new ImagePlus(String.format("My histogram of %s Underexposure: %b Overexposure: %b", title, uexp, oexp), histIp);
		histImg.show();
	}

}
