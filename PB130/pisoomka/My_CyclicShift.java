package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;
import ij.gui.GenericDialog;

/** This plugin cyclically shift a given image by a user-defined number of rows and columns. */
public class My_CyclicShift implements PlugInFilter 
{	
	/** The cyclic shift along the rows. */	
	static int rowShift = 50;		

	/** The cyclic shift along the columns. */	
	static int columnShift = -50;

	String title = null;		
	
	public int setup(String arg, ImagePlus im) 
	{
		if (im != null)
		{
			// store the short image title for future use
			title = im.getShortTitle();
			
			// this plugin accepts all supported image types
			return DOES_ALL + NO_CHANGES; 
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
		// show the dialog for setting the shift parameters
		if (showDialog())
		{
			// duplicate the input image
			ImageProcessor out = ip.duplicate();			
			
			// shift the image 'ip' cyclically by the user-defined number of rows and columns
			// these numbers are given in 'rowShift' and 'columnShift', respectively
			// store the shifted image in the output image 'out' 
			// you may find useful the function Math.floorMod()
			// WRITE YOUR CODE HERE
			// IJ.showMessage("NOT IMPLEMENTED!");


			int w = ip.getWidth();
			int h = ip.getHeight();
			int max = ip.getPixelCount();
			int rs = rowShift % h;
			int cs = columnShift % w;
			if (rs < 0){rs += h;}
			if (cs < 0){cs += w;}

			for (int y = 0; y < h; ++y){
				for (int x = 0; x < w; ++x){
					out.set((x + cs) % w, (y + rs) % h, ip.get(x, y));
					
				}
				
			}


			// NO CHANGES NEEDED AFTER THIS LINE			

			// display the output image
			ImagePlus outImg = new ImagePlus(String.format("Cyclic Shift of %s by %d rows and %d columns", title, rowShift, columnShift), out);
			outImg.show();
		}	
	}

	private boolean showDialog()
	{
		GenericDialog dlg = new GenericDialog("Cyclic Shift");
		dlg.addNumericField("Row shift:", rowShift, 0);
		dlg.addNumericField("Column shift:", columnShift, 0);
		dlg.showDialog();

		if (dlg.wasCanceled())
		{
			return false;
		}
		else
		{
			rowShift = (int) dlg.getNextNumber();
			columnShift = (int) dlg.getNextNumber();
			return true;
		}
	}

}
