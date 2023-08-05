import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import cv2
# import time
from scipy import signal
import time

def ploting_power_spectrum(filtered_signal, raw_signal, title, times_to_mark, show_it, results_path, file_name):
    """
    Plot the power spectrum of 2 signals
    :param filtered_signal (array): signal that has been filterd
    :param raw_signal (array): raw signal, in which no filter has been applied
    :param title (str): plot title
    :param times_to_mark (list or np.array): None or float values, for each value, a dashed vertical line will be ploted
    at the x coordinate given.
    :param show_it (bool): if True, plot the figure
    :param results_path (str): path where toe save the figure
    :param file_name (str): file_name in which to save the figure
    :return:
    """
    amplitude_thresholds = [0.5, 1]
    sampling_rate = 20
    fourier_transform = np.fft.rfft(filtered_signal)
    abs_fourier_transform = np.abs(fourier_transform)
    power_spectrum = np.square(abs_fourier_transform)
    frequency = np.linspace(0, sampling_rate / 2, len(power_spectrum))

    fourier_transform = np.fft.rfft(raw_signal)
    abs_fourier_transform = np.abs(fourier_transform)
    original_power_spectrum = np.square(abs_fourier_transform)
    original_frequency = np.linspace(0, sampling_rate / 2, len(original_power_spectrum))

    min_value = min(np.min(filtered_signal), np.min(raw_signal))
    max_value = max(np.max(filtered_signal), np.max(raw_signal))

    if show_it:
        linewidth = 1
    else:
        # for pdf to zoom
        linewidth = 0.1
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.2))
    ax1.plot(filtered_signal, c="blue", zorder=10, linewidth=linewidth)
    ax1.plot(raw_signal, c="red", zorder=5, linewidth=linewidth)
    ax2.plot(frequency, power_spectrum, c="blue", zorder=10, linewidth=linewidth)
    ax2.plot(original_frequency, original_power_spectrum, c="red", zorder=5, linewidth=linewidth)
    if times_to_mark is not None:
        for time_to_mark in times_to_mark:
            ax1.vlines(time_to_mark, min_value,
                       max_value, color="black", linewidth=linewidth * 1.5,
                       linestyles="dashed", zorder=1)
    for amplitude_threshold in amplitude_thresholds:
        ax1.hlines(amplitude_threshold, 0, len(raw_signal) - 1,
                   color="black", linewidth=linewidth,
                   linestyles="dashed")
    plt.title(title)
    if show_it:
        plt.show()

    save_formats = ["png", "pdf"]
    if isinstance(save_formats, str):
        save_formats = [save_formats]
    for save_format in save_formats:
        fig.savefig(f'{results_path}/{file_name}.{save_format}',
                    format=f"{save_format}",
                    facecolor=fig.get_facecolor())

    plt.close()


def butter_bandstop_filter(data, lowcut, highcut, fs, order):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq

    i, u = signal.butter(order, [low, high], btype='bandstop')
    # y = signal.lfilter(i, u, data)
    # TODO: see if there is also a shift here
    # to correct shift (https://stackoverflow.com/questions/45098384/butterworth-filter-x-shift)
    y = signal.filtfilt(i, u, data)
    return y


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    # produce a shift in the signal
    # y = signal.lfilter(b, a, data)
    # to correct shift (https://stackoverflow.com/questions/45098384/butterworth-filter-x-shift)
    y = signal.filtfilt(b, a, data)
    return y


def z_score_normalization_by_luminosity_state(mvt_signal, luminosity_states, first_frame, last_frame,
                                              flatten_transitions):
    """
    Normalize the signal using z_score on chunks based on frames indices in luminosity_states determining the change
    is luminosity
    Args:
        mvt_signal (1d array):
        luminosity_states: list of frames index (int)
        first_frame: int
        last_frame: int
        flatten_transitions (bool): if True, we put frames around the luminosity change at the mean of the previous or
        following segment

    Returns:

    """
    # TODO: Find a way to normalize even if doesn't start by the frame 0
    # plt.plot(mvt_signal)
    # plt.title(f"Before normalization")
    # plt.show()
    # print(f"luminosity_states {luminosity_states}, first_frame {first_frame}, last_frame {last_frame}, "
    #       f"flatten_transitions {flatten_transitions}")
    mvt_signal = np.copy(mvt_signal)
    last_chunk_frame = first_frame
    if len(luminosity_states) == 0:
        luminosity_states = [last_frame + 1]
    # tell us if at least when change of luminosity happens betwwen first_frame and last_frame
    with_luminosy_state = False

    luminosity_state_index = -1
    for luminosity_change_frame in luminosity_states:
        if luminosity_change_frame < first_frame:
            continue

        luminosity_state_index += 1
        with_luminosy_state = True

        # print(f"luminosity_change_frame {luminosity_change_frame}, last_chunk_frame {last_chunk_frame}")
        if flatten_transitions:
            if last_chunk_frame == first_frame:
                mvt_signal[first_frame] = np.mean(mvt_signal[first_frame+1:min(luminosity_change_frame, last_frame + 1)])
            else:
                last_frame_to_use = min(luminosity_change_frame, last_frame + 1)
                if (last_chunk_frame+3) < last_frame_to_use:
                    # flattening the frame aroudn the change in luninosity
                    mvt_signal[last_chunk_frame:last_chunk_frame + 3] = \
                        np.mean(mvt_signal[last_chunk_frame + 3:last_frame_to_use])

                if last_chunk_frame - 2 >= 0:
                    if luminosity_state_index <= 1:
                        # luminosity_state_index should not be equal 0, as in that case last_chunk_frame == first_frame
                        mvt_signal[last_chunk_frame - 2:last_chunk_frame] = \
                            np.mean(mvt_signal[first_frame:last_chunk_frame - 2])
                    else:
                        mvt_signal[last_chunk_frame - 2:last_chunk_frame] = \
                            np.mean(mvt_signal[luminosity_states[luminosity_state_index - 2]:last_chunk_frame - 2])

        if luminosity_change_frame > last_frame:
            mvt_signal[last_chunk_frame:last_frame+1] = stats.zscore(mvt_signal[last_chunk_frame:last_frame+1])
            last_chunk_frame = last_frame+1
            # plt.plot(mvt_signal)
            # plt.title(f"state {luminosity_state_index}, before break")
            # plt.show()
            break

        mvt_signal[last_chunk_frame:luminosity_change_frame] = \
            stats.zscore(mvt_signal[last_chunk_frame:luminosity_change_frame])
        last_chunk_frame = luminosity_change_frame
        # plt.plot(mvt_signal)
        # plt.title(f"state {luminosity_state_index}")
        # plt.show()

    if last_chunk_frame < last_frame:
        if flatten_transitions and (last_frame - last_chunk_frame > 5) and with_luminosy_state:
            mvt_signal[last_chunk_frame:last_chunk_frame + 3] = np.mean(mvt_signal[last_chunk_frame + 3:last_frame+1])
            if len(luminosity_states) > 2:
                mvt_signal[last_chunk_frame - 2:last_chunk_frame] = \
                    np.mean(mvt_signal[first_frame:last_chunk_frame - 2])
        mvt_signal[last_chunk_frame:last_frame+1] = stats.zscore(mvt_signal[last_chunk_frame:last_frame+1])
        # plt.plot(mvt_signal)
        # plt.title(f"Last chunk")
        # plt.show()

    # plt.plot(mvt_signal)
    # plt.title(f"Before return")
    # plt.show()

    return mvt_signal

def z_score_normalization_by_luminosity_state_old_version(mvt_signal, luminosity_states, n_frames, flatten_transitions):
    """
    Normalize the signal using z_score on chunks based on frames indices in luminosity_states determining the change
    is luminosity
    Args:
        mvt_signal (1d array):
        luminosity_states: list of frames index (int)
        n_frames: int, number of frames, starting at zero. Could be less than len(mvt_signal) in case we don't
        want to z-score it all
        flatten_transitions (bool): if True, we put frames around the luminosity change at the mean of the following
        segment

    Returns:

    """
    # TODO: Find a way to normalize even if doesn't start by the frame 0
    # plt.plot(mvt_signal)
    # plt.title(f"Before normalization")
    # plt.show()
    # print(f"luminosity_states {luminosity_states}, n_frames {n_frames}")
    mvt_signal = np.copy(mvt_signal)
    last_chunk_frame = 0
    if len(luminosity_states) == 0:
        luminosity_states = [n_frames + 1]
    for luminosity_state_index, luminosity_change_frame in enumerate(luminosity_states):

        # print(f"luminosity_change_frame {luminosity_change_frame}, last_chunk_frame {last_chunk_frame}")
        if flatten_transitions:
            if last_chunk_frame == 0:
                # print(f"mean_value : {np.mean(mvt_signal[1:min(luminosity_change_frame, n_frames)])}")
                mvt_signal[0] = np.mean(mvt_signal[1:min(luminosity_change_frame, n_frames)])
            else:
                last_frame = min(luminosity_change_frame, n_frames)
                # print(f"mean_value : {np.mean(mvt_signal[last_chunk_frame+3:last_frame])}")
                # flattening the frame aroudn the change in luninosity
                mvt_signal[last_chunk_frame:last_chunk_frame + 3] = np.mean(mvt_signal[last_chunk_frame + 3:last_frame])

                if luminosity_state_index == 1:
                    mvt_signal[last_chunk_frame - 2:last_chunk_frame] = \
                        np.mean(mvt_signal[:last_chunk_frame - 2])
                else:
                    mvt_signal[last_chunk_frame - 2:last_chunk_frame] = \
                        np.mean(mvt_signal[luminosity_states[luminosity_state_index - 2]:last_chunk_frame - 2])

        if luminosity_change_frame > n_frames:
            mvt_signal[last_chunk_frame:n_frames] = stats.zscore(mvt_signal[last_chunk_frame:n_frames])
            last_chunk_frame = n_frames
            # plt.plot(mvt_signal)
            # plt.title(f"state {luminosity_state_index}, before break")
            # plt.show()
            break

        mvt_signal[last_chunk_frame:luminosity_change_frame] = \
            stats.zscore(mvt_signal[last_chunk_frame:luminosity_change_frame])
        last_chunk_frame = luminosity_change_frame
        # plt.plot(mvt_signal)
        # plt.title(f"state {luminosity_state_index}")
        # plt.show()

    if last_chunk_frame < n_frames:
        if flatten_transitions and (n_frames - last_chunk_frame > 5):
            mvt_signal[last_chunk_frame:last_chunk_frame + 3] = np.mean(mvt_signal[last_chunk_frame + 3:n_frames])
            mvt_signal[last_chunk_frame - 2:last_chunk_frame] = \
                np.mean(mvt_signal[luminosity_states[-2]:last_chunk_frame - 2])
        mvt_signal[last_chunk_frame:n_frames] = stats.zscore(mvt_signal[last_chunk_frame:n_frames])
        # plt.plot(mvt_signal)
        # plt.title(f"Last chunk")
        # plt.show()

    # plt.plot(mvt_signal)
    # plt.title(f"Before return")
    # plt.show()

    return mvt_signal


def threshold_frame(img_frame, image_thresholds):
    """
    Apply thresholds to an image so the image will composed of only 2 to 3 pixels intensities
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


def from_camera_to_piezo_signal(roi_coords_dict, image_thresholds_dict, frames_dict, movie_readers_dict,
                                bodyparts, movie_id_by_bodypart_dict, progress_bar=None):
    """

    :param roi_coords_dict: dict with key bodypart and value for int/float x, y, with, height. x_y represents the coord
    of the lower left bottom of the ROI.
    :param image_thresholds_dict: key is the bodypart, value is a tuple of one or 2 int representing the thresholds
    :param frames_dict: key is movie_id, indicate how many frames should be analysed for a given movie bodyparts
    :param movie_readers_dict: key is a movie_id, value is an instance of OpenCvVideoReader
    :param bodyparts: list of str repsenting the bodypart to process
    :param movie_id_by_bodypart_dict: key is a bodypart, value is the movie_id corresponding to the bodypart
    :param progress_bar: None or instance of ProgressBar, is not None, the progress bar will be updated
    :return: dict with key bodypart, and value a 1d np.array with the piezo signal (length of the full movie, only
    the frames given in frames_dict have been processed)
    """
    analysis_start_time = time.time()
    # TODO: add doc
    # roi_coords_dict (dict): key is the bodypart, value is a list of 4 int representing the x y coordinates of the
    # left bottom corner of the roi, and witdth and height of the roi so : [x, y, width, length]
    piezo_signal_dict = dict()
    movie_ids = set([movie_id_by_bodypart_dict[bodypart] for bodypart in bodyparts])

    n_steps = 0
    progress_bar_value = 0
    # computing n_steps, useful to update progress bar
    if progress_bar is not None:
        n_frames_to_process = 0
        movie_ids_for_steps = [movie_id_by_bodypart_dict[bodypart] for bodypart in bodyparts]
        for movie_id in movie_ids_for_steps:
            n_frames_in_movie = frames_dict[movie_id][-1] - frames_dict[movie_id][0]
            n_frames_to_process += n_frames_in_movie
        n_steps = n_frames_to_process


    # looping through movie_id so we save memory by reading the frame image only once
    for movie_id in movie_ids:
        # key is a string representing the bodypart,
        # value is a 1d array representing the diff between each binarized frame
        # mvt_by_bodypart = dict()
        last_frame_by_bodypart = dict()
        n_frames_in_movie = movie_readers_dict[movie_id].length
        last_frame_to_read = frames_dict[movie_id][-1]
        movie_readers_dict[movie_id].start(first_frame_to_read=frames_dict[movie_id][0],
                                           last_frame_to_read=last_frame_to_read)
        # giving him a bit of advance
        time.sleep(5.0)
        # for frame in frames:
        # going though the frames
        frame = frames_dict[movie_id][0]

        # bodyparts in this movie
        bodyparts_in_movie = []
        for bodypart in bodyparts:
            if movie_id == movie_id_by_bodypart_dict[bodypart]:
                bodyparts_in_movie.append(bodypart)

        while True:
            # all_frames_on_queue
            if not movie_readers_dict[movie_id].more():
                if not movie_readers_dict[movie_id].all_frames_on_queue():
                    # then it means all frames are not in queue, then we make a break to let the thread fill a bit
                    time.sleep(1)
                else:
                    break
            # if frame % 2000 == 0:
            #     print(f"Processing frame {frame}")
            # img_frame = movie_dict[side].get_frame(frame)
            img_frame = movie_readers_dict[movie_id].read()
            # plt.imshow(img_frame, 'gray')
            # plt.show()

            for bodypart in bodyparts_in_movie:
                # diff of pixels between 2 consecutive binary frames
                if bodypart not in piezo_signal_dict:
                    piezo_signal_dict[bodypart] = np.zeros(n_frames_in_movie, dtype="float")
                    last_frame_by_bodypart[bodypart] = None

                # if frame == 0:
                #     print(f"bodypart_config {side}_{bodypart} : {bodypart_config}")
                x_bottom_left, y_bottom_left, width, height = roi_coords_dict[bodypart]

                img_frame_cropped = img_frame[y_bottom_left:y_bottom_left+height,
                                    x_bottom_left:x_bottom_left + width]
                # start_time = time.time()
                img_frame_cropped_bin = threshold_frame(img_frame_cropped, image_thresholds_dict[bodypart])
                # stop_time = time.time()
                # print(f"Time to binarize one frame: "
                #       f"{np.round(stop_time - start_time, 5)} s")
                # if frame < 1:
                #     plt.imshow(img_frame_cropped_bin, 'gray')
                #     plt.show()

                # diff between two frames, to build the movement 1d array
                if last_frame_by_bodypart[bodypart] is not None:
                    piezo_signal_dict[bodypart][frame] = np.sum(np.abs(np.subtract(last_frame_by_bodypart[bodypart],
                                                                                   img_frame_cropped_bin)))
                    # mvt[frame] = np.sum(last_frame == img_frame)
                last_frame_by_bodypart[bodypart] = img_frame_cropped_bin

                # updating progress bar every 5 frame
                if (progress_bar is not None) and (frame % 10 == 0):
                    time_elapsed = time.time() - analysis_start_time
                    increment_value = 100 / (n_steps / 10)
                    progress_bar_value += increment_value
                    # print(f"time_elapsed {time_elapsed}, increment_value {increment_value}")
                    progress_bar.update_progress_bar(time_elapsed=time_elapsed, increment_value=0,
                                                     new_set_value=progress_bar_value)

            frame += 1
        # movie_readers_dict[movie_id].stop()

    if progress_bar is not None:
        time_elapsed = time.time() - analysis_start_time
        progress_bar.update_progress_bar(time_elapsed=time_elapsed, increment_value=0, new_set_value=100)
    return piezo_signal_dict


def process_piezo_signal(signal_data, luminosity_states, first_frame, last_frame, apply_lowpass_filter,
                         apply_bandstop_filter=False,
                         cutoff=1.5, lowcut=2.8, highcut=3.5, fs=20, order=10):
    """

    :param signal_data (1d array):
    :param luminosity_states (list or array): int representing the frames at which the luminosity change
    :param first_frame (int): first_frame to process
    :param last_frame: (int) last frame to process
    :param apply_lowpass_filter (bool): if True apply a low pass filter from cutoff, sampling rate of fs and order.
    If False a bandstop filter is applied between lowcut and hightcut
    :param cutoff (float): cutoff value for the lowpass filter
    :param lowcut (float):
    :param highcut (float):
    :param fs (float): Signal sampling rate
    :param order (int): order for the filtering
    :return: two 1d arrays representing the normalized signal (z_score by luminisoty level) and
    the fully processed signal (with filter applied)
    """

    # normalization of the signal using z-score
    mvt = z_score_normalization_by_luminosity_state(mvt_signal=signal_data,
                                                    luminosity_states=luminosity_states,
                                                    first_frame=first_frame,
                                                    last_frame=last_frame,
                                                    flatten_transitions=True)
    normalized_signal = np.copy(mvt)

    if apply_lowpass_filter:
        # remove frequency higher than 2 Hz
        mvt = butter_lowpass_filter(data=mvt, cutoff=cutoff, fs=fs, order=order)
    if apply_bandstop_filter:
        # bandstop filter
        # issue with bandstop, session without laser have a ten-fold lower amplitude
        mvt = butter_bandstop_filter(data=mvt, lowcut=lowcut, highcut=highcut, fs=fs, order=order)
        # mvt = butter_bandstop_filter(data=mvt, lowcut=5.3, highcut=5.5, fs=20, order=6)
        # mvt = butter_bandstop_filter(data=mvt, lowcut=8, highcut=8.6, fs=20, order=6)

    if apply_lowpass_filter or apply_bandstop_filter:
        # second normalization after filtering
        fully_processed_signal = z_score_normalization_by_luminosity_state(mvt_signal=mvt,
                                                                           luminosity_states=luminosity_states,
                                                                           first_frame=first_frame,
                                                                           last_frame=last_frame,
                                                                           flatten_transitions=False)
    return normalized_signal, fully_processed_signal
