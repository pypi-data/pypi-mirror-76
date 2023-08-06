import cv2
import pandas

class drawex():
	
	def __init__(self):
		return

	
	def exceldraw(self,image):
	
		"""Function to calculate the mean of the data set.
		
		Args: 
			image is the only argument
			for example: if the image is at location, path= 'C:\Users\admin\Downloads\rf.jpg'
			you can pass exceldraw(path)
		Returns: 
			2 dataframes
			It works like this:
			do, dd =  exceldraw(path)
			do.to_csv('C:\Users\admin\Downloads\file12.csv') 
    			dd.to_csv('C:\Users\admin\Downloads\file22.csv')
	
		"""
					
    		img = cv2.imread(image)
    		grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    		(thresh, bw) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
    		bwo = cv2.resize(bw,(128,512))
    		do = pandas.DataFrame(np.zeros((bwo.shape[0], bwo.shape[1])))
    		dd = pandas.DataFrame(np.ones((bwo.shape[0], bwo.shape[1])))
    		for i in range(bwo.shape[0]):
        		for j in range(bwo.shape[1]):
            		if bwo[i][j]==255:
                		do.at[i,j] = 1
                		dd.at[i,j] = 0
	    	return do,dd
