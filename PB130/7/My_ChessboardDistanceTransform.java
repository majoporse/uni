package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;
import ij.process.ShortProcessor;
import ij.gui.GenericDialog;

/** This plugin computes the chessboard distance transform for the foreground of a given binary image. */
public class My_ChessboardDistanceTransform implements PlugInFilter 
{
	String title = null;
	String bCond = "Foreground";
	final static int INFTY = 65535;

	public int setup(String arg, ImagePlus im) 
	{
		if (im != null)
		{
			// store the short image title for future use
			title = im.getShortTitle();
			
			// this plugin accepts binary images only
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

			// create a distance map image initialized with zeros 
			// its one-pixel border is designated to deal with different boundary conditions
			// therefore, the corresponding information in the input image is ignored
			ShortProcessor dist = new ShortProcessor(w, h); 

			// turn on the foreground boundary conditions
			if (bCond.equals("Foreground"))
			{ 
				dist.set(INFTY);
			}

			// compute a chessboard distance map using a two-scan algorithm
			// limit the computation to only those pixels not belonging to the one-pixel border of the image domain
			// the first scan runs from top to bottom and from left to right
			// the second scan runs from bottom to top and from right to left
			// do not forget to ensure for the computed distance in the first scan not to exceed INFTY
			// WRITE YOUR CODE HERE
			int cur;

			for (int y = 1; y < h - 1; ++y)
			{
				for (int x = 1; x < w - 1; ++x)
				{
					if (ip.get(x,y) == 0){
						dist.set(x, y, 0);
						continue;
					}

					cur = dist.get(x-1,y);
					

					if (dist.get(x,y-1) < cur) {
						cur = dist.get(x,y-1);
					}

					if (dist.get(x-1,y-1) < cur) {
						cur = dist.get(x-1,y-1);
					}

					if (dist.get(x+1,y-1) < cur) {
						cur = dist.get(x+1,y-1);
					}
					if (cur == INFTY){
						continue;
					}
					dist.set(x,y,cur + 1);
					

					
				}
			}
			for (int y = h-2; y > 0; --y)
			{
				for (int x = w-2; x > 0; --x)
				{
				
					if (ip.get(x,y) == 0) {
						continue;
					}

					cur = dist.get(x+1,y);

					if (dist.get(x,y+1) < cur) {
						cur = dist.get(x,y+1);
					}

					if (dist.get(x+1,y+1) < cur) {
						cur = dist.get(x+1,y+1);
					}

					if (dist.get(x-1,y+1) < cur) {
						cur = dist.get(x-1,y+1);
					}

					if (cur < dist.get(x,y))
						dist.set(x,y,cur + 1);
				}
			}
			
			
			
			// NO CHANGES NEEDED AFTER THIS LINE

			// show the distance map image without its one-pixel border
			ShortProcessor res = new ShortProcessor(w - 2, h - 2);
		
			for (int y = 1; y < h - 1; ++y)
			{
				for (int x = 1; x < w - 1; ++x)
				{	
					res.set(x - 1, y - 1, dist.get(x, y));
				}
			}
			
			ImagePlus distImg = new ImagePlus("My chessboard distance transform of " + title, res);
			distImg.show();
		}
	}

	private boolean showDialog()
	{
		String[] conds = {"Background", "Foreground"};
		GenericDialog dlg = new GenericDialog("Chessboard Distance Transform");
		dlg.addChoice("Image domain border:", conds, bCond);
		dlg.showDialog();

		if (dlg.wasCanceled())
		{
			return false;
		}
		else
		{
			bCond = dlg.getNextChoice();
			return true;
		}
	}

}
