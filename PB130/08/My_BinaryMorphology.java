package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;
import ij.gui.GenericDialog;
import java.lang.Object;

/** This plugin applies basic morphological operators to a given binary image. */
public class My_BinaryMorphology implements PlugInFilter 
{
	String op = "Erosion";
	static int opRadius = 2;

	public int setup(String arg, ImagePlus im) 
	{
		// this plugin accepts binary images only
		return DOES_8G; 
	}

	public void run(ImageProcessor ip) 
	{	
		if (showOpDialog())
		{
			// apply the selected operator 
			if (showParamDialog())
			{			
				switch (op)
				{
					case "Erosion":
						binaryErosionWithDiskSE(ip, opRadius);
						break;
					case "Dilation":
						binaryDilationWithDiskSE(ip, opRadius);
						break;
					case "Opening":
						binaryOpeningWithDiskSE(ip, opRadius);
						break;
					case "Closing":
						binaryClosingWithDiskSE(ip, opRadius);
						break;
				}
			}
		}
	}

	/** Apply the erosion operator with a disk structuring element of given radius to a given binary image. To deal with situations when 
	  * the structuring element hits a coordinate outside the image domain, assume that the value at such a coordinate is set to 255. */
	private void binaryErosionWithDiskSE(ImageProcessor ip, int radius)
	{
		binaryEroDilWithDiskSE(ip, radius, 0);
	}
	
	/** Apply the dilation operator with a disk structuring element of given radius to a given binary image. To deal with situations when
	  * the structuring element hits a coordinate outside the image domain, assume that the value at such a coordinate is set to 0. */
	private void binaryDilationWithDiskSE(ImageProcessor ip, int radius)
	{
		binaryEroDilWithDiskSE(ip, radius, 255);
	}

	/** Apply the opening operator with a disk structuring element of given radius to a given binary image. */
	private void binaryOpeningWithDiskSE(ImageProcessor ip, int radius)
	{
		// return the result of this operator in the image 'ip'
		// you can use the existing functions 'binaryErosionWithDiskSE' and 'binaryDilationWithDiskSE', even though they are not memory efficient
		// do not forget to complete the function 'binaryEroDilWithDiskSE'
		// WRITE YOUR CODE HERE
		binaryErosionWithDiskSE(ip, radius);
		binaryDilationWithDiskSE(ip, radius);
		//IJ.showMessage("NOT IMPLEMENTED!");	
	}

	/** Apply the closing operator with a disk structuring element of given radius to a given binary image. */
	private void binaryClosingWithDiskSE(ImageProcessor ip, int radius)
	{
		// return the result of this operator in the image 'ip'
		// you can use the existing functions 'binaryErosionWithDiskSE' and 'binaryDilationWithDiskSE', even though they are not memory efficient
		// do not forget to complete the function 'binaryEroDilWithDiskSE'
		// WRITE YOUR CODE HERE
		binaryDilationWithDiskSE(ip, radius);
		binaryErosionWithDiskSE(ip, radius);
		// IJ.showMessage("NOT IMPLEMENTED!");
	}

	/** Apply the erosion (critical_value equals to 0) or dilation (critical_value equals to 255) operator with a disk structuring element of given radius to a given binary image. To deal with situations when 
	  * the structuring element hits a coordinate outside the image domain, assume that the value at such a coordinate is set to 255 - critical_value. */
	private void binaryEroDilWithDiskSE(ImageProcessor ip, int radius, int critical_value)
	{
		// return the result of this operator in the image 'ip'
		// do not forget to duplicate the image 'ip' before computation
		// it is forbidden to use continue, break, or alike commands
		// WRITE YOUR CODE HERE

		int w = ip.getWidth();
		int h = ip.getHeight();
		int cur;
		ImageProcessor lol = ip.duplicate();

		for(int y = 0; y < h; ++y){
			for(int x = 0; x < w; ++x){

				boolean stop = false;

				for (int yy = -radius; yy <= radius && !stop; ++yy){
					for (int xx = -radius; xx <= radius && !stop; ++xx){

						if ((xx * xx) + (yy * yy) > radius * radius){
							continue;
						}
						if (x + xx < 0 || x + xx >= w || y + yy < 0 || y + yy >= h){
							continue;
						}
						cur = lol.get(x + xx, y + yy);
						if (cur == critical_value){
							stop = true;
						}
					}
				}

				if (stop){
					if (critical_value == 255){
						ip.set(x, y, 255);
					} else if (critical_value == 0){
						ip.set(x, y, 0);
					}
				}


			}
		}
		// IJ.showMessage("NOT IMPLEMENTED!");
	}

	private boolean showOpDialog()
	{
		String[] op_list = {"Erosion", "Dilation", "Opening", "Closing"};
		GenericDialog dlg = new GenericDialog("Binary Morphology");
		dlg.addChoice("Operator:", op_list, op);
		dlg.showDialog();

		if (dlg.wasCanceled())
		{
			return false;
		}
		else
		{
			op = dlg.getNextChoice();
			return true;
		}
	}

	private boolean showParamDialog()
	{
		GenericDialog dlg = new GenericDialog("Structuring Element");
		dlg.addNumericField("Radius:", opRadius, 0);
		dlg.showDialog();

		if (dlg.wasCanceled())
		{
			return false;
		}
		else
		{
			double tmp = dlg.getNextNumber();

			if (tmp >= 0.0)
			{
				opRadius = (int)tmp;
				return true;		
			}
			else
			{
				IJ.error("The radius must be a nonnegative integer!");
				return false;	
			}
		}
	}

}
