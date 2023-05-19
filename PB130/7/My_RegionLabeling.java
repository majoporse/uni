package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;
import ij.process.ShortProcessor;
import java.util.Queue;
import java.util.ArrayDeque;

/** This class encapsulates the coordinates of a single pixel. */
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

/** This plugin applies a breath-first flood filling routine to label 4-connected foreground regions in a given binary image. */
public class My_RegionLabeling implements PlugInFilter 
{
	String title = null;
	final static int UNLABELED = 65535;

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
		// size of the input image
		int w = ip.getWidth();
		int h = ip.getHeight();
		
		// create an output image initialized with zeros
		ShortProcessor out = new ShortProcessor(w, h);

		// mark all foreground pixels as UNLABELED
		int num = w * h;
		for (int i = 0; i < num; ++i)
		{
			if (ip.get(i) == 255)
			{
				out.set(i, UNLABELED);
			}
		} 

		// region label
		int label = 1;	

		// go through the image 'out' and label individual 4-connected foreground regions using a breadth-first flood filling routine
		for (int y = 0; y < h; ++y)
		{
			for (int x = 0; x < w; ++x)
			{
				// check if the current pixel is UNLABELED
				if (out.get(x, y) == UNLABELED)
				{
					floodFill(out, x, y, label);
					++label;
				}
			}
		}

		// show the output image
		ImagePlus outImg = new ImagePlus(String.format("My labeling (Num=%d) of ", label - 1) + title, out);
		outImg.show();

		// apply a color look-up table
		IJ.run("3-3-2 RGB");
	}
	
	/** Perform breadth-first flood filling using a given label from a seed with coordinates 'x' and 'y'. */ 
	private void floodFill(ShortProcessor out, int x, int y, int label)
	{
		// create an empty queue
		Queue<Pixel> q = new ArrayDeque<Pixel>();

		// to add a pixel with coordinates 'x' and 'y' to the tail of the queue 'q', call q.add(new Pixel(x, y))
		// to check if the queue 'q' is empty, call q.isEmpty()
		// to remove a pixel from the head of the queue 'q' and store it in the variable 'n', call n = q.remove()
		// WRITE YOUR CODE HERE
		int x1, y1;
		int w = out.getWidth();
		int h = out.getHeight();
		q.add(new Pixel(x, y));
        while (!q.isEmpty())
        {
            Pixel p = q.remove();
			x1 = p.x;
			y1 = p.y;
            if (x1 >= 0 && x1 < w && y1 >=0 && y1 < h && out.get(x1, y1) == UNLABELED) {
                out.set(x1, y1, label);
                q.add(new Pixel(x1 + 1, y1));
                q.add(new Pixel(x1 - 1, y1));
                q.add(new Pixel(x1, y1 + 1));
                q.add(new Pixel(x1, y1 - 1));
            }
        }
	}

}