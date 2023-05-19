package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;
import ij.gui.GenericDialog;
import java.util.ArrayList;
import java.util.Collections;

/** This plugin applies median filtering with a square neighborhood on a given 8-bit grayscale image. */
public class My_MedianFilter implements PlugInFilter 
{
	/** The square neighborhood radius. */	
	static int radius = 1;		

	public int setup(String arg, ImagePlus im) 
	{
		// this plugin accepts 8-bit grayscale images only
		return DOES_8G;
	}

	public void run(ImageProcessor ip) 
	{
		if (showDialog())
		{
			// duplicate the image
			ImageProcessor tmp = ip.duplicate();

			// initialize a list for storing values in the square neighborhood
			ArrayList<Integer> neighbors = new ArrayList<Integer>();

			// go through the image 'tmp' and compute the median value in the square neighborhood of each pixel
			// do not forget to skip the values outside the image domain
			// store the computed median values into the image 'ip'
			// to add an integer value 'i' to the list, call neighbors.add(i) 
			// to clear the list, call neighbors.clear()
			// to find the median value of the list, call getMedian(neighbors)
			// do not forget to complete the 'getMedian()' method in this file 	
			// WRITE YOUR CODE HERE
			int w = tmp.getWidth();
			int h = tmp.getHeight();
			int result;
			
			for(int y = 0; y < h; ++y){
				for (int x = 0; x < w; ++x){
					
					
					for(int my = -radius; my <= radius; ++my){
						for(int mx = -radius; mx <= radius; ++mx){
							
						if( x + mx < 0 || x + mx >= w  || y + my < 0 || y + my >= h ){
							continue;
						}
						neighbors.add(tmp.get(x + mx, y + my));
						}
					}
					result = getMedian(neighbors);
					ip.set(x, y, result);
					
					neighbors.clear();
				}
			}
			// IJ.showMessage(Integer.toString(w));
			
			
		}
	}

	/** Get the median value of a given non-empty list of integers. */
	private int getMedian(ArrayList<Integer> a)
	{
		// sort the list 'a'
		Collections.sort(a);

		// the length of the list 'a'
		int len = a.size();
		
		// return the median value of the sorted list 'a'
		// to get the i-th value in the list, call a.get(i)
		// WRITE YOUR CODE HERE
		int res;

		if (len % 2 == 0){
			res = (int) (Math.round( (a.get(len / 2) + a.get((len / 2) - 1) ) / 2.0 ));
		} else{
			res = a.get((len / 2));
		}
		return res;
	}

	private boolean showDialog()
	{
		GenericDialog dlg = new GenericDialog("Median Filtering");
		dlg.addNumericField("Square neighborhood radius:", radius, 0);
		dlg.showDialog();

		if (dlg.wasCanceled())
		{
			return false;
		}
		else
		{
			double tmp = dlg.getNextNumber();

			if (tmp >= 1.0)
			{
				radius = (int)tmp;
				return true;		
			}
			else
			{
				IJ.error("The radius must be a positive integer!");
				return false;	
			}
		}
	}

}
