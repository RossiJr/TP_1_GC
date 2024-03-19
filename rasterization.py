def draw_DDA_line(x1, y1, x2, y2, cartesian_plane, color):
    """
        Draw a line using the Digital Differential Analyzer (DDA) algorithm.

        Args:
            x1 (int): x-coordinate of the starting point.
            y1 (int): y-coordinate of the starting point.
            x2 (int): x-coordinate of the ending point.
            y2 (int): y-coordinate of the ending point.
            cartesian_plane (Canvas): The canvas where the line will be drawn.
            color (tuple): RGB color tuple representing the line color.

        Returns:
            None
        """
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) > abs(dy):
        steps = abs(dx)
    else:
        steps = abs(dy)

    x_incr = dx / steps
    y_incr = dy / steps
    x = x1
    y = y1

    cartesian_plane.draw_pixel(round(x), round(y), color)
    for k in range(round(steps)):
        x += x_incr
        y += y_incr
        cartesian_plane.draw_pixel(round(x), round(y), color)


def draw_Bresenham_line(x_initial, y_initial, x_final, y_final, cartesian_plane, color):
    """
        Draw a line using the Bresenham's line drawing algorithm.

        Args:
            x_initial (int): x-coordinate of the starting point.
            y_initial (int): y-coordinate of the starting point.
            x_final (int): x-coordinate of the ending point.
            y_final (int): y-coordinate of the ending point.
            cartesian_plane (Canvas): The canvas where the line will be drawn.
            color (tuple): RGB color tuple representing the line color.

        Returns:
            None
        """
    dx = abs(x_final - x_initial)  # Delta x
    dy = abs(y_final - y_initial)  # Delta y

    if x_initial < x_final:
        incrx = 1
    else:
        incrx = -1

    if y_initial < y_final:
        incry = 1
    else:
        incry = -1

    x = x_initial
    y = y_initial

    cartesian_plane.draw_pixel(x, y, color)

    if dx > dy:
        decision_p = 2 * dy - dx
        incE = 2 * dy
        incNE = 2 * (dy - dx)

        for _ in range(dx):
            if decision_p <= 0:
                decision_p += incE
                x += incrx
            else:
                decision_p += incNE
                x += incrx
                y += incry
            cartesian_plane.draw_pixel(x, y, color)
    else:
        decision_p = 2 * dx - dy
        incN = 2 * dx
        incNE = 2 * (dx - dy)

        for _ in range(dy):
            if decision_p <= 0:
                decision_p += incN
                y += incry
            else:
                decision_p += incNE
                x += incrx
                y += incry
            cartesian_plane.draw_pixel(x, y, color)


def plot_circumference_points(xc, x, yc, y, cartesian_plane, color):
    """
        Plot points around the circumference of a circle.

        Args:
            xc (int): x-coordinate of the circle's center.
            x (int): x-coordinate of the point to plot relative to the center.
            yc (int): y-coordinate of the circle's center.
            y (int): y-coordinate of the point to plot relative to the center.
            cartesian_plane (Canvas): The canvas where the points will be drawn.
            color (tuple): RGB color tuple representing the point color.

        Returns:
            None
        """
    cartesian_plane.draw_pixel(xc - x, yc + y, color)
    cartesian_plane.draw_pixel(xc + x, yc - y, color)
    cartesian_plane.draw_pixel(xc + x, yc + y, color)
    cartesian_plane.draw_pixel(xc - x, yc - y, color)
    cartesian_plane.draw_pixel(xc + y, yc + x, color)
    cartesian_plane.draw_pixel(xc - y, yc + x, color)
    cartesian_plane.draw_pixel(xc + y, yc - x, color)
    cartesian_plane.draw_pixel(xc - y, yc - x, color)


def draw_Bresenham_circle(xc, yc, r, cartesian_plane, color):
    """
        Draw a circle using Bresenham's circle drawing algorithm.

        Args:
            xc (int): x-coordinate of the circle's center.
            yc (int): y-coordinate of the circle's center.
            r (int): Radius of the circle.
            cartesian_plane (Canvas): The canvas where the circle will be drawn.
            color (tuple): RGB color tuple representing the circle color.

        Returns:
            None
        """
    x = 0
    y = r
    p = 3 - 2 * r
    plot_circumference_points(xc, x, yc, y, cartesian_plane, color)
    while x < y:
        if p < 0:
            p = p + 4 * x + 6
        else:
            p = p + 4 * (x - y) + 10
            y -= 1
        x += 1
        plot_circumference_points(xc, x, yc, y, cartesian_plane, color)
