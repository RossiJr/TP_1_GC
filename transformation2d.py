import rasterization
import math


def translate(tx, ty, cartesian_plane, lines=None, circles=None):
    """
    Translate all lines and circles on the cartesian plane by the given translation vector (tx, ty).

    Args:
        tx (int): Translation amount along the x-axis.
        ty (int): Translation amount along the y-axis.
        cartesian_plane (Canvas): The canvas where the lines and circles will be translated.
        lines (list): List of lines to be translated.
        circles (list): List of circles to be translated.

    Returns:
        None
    """
    if lines is None:
        lines = []
    if circles is None:
        circles = []

    cartesian_plane.delete("all")
    cartesian_plane.draw_axes()

    for line in lines:
        rasterization.draw_DDA_line(line[0][0] + tx, line[0][1] + ty, line[1][0] + tx, line[1][1] + ty, cartesian_plane,
                                    color=(255, 0, 0))
    for circle in circles:
        cartesian_plane.draw_pixel(circle[0][0] + tx, circle[0][1] + ty, (255, 0, 0))
        rasterization.draw_Bresenham_circle(circle[0][0] + tx, circle[0][1] + ty, circle[1], cartesian_plane,
                                            color=(255, 0, 0))


def rotate(line, angle, cartesian_plane):
    """
        Rotate a line by a given angle around its starting point.

        Args:
            line (tuple): A tuple containing the coordinates of the starting and ending points of the line.
            angle (float): The angle of rotation in degrees.
            cartesian_plane (Canvas): The canvas where the rotated line will be drawn.

        Returns:
            tuple: A tuple containing the coordinates of the rotated line.
        """
    x1, y1 = line[0]
    x2, y2 = line[1]

    # Calculate pivot point (center of rotation)
    pivot_x, pivot_y = x1, y1

    angle_rad = math.radians(angle)

    c = math.cos(angle_rad)
    s = math.sin(angle_rad)

    # Translate line so that the pivot is at the origin
    x2 -= pivot_x
    y2 -= pivot_y

    # Perform rotation
    new_x2 = x2 * c - y2 * s
    new_y2 = x2 * s + y2 * c

    # Translate back to original position
    new_x2 += pivot_x
    new_y2 += pivot_y

    return (round(x1), round(y1)), (round(new_x2), round(new_y2))


def scale_line(line, scale_factor, cartesian_plane):
    """
        Scale a line by a given factor around its starting point.

        Args:
            line (tuple): A tuple containing the coordinates of the starting and ending points of the line.
            scale_factor (float): The scaling factor.
            cartesian_plane (Canvas): The canvas where the scaled line will be drawn.

        Returns:
            tuple: A tuple containing the coordinates of the scaled line.
        """
    (x1, y1), (x2, y2) = line

    # Calculate the distance between the pivot point (x1, y1) and the other point (x2, y2)
    dx = x2 - x1
    dy = y2 - y1

    # Scale the distance
    dx_scaled = dx * scale_factor
    dy_scaled = dy * scale_factor

    # Calculate the new coordinates for the second point (x2, y2)
    x2_new = x1 + dx_scaled
    y2_new = y1 + dy_scaled

    return (x1, y1), (x2_new, y2_new)


def scale_circle(circle, scale_factor, cartesian_plane):
    """
        Scale a circle by a given factor around its center.

        Args:
            circle (tuple): A tuple containing the coordinates of the center and the radius of the circle.
            scale_factor (float): The scaling factor.
            cartesian_plane (Canvas): The canvas where the scaled circle will be drawn.

        Returns:
            tuple: A tuple containing the coordinates of the scaled circle.
        """
    (xc, yc), r = circle

    # Scale the radius of the circle
    r_scaled = r * scale_factor

    return (xc, yc), r_scaled


def reflect_line(line, axis, cartesian_plane):
    """
        Reflect a line with respect to a given axis.

        Args:
            line (tuple): A tuple containing the coordinates of the starting and ending points of the line.
            axis (str): The axis ('X', 'Y', or 'XY') with respect to which the line will be reflected.
            cartesian_plane (Canvas): The canvas where the reflected line will be drawn.

        Returns:
            tuple: A tuple containing the coordinates of the reflected line.
        """
    (x1, y1), (x2, y2) = line
    x1, y1 = cartesian_plane.cartesian_plan_coordinates(x1, y1)
    x2, y2 = cartesian_plane.cartesian_plan_coordinates(x2, y2)

    if axis == 'X':
        return (cartesian_plane.get_pixel_coordinates(x1, -y1)), (cartesian_plane.get_pixel_coordinates(x2, -y2))
    elif axis == 'Y':
        return (cartesian_plane.get_pixel_coordinates(-x1, y1)), (cartesian_plane.get_pixel_coordinates(-x2, y2))
    elif axis == 'XY':
        return (cartesian_plane.get_pixel_coordinates(-x1, -y1)), (cartesian_plane.get_pixel_coordinates(-x2, -y2))


def reflect_circle(circle, axis, cartesian_plane):
    """
        Reflect a circle with respect to a given axis.

        Args:
            circle (tuple): A tuple containing the coordinates of the center and the radius of the circle.
            axis (str): The axis ('X', 'Y', or 'XY') with respect to which the circle will be reflected.
            cartesian_plane (Canvas): The canvas where the reflected circle will be drawn.

        Returns:
            tuple: A tuple containing the coordinates of the reflected circle.
        """
    (xc, yc), r = circle
    xc, yc = cartesian_plane.cartesian_plan_coordinates(xc, yc)

    if axis == 'X':
        return cartesian_plane.get_pixel_coordinates(xc, -yc), r
    elif axis == 'Y':
        return cartesian_plane.get_pixel_coordinates(-xc, yc), r
    elif axis == 'XY':
        return cartesian_plane.get_pixel_coordinates(-xc, -yc), r


