import tkinter as tk
from tkinter import simpledialog

import clipping
import rasterization
import transformation2d

import math


def euclidean_distance(x1, y1, x2, y2):
    """
        Calculates the Euclidean distance between two points in a two-dimensional plane.

        Parameters:
            x1 (float): The x-coordinate of the first point.
            y1 (float): The y-coordinate of the first point.
            x2 (float): The x-coordinate of the second point.
            y2 (float): The y-coordinate of the second point.

        Returns:
            float: The Euclidean distance between the two points.

        Euclidean distance is calculated using the formula:
            distance = sqrt((x2 - x1)^2 + (y2 - y1)^2)
        """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


class CartesianPlane(tk.Canvas):
    """
    Custom canvas widget representing a Cartesian plane for graphical operations.

    Parameters:
        master (tk.Widget): The parent widget.
        **kwargs: Additional keyword arguments to pass to the Canvas constructor.

    Attributes:
        origin (tuple): The origin point of the Cartesian plane.
        drawing_line_dda (bool): Flag indicating whether DDA line drawing mode is active.
        drawing_line_bresenham (bool): Flag indicating whether Bresenham line drawing mode is active.
        drawing_circle_bresenham (bool): Flag indicating whether Bresenham circle drawing mode is active.
        drawing_cohen_clipping (bool): Flag indicating whether Cohen-Sutherland clipping mode is active.
        drawing_liang_clipping (bool): Flag indicating whether Liang-Barsky clipping mode is active.
        edges (tuple): The coordinates of the clipping rectangle edges.
        lines (list): List containing tuples representing lines [(x1, y1), (x2, y2)].
        circles (list): List containing tuples representing circles [(center_x, center_y), radius].

    Methods:
        _on_resize(event): Event handler for canvas resize.
        draw_axes(): Draws the x and y axes on the canvas.
        cartesian_plan_coordinates(x, y): Converts canvas coordinates to Cartesian plane coordinates.
        get_pixel_coordinates(x, y): Converts Cartesian plane coordinates to canvas pixel coordinates.
        _on_mouse_move(event): Event handler for mouse movement.
        _on_click(event): Event handler for mouse clicks.
        translate_points(delta_x, delta_y): Translates all points by specified deltas.
        rotate_lines(angle): Rotates all lines by the specified angle.
        scale(factor): Scales all lines and circles by the specified factor.
        reflect(axis): Reflects all lines and circles across the specified axis.
        draw_pixel(x, y, color): Draws a pixel on the canvas at the specified coordinates with the given color.
        on_click_list(): Prints the list of lines to the console.
        toggle_cohen_clipping(): Activates Cohen-Sutherland clipping mode.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(bg="white", highlightthickness=0)
        self.bind("<Configure>", self._on_resize)
        self.bind("<Motion>", self._on_mouse_move)
        self.bind("<Button-1>", self._on_click)

        self.origin = None
        self.drawing_line_dda = False
        self.drawing_line_bresenham = False
        self.drawing_circle_bresenham = False
        self.drawing_cohen_clipping = False
        self.drawing_liang_clipping = False
        self.edges = None

        self.lines = []
        self.circles = []

    def _on_resize(self, event):
        """Handles canvas resize event."""
        self.update()
        self.origin = (self.winfo_width() / 2, self.winfo_height() / 2)
        self.draw_axes()

    def draw_axes(self):
        """Draws the x and y axes on the canvas."""
        self.delete("axes")
        width = self.winfo_width()
        height = self.winfo_height()
        self.create_line(0, self.origin[1], width, self.origin[1], fill="black", tags="axes")  # x axis
        self.create_line(self.origin[0], 0, self.origin[0], height, fill="black", tags="axes")  # y axis

    def cartesian_plan_coordinates(self, x, y):
        """Converts canvas coordinates to Cartesian plane coordinates."""
        if not self.origin:
            self.origin = (self.winfo_width() / 2, self.winfo_height() / 2)
        return x - self.origin[0], self.origin[1] - y

    def get_pixel_coordinates(self, x, y):
        """Converts Cartesian plane coordinates to canvas pixel coordinates."""
        if not self.origin:
            self.origin = (self.winfo_width() / 2, self.winfo_height() / 2)
        return x + self.origin[0], self.origin[1] - y

    def _on_mouse_move(self, event):
        """Event handler for mouse movement."""
        x, y = self.cartesian_plan_coordinates(event.x, event.y)
        self.master.coordinate_label.config(text=f"x: {x:.2f} | y: {y:.2f}")

    def _on_click(self, event):
        """Event handler for mouse clicks."""
        print(f"Clicked pixel: ({event.x - self.origin[0]},{event.y - self.origin[1]})")
        print(f"Clicked coordinate: ({event.x},{event.y})\n")

        x, y = event.x, event.y
        cX, cY = self.cartesian_plan_coordinates(x, y)
        self.draw_pixel(x, y, (0, 0, 0))

        if self.drawing_line_dda:
            if not self.edges:
                self.edges = (event.x, event.y)
            else:
                rasterization.draw_DDA_line(self.edges[0], self.edges[1], event.x, event.y, self, color=(0, 0, 0))
                self.lines.append(((self.edges[0], self.edges[1]), (event.x, event.y)))
                self.edges = None
        elif self.drawing_line_bresenham:
            if not self.edges:
                self.edges = (event.x, event.y)
            else:
                rasterization.draw_Bresenham_line(self.edges[0], self.edges[1], event.x, event.y, self, (0, 0, 255))
                self.lines.append(((self.edges[0], self.edges[1]), (event.x, event.y)))
                self.edges = None
        elif self.drawing_circle_bresenham:
            if not self.edges:
                self.edges = (event.x, event.y)
            else:
                rasterization.draw_Bresenham_circle(self.edges[0], self.edges[1],
                                                    euclidean_distance(self.edges[0], self.edges[1], event.x, event.y),
                                                    self, color=(0, 0, 0))
                self.circles.append(((self.edges[0], self.edges[1]),
                                     euclidean_distance(self.edges[0], self.edges[1], event.x, event.y)))
                self.edges = None
        elif self.drawing_cohen_clipping:
            if not self.edges:
                self.edges = (event.x, event.y)
            else:
                clipped_lines = []

                print()
                print(str(self.lines))
                for line in self.lines:
                    accepted, l = clipping.clipping_cohen_sutherland(line[0][0], line[0][1], line[1][0], line[1][1],
                                                                     self.edges, (event.x, event.y), self)
                    if accepted:
                        clipped_lines.append(l)
                print(str(clipped_lines))

                self.delete("all")
                self.draw_axes()

                self.create_rectangle(*self.edges, (event.x, event.y), outline="red")

                self.lines = clipped_lines
                self.edges = None
                self.drawing_cohen_clipping = False
                for line in self.lines:
                    rasterization.draw_DDA_line(line[0][0], line[0][1], line[1][0], line[1][1], self, (0, 0, 0))
        elif self.drawing_liang_clipping:
            if not self.edges:
                self.edges = (event.x, event.y)
            else:
                clipped_lines = []

                for line in self.lines:
                    accepted, l = clipping.clipping_liang_barsky(line[0][0], line[0][1], line[1][0], line[1][1],
                                                                 self.edges[0], self.edges[1], event.x, event.y, self)
                    if accepted:
                        clipped_lines.append(l)

                self.delete("all")
                self.draw_axes()

                self.create_rectangle(*self.edges, (event.x, event.y), outline="red")

                self.lines = clipped_lines
                self.edges = None
                self.drawing_liang_clipping = False
                for line in self.lines:
                    rasterization.draw_DDA_line(line[0][0], line[0][1], line[1][0], line[1][1], self, (0, 0, 0))

    def translate_points(self, delta_x, delta_y):
        """Translates all points by specified deltas."""""
        transformation2d.translate(delta_x, delta_y, self, self.lines, self.circles)

    def rotate_lines(self, angle):
        """Rotates all lines by the specified angle."""
        rotated_lines = []
        for line in self.lines:
            rotated_line = transformation2d.rotate(line, angle, self)
            rotated_lines.append(rotated_line)
        self.lines = rotated_lines

        self.delete("all")
        self.draw_axes()
        for line in self.lines:
            rasterization.draw_DDA_line(line[0][0], line[0][1], line[1][0], line[1][1], self, (0, 0, 0))
        for circle in self.circles:
            self.draw_pixel(circle[0][0], circle[0][1], (0, 0, 0))
            rasterization.draw_Bresenham_circle(circle[0][0], circle[0][1], circle[1], self, (0, 0, 0))

    def scale(self, factor):
        """Scales all lines and circles by the specified factor."""
        scaled_lines = []
        scaled_circles = []

        for line in self.lines:
            scaled_line = transformation2d.scale_line(line, factor, self)
            scaled_lines.append(scaled_line)
        for circle in self.circles:
            scaled_circle = transformation2d.scale_circle(circle, factor, self)
            scaled_circles.append(scaled_circle)

        self.delete("all")
        self.draw_axes()

        self.lines = scaled_lines
        self.circles = scaled_circles

        for line in self.lines:
            rasterization.draw_DDA_line(line[0][0], line[0][1], line[1][0], line[1][1], self, (0, 0, 0))
        for circle in self.circles:
            self.draw_pixel(circle[0][0], circle[0][1], (0, 0, 0))
            rasterization.draw_Bresenham_circle(circle[0][0], circle[0][1], circle[1], self, (0, 0, 0))

    def reflect(self, axis):
        """Reflects all lines and circles across the specified axis."""
        reflected_lines = []
        reflected_circles = []

        # Reflect lines
        for line in self.lines:
            reflected_line = transformation2d.reflect_line(line, axis, self)
            reflected_lines.append(reflected_line)

        # Reflect circles
        for circle in self.circles:
            reflected_circle = transformation2d.reflect_circle(circle, axis, self)
            reflected_circles.append(reflected_circle)

        # Clear canvas
        self.delete("all")
        self.draw_axes()

        self.lines = reflected_lines
        self.circles = reflected_circles

        # Draw reflected lines
        for line in self.lines:
            rasterization.draw_DDA_line(line[0][0], line[0][1], line[1][0], line[1][1], self, (0, 0, 0))

        # Draw reflected circles
        for circle in self.circles:
            self.draw_pixel(circle[0][0], circle[0][1], (0, 0, 0))
            rasterization.draw_Bresenham_circle(circle[0][0], circle[0][1], circle[1], self, (0, 0, 0))

    def draw_pixel(self, x, y, color):
        """Draws a pixel on the canvas at the specified coordinates with the given color."""
        color_hex = '#{0:02x}{1:02x}{2:02x}'.format(color[0], color[1], color[2])
        self.create_rectangle(x, y, x + 1, y + 1, fill=color_hex)

    def on_click_list(self):
        """Prints the list of lines to the console."""
        for line in self.lines:
            print(f"Line from: {line[0]} to {line[1]}")

    def toggle_cohen_clipping(self):
        """Activates Cohen-Sutherland clipping mode."""
        self.drawing_cohen_clipping = True


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TP1 - Graphical Computation")

        # Create Cartesian Plane
        self.cartesian_plane = CartesianPlane(self)
        self.cartesian_plane.place(relx=0, rely=0, relwidth=0.8, relheight=1)

        # Create Menu with Buttons
        self.menu_frame = tk.Frame(self, bg="lightgrey")
        self.menu_frame.place(relx=0.8, rely=0, relwidth=0.2, relheight=1)

        # Label to display mouse coordinates
        self.coordinate_label = tk.Label(self.menu_frame, text="x: 0.00 | y: 0.00")
        self.coordinate_label.pack(expand=True, pady=(10, 0))

        # Initialize button attributes
        self.dda_button = None
        self.bresenham_button = None
        self.bresenham_circle_button = None
        self.translate_button = None
        self.rotate_button = None
        self.scale_button = None
        self.reflect_button = None
        self.cohen_button = None
        self.liang_button = None
        self.clear_button = None

        # Create organized buttons
        self.create_buttons()

    def create_buttons(self):
        self.create_line_buttons()
        self.create_circle_button()
        self.create_transform_buttons()
        self.create_clip_buttons()
        self.create_other_buttons()

    def create_line_buttons(self):
        line_frame = tk.Frame(self.menu_frame, bg="lightgrey")
        line_frame.pack(expand=True, pady=10)

        self.dda_button = tk.Button(line_frame, text="DDA Line", command=self.toggle_dda)
        self.dda_button.pack(side=tk.LEFT, padx=(0, 5))

        self.bresenham_button = tk.Button(line_frame, text="Bresenham Line", command=self.toggle_bresenham)
        self.bresenham_button.pack(side=tk.LEFT)

    def create_circle_button(self):
        circle_frame = tk.Frame(self.menu_frame, bg="lightgrey")
        circle_frame.pack(expand=True, pady=10)

        self.bresenham_circle_button = tk.Button(circle_frame, text="Bresenham Circumference",
                                                 command=self.toggle_bresenham_circle)
        self.bresenham_circle_button.pack()

    def create_transform_buttons(self):
        transform_frame = tk.Frame(self.menu_frame, bg="lightgrey")
        transform_frame.pack(expand=True, pady=10)

        self.translate_button = tk.Button(transform_frame, text="Translate", command=self.translate_popup)
        self.translate_button.pack(side=tk.LEFT, padx=(0, 5))

        self.rotate_button = tk.Button(transform_frame, text="Rotate", command=self.rotate_popup)
        self.rotate_button.pack(side=tk.LEFT)

        self.scale_button = tk.Button(transform_frame, text="Scale", command=self.scale_popup)
        self.scale_button.pack(side=tk.LEFT, padx=(0, 5))

        self.reflect_button = tk.Button(transform_frame, text="Reflect", command=self.reflect_popup)
        self.reflect_button.pack(side=tk.LEFT)

    def create_clip_buttons(self):
        clip_frame = tk.Frame(self.menu_frame, bg="lightgrey")
        clip_frame.pack(expand=True, pady=10)

        self.cohen_button = tk.Button(clip_frame, text="Cohen Clipping", command=self.toggle_cohen_clipping)
        self.cohen_button.pack(side=tk.LEFT, padx=(0, 5))

        self.liang_button = tk.Button(clip_frame, text="Liang Clipping", command=self.toggle_liang_clipping)
        self.liang_button.pack(side=tk.LEFT)

    def create_other_buttons(self):
        other_frame = tk.Frame(self.menu_frame, bg="lightgrey")
        other_frame.pack(expand=True, pady=10)

        self.clear_button = tk.Button(other_frame, text="Clear", command=self.clear_screen)
        self.clear_button.pack()

    def toggle_dda(self):
        if self.cartesian_plane.drawing_line_dda:
            self.dda_button.config(relief=tk.RAISED)
            self.cartesian_plane.drawing_line_dda = False
        else:
            self.dda_button.config(relief=tk.SUNKEN)
            self.cartesian_plane.drawing_line_dda = True
            self.cartesian_plane.drawing_line_bresenham = False

    def toggle_cohen_clipping(self):
        if self.cartesian_plane.drawing_cohen_clipping:
            self.cohen_button.config(relief=tk.RAISED)
            self.cartesian_plane.drawing_cohen_clipping = False
        else:
            self.cohen_button.config(relief=tk.SUNKEN)
            self.cartesian_plane.drawing_cohen_clipping = True
            self.cartesian_plane.drawing_line_dda = False
            self.cartesian_plane.drawing_line_bresenham = False

    def toggle_liang_clipping(self):
        if self.cartesian_plane.drawing_liang_clipping:
            self.liang_button.config(relief=tk.RAISED)
            self.cartesian_plane.drawing_liang_clipping = False
        else:
            self.liang_button.config(relief=tk.SUNKEN)
            self.cartesian_plane.drawing_liang_clipping = True
            self.cartesian_plane.drawing_line_dda = False
            self.cartesian_plane.drawing_line_bresenham = False
            self.cartesian_plane.drawing_cohen_clipping = False

    def toggle_bresenham(self):
        if self.cartesian_plane.drawing_line_bresenham:
            self.bresenham_button.config(relief=tk.RAISED)
            self.cartesian_plane.drawing_line_bresenham = False
        else:
            self.bresenham_button.config(relief=tk.SUNKEN)
            self.cartesian_plane.drawing_line_bresenham = True
            self.cartesian_plane.drawing_line_dda = False

    def toggle_bresenham_circle(self):
        if self.cartesian_plane.drawing_circle_bresenham:
            self.bresenham_circle_button.config(relief=tk.RAISED)
            self.cartesian_plane.drawing_circle_bresenham = False
        else:
            self.bresenham_circle_button.config(relief=tk.SUNKEN)
            self.cartesian_plane.drawing_circle_bresenham = True
            self.cartesian_plane.drawing_line_dda = False
            self.cartesian_plane.drawing_line_bresenham = False

    def clear_screen(self):
        self.cartesian_plane.delete("all")
        self.cartesian_plane.lines = []
        self.cartesian_plane.circles = []
        self.cartesian_plane.draw_axes()

    def translate_popup(self):
        delta_x = tk.simpledialog.askinteger("Translate", "Enter delta x:")
        delta_y = tk.simpledialog.askinteger("Translate", "Enter delta y:")
        if delta_x is not None and delta_y is not None:
            self.cartesian_plane.translate_points(delta_x, delta_y)

    def scale_popup(self):
        x_factor = tk.simpledialog.askfloat("Scale", "Enter factor:")
        if x_factor is not None:
            self.cartesian_plane.scale(x_factor)

    def rotate_popup(self):
        angle = tk.simpledialog.askinteger("Angle", "Enter the angle:")
        if angle is not None:
            self.cartesian_plane.rotate_lines(angle)

    def reflect_popup(self):
        axis = tk.simpledialog.askstring("Reflection axis", "Enter axis (X, Y, XY):")
        if axis is not None and axis in ["X", "Y", "XY"]:
            self.cartesian_plane.reflect(axis)


if __name__ == "__main__":
    app = App()
    app.geometry("1000x600")  # Set initial window size
    app.mainloop()
