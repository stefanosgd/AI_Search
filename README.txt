Overview

There is a Python file entitled "validtourcheck.py". The code in this file takes a batch of tours and matches them against a batch of city-files and checks whether the tours are indeed tours and of the lengths claimed. 

Usage

1. Create a folder, of any name but let's call it "main", and in it place the file "validtourcheck.py".

2. In the folder "main", place a folder called "cityfiles" within which there is a collection of city-files, such as the 10 city-files supplied as part of the assignment. These city-files should all be of the format as directed in the assignment (this will be checked by the program) but there can be any number of them and they can have any names (they should all be text files with the suffix ".txt").

3. In the folder "main", place a folder, of any name but let's call it "dcs0ias", within which there are folders called "TourfileA" and "TourfileB". You don't need to include all these folders in "dcs0ias" as the program will spot that some might be missing and tell you (it will check the tours supplied in any of the folders that are present, though). You may include other files and folders in "dcs0ias" as they will be ignored.

4. In "TourfileA", for example, you should include tours, in the format as specified in the assignment, corresponding to some or all of the city-files in the folder "cityfiles" (the program will spot if some of the tour-files corresponding to city-files in "cityfiles" are missing and tell you).

5. Run the program "validtourcheck.py" (double click it). It will tell you if your tour-files are badly formatted and give you appropriate diagnostic messages. If your tour-files are correctly formatted then it will tell you if your tours are legitmate tours and if the lengths you have claimed match the actual lengths of the tours. All of this data will appear in the file "trace.txt" which will appear in the folder "main" after execution has stopped. Another file, "outputfile.txt", may also appear in "main". This file contains data for importing into an Excel spreadsheet and should be ignored.
