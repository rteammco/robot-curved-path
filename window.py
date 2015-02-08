import Tkinter as Tk
import math


class DemoUI():
  """Demo UI for the path computation stuff."""
  POINT_SIZE = 5
  LINE_SIZE = 25
  FIELD_COLOR = "#00680A"
  ROBOT_COLOR = "white"
  BALL_COLOR = "red"
  CTRL_POINT_COLOR = "blue"
  PATH_COLOR = "green"

  def __init__(self, width, height):
    """Initialize the window and default object locations (no control points)."""
    # initialize window and event listeners
    self.main_window = Tk.Tk()
    self.main_window.title("Demo")
    self.canvas = Tk.Canvas(self.main_window, width=width, height=height, background=self.FIELD_COLOR)
    self.canvas.bind("<Button-1>", self.left_click_handle)
    self.canvas.bind("<Button-2>", self.right_click_handle)
    self.canvas.pack()
    # set the control UI
    self.mode_var = Tk.IntVar()
    self.mode_var.set(1)
    options = [("Robot Location", 1), ("Ball Location", 2), ("Add Control Point", 3)]
    for option, val in options:
      Tk.Radiobutton(self.main_window, text=option, variable=self.mode_var,
                     indicatoron=0, value=val).pack(anchor=Tk.CENTER)
    Tk.Button(self.main_window, text="Clear Control Points",
              command=self.clear_all).pack(anchor=Tk.CENTER)
    # initialize object locations
    self.robot = (width/2, height/2, 0)
    self.ball = (width/2, 3*height/4, 0)
    self.control_points = []

  def left_click_handle(self, event):
    if self.mode_var.get() == 1:
      self.set_robot_pos(event.x, event.y, 0)
    elif self.mode_var.get() == 2:
      self.set_ball_pos(event.x, event.y, 0)
    else:
      self.add_control_point(event.x, event.y)
    self.render()

  def right_click_handle(self, event):
    print event.x, event.y

  def clear_all(self):
    """Clears all control points from the screen."""
    self.control_points = []
    self.render()

  def set_robot_pos(self, x, y, orientation):
    """Sets the starting location and orientation of the robot."""
    self.robot = (x, y, orientation)

  def set_ball_pos(self, x, y, trajectory):
    """Sets the location and desired trajectory of the ball."""
    self.ball = (x, y, trajectory)

  def add_control_point(self, x, y):
    """Adds and draws new path control point in the simulation."""
    self.control_points.append((x, y))

  def get_line_endpoints(self, x, y, angle):
    """Returns the end points of a line (LINE_SIZE long) given the angle and start point."""
    end_x = int(x + self.LINE_SIZE * math.cos(angle))
    end_y = int(y + self.LINE_SIZE * math.sin(angle))
    return (end_x, end_y)

  def render(self):
    """Clears the canvas, and draws everything again."""
    self.canvas.delete("all")
    r = self.POINT_SIZE
    for pnt in self.control_points:
      x = pnt[0]
      y = pnt[1]
      self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=self.CTRL_POINT_COLOR, outline="")
    x = self.ball[0]
    y = self.ball[1]
    angle = self.ball[2]
    self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=self.BALL_COLOR, outline="")
    self.canvas.create_line(x, y, self.get_line_endpoints(x, y, angle), fill=self.BALL_COLOR)
    x = self.robot[0]
    y = self.robot[1]
    angle = self.robot[2]
    self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=self.ROBOT_COLOR, outline="")
    self.canvas.create_line(x, y, self.get_line_endpoints(x, y, angle), fill=self.ROBOT_COLOR)


if __name__ == "__main__":
  print "hello"
  w = DemoUI(800, 480)
  w.render()
  w.main_window.mainloop()
  print "done"
