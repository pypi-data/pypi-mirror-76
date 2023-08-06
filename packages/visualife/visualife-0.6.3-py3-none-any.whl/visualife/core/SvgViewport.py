#! /usr/bin/env python 

from visualife.core.styles import create_style
from math import pi, sin, cos

class SvgViewport:
    """
    Saves a drawing in SVG file

    """
    default_drawing_style = """
    stroke:black;
    """
    """Default style for Svg- and HtmlViewport
    """
    default_text_style = """stroke-width:0;
    font-size: 10px;
    font-family:sans-serif;
    font-weight:normal;
    text-anchor:middle;
    color: black;
    """
    """Default text style for Svg- and HtmlViewport
    """

    #__slots__ = ['__viewport_width','__viewport_height', '__style', '__y_0', '__x_0',
     #            '__file_handler', '__file_name', '__innerHTML', '__text_style']

    def __init__(self, file_name, x_min, y_min, x_max, y_max,color="transparent",style=default_drawing_style,text_style=default_text_style):
        """
        Defines a drawing area

        :param file_name: name of file to write output svg 
        :type file_name: ``string``

        """
        
        self.__file_name = file_name
        self.__file_handler = open(file_name, "w") if len(file_name) > 0 else None
        self.__x_0 = x_min
        self.__y_0 = y_min
        self.__viewport_width = x_max - x_min
        self.__viewport_height = y_max - y_min
        self.__style=style
        self.__text_style = text_style

        self.__set_clean_viewport()

        if color != "transparent":
          self.__innerHTML += """<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" id="bg" style="fill:%s" />\n""" % (
                self.__x_0, self.__y_0, self.__viewport_width, self.__viewport_height, color)

    def __set_clean_viewport(self):

        self.__innerHTML = """<svg viewBox="%.1f %.1f %.1f %.1f" xmlns="http://www.w3.org/2000/svg" version="1.1">\n"""\
                               % (self.__x_0, self.__y_0, self.__viewport_width+self.__x_0, self.__viewport_height +self.__y_0)


        #if it's not called by HtmlViewport print <style> tag
        if self.__file_name != '': 
            self.__innerHTML += """<style>
            .default_text_style {%s}
            .default_drawing_style {%s}
            </style>\n""" % (self.__text_style,self.__style)

    def viewport_name(self):
        """Returns the name if this viewport, which is always "SVG"

        The method allows dynamic distinction between SVG and HTML viewports
        """
        return "SVG"

    def set_background(self,color):
        """Sets the background color - specially needed after clear() method"""
        self.__innerHTML +="""<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" id="bg" style="fill:%s" />\n""" % (\
                self.__x_0, self.__y_0, self.__viewport_width, self.__viewport_height, color)

    @property
    def style(self):
        """Defines the default drawing style

          :getter: returns the style
          :type: ``string``
        """
        return self.__style


    @property
    def text_style(self):
        """Defines the default style for drawing text

          :getter: returns the text style
          :type: ``string``
        """
        return self.__text_style

    def get_width(self):
        """
        Returns viewport_width
        """
        return self.__viewport_width

    def get_height(self):
        """
        Returns viewport height
        """
        return self.__viewport_height

    @property
    def innerHTML(self):
        """
        Returns innerHTML
        """
        return self.__innerHTML

    def close(self):
        """
        Closes SVG file
        """
        self.__innerHTML += "</svg>"
        if self.__file_name == "" :
            return self.__innerHTML
        else:
            self.__file_handler.write(self.__innerHTML)
            self.__file_handler.close()
            
    def clear(self):
        """
        Clears SVG file
        """
        self.__set_clean_viewport()
        
    def error_msg(self,msg):
        """
        Prints error message.

        This polymorphic method prints a given error message to sys.stderr;
        HtmlViewport will print to browser's console
        """
#        print(msg, file=sys.stderr)
        print(msg)

    def scale_x(self):
        return 1

    def scale_y(self):
        return 1

    def points_as_string(self,points):
        str = ""
        for p in points: str += "%.2f,%.2f " % (p[0], p[1])
        return str[:-1]

    def __prepare_attributes(self, **kwargs):
        """
        Parses attributes that are common for SVG elements

        :param kwargs: see below

        :Keyword Arguments:
            * *translate* (``list(number)`` or ``string``) --
              provides two coordinates for translation
            * *rotate* (``number``) --
              provide angle of rotation
            * *Class* (``string``) --
              provide CSS class name for an element (**Note** that it starts with capital 'C' since "class" is a Python keyword)
            * *transform* (``string``) --
              provide a transformation string in SVG notation
        """

        attrs = create_style(**kwargs)
        transform = ""
        if "Class" in kwargs:
            attrs += " class='%s' " % kwargs['Class']
        else:
            attrs += " class=' default_drawing_style ' " 
        if "translate" in kwargs:
            val = kwargs["translate"]
            if isinstance(val, list):
                transform = "translate(%.1f %.1f)" % (val[0], val[1])
            elif isinstance(val, str):
                transform = "translate("+val+")"
            else: self.error_msg("ERROR: unknown translate coordinates: "+str(val))
        if "rotate" in kwargs:
            transform += "rotate("+kwargs["rotate"]+")"

        if len(transform) > 0 :
            attrs += " transform='"+transform+"'"

        return attrs

    def radial_gradient(self,id_str,stop1,stop2,**kwargs):
        cx = kwargs.get("cx",'50%')
        fx = kwargs.get("fx",'50%')
        cy = kwargs.get("cy",'50%')
        fy = kwargs.get("fy",'50%')
        r = kwargs.get("r",'50%')
        self.__innerHTML += """<radialGradient id=\"%s\" cx=\"%s\" cy=\"%s\" r=\"%s\" fx=\"%s\" fy=\"%s\" >\n""" \
        % (id_str,cx,cy,r,fx,fy)
        
        self.__innerHTML += """<stop offset=\"%s\" style=\"stop-color:%s;stop-opacity:%s\" />\n"""%(stop1[0],stop1[1],stop1[2])
        self.__innerHTML += """<stop offset=\"%s\" style=\"stop-color:%s;stop-opacity:%s\" />\n"""%(stop2[0],stop2[1],stop2[2])     
        self.__innerHTML += """</radialGradient>\n"""

    def start_clip_path(self,id_str):
        self.__innerHTML += """<clipPath id="%s">\n""" % (id_str)

    def close_clip_path(self):
        self.__innerHTML += """</clipPath>\n"""

    def start_group(self,id_str,**kwargs):
        if 'clip_path' in kwargs and kwargs['clip_path']!="":
            clip_str = """ clip-path="url(#%s)" """ % kwargs['clip_path']
        else: clip_str = ""
        self.__innerHTML += """<g id="%s" %s %s>\n""" % (id_str, self.__prepare_attributes(**kwargs),clip_str)

    def close_group(self):
        self.__innerHTML += "</g>"

    def circles_group(self, gid, x, y, c, r, **kwargs):
            if not isinstance(r, list):
                r = [r]
            self.__innerHTML += """<g id="%s" %s>\n""" % (gid, self.__prepare_attributes(**kwargs))
            for i in range(len(x)):
                self.__innerHTML += \
                    """<circle cx="%.1f" cy="%.1f" r="%.1f" id="%s" fill="%s" />\n""" % (
                        x[i], y[i], r[i % len(r)], gid + ":" + str(i), c[i % len(c)].__str__())
                # self.circle(gid + ":" + str(i), x[i], y[i], r[i % len(r)],
                #             **dict(**kwargs, fill=c[i % len(c)].__str__()))
            self.__innerHTML += "</g>"

    def squares_group(self, gid, x, y, c, a, **kwargs):
            self.__innerHTML += """<g id="%s" %s>\n""" % (gid, self.__prepare_attributes(**kwargs))
            cl = "Class='" + kwargs["Class"] + "'" if "Class" in kwargs else ""
            for i in range(len(x)):
                self.__innerHTML += \
                    """<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" id="%s" fill="%s" %s />\n""" % (
                        x[i] - a / 2, y[i] - a / 2, a, a, gid + ":" + str(i), c[i % len(c)].__str__(), cl)
            self.__innerHTML += "</g>"

    def triangle_group(self, gid, x, y, c, r, **kwargs):
            self.__innerHTML += """<g id="%s" %s>\n""" % (gid, self.__prepare_attributes(**kwargs))
            for i in range(len(x)):
                self.triangle(gid + ":" + str(i), x[i], y[i], r, **dict(**kwargs, fill=c[i % len(c)].__str__()))
            self.__innerHTML += "</g>"

    def rhomb_group(self, gid, x, y, c, r, **kwargs):
            self.__innerHTML += """<g id="%s" %s>\n""" % (gid, self.__prepare_attributes(**kwargs))
            for i in range(len(x)):
                self.rhomb(gid + ":" + str(i), x[i], y[i], r, **dict(**kwargs, fill=c[i % len(c)].__str__()))
            self.__innerHTML += "</g>"

    def rect(self, id_str, x, y, w, h, **kwargs):
        """Creates a <rect> element

        :param id_str: string to be used as the ID of the element
        :param x: x coordinate of the top left corner
        :param y: y coordinate of the top left corner
        :param w: width of the rectangle
        :param h: height of the rectangle
        :param kwargs: see below

        :Keyword Arguments:
            * *rx* (``int``) --
              x radius for rounded corners
            * *ry* (``int``) --
              y radius for rounded corners
            * *angle* (``int``) --
              angle to rotate the rectangle around its center
        """

        s = " "
        if "rx" in kwargs: s += "rx='%.1f' " % kwargs["rx"]
        if "ry" in kwargs: s += "ry='%.1f' " % kwargs["ry"]
        if "angle" in kwargs:
            s += "transform='rotate(%.1f %.1f %.1f)'" % (float(kwargs["angle"]), x + w / 2.0, y + h / 2.0)

        self.__innerHTML += \
            """<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" id="%s" %s %s/>\n""" % ( \
                x, y, w, h, id_str, self.__prepare_attributes(**kwargs), s)

    def square(self,id_str,x,y,a,**kwargs):
        """Creates a square as <rect> element  

        :param id_str: string to be used as the ID of the element
        :param x: x coordinate of the center
        :param y: y coordinate of the center
        :param a: side length
        :param kwargs: parameters to prepare style attributs

        """
        self.__innerHTML +=  \
            """<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" id="%s" %s />\n""" % (\
                x-a/2, y-a/2, a, a,id_str, self.__prepare_attributes(**kwargs))

    def circle(self,id_str,x,y,r,**kwargs):
        """Creates a <circle> element  

        :param id_str: string to be used as the ID of the element
        :param x: x coordinate of the center
        :param y: y coordinate of the center
        :param r: radius length
        :param kwargs: parameters to prepare style attributs

        """
        self.__innerHTML +=  \
                """<circle cx="%.1f" cy="%.1f" r="%.1f" id="%s" %s />\n""" % (\
                x, y, r,id_str, self.__prepare_attributes(**kwargs))

    def line(self,id_str,xb, yb, xe, ye, **kwargs):
        """Creates a <line> element  

        :param id_str: string to be used as the ID of the element
        :param xb: x coordinate of line begin
        :param yb: y coordinate of line begin
        :param xe: side length of line end
        :param ye: side length of line end
        :param kwargs: parameters to prepare style attributs

        """
        self.__innerHTML +=  \
                """<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" id="%s" %s />\n"""\
                % (xb, yb, xe, ye, id_str, self.__prepare_attributes(**kwargs))

    def ellipse(self,id_str,x, y, rx, ry, **kwargs):
        """Creates a <ellipse> element  

        :param id_str: string to be used as the ID of the element
        :param x: x coordinate of a center
        :param y: y coordinate of a center
        :param rx: x radius length 
        :param ry: y radius length 
        :param kwargs: parameters to prepare style attributes

        """
        self.__innerHTML +=  \
                """<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" id="%s" %s />\n"""\
                % (x, y, rx, ry, id_str, self.__prepare_attributes(**kwargs))

    def polygon(self,id_str,points,**kwargs):
            str = self.points_as_string(points)
            self.__innerHTML +=  \
                """<polygon points="%s" id="%s"  %s />\n""" % (\
                    str, id_str, self.__prepare_attributes(**kwargs))

    def triangle(self,id_str,x,y,r,**kwargs):
        angle = 2 * pi / 3.0
        self.polygon(id_str, [[x + r * sin(0 * angle), y + r * cos(0 * angle)],
                            [x + r * sin(1 * angle), y + r * cos(1 * angle)],
                            [x + r * sin(2 * angle), y + r * cos(2 * angle)]],
                     **kwargs)

    def rhomb(self,id_str,x,y,r,**kwargs):
            self.polygon(id_str, [[x, y + r], [x + r, y], [x, y - r], [x - r, y]], **kwargs)

    def path(self, id_str, elements, **kwargs):

        str=""
        for e in elements:
            str += " "+e[0]
            if len(e) == 2 and isinstance(e[1], tuple):
                for coord in e[1]:
                    str += " %d" % coord if isinstance(coord, int) else " %.1f" % coord
            else:
                for coord in e[1:]:
                    str += " %d" % coord if isinstance(coord, int) else " %.1f" % coord
        self.__innerHTML += """<path d="%s" id="%s" %s />\n""" % (str, id_str, self.__prepare_attributes(**kwargs))

    def text(self,id_str,x,y,text,**kwargs):

        dy = kwargs.get('dy', "1.0em")
        angle = kwargs.get('angle', 0)

        font_size = kwargs.get('font_size',10)
        if isinstance(text, list): y -= font_size * (len(text))/2.0

        if angle == 0 :
            svg_txt =  """<text class= 'default_text_style' x="%.1f" y="%.1f" id='%s' %s>""" % ( x, y, id_str,create_style(**kwargs))
        else:
            svg_txt = """<text class= 'default_text_style' x="%.1f" y="%.1f" id='%s' %s transform="rotate(%.1f %.1f %.1f)"> """ % (
             x, y, id_str,create_style(**kwargs), angle, x, y)

        if isinstance(text, list):
            svg_txt += "\n"
            for it in text:
                svg_txt += """<tspan dy="%s" x="%.1f">%s</tspan>\n""" % (dy, x, it)
            svg_txt += "</text>\n"
        else:
            svg_txt += str(text)+"</text>\n"

        self.__innerHTML += svg_txt

    
