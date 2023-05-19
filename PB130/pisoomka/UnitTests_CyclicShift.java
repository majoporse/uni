package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.PlugIn;
import ij.process.ImageProcessor;

/** This plugin automatically validates all plugins within Exercise 01. */
public class UnitTests_CyclicShift implements PlugIn 
{	
	int failedTests = 0;
	String plugDir = IJ.getDirectory("plugins") + "PB130/";
	String srcDir = plugDir + "images/";
	String refDir = plugDir + "refs/";	

	public void run(String arg) 
	{
		IJ.open(srcDir + "chessboard.tif");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_CyclicShift.java");
		IJ.wait(500);
		IJ.run("Close All");
		IJ.run("Refresh Menus");
		IJ.log("\\Clear");
		IJ.log("Please wait, running all pre-defined tests...");
		IJ.log("Source image directory: " + srcDir);
		IJ.log("Reference image directory: " + refDir);
		IJ.log("=============================================");
		testPlugin("My CyclicShift", "row=50 column=-50", "chessboard.tif", "chessboard_r50_c-50.tif");
		testPlugin("My CyclicShift", "row=10 column=500", "chessboard.tif", "chessboard_r10_c500.tif");
		testPlugin("My CyclicShift", "row=-500 column=42", "chessboard.tif", "chessboard_r-500_c42.tif");
		testPlugin("My CyclicShift", "row=-100 column=-100", "chessboard.tif", "chessboard_r-100_c-100.tif");
		testPlugin("My CyclicShift", "row=13 column=-27", "leaf.jpg", "leaf_r13_c-27.tif");
		testPlugin("My CyclicShift", "row=83 column=800", "leaf.jpg", "leaf_r83_c800.tif");
		testPlugin("My CyclicShift", "row=-900 column=71", "leaf.jpg", "leaf_r-900_c71.tif");
		testPlugin("My CyclicShift", "row=-75 column=-84", "leaf.jpg", "leaf_r-75_c-84.tif");

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
