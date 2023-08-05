from abc import abstractmethod
from cv2 import VideoCapture
from threading import Thread
import cv2
import os

import sys

# from: https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/
# import the Queue class from Python 3
if sys.version_info >= (3, 0):
	from queue import Queue
# otherwise, import the Queue class for Python 2.7
else:
	raise Exception("Works only with Python 3")

class VideoReaderWrapper:
    """
        An abstract class that should be inherited in order to create a specific video format wrapper.
        A class can be created using either different packages or aim at specific format.

    """

    def __init__(self):
        self._length = None
        self._width = None
        self._height = None
        self._fps = None

    @property
    def length(self):
        return self._length

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def fps(self):
        return self._fps

    @abstractmethod
    def close_reader(self):
        pass


class OpenCvVideoReader(VideoReaderWrapper):
    """
    Use OpenCv to read video
    see https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/
    """

    def __init__(self, video_file_name, queueSize=128):
        """

        Args:
            video_file_name:
            queueSize : The maximum number of frames to store in the queue.
            This value defaults to 128 frames, but you depending on (1) the frame dimensions
            of your video and (2) the amount of memory you can spare, you may want to raise/lower this value.
        """
        VideoReaderWrapper.__init__(self)

        self.video_file_name = video_file_name
        self.basename_video_file_name = os.path.basename(video_file_name)

        # Create a VideoCapture object and read from input file
        # If the input is the camera, pass 0 instead of the video file name
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.video_capture = VideoCapture(self.video_file_name)
        self.stopped = False

        if self.video_capture.isOpened() == False:
            raise Exception(f"Error opening video file {self.video_file_name}")

        # initialize the queue used to store frames read from
        # the video file
        self.queueSize = queueSize
        self.video_queue = Queue(maxsize=queueSize)

        # length in frames
        self._length = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        # in pixels
        self._width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # frame per seconds
        self._fps = self.video_capture.get(cv2.CAP_PROP_FPS)

        # for the thread
        self.next_frame_to_read = 0
        self.last_frame_to_read = self._length - 1

        print(f"OpenCvVideoReader init for {self.basename_video_file_name}: "
              f"self.width {self.width}, self.height {self.height}, n frames {self._length}")

    def start(self, first_frame_to_read, last_frame_to_read):
        # start a thread to read frames from the file video stream
        self.next_frame_to_read = first_frame_to_read
        self.last_frame_to_read = min(self._length - 1, last_frame_to_read)
        self.video_queue = Queue(maxsize=self.queueSize)
        self.stopped = False
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

    def update(self):
        # keep looping infinitely
        while True:
            # if the thread indicator variable is set, stop the
            # thread
            if self.stopped:
                return
            # otherwise, ensure the queue has room in it
            if not self.video_queue.full():
                if self.next_frame_to_read > self.last_frame_to_read:
                    self.stop()
                    return
                # read the next frame from the file
                self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, self.next_frame_to_read)
                (grabbed, frame) = self.video_capture.read()
                # if the `grabbed` boolean is `False`, then we have
                # reached the end of the video file
                if not grabbed:
                    self.stop()
                    return
                # add the frame to the queue
                self.video_queue.put(frame)
                self.next_frame_to_read += 1

    def read(self):
        # return next frame in the queue
        return self.video_queue.get()

    def all_frames_on_queue(self):
        """
        Return True if all frames have been processed
        Returns:

        """
        if self.next_frame_to_read > self.last_frame_to_read:
            return True

    def more(self):
        return self.video_queue.qsize() > 0

    def get_frame(self, frame_index):
        if (frame_index >= self._length) or (frame_index < 0):
            return None

        # The first argument of cap.set(), number 2 defines that parameter for setting the frame selection.
        # Number 2 defines flag CAP_PROP_POS_FRAMES which is
        # a 0-based index of the frame to be decoded/captured next.
        # The second argument defines the frame number in range 0.0-1.0
        # frame_no = frame_index / self._length
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

        # Read the next frame from the video. If you set frame 749 above then the code will return the last frame.
        # 'res' is boolean result of operation, one may use it to check if frame was successfully read.
        res, frame = self.video_capture.read()

        if res:
            return frame
        else:
            return None

    def close_reader(self):
        # When everything done, release the capture
        self.video_capture.release()
        cv2.destroyAllWindows()
