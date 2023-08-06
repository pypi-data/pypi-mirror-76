Pyrmvtxt is created to remove the text in the large scale image with the user friendly method

Requirement
----------------
- library keras-ocr (require gpu processing)
- library pandas 

Background process
-------------------------
1.Split image into smaller part 
2.Using keras-ocr as the main function to do text detection
3.Locate the bounding box position
4.Convert bounding box scale into the original size
5.Remove the text in that area 
5.Get the Clean image  

Written by TASUN