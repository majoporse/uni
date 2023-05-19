package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.PlugIn;
import ij.process.ImageProcessor;

/** This plugin automatically validates the plugins within Exercise 03. */
public class UnitTests_03 implements PlugIn 
{	
	int failedTests = 0;
	String plugDir = IJ.getDirectory("plugins") + "PB130/";
	String srcDir = plugDir + "images/";
	String refDir = plugDir + "refs/";

	public void run(String arg) 
	{
		IJ.open(srcDir + "chessboard.tif");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_Inversion.java");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_IncreaseBrightness.java");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_IncreaseContrast.java");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_LinearStretch.java");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_GammaCorrection.java");
		IJ.wait(500);
		IJ.run("Close All");
		IJ.run("Refresh Menus");
		IJ.log("\\Clear");
		IJ.log("Please wait, running all pre-defined tests...");
		IJ.log("Source image directory: " + srcDir);
		IJ.log("Reference image directory: " + refDir);
		IJ.log("=============================================");
		testPlugin("My Inversion", "", "const.tif", "const_inversion.tif");
		testPlugin("My Inversion", "", "chessboard.tif", "chessboard_inversion.tif");
		testPlugin("My Inversion", "", "tree_rings.tif", "tree_rings_inversion.tif");
		testPlugin("My IncreaseBrightness", "", "const.tif", "const_brightness.tif");
		testPlugin("My IncreaseBrightness", "", "chessboard.tif", "chessboard_brightness.tif");
		testPlugin("My IncreaseBrightness", "", "tree_rings.tif", "tree_rings_brightness.tif");
		testPlugin("My IncreaseContrast", "", "const.tif", "const_contrast.tif");
		testPlugin("My IncreaseContrast", "", "chessboard.tif", "chessboard_contrast.tif");
		testPlugin("My IncreaseContrast", "", "tree_rings.tif", "tree_rings_contrast.tif");
		testPlugin("My LinearStretch", "", "const.tif", "const_linstretch.tif");
		testPlugin("My LinearStretch", "", "chessboard.tif", "chessboard_linstretch.tif");
		testPlugin("My LinearStretch", "", "tree_rings.tif", "tree_rings_linstretch.tif");
		testPlugin("My GammaCorrection", "gamma=2.20", "const.tif", "const_gamma220.tif");
		testPlugin("My GammaCorrection", "gamma=0.45", "const.tif", "const_gamma045.tif");
		testPlugin("My GammaCorrection", "gamma=2.20", "chessboard.tif", "chessboard_gamma220.tif");
		testPlugin("My GammaCorrection", "gamma=0.45", "chessboard.tif", "chessboard_gamma045.tif");
		testPlugin("My GammaCorrection", "gamma=2.20", "tree_rings.tif", "tree_rings_gamma220.tif");
		testPlugin("My GammaCorrection", "gamma=0.45", "tree_rings.tif", "tree_rings_gamma045.tif");

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
		ImagePlus out = IJ.getImage();
		IJ.run(pluginName, pluginParams);
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
