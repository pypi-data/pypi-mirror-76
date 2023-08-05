from qtpy.QtWidgets import *
from qtpy import QtCore, QtGui
from qtpy.QtCore import Qt

import platform
import os
import ctypes
import numpy as np
import pyqtgraph as pg
from cicada.gui.exploratory.cicada_finite_regions import FiniteLinearRegionItem, FiniteLine
from citnps.utils.signal import process_piezo_signal, from_camera_to_piezo_signal
from citnps.citnps_progress_bar import RemainingTime, ProgressBar
import time
from functools import partial


class DisplaySignalMainWindow(QMainWindow):
    def __init__(self, citnps_main_window, bodypart, citnps_central_widget, current_frame, piezo_threshold):
        super().__init__(parent=citnps_main_window)
        # QMainWindow.__init__(self)
        self.citnps_main_window = citnps_main_window
        self.citnps_central_widget = citnps_central_widget
        self.bodypart = bodypart
        self.movie_id = self.citnps_central_widget.movie_id_by_bodypart[self.bodypart]
        # To display a the window icon as the application icon in the task bar on Windows
        # if platform.system() == "Windows":
        #     myappid = u'cossart.cicada.gui.alpha'  # arbitrary string
        #     ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        # my_path = os.path.abspath(os.path.dirname(__file__))
        # self.setWindowIcon(QtGui.QIcon(os.path.join(my_path, '../icons/svg/cicada_open_focus.svg')))

        # data_to_explore should be an instance of CicadaAnalysisFormatWrapper
        # self.data_to_explore = data_to_explore
        # data_to_explore.get_intervals_names()
        # ----- misc attributes -----
        self.labels = []
        self.to_add_labels = []

        # allows to access config param
        # self.config_handler = config_handler

        # self.createActions()
        # self.createMenus()
        self.object_created = []
        self.labels = []
        self.setWindowTitle(f"{bodypart} signal")

        screenGeometry = QApplication.desktop().screenGeometry()
        # making sure the window is not bigger than the dimension of the screen
        width_window = min(2000, screenGeometry.width())
        # width_window = screenGeometry.width()
        height_window = min(700, screenGeometry.height())
        self.resize(width_window, height_window)

        ## creating widgets to put in the window
        self.central_widget = DisplaySignalCentralWidget(display_signal_main_window=self,
                                                         citnps_main_window=citnps_main_window,
                                                         citnps_central_widget=self.citnps_central_widget,
                                                         bodypart=self.bodypart, current_frame=current_frame,
                                                         piezo_threshold=piezo_threshold)
        self.setCentralWidget(self.central_widget)

        self.show()

    def set_piezo_threshold(self, piezo_threshold):
        """
        Set the piezo threshold value, will move the line on the plot
        :param piezo_threshold:
        :return:
        """
        self.central_widget.set_piezo_threshold(piezo_threshold)

    def set_current_frame(self, frame):
        self.central_widget.set_current_frame(frame=frame)

    def closeEvent(self, event):
        self.citnps_central_widget.signal_display_widgets.remove(self)


class DisplaySignalCentralWidget(QWidget):

    def __init__(self, display_signal_main_window, citnps_main_window, citnps_central_widget, bodypart, current_frame,
                 piezo_threshold):
        super().__init__(parent=display_signal_main_window)

        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        self.citnps_central_widget = citnps_central_widget
        self.citnps_main_window = citnps_main_window
        self.bodypart = bodypart
        self.movie_id = self.citnps_central_widget.movie_id_by_bodypart[self.bodypart]
        self.movie_reader = self.citnps_central_widget.movie_readers[self.movie_id]
        self.current_frame = current_frame

        self.main_layout = QVBoxLayout()

        self.plots_layout = QHBoxLayout()

        self.piezo_signal_widget = PiezoSignalWidget(description="Piezo signal", display_signal_central_widget=self,
                                                     piezo_threshold=piezo_threshold)
        self.plots_layout.addWidget(self.piezo_signal_widget)

        self.power_spectrum_widget = PowerSpectrumWidget(description="Power spectrum", parent=self)
        self.plots_layout.addWidget(self.power_spectrum_widget)
        self.plots_layout.addStretch(1)

        # TODO: Add the two plots

        self.main_layout.addLayout(self.plots_layout)

        self.config_layout = QVBoxLayout()

        # toto
        if len(self.citnps_main_window.luminosity_change_dict[self.movie_id]) > 0:
            self.luminosity_change_layout = QHBoxLayout()
            self.luminosity_change_layout.addStretch(1)

            # luminosity_change_frames = ", ".join([str(f) for f in
            #                                       self.citnps_main_window.luminosity_change_dict[self.movie_id]])
            luminosity_change_frames = [str(f) for f in self.citnps_main_window.luminosity_change_dict[self.movie_id]]
            self.luminosity_change_label = QLabel("Luminosity change frames: ")
            self.luminosity_change_label.setAlignment(Qt.AlignCenter)
            self.luminosity_change_label.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.luminosity_change_label.setAttribute(QtCore.Qt.WA_TranslucentBackground)

            self.luminosity_change_layout.addWidget(self.luminosity_change_label)

            self.luminosity_change_box = QComboBox()
            self.luminosity_change_box.setToolTip(f"Luminosity change frames")
            self.luminosity_change_box.addItems(luminosity_change_frames)
            # self.luminosity_change_box.currentIndexChanged.connect(self.)

            first_change_frame = luminosity_change_frames[0]
            index = self.luminosity_change_box.findText(first_change_frame, QtCore.Qt.MatchFixedString)

            if index >= 0:
                self.luminosity_change_box.setCurrentIndex(index)

            self.luminosity_change_layout.addWidget(self.luminosity_change_box)

            self.luminosity_change_layout.addStretch(1)

            self.config_layout.addLayout(self.luminosity_change_layout)

        self.citnps_main_window.luminosity_change_dict[self.movie_id]

        self.first_frame_layout = QHBoxLayout()
        self.first_frame_layout.addStretch(1)

        self.first_frame_label = QLabel("First frame: ")
        self.first_frame_label.setAlignment(Qt.AlignCenter)
        self.first_frame_label.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.first_frame_label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.first_frame_layout.addWidget(self.first_frame_label)

        self.first_frame_spin_box = QSpinBox()
        # TODO: change max
        self.first_frame_spin_box.setRange(0, self.movie_reader.length - 1)
        self.first_frame_spin_box.setSingleStep(1)
        self.first_frame_spin_box.setValue(0)
        # to just disable the text box but not the arrows
        # self.first_frame_spin_box.lineEdit().setReadOnly(True)
        self.first_frame_spin_box.setToolTip("First frame from which display the signal")
        # self.first_frame_spin_box.valueChanged.connect(self.first_frame_spin_box_value_changed)
        self.first_frame_layout.addWidget(self.first_frame_spin_box)
        self.first_frame_layout.addStretch(1)

        self.config_layout.addLayout(self.first_frame_layout)

        self.last_frame_layout = QHBoxLayout()
        self.last_frame_layout.addStretch(1)

        self.last_frame_label = QLabel("Last frame: ")
        self.last_frame_label.setAlignment(Qt.AlignCenter)
        self.last_frame_label.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.last_frame_label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.last_frame_layout.addWidget(self.last_frame_label)

        self.last_frame_spin_box = QSpinBox()
        self.last_frame_spin_box.setRange(10, self.movie_reader.length - 1)
        self.last_frame_spin_box.setSingleStep(1)
        self.last_frame_spin_box.setValue(min(1000, self.movie_reader.length - 1))
        # to just disable the text box but not the arrows
        # self.first_frame_spin_box.lineEdit().setReadOnly(True)
        self.last_frame_spin_box.setToolTip("Last frame from which display the signal")
        # self.last_frame_spin_box.valueChanged.connect(self.last_frame_spin_box_value_changed)
        self.last_frame_layout.addWidget(self.last_frame_spin_box)

        self.last_frame_max_value_label = QLabel(f" / {self.movie_reader.length - 1}")
        self.last_frame_max_value_label.setAlignment(Qt.AlignCenter)
        self.last_frame_max_value_label.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.last_frame_max_value_label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.last_frame_layout.addWidget(self.last_frame_max_value_label)

        self.last_frame_layout.addStretch(1)

        self.config_layout.addLayout(self.last_frame_layout)

        self.main_layout.addLayout(self.config_layout)

        self.display_signal_layout = QHBoxLayout()
        self.display_signal_layout.addStretch(1)
        self.display_signal_button = QPushButton(" Display signal ")
        self.display_signal_button.setToolTip(f"Display signal")
        self.display_signal_button.clicked.connect(self.display_signal_action)
        self.display_signal_layout.addWidget(self.display_signal_button)
        self.display_signal_layout.addStretch(1)
        self.config_layout.addLayout(self.display_signal_layout)

        self.threshold_layout = QHBoxLayout()
        self.threshold_layout.addStretch(1)
        self.threshold_label = QLabel(" ")
        self.threshold_label.setAlignment(Qt.AlignCenter)
        self.threshold_label.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.threshold_label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.threshold_layout.addWidget(self.threshold_label)
        self.threshold_layout.addStretch(1)
        self.config_layout.addLayout(self.threshold_layout)

        self.filter_layout = QHBoxLayout()
        self.filter_layout.addStretch(1)
        self.filter_label = QLabel(" ")
        self.filter_label.setAlignment(Qt.AlignCenter)
        self.filter_label.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.filter_label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.filter_layout.addWidget(self.filter_label)
        self.filter_layout.addStretch(1)
        self.config_layout.addLayout(self.filter_layout)

        self.progress_bar_layout = QHBoxLayout()
        # put main window on top
        go_home_button = QPushButton()
        go_home_button.setProperty("home", "True")
        go_home_button.clicked.connect(partial(self.bring_to_front, citnps_main_window))
        self.progress_bar_layout.addWidget(go_home_button)
        self.remaining_time_label = RemainingTime()
        self.progress_bar = ProgressBar(self.remaining_time_label, parent=self)
        self.progress_bar.setEnabled(False)

        self.progress_bar_layout.addWidget(self.progress_bar)
        self.progress_bar_layout.addWidget(self.remaining_time_label)
        self.config_layout.addLayout(self.progress_bar_layout)

        # TODO: add progress bar

        self.main_layout.addStretch(1)

        self.setLayout(self.main_layout)

    def bring_to_front(self, window_id, event):
        """
        Bring corresponding  window to the front (re-routed from the double click method)

        Args:
            window_id (QWidget) : Main Widget object
            event (QEvent) : Double click event
        """
        window_id.setWindowState(window_id.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        # For Windows/Linux
        window_id.activateWindow()
        # For Mac
        window_id.raise_()

    def current_frame_line_moved(self, frame):
        """
        Called when the line indicating the frame do display has been moved
        :return:
        """
        self.citnps_central_widget.change_frame(frame=frame, from_signal_widget=self)

    def piezo_threshold_line_moved(self, piezo_threshold):
        """
            Called when the line indicating the piezo threshold has been moved
            :return:
        """
        self.citnps_central_widget.set_piezo_threshold(piezo_threshold=piezo_threshold, bodypart=self.bodypart,
                                                       from_signal_widget=self)

    def set_piezo_threshold(self, piezo_threshold):
        """
        Set the piezo threshold value, will move the line on the plot
        :param piezo_threshold:
        :return:
        """
        self.piezo_signal_widget.set_piezo_threshold(piezo_threshold)

    def get_current_movie_displayed(self):
        return self.citnps_central_widget.current_movie_id

    def display_signal_action(self):
        """
        Called by the display signal button.
        :return:
        """
        first_frame = self.first_frame_spin_box.value()
        last_frame = self.last_frame_spin_box.value()
        if first_frame >= last_frame:
            display_msg_in_box("First frame should be inferior to last frame")
            return

        if (last_frame - first_frame) < 20:
            display_msg_in_box("At least 20 frames should be selected")
            return

        # if first_frame != 0:
        #     # for simplicity, it should start at zero for now
        #     return

        if self.bodypart not in self.citnps_central_widget.roi_coords_dict:
            display_msg_in_box("A bodypart must be set using the ROI widget")
            return

        # can only be run once
        self.display_signal_button.setEnabled(False)
        # time.sleep(0.1)

        image_thresholds = self.citnps_central_widget.image_thresholds_dict[self.bodypart]
        image_thresholds = " , ".join([str(t) for t in image_thresholds])
        apply_lowpass_filter = self.citnps_central_widget.lowpass_filter_checkbox.isChecked()
        lowpass_filter_cutoff = self.citnps_central_widget.lowpass_filter_cutoff

        movie_id = self.citnps_central_widget.movie_id_by_bodypart[self.bodypart]
        frames_dict = {movie_id:
                           np.arange(first_frame, last_frame + 1)}
        piezo_signal_dict = from_camera_to_piezo_signal(roi_coords_dict=self.citnps_central_widget.roi_coords_dict,
                                                        image_thresholds_dict=self.citnps_central_widget.
                                                        image_thresholds_dict,
                                                        frames_dict=frames_dict,
                                                        movie_readers_dict=self.citnps_central_widget.movie_readers,
                                                        bodyparts=[self.bodypart],
                                                        movie_id_by_bodypart_dict=self.citnps_central_widget.
                                                        movie_id_by_bodypart,
                                                        progress_bar=self.progress_bar)

        normalized_signal, fully_processed_signal = process_piezo_signal(signal_data=piezo_signal_dict[self.bodypart],
                                                                         luminosity_states=self.citnps_main_window.
                                                                         luminosity_change_dict[self.movie_id],
                                                                         first_frame=first_frame,
                                                                         last_frame=last_frame,
                                                                         apply_lowpass_filter=apply_lowpass_filter,
                                                                         cutoff=lowpass_filter_cutoff,
                                                                         fs=20, order=10)
        n_frames_in_movie = self.citnps_central_widget.movie_readers[movie_id].length
        # print(f"n_frames_in_movie {n_frames_in_movie}, len(fully_processed_signal) {len(fully_processed_signal)}")
        self.piezo_signal_widget.update_plot(frames=np.arange(first_frame, last_frame + 1),
                                             filtered_signal_data=fully_processed_signal[first_frame:last_frame+1],
                                             raw_signal_data=normalized_signal[first_frame:last_frame+1],
                                             luminosity_changes=self.citnps_main_window.
                                             luminosity_change_dict[self.movie_id])

        sampling_rate = 20
        fourier_transform = np.fft.rfft(fully_processed_signal[first_frame:last_frame+1])
        abs_fourier_transform = np.abs(fourier_transform)
        filtered_power_spectrum = np.square(abs_fourier_transform)
        frequency = np.linspace(0, sampling_rate / 2, len(filtered_power_spectrum))

        fourier_transform = np.fft.rfft(normalized_signal[first_frame:last_frame+1])
        abs_fourier_transform = np.abs(fourier_transform)
        raw_power_spectrum = np.square(abs_fourier_transform)
        # original_frequency = np.linspace(0, sampling_rate / 2, len(raw_power_spectrum))
        self.power_spectrum_widget.update_plot(frequencies=frequency,
                                               filtered_power_spectrum=filtered_power_spectrum,
                                               raw_power_spectrum=raw_power_spectrum,
                                               freq_markers=[lowpass_filter_cutoff])
        self.display_signal_button.setEnabled(True)

        # updating labels
        self.threshold_label.setText(f"Image thresholds : {image_thresholds}")
        if apply_lowpass_filter:
            self.filter_label.setText(f"Low pass filter with cutoff at {lowpass_filter_cutoff}")
        else:
            self.filter_label.setText(f"No low pass filter")

    def set_current_frame(self, frame):
        self.piezo_signal_widget.set_current_frame(frame)

def display_msg_in_box(msg):
    message_box = QMessageBox()
    message_box.setText(msg)
    message_box.exec()


class MyViewBox(pg.ViewBox):
    """
    Mixed between RectMode and PanMode.
    Left click drag act like in RectMode
    Right click drag act life left click will act in PanMode (move the view box)
    Allow to zoom.
    Code from pyqtgraph examples
    """

    def __init__(self, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        # self.setMouseMode(self.RectMode) ViewBox.PanMode

    def mouseClickEvent(self, ev):
        pass
        ## reimplement right-click to zoom out
        # if ev.button() == QtCore.Qt.RightButton:
        #     self.autoRange()

    def mouseDragEvent(self, ev):
        """
        Right click is used to zoom, left click is use to move the area
        Args:
            ev:

        Returns:

        """
        if ev.button() == QtCore.Qt.RightButton:
            self.setMouseMode(self.PanMode)
            # cheating, by telling it the left button is used instead
            ev._buttons = [QtCore.Qt.LeftButton]
            ev._button = QtCore.Qt.LeftButton
            pg.ViewBox.mouseDragEvent(self, ev)
        elif ev.button() == QtCore.Qt.LeftButton:
            self.setMouseMode(self.RectMode)
            pg.ViewBox.mouseDragEvent(self, ev)
        else:
            # ev.ignore()
            pg.ViewBox.mouseDragEvent(self, ev)


class PiezoSignalWidget(pg.PlotWidget):
    """
    Used to display a 1d signal
    """

    def __init__(self, description, display_signal_central_widget, piezo_threshold):

        pg.GraphicsLayoutWidget.__init__(self)

        self.display_signal_central_widget = display_signal_central_widget

        self.view_box = MyViewBox()
        pg.PlotWidget.__init__(self, title=description, parent=display_signal_central_widget, viewBox=self.view_box)
        self.description = description
        # allows the widget to be expanded in both axis
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # 230 is the height, the width 300 here doesn't really matter as it is expending
        self.setSceneRect(0, 0, 1000, 600)
        # represent the frame of the movie displayed on the camera window
        self.current_frame = display_signal_central_widget.current_frame
        self.frames_displayed = [0]
        # define a threshold that seems adequate to distinguish noise from bodypart movement
        self.piezo_threshold = piezo_threshold

        self.pg_plot = self.getPlotItem()
        # self.invertY(True)
        # hide the left axis, as the label of each tag is displayed on the line
        # self.pg_plot.hideAxis(axis='left')
        # self.pg_plot.hideAxis(axis='bottom')
        # view_box = pg_plot.getViewBox()

        self.pg_plot.setAspectLocked(True)
        self.luminosity_changes_items = []

        # ploting the signal, blue pen
        self.plot_raw_signal = self.pg_plot.plot(pen=(0, 0, 255))
        # with red pen
        self.plot_filtered_signal = self.pg_plot.plot(pen=(255, 0, 0))

        color_pen = (100, 149, 237) # light blue
        color_hover_pen = (255, 255, 255)  # white
        # show a line that would represent a possible threshold to classify mvt
        self.piezo_threshold_line_item = FiniteLine(pos=[0, self.piezo_threshold],
                                    angle=0, finite_values=None, pen=color_pen, movable=True,
                                    hoverPen=color_hover_pen, label=None, labelOpts=None,
                                    name=None, int_rounding=False,
                                    first_line=False,
                                    new_line_pos_callback=self.piezo_threshold_line_moved,
                                    time_interval=None)
        self.pg_plot.addItem(item=self.piezo_threshold_line_item)

        color_pen = (255, 255, 0)  # yellow
        color_hover_pen = (255, 0, 0)  # red
        self.current_frame_line_item = FiniteLine(pos=[self.current_frame, 0],
                                                  angle=90, finite_values=None, pen=color_pen, movable=True,
                                                  hoverPen=color_hover_pen, label=None, labelOpts=None,
                                                  name=None, int_rounding=False,
                                                  first_line=False,
                                                  new_line_pos_callback=self.current_frame_line_moved,
                                                  time_interval=None)
        self.pg_plot.addItem(item=self.current_frame_line_item)

        # TODO: See to add a vertical line that would be moved by the main widget

    def set_piezo_threshold(self, piezo_threshold):
        """

        :param piezo_threshold:
        :return:
        """
        self.piezo_threshold = piezo_threshold
        self.piezo_threshold_line_item.setPos(pos=[0, piezo_threshold])

    def piezo_threshold_line_moved(self, new_pos, first_value, time_interval):
        """
        The finite line representing the piezo threshold has been moved.
        Args:
            new_pos:

        Returns: None

        """
        if new_pos == self.piezo_threshold:
            # then it was a callback from the main window
            return
        self.piezo_threshold = new_pos
        self.display_signal_central_widget.piezo_threshold_line_moved(piezo_threshold=new_pos)

    def current_frame_line_moved(self, new_pos, first_value, time_interval):
        """
        The finite line has been moved. We change the frame displayed in consequence
        Args:
            new_pos:

        Returns: None

        """
        if self.display_signal_central_widget.get_current_movie_displayed() != \
                self.display_signal_central_widget.movie_id:
            # then the line shouldn't be moved and we put it back in place
            self._move_current_frame_line()
            return
        self.current_frame = max(0, int(new_pos))
        self.display_signal_central_widget.current_frame_line_moved(frame=self.current_frame)

    def set_current_frame(self, frame):
        self.current_frame = frame
        self._move_current_frame_line()

    def _move_current_frame_line(self):
        frame = self.current_frame
        if frame < np.min(self.frames_displayed):
            frame = np.min(self.frames_displayed)
        elif frame > np.max(self.frames_displayed):
            frame = np.max(self.frames_displayed)

        self.current_frame_line_item.setPos(pos=[frame, 0])

    def get_displayed_range(self):
        """
        Return the range of the displayed values in the plot
        Returns:

        """
        return self.pg_plot.getViewBox().viewRange()

    def update_plot(self, frames, filtered_signal_data, raw_signal_data, luminosity_changes):
        self.frames_displayed = frames
        self.plot_filtered_signal.setData(frames, filtered_signal_data)
        self.plot_raw_signal.setData(frames, raw_signal_data)
        y_min = min(np.min(filtered_signal_data), np.min(raw_signal_data))
        y_max = max(np.max(filtered_signal_data), np.max(raw_signal_data))
        range_signal = y_max - y_min
        # print(f"y_min {y_min}, y_max {y_max}, range_signal {range_signal}")
        self.view_box.setLimits(xMin=frames[0] - 1, xMax=frames[-1] + 1,
                                yMin=y_min - (range_signal / 5), yMax=y_max)
        # range of the plot that can be manipulated
        self.pg_plot.setXRange(frames[0], frames[-1])
        self.pg_plot.setYRange(y_min - (range_signal / 5), y_max)

        # removing older lines
        for item in self.luminosity_changes_items:
            self.pg_plot.removeItem(item=item)

        color_pen = (255, 255, 255)  # white
        color_hover_pen = (100, 149, 237)  # light blue
        for luminosity_change_frame in luminosity_changes:
            if (luminosity_change_frame >= frames[0]) and (luminosity_change_frame <= frames[-1]):
                luminosity_item = FiniteLine(pos=[luminosity_change_frame, 0],
                                             angle=90, finite_values=None, pen=color_pen, movable=False,
                                             hoverPen=color_hover_pen, label=None, labelOpts=None,
                                             name=None, int_rounding=False,
                                             first_line=False,
                                             time_interval=None)
                self.pg_plot.addItem(item=luminosity_item)
                self.luminosity_changes_items.append(luminosity_item)

        # update the position of the line representing the current_frame of the movie displayed
        self._move_current_frame_line()

        # so we get the full range of the signal displayed by default
        self.pg_plot.setAspectLocked(False)
        self.pg_plot.setAspectLocked(True)



class PowerSpectrumWidget(pg.PlotWidget):
    """
    Used to display a 1d signal
    """

    def __init__(self, description, main_window=None, parent=None):
        """

        Args:
            data_to_explore: Wrapper data format
            description (str): would be display in a corner
            signal_data:
            timestamps:  np.array of float, give the timestamp of each frame of the movie
            min_timestamp:
            max_timestamp:
            go_to_timestamp_fct: fct that take as first argument a timestamp, should be called if the current_timestamp
            changed
            current_timestamp: timestamp to display (the closest will be displayed)
            main_window:
            to_connect_to_main_window:
            parent:
        """
        pg.GraphicsLayoutWidget.__init__(self)

        self.view_box = MyViewBox()
        pg.PlotWidget.__init__(self, title=description, parent=parent, viewBox=self.view_box)
        self.description = description
        # allows the widget to be expanded in both axis
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # 230 is the height, the width 300 here doesn't really matter as it is expending
        self.setSceneRect(0, 0, 1000, 600)
        self.main_window = main_window

        self.pg_plot = self.getPlotItem()
        # self.invertY(True)
        # hide the left axis, as the label of each tag is displayed on the line
        # self.pg_plot.hideAxis(axis='left')
        # self.pg_plot.hideAxis(axis='bottom')
        # view_box = pg_plot.getViewBox()

        # self.pg_plot.setAspectLocked(True)
        self.luminosity_changes_items = []

        # ploting the signal, blue pen
        self.plot_raw_power_spectrum = self.pg_plot.plot(pen=(0, 0, 255))
        # with red pen
        self.plot_filtered_power_spectrum = self.pg_plot.plot(pen=(255, 0, 0))

        # vertical lines marking for exemple the filter cutoff
        self.marker_items = []

    def get_displayed_range(self):
        """
        Return the range of the displayed values in the plot
        Returns:

        """
        return self.pg_plot.getViewBox().viewRange()

    def update_plot(self, frequencies,
                    filtered_power_spectrum,
                    raw_power_spectrum, freq_markers):
        """

        :param frequencies: (1d array)
        :param filtered_power_spectrum: (1d array)
        :param raw_power_spectrum: (1d array)
        :param freq_markers: list, produce vertical line at the given frequencies
        :return:
        """
        self.plot_filtered_power_spectrum.setData(frequencies, filtered_power_spectrum)
        self.plot_raw_power_spectrum.setData(frequencies, raw_power_spectrum)
        y_min = min(np.min(filtered_power_spectrum), np.min(raw_power_spectrum))
        y_max = max(np.max(filtered_power_spectrum), np.max(raw_power_spectrum))
        range_signal = y_max - y_min
        # print(f"y_min {y_min}, y_max {y_max}, range_signal {range_signal}")
        self.view_box.setLimits(xMin=frequencies[0] - 1, xMax=frequencies[-1] + 1,
                                yMin=y_min - (range_signal / 5), yMax=y_max)
        # range of the plot that can be manipulated
        self.pg_plot.setXRange(frequencies[0], frequencies[-1])
        self.pg_plot.setYRange(y_min - (range_signal / 5), y_max)

        # removing older lines
        for item in self.marker_items:
            self.pg_plot.removeItem(item=item)

        color_pen = (255, 255, 255)  # white
        color_hover_pen = (100, 149, 237)  # light blue
        for freq_marker in freq_markers:
            if (freq_marker >= frequencies[0]) and (freq_marker <= frequencies[-1]):
                marker_item = FiniteLine(pos=[freq_marker, 0],
                                         angle=90, finite_values=None, pen=color_pen, movable=False,
                                         hoverPen=color_hover_pen, label=None, labelOpts=None,
                                         name=None, int_rounding=False,
                                         first_line=False,
                                         time_interval=None)
                self.pg_plot.addItem(item=marker_item)
                self.marker_items.append(marker_item)


