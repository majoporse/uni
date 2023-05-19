package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;
import ij.process.FloatProcessor;
import ij.process.ByteProcessor;
import ij.gui.GenericDialog;

/** This plugin computes the Laplacian zero-crossing of a given 8-bit grayscale image. */
public class My_LaplacianZeroCrossing implements PlugInFilter 
{
	/** The sigma value. */	
	static double sigma = 0.0;		

	/** The short image title. */
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
		if (showDialog())
		{
			// size of the input image
			int w = ip.getWidth();
			int h = ip.getHeight();

			// create a 32-bit version of the input image
			FloatProcessor fip = ip.convertToFloatProcessor();

			// apply the Gaussian blur on the 32-bit version of the input image
			fip.blurGaussian(sigma);

			// allocate the Laplacian image 
			FloatProcessor lip = new FloatProcessor(w, h);

			// go through the image 'fip' and compute the Laplacian at each pixel
			// skip pixels in which the operator looks outside the image domain
			// store the computed values into the image 'lip'
			// to work with floating-point values, use getf()/setf() methods of the 'ImageProcessor' class
			// WRITE YOUR CODE HERE
			// IJ.showMessage("NOT IMPLEMENTED!");
			
			for(int y = 1; y < h-1; ++y){
				for (int x = 1; x < w - 1; ++x){
					float d = -4f *fip.getf(x, y) + fip.getf(x-1, y) + fip.getf(x+1, y) + fip.getf(x, y-1) + fip.getf(x, y+1);
					lip.setf(x, y, d);
				}
			
			}
		
			// allocate the Laplacian zero-crossing image 
			ByteProcessor out = new ByteProcessor(w, h);

			// go through the Laplacian image 'lip' and compute its zero-crossing 
			// skip pixels in which the Laplacian operator looked outside the image domain
			// store the Laplacian zero-crossing into the image 'out', keeping the value of '0' for background and setting the value of '255' for the zero-crossing
			// the zero-crossing pixels are defined as those of negative Laplacian values having at least one 4-neighbour of a positive Laplacian value
			// WRITE YOUR CODE HERE
			
			for(int y = 1; y < h - 1; ++y){
				for (int x = 1; x < w - 1; ++x){
					float cur = lip.getf(x,y);
					if (cur < 0 && (lip.getf(x-1,y) > 0 || lip.getf(x+1,y) > 0 || lip.getf(x,y-1) > 0 || lip.getf(x,y+1) > 0 )) {
						out.setf(x, y, 255);
					} else {
						out.setf(x, y, 0);
					}
				}
			
			}
			// NO CHANGES NEEDED AFTER THIS LINE

			// show the Laplacian image
			ImagePlus lipImg = new ImagePlus("My Laplacian of " + title, lip);
			lipImg.show();


			// show the Laplacian zero-crossing image
			ImagePlus outImg = new ImagePlus("My Laplacian Zero-Crossing of " + title, out);
			outImg.show();
		}
	}

	private boolean showDialog()
	{
		GenericDialog dlg = new GenericDialog("Gaussian Blur");
		dlg.addNumericField("Sigma value:", sigma, 2);
		dlg.showDialog();

		if (dlg.wasCanceled())
		{
			return false;
		}
		else
		{
			double tmp = dlg.getNextNumber();

			if (tmp >= 0.0 && tmp <= 20.0)
			{
				sigma = tmp;
				return true;		
			}
			else
			{
				IJ.error("The sigma value must be within the [0, 20] interval!");
				return false;	
			}
		}
	}

}
