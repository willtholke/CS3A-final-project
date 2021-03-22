# CS3A-final-project
#### **Name:** William Tholke
#### **Date:** 03/21/2021
#### **Course:** CS3A w/ Professor Reed

## Overview
This project displays airbnb data from a .csv file in a way that allows user to interact with said data.

## Updates
This program has been modified since its last version such that the new global string object called 'filename' (which refers to the new airbnb data source, 'AB_NYC_2019.csv') is utilized in load_file(), the new method in the DataSet class that loads data from filename.
### Error Notes:
Added InvalidDataLength class to the DataSet class (lines 96, 97) as a logical error to be raised (lines 178-180) if the length of the file referred to by 'filename' is not 48895.
### Other Notes: 
Set global variable line_count equal to len(self.data) to avoid "Expected type 'Sized', got 'None' instead" error that occurred when attempting to print len(self.data) on line 477. The value of line_count is manipulated twice in the program, which does not affect the output in any unintended way.
