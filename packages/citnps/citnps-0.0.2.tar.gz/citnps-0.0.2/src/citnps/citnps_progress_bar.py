from qtpy.QtWidgets import *


class ProgressBar(QProgressBar):
    """Class containing the progress bar of the current analysis"""

    def __init__(self, remaining_time_label, parent=None):
        """

        Args:
            remaining_time_label: Associated analysis remaining time
        """
        QProgressBar.__init__(self)
        self.setMinimum(0)
        self.parent = parent
        self.remaining_time_label = remaining_time_label
        self.last_time_elapsed = 0

    def update_progress_bar(self, time_elapsed, increment_value=0, new_set_value=0):
        """
        Update the progress bar in the analysis widget and the corresponding remaining time
        Args:
            time_elapsed (float): Time elapsed since beginning of analysis, in seconds
            increment_value (float): Value that should be added to the current value of the progress bar.
            Work for value > 1
            new_set_value (float):  Value that should be set as the current value of the progress bar

        Returns:

        """
        self.setEnabled(True)

        # useful for the last called to set the bar at 100%
        if time_elapsed == 0:
            time_elapsed = self.last_time_elapsed
        else:
            self.last_time_elapsed = time_elapsed

        if new_set_value != 0:
            self.setValue(new_set_value)

        if increment_value != 0:
            self.setValue(self.value() + increment_value)

        if self.isEnabled() and self.value() != 0:
            if self.value() == 100:
                self.remaining_time_label.update_remaining_time(self.value(), time_elapsed=time_elapsed,
                                                                done=True)
            else:
                self.remaining_time_label.update_remaining_time(self.value(), time_elapsed=time_elapsed)

    def update_progress_bar_overview(self, name, increment_value=0, new_set_value=0):
        """
        Update the overview progress bar

        Args:
            name (str): Analysis ID
            time_started (float): Start time of the analysis
            increment_value (float): Value that should be added to the current value of the progress bar
            new_set_value (float):  Value that should be set as the current value of the progress bar

        """
        obj = self.parent.parent.analysis_overview
        try:
            progress_bar_instance = getattr(obj, name + '_progress_bar')
            progress_bar_instance.setEnabled(True)
            if new_set_value != 0:
                progress_bar_instance.setValue(new_set_value)

            if increment_value != 0:
                progress_bar_instance.setValue(progress_bar_instance.value() + increment_value)
            if progress_bar_instance.isEnabled() and progress_bar_instance.value() != 0:
                progress_bar_instance.setEnabled(True)
        except:
            pass

class RemainingTime(QLabel):
    """Class containing the remaining time of the analysis"""

    def __init__(self, parent=None):
        QLabel.__init__(self, parent=parent)
        self.setMinimumSize(0, 0)
        self.setMaximumSize(self.size())
        self.setText("Time remaining : " + " " * 60)

    def update_remaining_time(self, progress_value, time_elapsed, done=False):
        """
        Update the remaining time
        Args:
            progress_value (float): Current progress bar value
            time_elapsed (float): Time elepased since the beginning of the analysis (in sec)
            done (bool): True if the analysis is done and false if still running

        """
        if not done:
            remaining_time = time_elapsed * (100 / progress_value)
            remaining_time_text = self.correct_time_converter(remaining_time)
            time_elapsed_text = self.correct_time_converter(time_elapsed)
            self.setText("Time remaining : " + time_elapsed_text + "/" + remaining_time_text)
        else:
            time_elapsed_text = self.correct_time_converter(time_elapsed)
            self.setText("Analysis done in " + time_elapsed_text + " " * 40)

    @staticmethod
    def correct_time_converter(time_to_convert):
        """
        Convert a float in a correct duration value
        Args:
            time_to_convert (float): Float value representing seconds to be converted in a correct duration with MM.SS

        Returns:
            time_text (str): String of the correct duration
        """
        time_to_convert_str = str(time_to_convert)
        dot_index = time_to_convert_str.find(".")
        if dot_index == -1:
            seconds = time_to_convert
            m_sec = "00"
        else:
            seconds = int(time_to_convert_str[:dot_index])
            if dot_index < len(time_to_convert_str) - 1:
                m_sec = time_to_convert_str[dot_index + 1:min(dot_index + 3, len(time_to_convert_str))]
            else:
                m_sec = "00"
        # converting in minutes
        minutes = seconds // 60
        seconds_remaining = str(seconds % 60)
        if len(seconds_remaining) == 1:
            seconds_remaining = "0" + seconds_remaining
        time_text = ""
        if minutes >= 1:
            minutes_str = str(minutes)
            if len(minutes_str) == 1:
                minutes_str = "0" + minutes_str
            time_text = time_text + minutes_str + ":"
        else:
            time_text = time_text + "00" + ":"
        time_text = time_text + seconds_remaining + "." + m_sec

        return time_text
