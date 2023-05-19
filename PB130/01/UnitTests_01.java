package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.PlugIn;
import ij.process.ImageProcessor;

/** This plugin automatically validates the plugins within Exercise 01. */
public class UnitTests_01 implements PlugIn 
{	
	int failedTests = 0;
	String plugDir = IJ.getDirectory("plugins") + "PB130/";
	String srcDir = plugDir + "images/";
	String refDir = plugDir + "refs/";

	public void run(String arg) 
	{
		IJ.open(srcDir + "leaf.jpg");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_FlipX.java");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_FlipY.java");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_FlipXY.java");
		IJ.wait(500);
		IJ.run("Close All");
		IJ.run("Refresh Menus");
		IJ.log("\\Clear");
		IJ.log("Please wait, running all pre-defined tests...");
		IJ.log("Source image directory: " + srcDir);
		IJ.log("Reference image directory: " + refDir);
		IJ.log("=============================================");
		testPlugin("My FlipX", "tree_rings.tif", "tree_rings_flipx.tif");
		testPlugin("My FlipX", "noisy_chessboard.tif", "noisy_chessboard_flipx.tif");
		testPlugin("My FlipX", "leaf.jpg", "leaf_flipx.tif");
		testPlugin("My FlipX", "rotated_leaf.jpg", "rotated_leaf_flipx.tif");
		testPlugin("My FlipY", "tree_rings.tif", "tree_rings_flipy.tif");
		testPlugin("My FlipY", "noisy_chessboard.tif", "noisy_chessboard_flipy.tif");
		testPlugin("My FlipY", "leaf.jpg", "leaf_flipy.tif");
		testPlugin("My FlipY", "rotated_leaf.jpg", "rotated_leaf_flipy.tif");
		testPlugin("My FlipXY", "tree_rings.tif", "tree_rings_flipxy.tif");
		testPlugin("My FlipXY", "noisy_chessboard.tif", "noisy_chessboard_flipxy.tif");
		testPlugin("My FlipXY", "leaf.jpg", "leaf_flipxy.tif");
		testPlugin("My FlipXY", "rotated_leaf.jpg", "rotated_leaf_flipxy.tif");

		if (failedTests > 0)
		{
			IJ.log("Total number of tests failed: " + failedTests);
		}
		else
		{
			IJ.log("CONGRATULATIONS! ALL TESTS PASSED.");
		}		
	}

	private void testPlugin(String pluginName, String srcImage, String refImage)
	{
		IJ.log("Plugin name: " + pluginName);
		IJ.log("Source image: " + srcImage);
		IJ.log("Reference image: " + refImage);
		IJ.open(srcDir + srcImage);
		ImagePlus out = IJ.getImage();
		IJ.run(pluginName);
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
