package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;
import java.util.Queue;
import java.util.ArrayDeque;

class Pixel
{
	/** Pixel coordinates. */
	int x, y;

	/** Constructor. */
	Pixel(int x, int y)
	{
		this.x = x;
		this.y = y;
	}
}

/** This plugin fills holes in a given binary image by emulating morphological reconstruction via flood filling. */
public class My_BinaryHoleFilling implements PlugInFilter 
{	
	final static int BACKGROUND_LABEL = 0; // alias for the background label of a binary image
	final static int TMP_LABEL = 128; // alias for the temporary label used during flood filling

	public int setup(String arg, ImagePlus im) 
	{
		// this plugin accepts binary images
		return DOES_8G; 
	}

	public void run(ImageProcessor ip) 
	{	
		// go through the one-pixel image border of 'ip' and apply flood filling to all background pixels
		// represented by BACKGROUND_LABEL, relabeling them to TMP_LABEL and storing the intermediate output in 'ip'
		// binarize the intermediate output (TMP_LABEL -> 0, otherwise -> 255) directly in 'ip'
		// WRITE YOUR CODE HERE
		Queue<Pixel> q = new ArrayDeque<Pixel>();

		int x, y;
		int w = ip.getWidth();
		int h = ip.getHeight();

		for(int i = 0; i < w; ++i){
			q.add(new Pixel(i, 0));
			q.add(new Pixel(i, h-1));
		}
		for (int i = 0; i < h; ++i){
			q.add(new Pixel(0, i));
			q.add(new Pixel(w - 1, i ));
		}

		while (!q.isEmpty())
        {
            Pixel p = q.remove();
			x = p.x;
			y = p.y;
            if (x >= 0 && x < w && y >=0 && y < h && ip.get(x, y) == BACKGROUND_LABEL) {
                ip.set(x, y, TMP_LABEL);
                q.add(new Pixel(x + 1, y));
                q.add(new Pixel(x - 1, y));
                q.add(new Pixel(x, y + 1));
                q.add(new Pixel(x, y - 1));
            }
        }

		for(y = 0; y < h; ++y){
			for(x = 0; x < w; ++x){
				if (ip.get(x, y) == TMP_LABEL){
					ip.set(x, y, 0);
				} else {
					ip.set(x, y, 255);
				}
			}
		}
		// IJ.showMessage("NOT IMPLEMENTED!");
	}
	
}
