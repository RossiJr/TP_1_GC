INSIDE = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8

def clipping_cohen_sutherland(x_initial, y_initial, x_final, y_final, c_initial, c_final, cartesian_plane):
    """
        Implements the Cohen-Sutherland line clipping algorithm.

        Args:
            x_initial, y_initial: Coordinates of the initial point of the line.
            x_final, y_final: Coordinates of the final point of the line.
            c_initial, c_final: Coordinates of the clipping window (rectangle).
            cartesian_plane: Tkinter canvas object to draw the clipped line.

        Returns:
            Tuple: (accept, clipped_line), where accept is a boolean indicating if the line was accepted after clipping,
            and clipped_line is a tuple containing the coordinates of the clipped line segment.
        """

    width = cartesian_plane.winfo_width()
    height = cartesian_plane.winfo_height()

    x_min, y_min = c_initial
    x_max, y_max = c_final

    code1 = region_code(x_initial, y_initial, x_min, x_max, y_min, y_max)
    code2 = region_code(x_final, y_final, x_min, x_max, y_min, y_max)

    accept = False
    line_accepted = False  # Verifica se pelo menos parte da linha está dentro da área de recorte

    while True:
        # If both endpoints lie within rectangle or both are outside rectangle in the same region
        if (code1 == 0 and code2 == 0) or (code1 & code2 != 0):
            accept = True
            break
        # If both endpoints are outside rectangle, in the same region
        elif (code1 & code2) != 0:
            break
        else:  # Some segment of line lies within the rectangle
            code_out = 0
            x, y = 0, 0

            if code1 != 0:
                code_out = code1
            else:
                code_out = code2

            if (code_out & TOP) != 0:
                x = x_initial + (x_final - x_initial) * (y_max - y_initial) / (y_final - y_initial)
                y = y_max
            elif (code_out & BOTTOM) != 0:
                x = x_initial + (x_final - x_initial) * (y_min - y_initial) / (y_final - y_initial)
                y = y_min
            elif (code_out & RIGHT) != 0:
                y = y_initial + (y_final - y_initial) * (x_max - x_initial) / (x_final - x_initial)
                x = x_max
            elif (code_out & LEFT) != 0:
                y = y_initial + (y_final - y_initial) * (x_min - x_initial) / (x_final - x_initial)
                x = x_min

            # Now intersection point x, y is found
            # Replace point outside rectangle with intersection point
            if code_out == code1:
                x_initial = x
                y_initial = y
                code1 = region_code(x_initial, y_initial, x_min, x_max, y_min, y_max)
            else:
                x_final = x
                y_final = y
                code2 = region_code(x_final, y_final, x_min, x_max, y_min, y_max)

            # Verifica se pelo menos parte da linha está dentro da área de recorte
            if (x_min <= x_initial <= x_max and y_min <= y_initial <= y_max) or (x_min <= x_final <= x_max and y_min <= y_final <= y_max):
                line_accepted = True

    if accept and line_accepted:  # Aceita a linha somente se pelo menos parte dela estiver dentro da área de recorte
        print("Line accepted from " + str(x_initial) + ", " + str(y_initial) + " to " + str(x_final) + ", " + str(
            y_final))
        cartesian_plane.create_line(x_initial, y_initial, x_final, y_final, fill="red")
        return True, ((x_initial, y_initial), (x_final, y_final))
    else:
        print("Line rejected")
        return False, (None, None)

def region_code(x, y, x_min, x_max, y_min, y_max):
    """
        Determines the region code for a given point with respect to a rectangle.

        Args:
            x, y: Coordinates of the point.
            x_min, x_max, y_min, y_max: Coordinates of the rectangle defining the clipping area.

        Returns:
            int: Region code based on the position of the point relative to the rectangle.
        """
    code = INSIDE

    if x < x_min:  # to the left of rectangle
        code |= LEFT
    elif x > x_max:  # to the right of rectangle
        code |= RIGHT
    if y < y_min:  # below the rectangle
        code |= BOTTOM
    elif y > y_max:  # above the rectangle
        code |= TOP

    return code



def clipping_liang_barsky(x1, y1, x2, y2, xmin, ymin, xmax, ymax, cartesian_object):
    """
        Implements the Liang-Barsky line clipping algorithm.

        Args:
            x1, y1: Coordinates of the initial point of the line.
            x2, y2: Coordinates of the final point of the line.
            xmin, ymin: Minimum coordinates of the clipping window.
            xmax, ymax: Maximum coordinates of the clipping window.
            cartesian_object: Tkinter canvas object to draw the clipped line.

        Returns:
            Tuple: (accept, clipped_line), where accept is a boolean indicating if the line was accepted after clipping,
            and clipped_line is a tuple containing the coordinates of the clipped line segment.
        """
    # defining variables
    p1 = -(x2 - x1)
    p2 = -p1
    p3 = -(y2 - y1)
    p4 = -p3

    q1 = x1 - xmin
    q2 = xmax - x1
    q3 = y1 - ymin
    q4 = ymax - y1

    posarr = [1]
    negarr = [0]
    posind = 1
    negind = 1

    if ((p1 == 0 and q1 < 0) or (p2 == 0 and q2 < 0) or (p3 == 0 and q3 < 0) or (p4 == 0 and q4 < 0)):
        print("Line is parallel to clipping window!")
        return False, (None, None)

    if p1 != 0:
        r1 = q1 / p1
        r2 = q2 / p2
        if p1 < 0:
            negarr.append(r1)  # for negative p1, add it to negative array
            posarr.append(r2)  # and add p2 to positive array
        else:
            negarr.append(r2)
            posarr.append(r1)

    if p3 != 0:
        r3 = q3 / p3
        r4 = q4 / p4
        if p3 < 0:
            negarr.append(r3)
            posarr.append(r4)
        else:
            negarr.append(r4)
            posarr.append(r3)

    rn1 = max(negarr)  # maximum of negative array
    rn2 = min(posarr)  # minimum of positive array

    if rn1 > rn2:  # reject
        print("Line is outside the clipping window!")
        return False, (None, None)

    xn1 = x1 + p2 * rn1
    yn1 = y1 + p4 * rn1  # computing new points

    xn2 = x1 + p2 * rn2
    yn2 = y1 + p4 * rn2

    cartesian_object.create_line(xn1, yn1, xn2, yn2, fill="red")

    return True, ((xn1, yn1), (xn2, yn2))