#! /usr/bin/env python

import sys
from core.styles import ColorRGB
from math import pi,sin,cos

class CanvasViewport:
    """
    Creates a Canvas drawing

    """

    __slots__ = ['__canvas','__viewport_width','__viewport_height']

    def __init__(__self__, canvas, width, height):
        """
        Defines a drawing area
        """
        __self__.__canvas = canvas
        __self__.__viewport_width = width
        __self__.__viewport_height = height
        __self__.__if_stroke = True

    def __prepare_attributes(__self__, **kwargs):
        """Sets all attributes connected with drawing style and text style 
        """
        if 'fill' in kwargs : __self__.__canvas.fillStyle = str(kwargs['fill'])
        if 'stroke_width' in kwargs:
            if kwargs['stroke_width'] == 0:
                __self__.__if_stroke = False
            else:
                __self__.__canvas.lineWidth = kwargs['stroke_width']
        __self__.__canvas.strokeStyle="#000000"
        if 'stroke' in kwargs :
            if kwargs['stroke'] == "none" :
                __self__.__if_stroke = False
            else:
                __self__.__canvas.strokeStyle = kwargs['stroke']
        font_str = ' '
        if 'font_weight' in kwargs:
            font_str+=kwargs['font_weight']+" "
        font_str += " %dpx " % kwargs.get('font_size',12)
        font_str += " "+ kwargs.get('font_family',"Arial")
        __self__.__canvas.font= font_str

        if 'text_anchor' in kwargs:
            if kwargs['text_anchor'] == "middle":
                __self__.__canvas.textAlign="center"
            else:
                __self__.__canvas.textAlign=kwargs['text_anchor']

    def rect(__self__,id_str,x,y,w,h,**kwargs):
        """Draws a rect 

        :param id_str: id of this rect
        :param x: x coordinate
        :param y: y coordinate
        :param w: width of this rect
        :param h: height of this rect
        :return: None
        """
        __self__.__prepare_attributes(**kwargs)
        if 'fill' in kwargs:
            __self__.__canvas.fillRect(x,y,w,h)

        if __self__.__if_stroke:
            __self__.__canvas.strokeRect(x,y,w,h)

    def square(__self__,id_str,x,y,a,**kwargs):
        """Draws a square

        :param id_str: id of this square
        :param x: x coordinate of the center of this square
        :param y: y coordinate of the center of this square
        :param a: side length 
        :return: None
        """
        __self__.__prepare_attributes(**kwargs)
        if 'fill' in kwargs:
            __self__.__canvas.fillRect(x-a/2, y-a/2, a, a)
        if __self__.__if_stroke:
            __self__.__canvas.strokeRect(x-a/2, y-a/2, a, a)

    def circle(__self__,id_str,x,y,r,**kwargs):
        """Draws a circle

        :param id_str: id of this circle
        :param x: x coordinate
        :param y: y coordinate
        :param r: radius length 
        :return: None
        """
        __self__.__prepare_attributes(**kwargs)
        __self__.__canvas.beginPath()
        __self__.__canvas.arc(x, y, r,0,2*pi)
        __self__.__canvas.fill()
        __self__.__canvas.stroke()

    def circle_segment(__self__, id_str, x0, y0, r_in, r_out, deg_from, deg_to, **kwargs):
        raise NotImplementedError

    def line(__self__,id_str,xb, yb, xe, ye, **kwargs):
        """Draws a line

        :param id_str: id of this line
        :param xb: x coordinate of line begin
        :param yb: y coordinate of line begin
        :param xe: side length of line end
        :param ye: side length of line end
        :return: None
        """
        __self__.__prepare_attributes(**kwargs)
        __self__.__canvas.beginPath()
        __self__.__canvas.moveTo(xb, yb)
        __self__.__canvas.lineTo(xe, ye)
        __self__.__canvas.stroke()

    def ellipse(__self__,id_str,x, y, rx, ry, **kwargs):
        """Draws an ellipse

        :param id_str: id of this ellipse
        :param x: x coordinate of a center
        :param y: y coordinate of a center
        :param rx: x radius length 
        :param ry: y radius length 
        :return: None
        """
        raise NotImplementedError

    def polygon(__self__,id_str,points,**kwargs):
        """Draws a polygon

        :param id_str: id of this polygon
        :param points: list of points
        :return: None
        """
        __self__.__prepare_attributes(**kwargs)
        __self__.__canvas.beginPath()
        __self__.__canvas.moveTo(points[0][0], points[0][1])
        for p in points[1:]:
            __self__.__canvas.lineTo(p[0], p[1])
        __self__.__canvas.closePath()
        __self__.__canvas.fill()
        __self__.__canvas.stroke()

    def triangle(__self__,id_str,x,y,r,**kwargs):
        """Draws a tiangle

        :param id_str: id of this triangle
        :param x: x coordinate of a center
        :param y: y coordinate of a center
        :param r: side length 
        :return: None
        """
        angle = 2 * pi / 3.0
        points = [[x + r * sin(0 * angle), y + r * cos(0 * angle)],
                            [x + r * sin(1 * angle), y + r * cos(1 * angle)],
                            [x + r * sin(2 * angle), y + r * cos(2 * angle)]]
        __self__.polygon(id_str,points,**kwargs)


    def rhomb(__self__,id_str,x,y,r,**kwargs):
        """Draws a rhomb

        :param id_str: id of this rhomb
        :param x: x coordinate of a center
        :param y: y coordinate of a center
        :param r: side length 
        :return: None
        """
        points = [[x, y + r], [x + r, y], [x, y - r], [x - r, y]]
        __self__.polygon(id_str,points,**kwargs)

    def path(__self__, id_str, elements, **kwargs):
        __self__.__prepare_attributes(**kwargs)
        raise NotImplementedError
    
    def text(__self__,id_str,x,y,text,**kwargs):
        """Draws a text

        :param id_str: id of this text
        :param x: x coordinate of a center
        :param y: y coordinate of a center
        :param text: text to be written
        :return: None
        """
        __self__.__prepare_attributes(**kwargs)
        __self__.__canvas.fillText(text, x, y)

    def circles_group(__self__,gid,x,y,c,r,**kwargs):
        """Draws a circles group

        :param id_str: id of this group
        :param x: list of x coordinates 
        :param y: list of y coordinates 
        :param r: radius length or a list of radius lengths
        :return: None
        """

        if not isinstance(r, list):
                r = [r]
        for i in range(len(x)):
            __self__.circle(gid+":"+str(i),x[i],y[i],r[i%len(r)],fill=c[i%len(c)].__str__())

    def squares_group(__self__,gid,x,y,c,a,**kwargs):
        """Draws a squares group

        :param id_str: id of this group
        :param x: list of x coordinates 
        :param y: list of y coordinates 
        :param a: side length 
        :return: None
        """
        for i in range(len(x)):
            __self__.square(gid+":"+str(i),x[i],y[i],a,fill=c[i%len(c)].__str__())

    def triangle_group(__self__,gid,x,y,c,r,**kwargs):
        """Draws a triangle group

        :param id_str: id of this group
        :param x: list of x coordinates 
        :param y: list of y coordinates 
        :param r: side length 
        :return: None
        """
        for i in range(len(x)):
            __self__.triangle(gid+":"+str(i),x[i],y[i],r,fill=c[i%len(c)].__str__())

    def rhomb_group(__self__,gid,x,y,c,r,**kwargs):
        """Draws a rhomb group

        :param id_str: id of this group
        :param x: list of x coordinates 
        :param y: list of y coordinates 
        :param r: side length 
        :return: None
        """
        for i in range(len(x)):
            __self__.rhomb(gid+":"+str(i),x[i],y[i],r,fill=c[i%len(c)].__str__())


    def translate(__self__,delta_x,delta_y):
      __self__.__canvas.translate(delta_x,delta_y)

    def viewport_name(__self__):
      """Returns the name if this viewport, which is always "CANVAS"

      """
      return "CANVAS"

    def get_width(__self__):
        """Returns viewport width
        """
        return __self__.__viewport_width

    def get_height(__self__):
        """Returns viewport height
        """
        return __self__.__viewport_height

    def error_msg(__self__,msg):
        """
        Prints error message 

        Prints error message to screen or browser's console
        """
        print(msg)
