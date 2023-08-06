#! /usr/bin/env python

import math
from visualife.core.styles import ColorRGB, hex_to_rgb, color_by_name

try:
  from browser import document
except:  document = None

# --- filter to be added in CSS
#filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.5));

base_color = ColorRGB(*hex_to_rgb("#6AB0DE"))
stroke_color = base_color.create_darker(0.2)
stroke_width = 2
fill_color = base_color.mix(0.8,color_by_name("white"))
highlighted_color = base_color.deepcopy().mix(0.15, color_by_name("red"))
default_node_style = """ stroke-width:%dpx; stroke:%s; fill:%s ;""" % (stroke_width, stroke_color, fill_color)
default_text_style = """ stroke-width:0px; fill:black; text-anchor:middle; alignment-baseline:middle; """
default_segment_length = 30 # in pixels


class Point:
    """A simple data structure to hold X,Y coordinates on a screen"""

    def __init__(self, x, y):
        """Creates a point from the given coordinates"""
        self.x = x
        self.y = y

    def __str__(self): return "%.1f %.1f" % (self.x, self.y)

    def __add__(self, rhs):
        """Adds a rhs point and this point, returns a new Point object"""
        return Point(self.x + rhs.x, self.y + rhs.y)

    def __sub__(self, rhs):
        """Subtracts a rhs point from this point, returns a new Point object"""
        return Point(self.x + rhs.x, self.y + rhs.y)

    def distance_to(self, another_point):
        d = another_point.x - self.x
        d2 = d*d
        d = another_point.y - self.y
        d2 += d*d
        return math.sqrt(d2)


def average_point(points):
    p = Point(0,0)
    for pi in points:
        p.x += pi.x
        p.y += pi.y
    p.x /= len(points)
    p.y /= len(points)
    return p


class NodeBase(Point):

    def __init__(self, id, x, y):
        super().__init__(x,y)
        self.__id = id
        self.__x_center = x
        self.__y_center = y

    @property
    def x_center(self): return self.__x_center

    @property
    def y_center(self): return self.__y_center

    @property
    def id(self): return self.__id


class DotNode(NodeBase):

    def __init__(self, viewport, id, x, y, r, **attrs):
        super().__init__(id, x, y)
        self.__node_style = attrs.get("node_style", default_node_style)
        dot_attrs = dict(**attrs, style=self.__node_style)
        viewport.circle(id, x, y, r=r, **dot_attrs)


class RectNode(NodeBase):

    def __init__(self, viewport, id, text, x, y, w, h, **attrs):

        """Creates a rectangular node.

        :param viewport: - where to draw thr rectangle
        :param id: - id to be set to the SVG element of the rectangle
        :param text: - text to be displayed in the box
        :param x: - X of the top left corner
        :param y: - Y of the top left corner
        :param w: - width of the box
        :param h: - height of the box
        :param attrs: see below

        :Keyword Arguments:
            * *text_style* (``string``) --
              a style for text
            * *node_style* (``string``) --
              a style for drawing
        """
        super().__init__(id, x + w / 2.0, y + h / 2.0)
        self.__text = text
        self.__x_top_left = x
        self.__y_top_left = y
        self.__w = w
        self.__h = h
        self.__node_style = attrs.get("node_style", default_node_style)
        self.__text_style = attrs.get("text_style", default_text_style)

        box_attrs = dict(**attrs, style=self.__node_style)
        viewport.rect(id + "-box", x, y, w, h, **box_attrs)
        viewport.text(id + "-text", x + w / 2.0, y + h / 2.0, text, style=self.__text_style)

    @property
    def w(self): return self.__w

    @property
    def h(self): return self.__h

    def left(self): return Point(self.__x_top_left, self.y_center)

    def right(self): return Point(self.__x_top_left + self.__w, self.y_center)

    def top(self): return Point(self.x_center, self.__y_top_left)

    def bottom(self): return Point(self.x_center, self.__y_top_left+self.__h)

    def highlight(self):
        if document:
            document[self.id + "-box"].attrs["fill"] = str(highlighted_color)

    def clear(self):
        if document:
            document[self.id + "-box"].attrs["fill"] = str(fill_color)

    def box_attribute(self, attr_name, value):
        document[self.id + "-box"].attrs[attr_name] = value


class DimondNode(RectNode):

    def __init__(self, viewport, id, text, xc, yc, w, **attrs):

        """Creates a rectangular node with rounded corners.

        :param viewport: - where to draw thr rectangle
        :param id: - id to be set to the SVG element of the rectangle
        :param text: - text to be displayed in the box
        :param xc: - X of the bottom left corner
        :param yc: - Y of the bottom left corner
        :param w: - width of the box
        :param attrs: see below

        :Keyword Arguments:
            * *text_style* (``string``) --
              a style for text
            * *node_style* (``string``) --
              a style for drawing
        """

        super().__init__(viewport, id, text, xc-w/2.0, yc-w/2.0, w, w, **dict(**attrs, angle=45))

    def left(self):
        return Point(self.x_center - self.w  * math.sqrt(2) / 2.0, self.y_center)

    def right(self):
        return Point(self.x_center + self.w  * math.sqrt(2) / 2.0, self.y_center)

    def top(self):
        return Point(self.x_center, self.y_center - self.w * math.sqrt(2)/2.0)

    def bottom(self):
        return Point(self.x_center, self.y_center + self.w * math.sqrt(2) / 2.0)


class Connector(NodeBase):
    """
    Connector is a line that connects two nodes of a diagram.

    It's also derived from NodeBase so it's possible to compute its center and assign a location
    """

    def __init__(self, viewport, id, *points, **attrs):
        """Creates a new Connector instance
        :param viewport: where to actually draw the line
        :param id: (``string``) unique ID of this line, important for ``HtmlViewport``
        :param points: (``list[Point]``) of points to connect with a line
        :param attrs: parameters to style the line: color, width etc.
        """
        super().__init__(id, average_point(points).x, average_point(points).y)
        self.points = points
        arrow_size = attrs.get("arrow_size",3)
        for i in range(1, len(points)):
            viewport.line(id + "-%d" % i, points[i - 1].x, points[i - 1].y, points[i].x, points[i].y, **attrs)

        if points[-1].x == points[-2].x: # vertical line
            s = 1 if points[-1].y < points[-2].y else -1    # we go up else down
            elms = [("M", points[-1].x, points[-1].y + s*stroke_width/2.0),
                    ("l", -arrow_size, s*2*arrow_size), ("l", 2*arrow_size, 0), ("Z")]
        else:
            s = 1 if points[-1].x < points[-2].x else -1    # we go left else right
            elms = [("M", points[-1].x + s*stroke_width/2.0, points[-1].y),
                    ("l", s*2*arrow_size, -arrow_size), ("l", 0, 2*arrow_size), ("Z")]
        viewport.path(id + "arrow", elms, **attrs)


class Diagram:

    def __init__(self, viewport, id):
        self.__viewport = viewport
        self.__nodes = []
        self.__id = id
        self.__node_style = default_node_style
        self.__text_style = default_text_style
        self.__last_id = 0

    def clear_all(self):
        for n in self.__nodes: n.clear()

    def add_condition(self, text, w, **attrs):

        xc = Diagram.__get_and_remove(attrs, "xc", 50)
        yc = Diagram.__get_and_remove(attrs, "yc", 50)

        if "below" in attrs :
            b = attrs["below"].bottom()
            dy = attrs.get("dy", default_segment_length)
            yc = b.y + float(dy) + math.sqrt(2.0) * w / 2.0
            xc = b.x
        if "center_at" in attrs:
            b = attrs["center_at"]
            yc = b.y
            xc = b.x
        id = self.__id + ":" + str(self.__last_id)
        self.__last_id += 1
        d = DimondNode(self.__viewport, id, text, xc, yc, w, **attrs)
        self.__nodes.append(d)
        connector = None
        if attrs.get("autoconnect", True) and "below" in attrs:
            connector = self.connect(b, d.top())

        if not connector:
            if "connect_xy" in attrs:
                t = d.top()
                ref = attrs["connect_xy"]
                if t.distance_to(ref.left()) < t.distance_to(ref.right()):
                    connector = self.connect_xy(ref.left(),t)
                else:
                    connector = self.connect_xy(ref.right(), t)
            elif "connect_yx" in attrs:
                t = d.top()
                ref = attrs["connect_yx"]
                if t.distance_to(ref.left()) < t.distance_to(ref.right()):
                    connector = self.connect_yx(ref.left(), t)
                else:
                    connector = self.connect_yx(ref.right(), t)

        return d, connector

    def add_box(self, text, w, h, **attrs):

        """ Add a new rectangular b ox to this diagram
        :param text: - text to be shown inside the rectangle
        :param w: - width of the box
        :param h: - height of the box
        :param attrs: see below
        :return: a ``RectNode`` object

        :Keyword Arguments:
            * *x* (``number``) --
              x position of the top left corner of the newly created box
            * *y* (``number``) --
              y position of the top left corner of the newly created box
            * *below* (``object``) --
              place the newly created box below the given argument
            * *dx* (``number``) --
              length of a linker for horizontal connections (right_of=, left_of=)
            * *dy* (``number``) --
              length of a linker for vertical connections (below=)
            * *autoconnect* (``bool``) if ``True`` (and this is the default), this method also create a connecting line
              i.e. creates an appropriate ``Connector`` instance. *autoconnect* works only if the new node is placed
              *below*, *right_of* or *left_of* another node. Say ``autoconnect=False`` to switch it off for
              one of these these cases.
        """

        id = self.__id + ":" + str(self.__last_id)
        connector = None
        if "center_at" in attrs:
            b = attrs["center_at"]
            y = b.y - h/2.0
            x = b.x - w/2.0
            r = RectNode(self.__viewport, id, text, x, y, w, h, **attrs)
        elif "below" in attrs:
            b = attrs["below"].bottom()
            dy = attrs.get("dy", default_segment_length)
            y = b.y + float(dy)
            x = b.x - w/2.0
            r = RectNode(self.__viewport, id, text, x, y, w, h, **attrs)
            if attrs.get("autoconnect", True):
                connector = self.connect(b, r.top())
        elif "above" in attrs:
            b = attrs["above"].top()
            dy = attrs.get("dy", default_segment_length)
            y = b.y - float(dy) - h
            x = b.x - w / 2.0
            r = RectNode(self.__viewport, id, text, x, y, w, h, **attrs)
            if attrs.get("autoconnect", True):
                connector = self.connect(b, r.bottom())
        elif "right_of" in attrs:
            dx = attrs.get("dx", default_segment_length)
            b = attrs["right_of"].right()
            x = b.x + float(dx)
            y = b.y - h/2.0
            r = RectNode(self.__viewport, id, text, x, y, w, h, **attrs)
            if attrs.get("autoconnect", True):
                connector = self.connect(b, r.left())
        elif "left_of" in attrs:
            dx = attrs.get("dx", default_segment_length)
            b = attrs["left_of"].left()
            x = b.x - float(dx) - w
            y = b.y - h/2.0
            r = RectNode(self.__viewport, id, text, x, y, w, h, **attrs)
            if attrs.get("autoconnect", True):
                connector = self.connect(b, r.right())
        else:
            x = Diagram.__get_and_remove(attrs, "x", self.__viewport.get_width() / 2.0)
            y = Diagram.__get_and_remove(attrs, "y", 10)
            r = RectNode(self.__viewport, id, text, x, y, w, h, **attrs)

        if not connector:
            if "connect_xy" in attrs:
                t = r.top()
                ref = attrs["connect_xy"]
                if t.distance_to(ref.left()) < t.distance_to(ref.right()):
                    connector = self.connect_xy(ref.left(),t)
                else:
                    connector = self.connect_xy(ref.right(), t)
            elif "connect_yx" in attrs:
                t = r.top()
                ref = attrs["connect_yx"]
                if t.distance_to(ref.left()) < t.distance_to(ref.right()):
                    connector = self.connect_yx(ref.left(), t)
                else:
                    connector = self.connect_yx(ref.right(), t)
            elif "connect_yr" in attrs:
                t = r.left()
                ref = attrs["connect_yr"]
                if t.distance_to(ref.left()) < t.distance_to(ref.right()):
                    connector = self.connect_yx(ref.left(), t)
                else:
                    connector = self.connect_yx(ref.right(), t)
            elif "connect_yl" in attrs:
                t = r.right()
                ref = attrs["connect_yl"]
                if t.distance_to(ref.left()) < t.distance_to(ref.right()):
                    connector = self.connect_yx(ref.left(), t)
                else:
                    connector = self.connect_yx(ref.right(), t)
        self.__last_id += 1
        self.__nodes.append(r)
        return r, connector

    def connect(self, *what):

        id = self.__id + ":" + str(self.__last_id)
        self.__last_id += 1
        c = Connector(self.__viewport, id, *what, style=default_node_style)
        return c

    def add_dot(self, **attrs):
        x, y = 0, 0
        if "center_at" in attrs:
            b = attrs["center_at"]
            y = b.y
            x = b.x

        id = self.__id + ":" + str(self.__last_id)
        self.__last_id += 1
        d = DotNode(self.__viewport, id, x, y, 5, **attrs)
        return d

    def connect_xy(self, start, stop):

        id = self.__id + ":" + str(self.__last_id)
        self.__last_id += 1
        coords = [start, Point(stop.x, start.y), stop]
        c = Connector(self.__viewport, id, *coords, style=default_node_style)
        return c

    def connect_yx(self, start, stop):

        id = self.__id + ":" + str(self.__last_id)
        self.__last_id += 1
        coords = [start, Point(start.x, stop.y), stop]
        c = Connector(self.__viewport, id, *coords, style=default_node_style)
        return c

    def max_x(self):
        max_x = self.__nodes[0].bottom().x
        for n in self.__nodes[1:]: max_x = max(max_x, n.bottom().x)

    def max_y(self):
        max_y = self.__nodes[0].bottom().y
        for n in self.__nodes[1:]:
            max_y = max(max_y, n.bottom().y)
        return max_y

    @staticmethod
    def __get_and_remove(dictionary, key, default_value):
        v = default_value
        if key in dictionary:
            v = dictionary[key]
            del dictionary[key]
        return v
