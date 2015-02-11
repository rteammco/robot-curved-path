import Tkinter as Tk
import math


class DemoUI():
  """Demo UI for the path computation stuff."""
  # computation constants
  CURVE_RATE = 1
  CURVE_RESOLUTION = 25
  # display object sizes
  POINT_SIZE = 5
  LINE_SIZE = 25
  # display colors
  FIELD_COLOR = "#00680A"
  ROBOT_COLOR = "white"
  BALL_COLOR = "red"
  OBSTACLE_COLOR = "blue"
  CTRL_POINT_COLOR = "black"
  TRIANGLE_COLOR = "yellow"
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
    self.robot = [width/2, height/2, 0, (0, 0)]
    self.ball = [width/2, 3*height/4, 0, (0, 0)]
    self.obstacles = []
    self.control_points = []
    self.ctrl_dist_to_base = 0
    self.dist_to_ball = 0
    self.update_dist_to_ball()

  def left_click_handle(self, event):
    """Handles action for a left-click event (set location)."""
    if self.mode_var.get() == self.SELECT_ROBOT:
      self.set_robot_pos(event.x, event.y)
      self.update_dist_to_ball()
    elif self.mode_var.get() == self.SELECT_BALL:
      self.set_ball_pos(event.x, event.y)
      self.update_dist_to_ball()
    else:
      self.add_obstacle(event.x, event.y)
    self.render()

  def right_click_handle(self, event):
    """Handles action for a right-click event (set orientation/trajectory)."""
    if self.mode_var.get() == self.SELECT_ROBOT:
      angle, normal = self.get_angle(self.robot[0], self.robot[1], event.x, event.y)
      if angle is not None:
        self.set_robot_orientation(angle, normal)
        self.render()
    elif self.mode_var.get() == self.SELECT_BALL:
      angle, normal = self.get_angle(self.ball[0], self.ball[1], event.x, event.y)
      if angle is not None:
        self.set_ball_trajectory(angle, normal)
        self.render()

  def get_angle(self, x1, y1, x2, y2):
    """
    Computes and returns the angle between points x1,y1 and x2,y2.
    Also returns the normal of the tangent vector of the two points.
    """
    if x1 == x2 and y1 == y2:
      return None
    x_diff = x2 - x1
    y_diff = y2 - y1
    norm = math.sqrt(x_diff*x_diff + y_diff*y_diff)
    normal = (x_diff / norm, y_diff / norm)
    return math.atan2(y_diff, x_diff), normal

  def update_dist_to_ball(self):
    """Computes the distance between the robot and the ball."""
    self.dist_to_ball = self.get_dist(self.robot[0], self.robot[1], self.ball[0], self.ball[1])

  def get_dist(self, x1, y1, x2, y2):
    """Returns the distance between the given two points."""
    return math.sqrt((y2 - y1)*(y2 - y1) + (x2 - x1)*(x2 - x1))

  def distance_to_line(self, x1, y1, x2, y2, x0, y0):
    """
    Computes the distance from point x0, y0 to the line defined by points
    x1, y1 and x2, y2.
    """
    top = abs((y2 - y1)*x0 - (x2 - x1)*y0 + x2*y1 - y2*x1)
    return top / self.get_dist(x1, y1, x2, y2)

  def compute_path(self):
    """Sets up the control point(s) for the path computation."""
    # compute the control point (and add to the list)
    control_point = self.compute_control_point()
    self.ctrl_dist_to_base = self.distance_to_line(
         self.robot[0], self.robot[1],
         self.ball[0], self.ball[1],
         control_point[0], control_point[1])
    if len(self.control_points) == 0:
      self.control_points.append(control_point)
    else:
      self.control_points[0] = control_point
    # use control point to calculate the Bezier curve
    self.render()

  def cubic_hermite_spline(self, t):
    """
    Computes the CHS path at position t [0, 1] using the pre-computed control
    point and angles (tangents).
    Returns the (x, y) position at time t,
    or (0, 0) when t is invalid or when the control point is undefined.
    """
    if t < 0 or t > 1:# or len(self.control_points) == 0:
      return (0, 0)
    t2 = t*t
    t3 = t2*t
    p0x, p0y = self.robot[0], self.robot[1]
    p1x, p1y = self.ball[0], self.ball[1]
    scalar = self.dist_to_ball * self.CURVE_RATE#self.ctrl_dist_to_base * self.CURVE_RATE
    m0x, m0y = scalar*self.robot[3][0], scalar*self.robot[3][1]
    m1x, m1y = -scalar*self.ball[3][0], -scalar*self.ball[3][1]
    x = (2*t3 - 3*t2 + 1)*p0x + (t3 - 2*t2 + t)*m0x +\
        (-2*t3 + 3*t2)*p1x + (t3 - t2)*m1x
    y = (2*t3 - 3*t2 + 1)*p0y + (t3 - 2*t2 + t)*m0y +\
        (-2*t3 + 3*t2)*p1y + (t3 - t2)*m1y
    return (x, y)

  def compute_control_point(self):
    """Computes the main control point for the path."""
    # compute slope and y-intercept for robot using orientation
    robot_slope = math.tan(self.robot[2])
    robot_intercept = self.robot[1] - robot_slope * self.robot[0]
    # compute slope and y-intercept for ball (using inverse trajectory)
    ball_slope = math.tan(self.ball[2])
    ball_intercept = self.ball[1] - ball_slope * self.ball[0]
    # solve for x where the lines meet
    x = (ball_intercept - robot_intercept) / (robot_slope - ball_slope)
    y = robot_slope * x + robot_intercept
    control_point = (x, y)
    return control_point

  def clear_all(self):
    """Clears all obstacles and the path from the screen."""
    self.obstacles = []
    self.control_points = []
    self.render()

  def set_robot_pos(self, x, y):
    """Sets the starting location of the robot, preserving orientation."""
    self.robot[0] = x
    self.robot[1] = y

  def set_robot_orientation(self, orientation, tangent):
    """Sets the robot's orientation, preserving location."""
    self.robot[2] = orientation
    self.robot[3] = tangent

  def set_ball_pos(self, x, y):
    """Sets the location of the ball, preserving trajectory."""
    self.ball[0] = x
    self.ball[1] = y

  def set_ball_trajectory(self, trajectory, tangent):
    """Sets the ball's desired trajectory, preserving location."""
    self.ball[2] = trajectory
    self.ball[3] = tangent

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
    # draw obstacles
    for pnt in self.obstacles:
      x = pnt[0]
      y = pnt[1]
      self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=self.OBSTACLE_COLOR, outline="")
    # draw control points (for the curve)
    for pnt in self.control_points:
      x = pnt[0]
      y = pnt[1]
      self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=self.CTRL_POINT_COLOR, outline="")
    # if the main control point exists, draw the triangle between it, and finally the path
    if len(self.control_points) > 0:
      start_x, start_y = self.control_points[0][0], self.control_points[0][1]
      end_x, end_y = self.robot[0], self.robot[1]
      self.canvas.create_line(start_x, start_y, end_x, end_y, fill=self.TRIANGLE_COLOR, dash=(4, 4))
      end_x, end_y = self.ball[0], self.ball[1]
      self.canvas.create_line(start_x, start_y, end_x, end_y, fill=self.TRIANGLE_COLOR, dash=(4, 4))
    last_x, last_y = self.robot[0], self.robot[1]
    for i in range(self.CURVE_RESOLUTION):
      t = float(i+1) / float(self.CURVE_RESOLUTION)
      x, y = self.cubic_hermite_spline(t)
      self.canvas.create_line(last_x, last_y, x, y, fill=self.PATH_COLOR)
      last_x, last_y = x, y
    # draw the ball, displaying its trajectory
    x = self.ball[0]
    y = self.ball[1]
    angle = self.ball[2]
    self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=self.BALL_COLOR, outline="")
    self.canvas.create_line(x, y, self.get_line_endpoints(x, y, angle), fill=self.BALL_COLOR)
    # draw the robot, displaying its orientation
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
