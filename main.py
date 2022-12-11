import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import tkinter as tk
from tkinter.filedialog import *
from PIL import ImageGrab
import numpy as np
import cv2
import time

time.sleep(1)
class MyWidget(QtWidgets.QWidget):
  def __init__(self):
    super().__init__()
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    self.setGeometry(0, 0, screen_width, screen_height)
    self.setWindowTitle(' ')
    self.begin = QtCore.QPoint()
    self.end = QtCore.QPoint()
    self.setWindowOpacity(0.3)
    QtWidgets.QApplication.setOverrideCursor(
        QtGui.QCursor(QtCore.Qt.CrossCursor)
    )
    self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    print('Capture the screen...')
    self.show()

  def paintEvent(self, event):
    qp = QtGui.QPainter(self)
    qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
    qp.setBrush(QtGui.QColor(128, 128, 255, 128))
    qp.drawRect(QtCore.QRect(self.begin, self.end))

  # mouse press cordinates
  def mousePressEvent(self, event):
    self.begin = event.pos()
    self.end = self.begin
    self.update()

  # mouse release cordinates
  def mouseMoveEvent(self, event):
    self.end = event.pos()
    self.update()

  # get above cords to mark x1, x2, y1, y2
  def mouseReleaseEvent(self, event):
    self.close()

    x1 = min(self.begin.x(), self.end.x())
    y1 = min(self.begin.y(), self.end.y())
    x2 = max(self.begin.x(), self.end.x())
    y2 = max(self.begin.y(), self.end.y())

    # save video
    save_path = asksaveasfilename()
    file_name = save_path+"_video.mp4"

    width = x2 + x1
    height = y2 + y1
    
    fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
    captured_video = cv2.VideoWriter(file_name, fourcc, 20.0, (width, height))

    while True:
      img = ImageGrab.grab(bbox=(0, 0, width, height))
      img_np = np.array(img)
      img_final = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
      cv2.imshow("Screen Recorder", img_final)
      captured_video.write(img_final)
      if cv2.waitKey(10) == ord("q"):
        break

    cv2.destroyAllWindows()


if __name__ == '__main__':
  app = QtWidgets.QApplication(sys.argv)
  window = MyWidget()
  window.show()
  app.aboutToQuit.connect(app.deleteLater)
  sys.exit(app.exec_())