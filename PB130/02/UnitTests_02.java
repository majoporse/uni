package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.PlugIn;
import ij.process.ImageProcessor;

/** This plugin automatically validates the plugins within Exercise 02. */
public class UnitTests_02 implements PlugIn 
{	
	int failedTests = 0;
	String plugDir = IJ.getDirectory("plugins") + "PB130/";
	String srcDir = plugDir + "images/";
	String refDir = plugDir + "refs/";	

	public void run(String arg) 
	{
		IJ.open(srcDir + "chessboard.tif");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_Histogram.java");
		IJ.wait(500);
		IJ.open(srcDir + "lena16b.tif");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_BinnedHistogram.java");
		IJ.wait(500);
		IJ.selectWindow("chessboard.tif");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_CumulativeHistogram.java");
		IJ.wait(500);
		IJ.selectWindow("chessboard.tif");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_GaussianNoise.java");
		IJ.wait(500);
		IJ.run("Close All");
		IJ.run("Refresh Menus");
		IJ.log("\\Clear");
		IJ.log("Please wait, running all pre-defined tests...");
		IJ.log("Source image directory: " + srcDir);
		IJ.log("Reference image directory: " + refDir);
		IJ.log("=============================================");
		testPluginWithFlags("My Histogram", "chessboard.tif", "chessboard_hist.tif", false, false);
		testPluginWithFlags("My Histogram", "photo.tif", "photo_hist.tif", true, false);
		testPluginWithFlags("My Histogram", "photo2.tif", "photo2_hist.tif", false, true);
		testPluginWithFlags("My Histogram", "photo3.tif", "photo3_hist.tif", true, true);
		testPlugin("My CumulativeHistogram", "", "ramp.tif", "ramp_cumulativehist.tif");
		testPlugin("My BinnedHistogram", "", "lena16b.tif", "lena16b_binnedhist.tif");
		testPlugin("My GaussianNoise", "standard=10", "chessboard.tif", "chessboard_gaussnoise10.tif");
		testPlugin("My GaussianNoise", "standard=20", "chessboard.tif", "chessboard_gaussnoise20.tif");		

		if (failedTests > 0)
		{
			IJ.log("Total number of tests failed: " + failedTests);
		}
		else
		{
			IJ.log("CONGRATULATIONS! ALL TESTS PASSED.");
		}		
	}

	private void testPlugin(String pluginName, String pluginParams, String srcImage, String refImage)
	{
		IJ.log("Plugin name: " + pluginName);
		IJ.log("Source image: " + srcImage);
		IJ.log("Reference image: " + refImage);
		IJ.open(srcDir + srcImage);
		ImagePlus src = IJ.getImage();
		IJ.run(pluginName, pluginParams);
		ImagePlus out = IJ.getImage();
		IJ.open(refDir + refImage);
		ImagePlus ref = IJ.getImage();
		
		if (compare(ref.getProcessor(), out.getProcessor()))
		{
			IJ.log("Test passed!");
			
		}
		else
		{
			IJ.log("Test failed!");
			++failedTests;
		}

		src.changes = false;
		src.close();
		out.changes = false;
		out.close();
		ref.changes = false;
		ref.close();
		IJ.log("=============================================");
	}

	private void testPluginWithFlags(String pluginName, String srcImage, String refImage, boolean uexp, boolean oexp)
	{
		IJ.log("Plugin name: " + pluginName);
		IJ.log("Source image: " + srcImage);
		IJ.log("Reference image: " + refImage);
		IJ.log("Underexposure flag: " + uexp);
		IJ.log("Overexposure flag: " + oexp);
		IJ.open(srcDir + srcImage);
		ImagePlus src = IJ.getImage();
		IJ.run(pluginName);
		ImagePlus out = IJ.getImage();
		IJ.open(refDir + refImage);
		ImagePlus ref = IJ.getImage();

		if (compare(ref.getProcessor(), out.getProcessor()) && 
		    out.getTitle().equals(String.format("My histogram of %s Underexposure: %b Overexposure: %b", src.getShortTitle(), uexp, oexp)))
		{
			IJ.log("Test passed!");
			
		}
		else
		{
			IJ.log("Test failed!");
			++failedTests;
		}

		src.changes = false;
		src.close();
		out.changes = false;
		out.close();
		ref.changes = false;
		ref.close();
		IJ.log("=============================================");
	}

	private boolean compare(ImageProcessor ref, ImageProcessor out)
	{	
		if (ref.getWidth() != out.getWidth() || ref.getHeight() != out.getHeight())
		{
			IJ.log("Error: Inconsistent image size between the reference and tested images!");
			return false;
		}
		
		int num = ref.getPixelCount();

		for (int i = 0; i < num; ++i)
		{
			if (ref.get(i) != out.get(i))
			{
				return false;  		
			}
		}
		
		return true;		
	}

}
