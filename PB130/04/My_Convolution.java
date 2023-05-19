package PB130;

import ij.IJ;
import ij.plugin.PlugIn;
import java.util.Arrays;

/** A two-dimensional matrix representation with the interface similar to the "ij.process.ImageProcessor" class. */
class MyMatrix
{
	/** A two-dimensional array storing the matrix values. */	
	int[][] m_array;

	/** Constructor. */		
	public MyMatrix(int[][] array)
	{
		m_array = array;
	}	

	/** Constructor. The matrix is initialized with zeros. */
	public MyMatrix(int width, int height)
	{
		m_array = new int[height][width];
	}	

	/** Get the width of the matrix. */
	public int getWidth()
	{
		return m_array[0].length;
	}	

	/** Get the height of the matrix. */
	public int getHeight()
	{
		return m_array.length;
	}

	/** Get the value at the x-th column and y-th row. If the given position is outside the matrix domain, return 0. */
	public int getElement(int x, int y)
	{
		// check whether the given position is outside the matrix domain or not
		if (x >= 0 && x < getWidth() && y >= 0 && y < getHeight())
		{
			return m_array[y][x];
		}
		else
		{
			return 0;
		}
	}

	/** Set the value at the x-th column and y-th row to the given value. If the given position is outside the matrix domain, do nothing. */
	public void setElement(int x, int y, int value)
	{
		// check whether the given position is outside the matrix domain or not
		if (x >= 0 && x < getWidth() && y >= 0 && y < getHeight())
		{
			m_array[y][x] = value;
		}
	}

	/** Check the content equality to a given two-dimensional array that stores the matrix values. */
	public boolean equalContent(int[][] array)
	{
		return Arrays.deepEquals(m_array, array);
	}

	/** Convert the matrix content to a string representation. */
	public String print()
	{
		String str = "";
		int w = getWidth();
		int h = getHeight();

		for (int y = 0; y < h; ++y)
		{
			str += "\n";

			for (int x = 0; x < w; ++x)
			{
				str += String.format("%5d ", m_array[y][x]);
			}
		}

		return str;
	}
}

/** This plugin convolves two integer matrices with zero boundary conditions. */
public class My_Convolution implements PlugIn
{	
	public void run(String arg) 
	{	
		// input matrix
		int[][] matArray = { {-2, 0, 1}, {0, 4, 3}, {2, 1, -1} }; 
		MyMatrix matrix = new MyMatrix(matArray);

		// convolution kernel
		int[][] kerArray = { {-1, 0, 1}, {0, 3, 2} };
		MyMatrix kernel = new MyMatrix(kerArray);

		// convolve the input matrix with the convolution kernel
		MyMatrix result = doConvolution(matrix, kernel);
		
		// the reference output matrix to compare with
		int[][] refArray = { {2, 0, -3, 0, 1}, {0, -10, -7, 7, 5}, {-2, -1, 15, 18, 5}, {0, 6, 7, -1, -2} };
		
		// display the result and check its equality to the reference output matrix
		IJ.showMessage("Correct result: " + result.equalContent(refArray),
			       "Matrix:" + matrix.print() +  "\n \nKernel:" + kernel.print() + "\n \nResult:" + result.print());
	}

	private MyMatrix doConvolution(MyMatrix matrix, MyMatrix kernel)
	{
		// size of the input matrix
		int matW = matrix.getWidth();
		int matH = matrix.getHeight();

		// size of the convolution kernel
		int kerW = kernel.getWidth();
		int kerH = kernel.getHeight();

		// size of the result
		int resW = matW + kerW - 1;
		int resH = matH + kerH - 1;

		// create the output matrix filled with zeros by default
		MyMatrix result = new MyMatrix(resW, resH);
				
		// convolve the input matrix with the convolution kernel
		// to obtain a value from or modify a value in a matrix 'm', call m.getElement(x, y) or m.setElement(x, y, value), respectively
		// WRITE YOUR CODE HERE


		for(int my = 0; my < resH; ++my){
			for (int mx = 0; mx < resW; ++mx){

				int sum = 0;

				for (int ky = 0; ky < kerH; ++ky){
					for (int kx = 0; kx < kerW; ++kx){

						int ker = kernel.getElement(kx, ky);
						int mat = matrix.getElement(mx - kx, my - ky);
						sum += mat * ker;
						
					}
				}

				result.setElement(mx, my, sum);

			}
			
		}

		//IJ.showMessage("NOT IMPLEMENTED!");

		return result;
	}
	
}
