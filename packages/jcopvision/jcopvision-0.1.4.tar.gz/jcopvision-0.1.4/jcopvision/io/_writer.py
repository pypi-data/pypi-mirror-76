import cv2
from jcopvision.exception import IncorrectExtensionError


class BaseWriter:
    def __init__(self, output_path, width, height, fps, fourcc):
        self.width = int(width)
        self.height = int(height)
        self._writer = cv2.VideoWriter(output_path, fourcc, fps, (self.width, self.height))

    def write(self, frame):
        h, w, c = frame.shape
        if (w != self.width) | (h != self.height):
            frame = cv2.resize(frame, (self.width, self.height))
        self._writer.write(frame)

    def close(self):
        self._writer.release()


class MP4Writer(BaseWriter):
    """
    A video writer with mp4 compression.
    """
    def __init__(self, output_path, width, height, fps):
        if not output_path.endswith(".mp4"):
            raise IncorrectExtensionError("output_path should have .mp4 extension")

        fourcc = cv2.VideoWriter_fourcc(*"MP4V")
        super().__init__(output_path, width, height, fps, fourcc)


class AVIWriter(BaseWriter):
    """
    A video writer with avi compression.
    """
    def __init__(self, output_path, width, height, fps):
        if not output_path.endswith(".avi"):
            raise IncorrectExtensionError("output_path should have .avi extension")

        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        super().__init__(output_path, width, height, fps, fourcc)

