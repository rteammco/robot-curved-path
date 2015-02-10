import Tkinter as Tk
import math


class DemoUI():
  """Demo UI for the path computation stuff."""
  # display object sizes
  POINT_SIZE = 5
  LINE_SIZE = 25
  # display colors
  FIELD_COLOR = "#00680A"
  ROBOT_COLOR = "white"
  BALL_COLOR = "red"
  OBSTACLE_COLOR = "blue"
  PATH_COLOR = "green"
  # option constants
  SELECT_ROBOT = 1
  SELECT_BALL = 2
  SELECT_OBSTACLE = 3

  def __init__(self, width, height):
    """Initialize the window and default object locations (no control points)."""
    # initialize window and event listeners
    self.main_window = Tk.Tk()
    self.main_window.title("Demo")
    self.canvas = Tk.Canvas(self.main_window, width=width, height=height, background=self.FIELD_COLOR)
    self.canvas.bind("<Button-1>", self.left_click_handle)
    self.canvas.bind("<Button-2>", self.right_click_handle)
    self.canvas.pack()
    # set the control UI: buttons and click action selection
    self.mode_var = Tk.IntVar()
    self.mode_var.set(1)
    options = [("Robot Location", self.SELECT_ROBOT),
               ("Ball Location", self.SELECT_BALL),
               ("Add Obstacle", self.SELECT_OBSTACLE)]
    for option, val in options:
      Tk.Radiobutton(self.main_window, text=option, variable=self.mode_var,
                     indicatoron=0, value=val).pack(anchor=Tk.CENTER)
    Tk.Button(self.main_window, text="Compute Path",
              command=self.compute_path).pack(anchor=Tk.CENTER)
    Tk.Button(self.main_window, text="Clear Everything",
              command=self.clear_all).pack(anchor=Tk.CENTER)
    # initialize object locations
    self.robot = [width/2, height/2, 0]
    self.ball = [width/2, 3*height/4, 0]
    self.obstacles = []

  def left_click_handle(self, event):
    """Handles action for a left-click event (set location)."""
    if self.mode_var.get() == self.SELECT_ROBOT:
      self.set_robot_pos(event.x, event.y)
    elif self.mode_var.get() == self.SELECT_BALL:
      self.set_ball_pos(event.x, event.y)
    else:
      self.add_obstacle(event.x, event.y)
    self.render()

  def right_click_handle(self, event):
    """Handles action for a left-click event (set location)."""
    if self.mode_var.get() == self.SELECT_ROBOT:
      pass
    elif self.mode_var.get() == self.SELECT_BALL:
      pass

  def compute_path(self):
    """Computes and renders the desired path."""
    pass

  def clear_all(self):
    """Clears all obstacles and the path from the screen."""
    self.obstacles = []
    self.render()

  def set_robot_pos(self, x, y):
    """Sets the starting location of the robot, preserving orientation."""
    self.robot[0] = x
    self.robot[1] = y

  def set_robot_orientation(self, orientation):
    """Sets the robot's orientation, preserving location."""
    self.robot[2] = orientation

  def set_ball_pos(self, x, y):
    """Sets the location of the ball, preserving trajectory."""
    self.ball[0] = x
    self.ball[1] = y

  def set_ball_trajectory(self, trajectory):
    """Sets the ball's desired trajectory, preserving location."""
    self.ball[2] = trajectory

  def add_obstacle(self, x, y):
    """Adds an obstacle and redraws the simulation."""
    self.obstacles.append((x, y))

  def get_line_endpoints(self, x, y, angle):
    """Returns the end points of a line (LINE_SIZE long) given the angle and start point."""
    end_x = int(x + self.LINE_SIZE * math.cos(angle))
    end_y = int(y + self.LINE_SIZE * math.sin(angle))
    return (end_x, end_y)

  def render(self):
    """Clears the canvas, and draws everything again."""
    self.canvas.delete("all")
    r = self.POINT_SIZE
    for pnt in self.obstacles:
      x = pnt[0]
      y = pnt[1]
      self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=self.OBSTACLE_COLOR, outline="")
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
  print "Hello!"
  w = DemoUI(800, 480)
  w.render()
  w.main_window.mainloop()
  print "Goodbye."
