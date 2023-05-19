package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.PlugIn;
import ij.process.ImageProcessor;
import ij.process.FloatProcessor;

/** This plugin automatically validates the plugins within Exercise 05. */
public class UnitTests_05 implements PlugIn 
{	
	int failedTests = 0;
	String plugDir = IJ.getDirectory("plugins") + "PB130/";
	String srcDir = plugDir + "images/";
	String refDir = plugDir + "refs/";

	public void run(String arg) 
	{
		IJ.open(srcDir + "chessboard.tif");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_GradientX.java");
		IJ.wait(500);
		IJ.selectWindow("chessboard.tif");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_GradientY.java");
		IJ.wait(500);
		IJ.selectWindow("chessboard.tif");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_GradientMagnitude.java");
		IJ.wait(500);
		IJ.selectWindow("chessboard.tif");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_GradientOrientation.java");
		IJ.wait(500);
		IJ.selectWindow("chessboard.tif");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_LaplacianZeroCrossing.java");
		IJ.wait(500);
		IJ.run("Close All");
		IJ.run("Refresh Menus");
		IJ.log("\\Clear");
		IJ.log("Please wait, running all pre-defined tests...");
		IJ.log("Source image directory: " + srcDir);
		IJ.log("Reference image directory: " + refDir);
		IJ.log("=============================================");
		testPlugin("My GradientX", "xx.tif", "xx_gradx.tif");
		testPlugin("My GradientX", "yy.tif", "yy_gradx.tif");
		testPlugin("My GradientX", "ramp.tif", "ramp_gradx.tif");
		testPlugin("My GradientX", "chessboard.tif", "chessboard_gradx.tif");
		testPlugin("My GradientX", "nuts_bolts.tif", "nuts_bolts_gradx.tif");
		testPlugin("My GradientX", "orka.tif", "orka_gradx.tif");
		testPlugin("My GradientX", "taxi.tif", "taxi_gradx.tif");
		testPlugin("My GradientY", "xx.tif", "xx_grady.tif");
		testPlugin("My GradientY", "yy.tif", "yy_grady.tif");
		testPlugin("My GradientY", "ramp.tif", "ramp_grady.tif");
		testPlugin("My GradientY", "chessboard.tif", "chessboard_grady.tif");
		testPlugin("My GradientY", "nuts_bolts.tif", "nuts_bolts_grady.tif");
		testPlugin("My GradientY", "orka.tif", "orka_grady.tif");
		testPlugin("My GradientY", "taxi.tif", "taxi_grady.tif");
		testPlugin("My GradientMagnitude", "xx.tif", "xx_gradmag.tif");
		testPlugin("My GradientMagnitude", "yy.tif", "yy_gradmag.tif");
		testPlugin("My GradientMagnitude", "ramp.tif", "ramp_gradmag.tif");
		testPlugin("My GradientMagnitude", "chessboard.tif", "chessboard_gradmag.tif");
		testPlugin("My GradientMagnitude", "nuts_bolts.tif", "nuts_bolts_gradmag.tif");
		testPlugin("My GradientMagnitude", "orka.tif", "orka_gradmag.tif");
		testPlugin("My GradientMagnitude", "taxi.tif", "taxi_gradmag.tif");
		testPlugin("My GradientOrientation", "xx.tif", "xx_gradorient.tif");
		testPlugin("My GradientOrientation", "yy.tif", "yy_gradorient.tif");
		testPlugin("My GradientOrientation", "ramp.tif", "ramp_gradorient.tif");
		testPlugin("My GradientOrientation", "chessboard.tif", "chessboard_gradorient.tif");
		testPlugin("My GradientOrientation", "nuts_bolts.tif", "nuts_bolts_gradorient.tif");
		testPlugin("My GradientOrientation", "orka.tif", "orka_gradorient.tif");
		testPlugin("My GradientOrientation", "taxi.tif", "taxi_gradorient.tif");
		testPluginWithTwoOutputs("My LaplacianZeroCrossing", "sigma=0.0", "chessboard.tif", "chessboard_laplacianzc0.tif", "chessboard_laplacian0.tif");
		testPluginWithTwoOutputs("My LaplacianZeroCrossing", "sigma=0.0", "nuts_bolts.tif", "nuts_bolts_laplacianzc0.tif", "nuts_bolts_laplacian0.tif");
		testPluginWithTwoOutputs("My LaplacianZeroCrossing", "sigma=0.0", "orka.tif", "orka_laplacianzc0.tif", "orka_laplacian0.tif");
		testPluginWithTwoOutputs("My LaplacianZeroCrossing", "sigma=3.0", "orka.tif", "orka_laplacianzc3.tif", "orka_laplacian3.tif");
		testPluginWithTwoOutputs("My LaplacianZeroCrossing", "sigma=3.0", "taxi.tif", "taxi_laplacianzc3.tif", "taxi_laplacian3.tif");

		if (failedTests > 0)
		{
			IJ.log("Total number of tests failed: " + failedTests);
		}
		else
		{
			IJ.log("CONGRATULATIONS! ALL TESTS PASSED.");
		}

		IJ.run("Close All");		
	}

	private void testPlugin(String pluginName, String srcImage, String refImage)
	{
		IJ.log("Plugin name: " + pluginName);
		IJ.log("Source image: " + srcImage);
		IJ.log("Reference image: " + refImage);
		IJ.open(srcDir + srcImage);
		ImagePlus src = IJ.getImage();
		IJ.run(pluginName);
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

	private void testPluginWithTwoOutputs(String pluginName, String pluginParams, String srcImage, String primRefImage, String secRefImage)
	{
		IJ.log("Plugin name: " + pluginName);
		IJ.log("Source image: " + srcImage);
		IJ.log("Primary reference image: " + primRefImage);
		IJ.log("Secondary reference image: " + secRefImage);
		IJ.open(srcDir + srcImage);
		ImagePlus src = IJ.getImage();
		IJ.run(pluginName, pluginParams);
		ImagePlus primOut = IJ.getImage();
		IJ.selectWindow("My Laplacian of " + src.getShortTitle());
		ImagePlus secOut = IJ.getImage();
		IJ.open(refDir + primRefImage);
		ImagePlus primRef = IJ.getImage();
		IJ.open(refDir + secRefImage);
		ImagePlus secRef = IJ.getImage();

		if (compare(secRef.getProcessor(), secOut.getProcessor()))
		{
			int count = countSubstantialDifferences(primRef.getProcessor(), primOut.getProcessor());
			IJ.log("Number of differences in the primary output: " + count);
			
			if (count <= 10)
			{
				IJ.log("Test passed!");
			}
			else
			{
				IJ.log("Test failed on the primary output image!");
				++failedTests;
			}
		}
		else
		{
			IJ.log("Test failed on the secondary output image!");
			++failedTests;
		}
		

		src.changes = false;
		src.close();
		primOut.changes = false;
		primOut.close();
		secOut.changes = false;
		secOut.close();
		primRef.changes = false;
		primRef.close();
		secRef.changes = false;
		secRef.close();
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
			if (Math.abs(ref.getf(i) - out.getf(i)) > 0.001f)
			{
				return false;  		
			}
		}
		
		return true;		
	}

	private int countSubstantialDifferences(ImageProcessor ref, ImageProcessor out)
	{	
		if (ref.getWidth() != out.getWidth() || ref.getHeight() != out.getHeight())
		{
			IJ.log("Error: Inconsistent image size between the reference and tested images!");
			return ref.getPixelCount();
		}

		int count = 0;		
		int num = ref.getPixelCount();

		for (int i = 0; i < num; ++i)
		{
			if (Math.abs(ref.getf(i) - out.getf(i)) > 0.001f)
			{
				++count;
			}
		}
		
		return count;		
	}

}
