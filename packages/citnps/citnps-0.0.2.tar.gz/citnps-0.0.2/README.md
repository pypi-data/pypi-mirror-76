----------------------------------------------------------
CITNPS stands for "Camera Is The New Piezoelectric Sensor"
----------------------------------------------------------

It is a simple toolbox designed to extract the movement of the body-parts of an head-fixed animal 
from one or multiple movies. 

Each body-part is defined by an area (for now a rectangular one), we then apply one or two threshold on the image, and 
extract a signal composed of the difference of each pixel intensity between two consecutive frames, the bigger 
the movement the bigger the amplitude of the movement. The signal is then normalized using a z-score. 
The signal is then similar to the one that would be obtained with a Piezoelectric sensor. 

There are options to normalize/filter the signal extracted depending on the luminosity state and 
some potential oscillatory noise such as produced by the laser while recording 2photons calcium-imaging. 

------------
Installation
------------

To install or update CITNPS distribution from PyPI simply run:

    pip install -U citnps
   
Some requirements are necessary and can be found in the requirements.txt. To install them:

    pip install -r requirements.txt

---------------
To open the GUI
---------------

You will need to write a Python script to call the main function to launch the GUI.

You need to import run_citnps:

    from citnps.citnps_main_window import run_citnps

Run_citnps() takes the following arguments:

* **movies_dict**: (dict), each key is a str representing the id of a movie, and the value is the file_path of the
  movie (avi or mp4 format for now)

* **bodyparts_dict**:  (dict), key is a string, should be the same keys as movies_dict, value is a list
  of string representing the name of the body-parts to extract from this movie. All body-parts should have unique names,
  even if not from the same movie.

* **from_cicada**: (bool), should be put to False. It would be put as True if CITNPS is launch from the CICADA toolbox (not
  available yet).

* **data_id**: (str) identifier of the session, will be put on the name of the files saved

* **behavior_time_stamps_dict**: (dict) with key the movie_id, and value a 1d np.array of length the number
  of frames in the movie, each value (float) representing the timestamps of the frame

* **luminosity_change_dict**: (dict) indicate when there is a change in luminosity (laser on/off for example)
  (epochs in frames). Each key is the id of a movie, 1d array of len n_transitions, each value (int) represent a
  frame when the luminosity transition happens. Allows to normalize the signal according to luminosity.

* **movie_queue_size**: (int) size of the buffer to read the frames of the movie, depends on your computer memory.
  You can set it at 2000.

* **results_path**: (str) if None, the user will be able to select the path where to save the data from the GUI.
  Otherwise indicate in which directory to save the results. A directory with the timestamps of the time of the analysis
  will be created results_path.

* **yaml_config_file**: (str) if not None, used to load the body-parts config/parameters such as the ROI coordinates,
  the image thresholds and the threshold for the "piezo" signal. The file is the yaml file produce by the toolbox on
  a previous analysis.


----------
GUI manual
----------
**Main window with the left hindlimb selected**: 

![alt text](images/citnps_main_window_hindlimb_left_with_labels.png "Main window, left hindlimb")

**Signal window for the left hindlimb**:

![alt text](images/citnps_signal_window_hindlimb_left_with_labels.png "Signal window, left hindlimb")

**Main window with the right forelimb selected and image threshold mode activated**: 

![alt text](images/citnps_main_window_threshold_forelimb_right.png "Main window, right forelimb")

**Signal window for the right forelimb**:

![alt text](images/citnps_signal_window_forelimb_right.png "Signal window, right forelimb")


**Main window description**:
 
That's the first window to be opened. Here is the description of its content using 
the red annotation on the first image as a landmark. 

1. **Image widget**:  displays the current frame to the selected body-part. 
 It is possible to zoom using the mouse wheel and to move the image using the left mouse click. 
 
2. **Body-part ROI** (Region Of Interest): Delimits the contours of the area used to produce the "piezo" signal. 
 Left click on its surface to move it.
 The two white diamonds can be used to change the dimension (left click). Make sure the area covers most of the 
 body-part positions. Note that it is preferable to have the smallest area as possible especially if there is a high 
 noise level.  

3. **Body-parts combobox**: select the body-part to display and change the parameters accordingly. 
 
4. **Frame slider**: allows the selection of the frame to be displayed. It is also possible to use the spinbox on the 
 right. Note the keyboard shortcut "p" (plus) and "m" (minus) allows to display the next and previous frame accordingly. 
 
5. **Random frame button**: select a frame randomly. "r" keyboard shortcut also available. 

6. **Previous frame button**: display the last displayed  frame ("p" shortcut)

7. **Image threshold mode**: if the checkbox is selected, the image will be displayed on threshold mode 
 (see 2nd main window screenshot for an example), the "t" shortcut also activate/deactivate this mode. This mode doesn't
 change the output, it is just for display purpose. In both case, the thresholds will be applied to the image for 
 extracting the signal. 
 **threshold values**: use the text field to put one or two integer values (separate with comma) and click on update 
 to update the values.
 
8. **Low pass filter cutoff**: if checkbox activated, a low pass filter will be applied to the signal. The cutoff is 
 indicated in the spinbox, the value is multiplied by 10, so if 15 is displayed, 1.5 will be the real cutoff. 
 
9. **Piezo signal threshold**: Threshold applied to decide if a movement happens. 
 The value is set through the signal window.

10. **Display signal button**: open the window that displays the signal (piezo and power spectrum). You can open 
 multiple window. The parameters used to process the signal will the one currently display on the main window. 

11. **Save config**: save the current configuration (ROI coordinates, image thresholds and piezo threshold) 
 on a yaml file. A dialog will be opened to select the directory where to save it if not already given in the code. 
 The configuration file will be also saved when processing the movie. 

12. **Process button**: process the movies and extract the body-part signal, produces the output files. 
 The GUI is not usable during the whole process.  

13. **Progress bar**: indicates the progress of the processing as well as the time remaining. 

**Signal window**

This window is used to have a preview of the signal on some frames of the movie, so you can set up the parameters to 
optimize the results. 

1. **Piezo signal widget**: Display the signal representing the movement of the body-part. The x-axis represents 
 the frame indices, y-axis is a z-score normalization (0 represents the mean, 1 the std). 

2. **Raw signal**: The blue signal is the raw signal without filtering with just a z-score normalization applied. 

3. **Filtered signal**: The red signal is the filtered one, for which we applied a low-pass filter if the option was 
  selected. 
 
4. **Luminosity change marker**: The vertical white lines represent the frame at which there is a change in luminosity. 

5. **Current frame marker**: The vertical yellow line (red when hover with the mouse) represents the current frame 
 displayed in the main window. If the line is not visible, you can change the frame displayed in the main window to make 
 it appears (in the range processed). The line is movable, left click on it to move it, the frame displayed will also 
 change if the movie on the main window contains the body-part analysed. 

6. **Power spectrum widget**: display the power spectrum, blue is the original signal, red is the filtered one. 
 The x-axis represents the frequencies, the y-axis the powers. 

7. **Low pass cutoff**: the white vertical line represents the cutoff value. 

8. **Luminosity change frames**: combobox allowing to know the frames at which a change of luminosity happens. 

9. **First frame**: Indicate the first frame index of the interval to processed. 

10. **Last frame**: Indicate the last frame index of the interval to processed. On the right is the index 
 of the last frame of the movie.  

11. **Display signal button**: click on it to process the signal on the frame interval indicated. 
 During the processing, you can't use the GUI and have to wait for it to end. You can press again on process again after
 it is finished, if some parameters on the main window or the signal window have been changed, 
 it will be taken in consideration.
 
12. **Image thresholds**: appears after the processing, indicate which values were used to get this signal. 

13. **Low pass filter with cutoff**: appears after the processing, indicate which values were used to get this signal. 

14. **Progress bar**: indicate the progress of the processing. 

15. **Piezo signal threshold**: the light blue horizontal line represents the threshold you consider the best to apply 
 for binarizing the signal, with movement of the body-part considered on top of the threshold. The threshold will just be 
 saved on the yaml configuration file, and you will be able to use it later on to work on the extracted signal. 

You can open multiple signal windows (running the signal processing only one at a time), they will be synchronized with 
the main window and between themselves if some elements are changing 
(such as the frame displayed, the piezo threshold)


**Running time**

It takes around 25 min to process 2 movies of 40000 frames and resolution of 1920*1200 with 3 bodyparts each. 

 
**Processing outputs**

Two kind of files will be created:

* **Yaml configuration file** with the parameters set for each body-part (ROI, image and piezo thresholds)

* **signal files**: one .npz file for each body-part signal containing the filtered signal. 
 Each npz contains two 1d array. The first one's key is the body-part name and the value represent the filtered signal. 
 The second's key is "timestamps" and is the same length as the first one and contains the timestamps of each frame 
 from which the signal is extracted. 
 

--------
Contacts
--------

Main developer : Julien Denis (julien.denis3[at]gmail.com)

-------
LICENSE
-------

Copyright (c) 2019 Cossart lab

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
