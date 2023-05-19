package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;
import ij.gui.GenericDialog;
import java.util.ArrayList;
import java.util.Collections;

/** This plugin applies advanced median filtering with a square neighborhood on a given 8-bit grayscale image corrupted with salt-and-pepper noise. The filter is applied to the noise-corrupted pixels only, working only with the noise-uncorrupted pixels in the neighborhood. */
public class My_AdvancedMedianFilter implements PlugInFilter 
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
			// WRITE YOUR CODE HERE
			ImageProcessor tmp = ip.duplicate();
			
			ArrayList<Integer> neighbors = new ArrayList<Integer>();
			
			int w = tmp.getWidth();
			int h = tmp.getHeight();
			int result;
			
			for(int y = 0; y < h; ++y){
				for (int x = 0; x < w; ++x){
					
					if (tmp.get(x, y) != 0 && tmp.get(x, y) != 255){
						continue;
					}
					
					// is 0 or 255
					for(int my = -radius; my <= radius; ++my){
						for(int mx = -radius; mx <= radius; ++mx){

						if( x + mx < 0 || x + mx >= w  || 
							y + my < 0 || y + my >= h || 
							tmp.get(x + mx, y + my) == 0 || 
							tmp.get(x + mx, y + my) == 255){
							continue;
						}
						neighbors.add(tmp.get(x + mx, y + my));
						}
					}
					if (neighbors.size() == 0){
						result = tmp.get(x,y);
					} else {
						result = getMedian(neighbors);
					}
					ip.set(x, y, result);
					
					neighbors.clear();
				}
			}
			// IJ.showMessage("NOT IMPLEMENETD!");
		}
	}
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
		GenericDialog dlg = new GenericDialog("Advanced Median Filtering");
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
