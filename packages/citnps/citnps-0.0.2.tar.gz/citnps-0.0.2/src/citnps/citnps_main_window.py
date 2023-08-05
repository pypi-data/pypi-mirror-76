from qtpy.QtWidgets import *
from qtpy import QtGui
from qtpy import QtCore
from qtpy.QtCore import Qt
import os
import sys
import cv2
import numpy as np
from functools import partial
import yaml

import platform
from sortedcontainers import SortedDict
from random import randrange

import ctypes

import pyqtgraph as pg

from citnps.utils.video.video_reader import OpenCvVideoReader
from citnps.display_signal_main_window import DisplaySignalMainWindow
from citnps.citnps_progress_bar import RemainingTime, ProgressBar
from citnps.utils.signal import process_piezo_signal, from_camera_to_piezo_signal

from datetime import datetime


def do_image_thresholding(img_frame, image_thresholds):
    """

    Args:
        img_frame:
        image_thresholds: list of 1 to 2 int, between 0 and 255, in ascending order, representing the different
            level of gray

    Returns:

    """
    # into grey_scale
    img_frame = cv2.cvtColor(img_frame, cv2.COLOR_BGR2GRAY)

    # plt.imshow(img_frame, 'gray')
    # plt.show()

    # img_frame = img_frame.astype(np.uint8)
    img_frame = ((img_frame / img_frame.max(axis=0).max(axis=0)) * 255).astype(np.uint8)

    # bluring the image a bit
    img_frame = cv2.medianBlur(img_frame, 5)

    # Applying Histogram Equalization
    # img_frame = cv2.equalizeHist(img_frame)

    if len(image_thresholds) == 1:
        # used to be 75
        ret, th1 = cv2.threshold(img_frame, image_thresholds[0], 255, cv2.THRESH_BINARY)
    else:
        if len(image_thresholds) != 2:
            raise Exception("Only 1 or 2 image_thresholds are supported yet")
        # used to be [65, 150]
        th1 = np.zeros_like(img_frame)
        th1[img_frame < image_thresholds[0]] = 0
        th1[np.logical_and(img_frame >= image_thresholds[0], img_frame < image_thresholds[1])] = 127
        th1[img_frame >= image_thresholds[1]] = 255
    # print(f"np.unique(th1) {np.unique(th1)}")
    # Otsu's thresholding
    # ret2, th1 = cv2.threshold(img_frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    th1 = np.array(th1).astype(float)
    # th3 = cv2.adaptiveThreshold(img_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                             cv2.THRESH_BINARY, 11, 2)

    """
                th2 = cv2.adaptiveThreshold(img_frame, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                            cv2.THRESH_BINARY, 11, 2)
                th3 = cv2.adaptiveThreshold(img_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY, 11, 2)

                titles = ['Original Image', 'Global Thresholding (v = 127)',
                          'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
                images = [img_frame, th1, th2, th3]

                for i in range(4):
                    plt.subplot(2, 2, i + 1), plt.imshow(images[i], 'gray')
                    plt.title(titles[i])
                    plt.xticks([]), plt.yticks([])
                plt.show()
    """

    return th1


def run_citnps(movies_dict, bodyparts_dict, from_cicada, data_id,
               behavior_time_stamps_dict,
               luminosity_change_dict=None, movie_queue_size=2000,
               results_path=None,
               yaml_config_file=None):
    """

    :param movies_dict:
    :param bodyparts_dict:
    :param from_cicada:
    :param data_id:
    :param behavior_time_stamps_dict: dict with key the movie_id, and value a 1d np.array of length the number
                    of frames in the movie, each value (float) representing the timestamps of the frame
    :param luminosity_change_dict (dict): indicate when their is a change in luminosity (laser on/off)
    (epochs in frames). Each key is the id of a movie, 1d array of len n_transitions, each value (int) represent a
    frame when the luminosity transition happens. Allows to normalize the signal according to luminosity.
    :param movie_queue_size:
    :param results_path: (str) if None, the use will be able to select the path where to save the data.
    Otherwise indicate in which directory to save the results. A directory with the timestamps of the time of the analysis
    will be created results_path.
    :param yaml_config_file: if not None, used to load the bodyparts config/parameters such as the ROI coordinates,
    the image thresholds and
    :return:
    """
    if not from_cicada:
        app = QApplication(sys.argv)

        my_path = os.path.abspath(os.path.dirname(__file__))

        # dark_style_style_sheet = qdarkstyle.load_stylesheet_from_environment(is_pyqtgraph=True)
        # from package qdarkstyle, modified css
        my_path = os.path.abspath(os.path.dirname(__file__))
        if platform.system() == "Windows":
            to_insert = os.path.join(my_path, "icons/")
            to_insert = to_insert.replace("\\", "/")
        else:
            to_insert = os.path.join(my_path, "icons/")

        file_name = os.path.join(my_path, "citnps_qdarkstyle.css")
        # with open(file_name, "w", encoding='UTF-8') as file:
        #     file.write(dark_style_style_sheet)
        with open(file_name, "r", encoding='UTF-8') as file:
            dark_style_cicada_style_sheet = file.read()

        dark_style_cicada_style_sheet = dark_style_cicada_style_sheet.replace("icons/", to_insert)
        app.setStyleSheet(dark_style_cicada_style_sheet)

    bodyparts_config = None
    if yaml_config_file is not None:
        if os.path.isfile(yaml_config_file):
            print(f"Loading config for  {data_id} from {os.path.basename(yaml_config_file)}")
            with open(yaml_config_file, 'r') as stream:
                bodyparts_config = yaml.load(stream, Loader=yaml.FullLoader)

    # cicada_first_window = CicadaMainWindow(config_handler=config_handler)
    first_window = CintpsMainWindow(data_id=data_id, movies_dict=movies_dict,
                                    bodyparts_dict=bodyparts_dict,
                                    bodyparts_config=bodyparts_config,
                                    behavior_time_stamps_dict=behavior_time_stamps_dict,
                                    luminosity_change_dict=luminosity_change_dict,
                                    movie_queue_size=movie_queue_size,
                                    results_path=results_path)

    # putting the window at the center of the screen
    # screenGeometry is an instance of Qrect
    screenGeometry = QApplication.desktop().screenGeometry()
    x = (screenGeometry.width() - first_window.width()) / 2
    y = (screenGeometry.height() - first_window.height()) / 2

    first_window.move(x, y)
    first_window.show()

    if not from_cicada:
        sys.exit(app.exec_())


class CintpsMainWindow(QMainWindow):
    """Main window of the GUI"""

    def __init__(self, data_id, movies_dict, bodyparts_dict, behavior_time_stamps_dict,
                 default_image_thresholds=(65, 150),
                 luminosity_change_dict=None,
                 bodyparts_config=None,
                 movie_queue_size=2000,
                 results_path=None):
        """

                Args:
                    data_id (str): identifier of the session
                    movies_dict (dict): key is a string identifying the movie (added to the extracted activity) and
                    the value if the file_name of the movie (avi or mp4 format for now)
                    bodyparts_dict (dict): key is a string, should be the same keys as movies_dict, value is a list
                    of string representing the name of the bodyparts to extract. All bodyparts should have unique names,
                    even if not from the same movie.
                    behavior_time_stamps_dict: dict with key the movie_id, and value a 1d np.array of length the number
                    of frames in the movie, each value (float) representing the timestamps of the frame
                    movie_queue_size (int): size of the buffer allowing to pre-loading in a different thred the frames
                    of the movie
                    :param luminosity_change_dict (dict): indicate when their is a change in luminosity (laser on/off)
                    (epochs in frames). Each key is the id of a movie, 1d array of len n_transitions, each value (int) represent a
                    frame when the luminosity transition happens. Allows to normalize the signal according to luminosity.
                    :param bodyparts_config : (dict or string) each key is a bodypart id (name) and the value is a dict, with
                    each key being a param and its value (image_thresholds (list of int) & roi_coords (x, y, width, height)).
                    bodyparts_config can also be string a representing a yaml file that will be loaded. The yaml file
                    represents a configuration saved from a past execution of citnps
                    :param results_path: (str) if None, the use will be able to select the path where to save the data
                """
        super().__init__()
        # To display an the window icon as the application icon in the task bar on Windows
        if platform.system() == "Windows":
            myappid = u'cossart.citnps.gui.alpha'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        # my_path = os.path.abspath(os.path.dirname(__file__))

        self.data_id = data_id

        self.behavior_time_stamps_dict = behavior_time_stamps_dict

        self.luminosity_change_dict = luminosity_change_dict if luminosity_change_dict is not None else dict()
        if luminosity_change_dict is None:
            for movie_id in movies_dict.keys():
                self.luminosity_change_dict[movie_id] = []

        if bodyparts_config is None:
            self.bodyparts_config = dict()
        elif isinstance(bodyparts_config, str):
            self.bodyparts_config = None
        elif isinstance(bodyparts_config, dict):
            self.bodyparts_config = bodyparts_config
        else:
            self.bodyparts_config = dict()

        if self.data_id is not None:
            self.setWindowTitle(f"CITNPS - {self.data_id}")
        else:
            self.setWindowTitle(f"CITNPS")

        screenGeometry = QApplication.desktop().screenGeometry()
        # making sure the window is not bigger than the dimension of the screen
        width_window = min(1500, screenGeometry.width())
        # width_window = screenGeometry.width()
        height_window = min(1000, screenGeometry.height())
        self.resize(width_window, height_window)
        self.results_path = results_path

        # self.load_data_from_config()
        self.movies_dict = movies_dict
        self.bodyparts_dict = bodyparts_dict
        self.movie_queue_size = movie_queue_size

        self.default_image_thresholds = list(default_image_thresholds)

        # threshold for the piezo signal
        self.default_piezo_threshold = 1

        self.central_widget = InitialCentralWidget(main_window=self)

        self.setCentralWidget(self.central_widget)

        self.show()


class ImageWidget(pg.GraphicsLayoutWidget):

    def __init__(self, main_window, central_widget, roi_coords_dict):
        pg.GraphicsLayoutWidget.__init__(self)

        self.main_window = main_window
        self.central_widget = central_widget
        self.roi_coords_dict = roi_coords_dict

        self.view_box = self.addViewBox(lockAspect=True, row=0, col=0, invertY=True)
        self.view_box.setMenuEnabled(False)

        # self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.image_displayed = pg.ImageItem(axisOrder='row-major', border='w')
        self.view_box.addItem(self.image_displayed)

        screenGeometry = QApplication.desktop().screenGeometry()
        # making sure the window is not bigger than the dimension of the screen
        width_window = min(1000, screenGeometry.width() // 2)
        # width_window = screenGeometry.width()
        height_window = min(700, screenGeometry.height() // 2)
        self.resize(width_window, height_window)

        self.current_image_data = None

        # use to know when display_image() is called, if a new bodypart is actually displayed
        # then we update the ROI position
        self.current_bodypart = None

        # Custom ROI for selecting an image region
        # lower-left corner (but invertY is True, so top-left) (x, y) & (with & height)
        roi_pen = pg.mkPen(color="#FF0000")  # width=
        if self.central_widget.current_bodypart in self.roi_coords_dict:
            x, y, width, height = self.roi_coords_dict[self.central_widget.current_bodypart]
        else:
            # TODO: put default values
            x, y, width, height = self.central_widget.default_roi_coords
        self.roi = pg.ROI([x, y], [width, height], pen=roi_pen)
        # self.roi.pos()
        self.roi.addScaleHandle([0.5, 1], [0.5, 0.5])
        self.roi.addScaleHandle([0, 0.5], [0.5, 0.5])
        # update saved coords
        self.roi.sigRegionChanged.connect(self.update_roi_coords)
        self.view_box.addItem(self.roi)
        self.roi.setZValue(10)  # make sure ROI is drawn above image

    def display_image(self, image_data):
        self.current_image_data = image_data

        if self.current_bodypart != self.central_widget.current_bodypart:
            if self.central_widget.current_bodypart in self.roi_coords_dict:
                x, y, width, height = self.roi_coords_dict[self.central_widget.current_bodypart]
            else:
                x, y, width, height = self.central_widget.default_roi_coords
            self.roi.setPos(x, y)
            self.roi.setSize((width, height))
        self.update_display()

    def update_roi_coords(self):
        x, y = self.roi.pos()
        width, height = self.roi.size()
        self.roi_coords_dict[self.central_widget.current_bodypart] = [int(x), int(y), int(width), int(height)]

    def update_display(self):
        if self.current_image_data is None:
            return

        self.current_bodypart = self.central_widget.current_bodypart

        if self.central_widget.threshold_image_mode:
            image_thresholded = do_image_thresholding(self.current_image_data,
                                                      image_thresholds=self.central_widget.get_current_image_thresholds())
            self.image_displayed.setImage(image_thresholded)
        else:
            self.image_displayed.setImage(self.current_image_data)


class NoWheelQComboBox(QComboBox):
    # deactivate the wheel action over a combo box, to avoid wrong manipulation
    def __init__(self, *args, **kwargs):
        super(NoWheelQComboBox, self).__init__(*args, **kwargs)

    def wheelEvent(self, *args, **kwargs):
        return


def display_msg_in_box(msg):
    message_box = QMessageBox()
    message_box.setText(msg)
    message_box.exec()


class InitialCentralWidget(QWidget):

    def __init__(self, main_window):
        super().__init__(parent=main_window)

        self.main_window = main_window

        self.main_layout = QVBoxLayout()

        # last frames displayed
        self.last_frames_dict = dict()

        self.threshold_image_mode = False

        # value of the low pass filter cutoff
        self.lowpass_filter_cutoff = 1.5

        # keep in memory the widget open, so we can display a bar in the signal showing which frame
        # is being display on the camera widget
        self.signal_display_widgets = []

        # video readers
        self.movie_readers = dict()
        self.current_frame_dict = dict()
        self.current_movie_id = None
        for movie_id, movie_file in self.main_window.movies_dict.items():
            self.movie_readers[movie_id] = OpenCvVideoReader(video_file_name=movie_file,
                                                             queueSize=self.main_window.movie_queue_size)
            self.current_frame_dict[movie_id] = 0
            self.current_movie_id = movie_id
            self.last_frames_dict[movie_id] = []

        # associate a movie to each bodypart
        self.movie_id_by_bodypart = dict()
        # the key is a body part
        self.image_thresholds_dict = dict()
        # key is the bodypart
        self.piezo_thresholds_dict = dict()
        # the key is a body part, value is a list of 4 int: (x, y, with, height)
        # x,y representing the lower-left corner of the ROI
        self.roi_coords_dict = dict()
        self.default_roi_coords = [50, 50, 350, 250]
        # all bodyparts
        self.bodyparts = []
        self.current_bodypart = None
        for movie_id, bodyparts in self.main_window.bodyparts_dict.items():
            for bodypart in bodyparts:
                # new_bodypart_name = bodypart + "_" + movie_id
                self.bodyparts.append(bodypart)
                if bodypart in self.movie_id_by_bodypart:
                    raise Exception(f"The bodypart {bodypart} is present more than once")
                self.movie_id_by_bodypart[bodypart] = movie_id
                if bodypart in self.main_window.bodyparts_config:
                    self.image_thresholds_dict[bodypart] = self.main_window.bodyparts_config[bodypart][
                        "image_thresholds"]
                    self.roi_coords_dict[bodypart] = self.main_window.bodyparts_config[bodypart]["roi_coords"]
                    self.piezo_thresholds_dict[bodypart] = self.main_window.bodyparts_config[bodypart][
                        "piezo_threshold"]
                else:
                    self.image_thresholds_dict[bodypart] = self.main_window.default_image_thresholds
                    self.piezo_thresholds_dict[bodypart] = self.main_window.default_piezo_threshold

        self.current_bodypart = self.bodyparts[0]

        self.image_widget = ImageWidget(main_window=self.main_window, central_widget=self,
                                        roi_coords_dict=self.roi_coords_dict)
        # self.image_widget.display_image(image_data=self.movie_readers[self.current_movie_id].
        #                            get_frame(self.current_frame_dict[self.current_movie_id]))
        self.main_layout.addWidget(self.image_widget)

        self.config_layout = QVBoxLayout()

        self.bodypart_layout = QHBoxLayout()
        self.bodypart_combo_box = NoWheelQComboBox()
        self.bodypart_combo_box.setToolTip(f"Bodypart to display")
        self.bodypart_combo_box.addItems(self.bodyparts)
        self.bodypart_combo_box.currentIndexChanged.connect(self.change_bodypart)

        self.current_movie_id = self.movie_id_by_bodypart[self.current_bodypart]
        index = self.bodypart_combo_box.findText(self.current_bodypart, QtCore.Qt.MatchFixedString)

        if index >= 0:
            self.bodypart_combo_box.setCurrentIndex(index)
        self.bodypart_layout.addStretch(1)
        self.bodypart_layout.addWidget(self.bodypart_combo_box)
        self.bodypart_layout.addStretch(1)
        self.config_layout.addLayout(self.bodypart_layout)

        self.frame_slider_layout = QHBoxLayout()
        self.frame_slider = QSlider(QtCore.Qt.Horizontal)
        # self.frame_slider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.frame_slider.setTickInterval(5)
        self.frame_slider.setTracking(False)
        self.frame_slider.setMaximum(self.movie_readers[self.current_movie_id].length - 1)
        self.frame_slider.setMinimum(0)
        # self.frame_slider.setEnabled(False)
        self.frame_slider.valueChanged.connect(self.frame_slider_action)
        self.frame_slider_layout.addWidget(self.frame_slider)

        self.frame_spin_box = QSpinBox()
        self.frame_spin_box.setRange(0, self.movie_readers[self.current_movie_id].length)
        self.frame_spin_box.setSingleStep(1)
        self.frame_spin_box.setValue(self.current_frame_dict[self.current_movie_id])
        # to just disable the text box but not the arrows
        self.frame_spin_box.lineEdit().setReadOnly(True)
        self.frame_spin_box.setToolTip("Frame")
        self.frame_spin_box.valueChanged.connect(self.frame_spin_box_value_changed)
        self.frame_slider_layout.addWidget(self.frame_spin_box)

        self.random_frame_button = QPushButton(" R ")
        self.random_frame_button.setToolTip(f"Pick a random frame")
        self.random_frame_button.clicked.connect(self.display_random_frame)
        self.frame_slider_layout.addWidget(self.random_frame_button)

        self.last_frame_button = QPushButton(" <- ")
        self.last_frame_button.setToolTip(f"Come back to last frame displayed")
        self.last_frame_button.setToolTip(f"Come back to last frame displayed")
        self.last_frame_button.clicked.connect(self.display_last_frame)
        self.frame_slider_layout.addWidget(self.last_frame_button)

        self.config_layout.addLayout(self.frame_slider_layout)

        self.threshold_mode_slider_layout = QHBoxLayout()
        self.threshold_mode_checkbox = QCheckBox("Threshold mode")
        self.threshold_mode_checkbox.setToolTip("Set image threshold mode")
        self.threshold_mode_checkbox.setChecked(self.threshold_image_mode)
        self.threshold_mode_checkbox.stateChanged.connect(self.threshold_mode_checkbox_action)
        self.threshold_mode_slider_layout.addWidget(self.threshold_mode_checkbox)

        self.image_thresholds_text_edit = QLineEdit()
        self.image_thresholds_text_edit.setText(self._convert_image_tresholds_to_str())
        self.threshold_mode_slider_layout.addWidget(self.image_thresholds_text_edit)

        self.image_thresholds_button = QPushButton(" Update ")
        self.image_thresholds_button.setToolTip(f"Update the image thresholds values")
        self.image_thresholds_button.clicked.connect(self.image_thresholds_button_action)
        self.threshold_mode_slider_layout.addWidget(self.image_thresholds_button)

        self.image_thresholds_label = QLabel(self._convert_image_tresholds_to_str())
        self.image_thresholds_label.setAlignment(Qt.AlignCenter)
        self.image_thresholds_label.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.image_thresholds_label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.threshold_mode_slider_layout.addWidget(self.image_thresholds_label)

        self.threshold_mode_slider_layout.addStretch(1)
        self.config_layout.addLayout(self.threshold_mode_slider_layout)

        self.power_spectrum_layout = QHBoxLayout()

        self.lowpass_filter_checkbox = QCheckBox("Low pass filter cutoff")
        self.lowpass_filter_checkbox.setToolTip("Use low pass filter")
        self.lowpass_filter_checkbox.setChecked(True)
        # self.lowpass_filter_checkbox.stateChanged.connect(self.threshold_mode_checkbox_action)
        self.power_spectrum_layout.addWidget(self.lowpass_filter_checkbox)

        # self.lowpass_filter_label = QLabel("Low pass filter cutoff")
        # self.lowpass_filter_label.setAlignment(Qt.AlignCenter)
        # self.lowpass_filter_label.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.lowpass_filter_label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.power_spectrum_layout.addWidget(self.lowpass_filter_label)

        self.lowpass_filter_spin_box = QSpinBox()
        self.lowpass_filter_spin_box.setRange(1, 100)
        self.lowpass_filter_spin_box.setSingleStep(1)
        self.lowpass_filter_spin_box.setValue(int(self.lowpass_filter_cutoff * 10))
        # to just disable the text box but not the arrows
        self.lowpass_filter_spin_box.lineEdit().setReadOnly(True)
        self.lowpass_filter_spin_box.setToolTip("Low pass filter cutoff")
        self.lowpass_filter_spin_box.valueChanged.connect(self.lowpass_filter_spin_box_value_changed)
        self.power_spectrum_layout.addWidget(self.lowpass_filter_spin_box)

        self.power_spectrum_layout.addStretch(1)
        self.config_layout.addLayout(self.power_spectrum_layout)

        self.piezo_threshold_layout = QHBoxLayout()
        self.piezo_threshold_title_label = QLabel("Piezo signal threshold: ")
        self.piezo_threshold_title_label.setAlignment(Qt.AlignCenter)
        self.piezo_threshold_title_label.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.piezo_threshold_title_label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.piezo_threshold_layout.addWidget(self.piezo_threshold_title_label)

        self.piezo_threshold_title_value = QLabel(f"{self.piezo_thresholds_dict[self.current_bodypart]:.2f}")
        self.piezo_threshold_title_value.setAlignment(Qt.AlignCenter)
        self.piezo_threshold_title_value.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.piezo_threshold_title_value.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.piezo_threshold_layout.addWidget(self.piezo_threshold_title_value)

        self.piezo_threshold_layout.addStretch(1)
        self.config_layout.addLayout(self.piezo_threshold_layout)

        self.display_signal_layout = QHBoxLayout()
        self.display_signal_layout.addStretch(1)
        self.display_signal_button = QPushButton(" Display signal ")
        self.display_signal_button.setToolTip(f"Display signal")
        self.display_signal_button.clicked.connect(self.display_signal_action)
        self.display_signal_layout.addWidget(self.display_signal_button)
        self.display_signal_layout.addStretch(1)
        self.config_layout.addLayout(self.display_signal_layout)

        self.process_layout = QHBoxLayout()
        self.process_layout.addStretch(1)

        self.save_config_button = QPushButton(" Save config ")
        self.save_config_button.setToolTip(f"Save the config (ROIs, image threshold, piezo signal threshold)")
        self.save_config_button.clicked.connect(self.save_config_button_action)
        self.process_layout.addWidget(self.save_config_button)

        self.process_button = QPushButton(" Process ")
        self.process_button.setToolTip(f"Run analysis")
        self.process_button.clicked.connect(self.process_data)
        self.process_layout.addWidget(self.process_button)

        self.process_layout.addStretch(1)
        self.config_layout.addLayout(self.process_layout)

        self.progress_bar_layout = QHBoxLayout()

        self.remaining_time_label = RemainingTime()
        self.progress_bar = ProgressBar(self.remaining_time_label, parent=self)
        self.progress_bar.setEnabled(False)

        self.progress_bar_layout.addWidget(self.progress_bar)
        self.progress_bar_layout.addWidget(self.remaining_time_label)
        self.config_layout.addLayout(self.progress_bar_layout)

        # self.config_layout.addStretch(1)

        self.change_frame(frame=self.current_frame_dict[self.current_movie_id], initialization=True)

        self.main_layout.addLayout(self.config_layout)

        self.setLayout(self.main_layout)

    def _convert_image_tresholds_to_str(self):
        """
        Get the thresholds in a string format to display in label
        :return:
        """
        return " , ".join([str(t) for t in self.image_thresholds_dict[self.current_bodypart]])

    def print_keyboard_shortcuts(self):
        print("GUI keyboard shortcuts")
        print(f"r -> display a random frame")
        print(f"l -> Last frame displayed")
        print(f"m -> Display the frame just before in time")
        print(f"p -> Display the frame just after in time")
        print(f"b -> In/out threshold image mode")
        print(" ")

    def _get_image_thresholds_from_widget(self, with_message_boxes=True):
        """

        :param with_message_boxes (bool): if True and there is an error, then a message box is displayed
        :return:
        """
        thresholds_str_input = self.image_thresholds_text_edit.text()
        split_values = thresholds_str_input.split(",")
        new_thresholds = []
        for split_value in split_values:
            try:
                thr = int(split_value)
                if thr < 1 or thr > 254:
                    if with_message_boxes:
                        display_msg_in_box(f"{thr} out of bounds 1-254")
                    else:
                        print(f"{thr} out of bounds 1-254")
                    return
                if (len(new_thresholds) > 0) and (thr <= new_thresholds[-1]):
                    if with_message_boxes:
                        display_msg_in_box(f"{split_values}: should be in ascending order")
                    else:
                        print(f"{split_values}: should be in ascending order")
                    return None
                new_thresholds.append(thr)
            except ValueError:
                if with_message_boxes:
                    display_msg_in_box(f"{split_value} is not an integer")
                else:
                    print(f"{split_value} is not an integer")
                return

        if len(new_thresholds) == 0 or len(new_thresholds) > 2:
            if with_message_boxes:
                display_msg_in_box(f"{new_thresholds} len should be 1 or 2")
            else:
                print(f"{new_thresholds} len should be 1 or 2")
            return

        return new_thresholds

    def keyPressEvent(self, event):
        # print('press', event.key())
        sys.stdout.flush()
        if event.key() == QtCore.Qt.Key_R:
            self.display_random_frame()
        elif event.key() == QtCore.Qt.Key_P:
            # like plus one
            current_frame = self.current_frame_dict[self.current_movie_id]
            if current_frame < (self.movie_readers[self.current_movie_id].length - 1):
                self.change_frame(current_frame + 1)
        elif event.key() == QtCore.Qt.Key_M:
            # like minus one
            current_frame = self.current_frame_dict[self.current_movie_id]
            if current_frame > 0:
                self.change_frame(current_frame - 1)
        elif event.key() == QtCore.Qt.Key_L:
            self.display_last_frame()
        elif event.key() == QtCore.Qt.Key_T:
            self.threshold_image_mode = not self.threshold_image_mode
            self.threshold_mode_checkbox.setChecked(self.threshold_image_mode)
            self.image_widget.update_display()

    def threshold_mode_checkbox_action(self):
        self.threshold_image_mode = self.threshold_mode_checkbox.isChecked()
        self.image_widget.update_display()

    def get_current_image_thresholds(self):
        return self.image_thresholds_dict[self.current_bodypart]

    def image_thresholds_button_action(self):
        new_thresholds = self._get_image_thresholds_from_widget()
        if new_thresholds is None:
            self.image_thresholds_text_edit.setText(self._convert_image_tresholds_to_str())
        else:
            # updating the thresholds
            self.image_thresholds_dict[self.current_bodypart] = new_thresholds
            self.image_thresholds_label.setText(self._convert_image_tresholds_to_str())
            self.image_widget.update_display()

    def update_image_thresholds_widgets(self):
        """
        Based on current_bodypart, the label and text edit of image threshold will be updated
        :return:
        """
        self.image_thresholds_text_edit.setText(self._convert_image_tresholds_to_str())
        self.image_thresholds_label.setText(self._convert_image_tresholds_to_str())

    def display_signal_action(self):
        """
        Called by the display signal button.
        Will open a new window allowing to display the signal for a given range of frame
        :return:
        """
        signal_widget = DisplaySignalMainWindow(citnps_main_window=self.main_window, bodypart=self.current_bodypart,
                                                citnps_central_widget=self,
                                                current_frame=self.current_frame_dict[self.current_movie_id],
                                                piezo_threshold=self.piezo_thresholds_dict[self.current_bodypart])
        self.signal_display_widgets.append(signal_widget)

    def _open_file_dialog(self, title):
        """
        Allows to choose a directory
        :param title:
        :return: the path name or None if none is selected
        """
        # then we open a window to select it
        file_dialog = QFileDialog(self, "Folder where to save the results")

        # setting options
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.DontUseCustomDirectoryIcons
        file_dialog.setOptions(options)

        # ARE WE TALKING ABOUT FILES OR FOLDERS
        directory_only = True
        if directory_only:
            file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        else:
            file_dialog.setFileMode(QFileDialog.AnyFile)

        if file_dialog.exec_() == QDialog.Accepted:
            return file_dialog.selectedFiles()[0]  # returns a list

        return None

    def save_config_button_action(self):
        """

        :return:
        """
        results_path = self._open_file_dialog(title="Folder where to save the config")
        # creating a sub-folder with the timestamp
        time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")
        results_path = os.path.join(results_path, self.main_window.data_id + "_config_" + time_str)
        os.mkdir(results_path)

        self._save_config_in_yaml_file(results_path)

    def _save_config_in_yaml_file(self, results_path):
        """

        :param results_path:
        :return:
        """
        citnps_config = dict()
        for bodypart in self.bodyparts:
            citnps_config[bodypart] = dict()
            # bodypart will be in roi_coords_dict only if the ROI has been moved or loaded from config
            if bodypart in self.roi_coords_dict:
                citnps_config[bodypart]["image_thresholds"] = list(self.image_thresholds_dict[bodypart])
                citnps_config[bodypart]["roi_coords"] = list(self.roi_coords_dict[bodypart])
                citnps_config[bodypart]["piezo_threshold"] = float(np.round(self.piezo_thresholds_dict[bodypart], 2))

        with open(os.path.join(results_path, f'{self.main_window.data_id}_citnps_config.yaml'), 'w') as outfile:
            yaml.dump(citnps_config, outfile, default_flow_style=False)

    def process_data(self):
        # first checking is some bodypart are missing
        missing_bodyparts = []
        for bodypart in self.bodyparts:
            if bodypart not in self.roi_coords_dict:
                missing_bodyparts.append(bodypart)

        if len(missing_bodyparts) > 0:
            display_msg_in_box(msg=f"These bodyparts have not been configurated: {' '.join(missing_bodyparts)} ")
            return

        # Saving parameters in a yaml file
        if self.main_window.results_path is None:
            self.main_window.results_path = self._open_file_dialog(title="Folder where to save the results")

        # creating a sub-folder with the timestamp
        time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")
        results_path = os.path.join(self.main_window.results_path, self.main_window.data_id + "_" + time_str)
        os.mkdir(results_path)

        self._save_config_in_yaml_file(results_path)

        self.process_button.setEnabled(False)

        apply_lowpass_filter = self.lowpass_filter_checkbox.isChecked()
        lowpass_filter_cutoff = self.lowpass_filter_cutoff

        frames_dict = dict()
        for movie_id in self.movie_readers.keys():
            frames_dict[movie_id] = np.arange(0, self.movie_readers[movie_id].length)

        piezo_signal_dict = from_camera_to_piezo_signal(roi_coords_dict=self.roi_coords_dict,
                                                        image_thresholds_dict=self.image_thresholds_dict,
                                                        frames_dict=frames_dict,
                                                        movie_readers_dict=self.movie_readers,
                                                        bodyparts=self.bodyparts,
                                                        movie_id_by_bodypart_dict=self.movie_id_by_bodypart,
                                                        progress_bar=self.progress_bar)

        for bodypart in self.bodyparts:
            movie_id = self.movie_id_by_bodypart[bodypart]
            first_frame = 0
            last_frame = self.movie_readers[self.current_movie_id].length - 1
            normalized_signal, fully_processed_signal = \
                process_piezo_signal(signal_data=piezo_signal_dict[bodypart],
                                     luminosity_states=self.main_window.luminosity_change_dict[movie_id],
                                     first_frame=first_frame,
                                     last_frame=last_frame,
                                     apply_lowpass_filter=apply_lowpass_filter,
                                     cutoff=lowpass_filter_cutoff,
                                     fs=20, order=10)
            arg_dict = {bodypart: fully_processed_signal,
                        "timestamps": self.main_window.behavior_time_stamps_dict[movie_id]}
            np.savez(os.path.join(results_path, f"{self.main_window.data_id}_{bodypart}_citnps_piezo_signal.npz"),
                     **arg_dict)
        print(f"Data processed")

    def display_random_frame(self):
        random_frame = randrange(self.movie_readers[self.current_movie_id].length)
        self.change_frame(frame=random_frame)

    def display_last_frame(self):
        if len(self.last_frames_dict[self.current_movie_id]) > 0:
            last_frame = self.last_frames_dict[self.current_movie_id][-1]
            self.last_frames_dict[self.current_movie_id] = self.last_frames_dict[self.current_movie_id][:-1]
            self.change_frame(frame=last_frame, from_last_frame=True)

    def frame_slider_action(self):
        self.change_frame(int(self.frame_slider.value()), from_slider=True)
        # self.go_to_timestamp(timestamp=self.frame_slider.value())

    def lowpass_filter_spin_box_value_changed(self, value):
        self.lowpass_filter_cutoff = int(value) / 10

    def frame_spin_box_value_changed(self, value):
        self.change_frame(int(value), from_spin_box=True)

    def set_piezo_threshold(self, piezo_threshold, bodypart, from_signal_widget):
        """
        New piezo threshold
        :param piezo_threshold: float
        :param bodypart: (str) the bodypart threshold
        :param from_signal_widget: (SignalWidget)
        :return:
        """
        self.piezo_thresholds_dict[bodypart] = piezo_threshold
        if bodypart == self.current_bodypart:
            self._update_piezo_threshold_label()
        if from_signal_widget is not None:
            for signal_widget in self.signal_display_widgets:
                if from_signal_widget == signal_widget:
                    continue
                if signal_widget.bodypart != from_signal_widget.bodypart:
                    continue
                signal_widget.set_piezo_threshold(piezo_threshold)

    def change_frame(self, frame, from_slider=False, from_spin_box=False, initialization=False,
                     from_last_frame=False, from_signal_widget=None):
        """
        Update the frame to be displayed
        :param frame:
        :param from_slider:
        :param from_spin_box:
        :param initialization:
        :param from_signal_widget: SignalWidget instance, if not None, means the change of frame comes from this
        instance, and so this one should not be updated
        :return:
        """
        if (not initialization) and (frame == self.current_frame_dict[self.current_movie_id]):
            return

        if from_signal_widget is not None:
            if from_signal_widget.movie_id != self.current_movie_id:
                return

        if not from_last_frame:
            self.last_frames_dict[self.current_movie_id].append(self.current_frame_dict[self.current_movie_id])

        # updating the location of frame displayed on the signal widget
        for signal_widget in self.signal_display_widgets:
            if (from_signal_widget is not None) and (from_signal_widget == signal_widget):
                continue
            if signal_widget.movie_id != self.current_movie_id:
                continue
            signal_widget.set_current_frame(frame=frame)

        self.current_frame_dict[self.current_movie_id] = frame
        if not from_slider:
            self.frame_slider.setValue(frame)
        if not from_spin_box:
            self.frame_spin_box.setValue(frame)

        self.image_widget.display_image(image_data=self.movie_readers[self.current_movie_id].get_frame(
            self.current_frame_dict[self.current_movie_id]))

    def _update_piezo_threshold_label(self):
        """

        :return:
        """
        self.piezo_threshold_title_value.setText(f"{self.piezo_thresholds_dict[self.current_bodypart]:.2f}")

    def change_bodypart(self, index):
        """
        Called if the selection is changed either by the user or by the code
        Args:
            index:

        Returns:

        """

        # it should not be empty
        if self.bodypart_combo_box.count() == 0:
            return

        # TODO: change image thresholds

        self.current_bodypart = self.bodypart_combo_box.currentText()
        self.current_movie_id = self.movie_id_by_bodypart[self.current_bodypart]

        current_frame = self.current_frame_dict[self.current_movie_id]
        self.change_frame(current_frame, initialization=True)
        self._update_piezo_threshold_label()
        # updating the image threshold
        self.update_image_thresholds_widgets()
