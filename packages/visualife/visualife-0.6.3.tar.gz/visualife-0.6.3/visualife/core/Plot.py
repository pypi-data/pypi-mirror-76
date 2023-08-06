#! /usr/bin/env python

from visualife.core.axes import AxisX, AxisY
from visualife.core.styles import *
from math import sqrt
import math

plot_counter = 0

class PlotLegend:
  """Stores series data to draw a plot legend
  """
  def __init__(self):
    """Creates an empty PlotLegend object
    """
    self.__series = []

  def add_serie(self,title,markerstyle,markersize,color):
    """Adds serie to the list of series

       :param title: title of a serie
       :type title: ``string``
       :param markerstyle: style of series points
       :type markerstyle: ``string``
       :param markersize: size of series points
       :type markersize: ``float``
       :param color: color of series points
       :type color: ``string``
       

    """
    self.__series.append([title,markerstyle,markersize,color])

  @property
  def series(self):
    """Returns series list
    """
    return self.__series

  def draw(self,viewport,screen_x,screen_y,width,height):
    """Draws a legend on a plot

       :param screen_x: x coordinate of legend
       :type screen_x: ``float``
       :param screen_y: y coordinate of legend
       :type screen_y: ``float``
       :param width: legend width
       :type width: ``float``
       :param height: legend height
       :type height: ``float``

    """
    viewport.rect("Legend",screen_x,screen_y,width,height,fill="white")
    for i in range(len(self.series)):
      x_c =screen_x+5+self.series[i][2]
      x_t = screen_x+10+2*self.series[i][2]
      y_c = screen_y+(i+1)*height/(len(self.series)+1)
      y_t = y_c+self.series[i][2]/2
      viewport.circle("lgnd-serie1-p",x_c,y_c,self.series[i][2],fill=self.series[i][3])
      viewport.text("lgnd-serie1",x_t,y_t,self.__series[i][0],text_anchor="start")


class DataConverter:
  """Converts plot data values to screen coordinates values
  """

  __slots__ = ['__x_data', '__y_data', '__z_data', '__max_x', '__max_y', '__min_x', '__min_y', '__min_z', '__max_z']

  def __init__(self, plot, *args):
    """Converts data from ``*args`` for a given plot

       :param plot: plot object is necessary, it provides axis to calculate coordinates
       :type plot: :class:`core.Plot` 
       :param ``*args``: data to be plotted; can be :
         - two 1D lists with X and Y
         - three 1D lists with X, Y and Z
         - a list of (X,Y) pairs or (X,Y,Z) triplets
       :param type: ``list``
    """
    self.__x_data = []
    self.__y_data = []
    self.__z_data = []

    self.__min_z, self.__max_z = 0, 0

    if len(args) >= 2:  # X and Y (and possibly Z) are given as separate arrays
      self.__max_x = max(args[0])
      self.__max_y = max(args[1])
      self.__min_x = min(args[0])
      self.__min_y = min(args[1])
      if len(args) > 2:
        self.__min_z = max(args[2])
        self.__max_z = max(args[2])
        self.__z_data = args[2]

      for i in range(len(args[0])):
        ix = plot.axes['B'].screen_coordinate(args[0][i])
        iy = plot.axes['L'].screen_coordinate(args[1][i])
        self.__x_data.append(ix)
        self.__y_data.append(iy)
    else:
      self.__max_x = args[0][0][0]
      self.__max_y = args[0][0][1]
      self.__min_x = self.__max_x
      self.__min_y = self.__max_y
      found_z = False
      if len(args[0][0]) > 2:
        self.__max_z = args[0][0][2]
        self.__min_z = self.__max_z
        found_z = True

      for i in range(len(args[0])):  # there is only one array given, it holds X and Y values as rows
        self.__max_x = max(self.__max_x, args[0][i][0])
        self.__min_x = min(self.__min_x, args[0][i][0])
        self.__max_y = max(self.__max_y, args[0][i][1])
        self.__min_y = min(self.__min_y, args[0][i][1])
        ix = plot.axes['B'].screen_coordinate(args[0][i][0])# bottom axis provides scaling for X
        iy = plot.axes['L'].screen_coordinate(args[0][i][1])# left axis provides scaling for Y
        self.__x_data.append(ix)
        self.__y_data.append(iy)
        if found_z:
          v = args[0][i][2]
          if v > self.__max_z: self.__max_z = v
          elif v < self.__min_z: self.__min_z = v
          self.__z_data.append(v)

  @property
  def x_data(self):
    """Returns list with X data in screen coordinates"""
    return self.__x_data

  @property
  def y_data(self):
    """Returns list with Y data in screen coordinates"""
    return self.__y_data

  @property
  def z_data(self):
    """Returns list with Z data as provided to this object

    The returned list may be empty
    """
    return self.__z_data

  @property
  def max_x(self):
    """Returns maximum of X data in screen coordinates"""
    return self.__max_x

  @property
  def min_x(self):
    """Returns minimum of X data in screen coordinates"""
    return self.__min_x

  @property
  def max_y(self):
    """Returns maximum of Y data in screen coordinates"""
    return self.__max_y

  @property
  def min_y(self):
    """Returns minimum of Y data in screen coordinates"""
    return self.__min_y

  @property
  def max_z(self):
    """Returns maximum of Z data"""
    return self.__max_z

  @property
  def min_z(self):
    """Returns minimum of Z data"""
    return self.__min_z


class Plot:
  """Represents a plot object
  """

  __slots__ = ['__viewport','__axes', '__plot_label', '__default_style_index', '__mask_element', '__label_text_style',
               '__data_ids', '__clip_path_name','__clip_path_tics','__axes_svg', '__plot_label_font_size',
               '__max_x', '__max_y', '__min_x','__min_y','__x_range', '__y_range', '__extra_labels','__x_screen_range',
               '__y_screen_range','__axes_definition','__legend']


  def __init__(self, viewport, min_screen_x, max_screen_x, min_screen_y, max_screen_y, min_data_x, max_data_x,
               min_data_y, max_data_y, axes_definition="BL"):
    """Creates a plot object with axes

       :param viewport: selected viewport object to draw a plot
       :type viewport: :class:`core.HtmlViewport` or :class:`core.SvgViewport`
       :param min_screen_x: starting x value to draw a plot in screen coordinates
       :type min_screen_x: ``float``
       :param max_screen_x:
         ending point x value to draw a plot in screen coordinate
       :type max_screen_x: ``float``
       :param min_screen_y:
         starting point x value to draw a plot in screen coordinate
       :type min_screen_y: ``float``
       :param max_screen_y:
         ending point x value to draw a plot in screen coordinate
       :type max_screen_y: ``float``
       :param min_data_x:
         minimum x data value
       :type min_data_x: ``float``
       :param max_data_x:
         maximum x data value
       :type max_data_x: ``float``
       :param min_data_y:
         minimum y data value
       :type min_data_y: ``float``
       :param max_data_y:
         maximum y data value
       :type max_data_y: ``float``
       :param axes_definition:
         string containg letters represents axis to create in a plot <B - bottom, U - upper, R - right, L - left> ("BL" set by default)
       :type axes_definition: ``string``

       The example below creates a plot in a SVG viewport:

       .. code-block:: python

           drawing = SvgViewport("scatterplot.svg", 0, 0, 800, 400)
           plot = Plot(drawing,50,750,50,350,0.0,0.5,0.0,0.5, axes_definition="UBLR")

       Viewport is 800x400, the plot takes 700x300 of it (from 50 to 750 and from 50 to 350 along X and Y asis, respectively)
       All four axis will be shown because of "UBLR" argument. Output plot will be stored in ``scatterplot.svg`` file (SVG format).
       If you want to make a plot on a web-page, use :class:`core.HtmlViewport`:

       .. code-block:: python

              from random import random
              from browser import document
              from core.HtmlViewport import HtmlViewport
              from core.Plot import Plot

              xy_data = [ (random(), random()) for i in range(500)]
              drawing = HtmlViewport(document['svg'],0,0,600,400)
              pl = Plot(drawing,50,550,50,350,0.0,1.0,0.0,1.0, axes_definition="UBLR")
              pl.scatter(xy_data)
              pl.draw_axes()

       .. raw:: html

          <div> <svg  id="svg" xmlns="http://www.w3.org/2000/svg" class="right" width="600" height="400"></svg> </div>
          <script type="text/python">
              from random import random
              from browser import document
              from core.HtmlViewport import HtmlViewport
              from core.Plot import Plot

              xy_data = [ (random(), random()) for i in range(500)]
              drawing = HtmlViewport(document['svg'],0,0,600,400)
              pl = Plot(drawing,50,550,50,350,0.0,1.0,0.0,1.0, axes_definition="UBLR")
              pl.scatter(xy_data)
              pl.draw_axes()
              drawing.close()
          </script>
    """

    global plot_counter
    self.__viewport = viewport
    self.__axes = {}
    self.__plot_label = ''
    self.__extra_labels = []
    self.__default_style_index = 0 # We start plotting with the very first default style and increment them by one
    self.__plot_label_font_size = get_font_size((max_screen_x-min_screen_x)/40)
    self.__data_ids = []
    self.__axes_svg = {}
    self.__clip_path_name = ''
    self.__clip_path_tics = ''
    self.__max_x = None
    self.__max_y = None
    self.__min_x = None
    self.__min_y = None
    self.__x_range = (min_data_x,max_data_x)
    self.__y_range = (min_data_y,max_data_y)
    self.__x_screen_range = (min_screen_x,max_screen_x)
    self.__y_screen_range = (min_screen_y,max_screen_y)
    self.__axes_definition = axes_definition
    self.__legend = PlotLegend()

    Plot.__set_axes(min_screen_x, max_screen_x, min_screen_y, max_screen_y, min_data_x, max_data_x,
               min_data_y, max_data_y,self.__axes,axes_definition)

  @staticmethod
  def __set_axes(min_screen_x, max_screen_x, min_screen_y, max_screen_y, min_data_x, max_data_x,
               min_data_y, max_data_y,axes,axes_definition="BL"):

    if axes_definition.find("B") != -1:
      x_bottom_axis = AxisX(max_screen_y, min_screen_x, max_screen_x, min_data_x, max_data_x, 'B')
      if x_bottom_axis.label == "" : x_bottom_axis.label = " "
      x_bottom_axis.tics(13,5)
      x_bottom_axis.add_tics_labels()
      axes["B"] = x_bottom_axis

    if axes_definition.find("U") != -1:
      x_top_axis = AxisX(min_screen_y, min_screen_x, max_screen_x, min_data_x, max_data_x, 'U')
      if x_top_axis.label == "" : x_top_axis.label = " "
      x_top_axis.tics(13,5)
      x_top_axis.add_tics_labels()
      axes["U"] = x_top_axis

    if axes_definition.find("L") != -1:
      y_left_axis = AxisY(min_screen_x, max_screen_y, min_screen_y, min_data_y, max_data_y, 'L')
      if y_left_axis.label == "" : y_left_axis.label = " "
      y_left_axis.tics(13,5)
      y_left_axis.add_tics_labels()
      axes["L"] = y_left_axis

    if axes_definition.find("R") != -1:
      y_right_axis = AxisY(max_screen_x, max_screen_y, min_screen_y, min_data_y, max_data_y, 'R')
      y_right_axis.tics(13,5)
      y_right_axis.add_tics_labels()
      if y_right_axis.label == "": y_right_axis.label = " "
      axes["R"] = y_right_axis

  def clear(self):
    for name,group in self.__axes_svg.items() :
      group.parent.removeChild(group)
    self.__axes_svg.clear()

  def axes_svg_x(self):
    """Returns axes elements as an svg object"""
    return self.__axes_svg["axis"].children[1].children

  def axes_svg_y(self):
    """Returns axes elements as an svg object"""
    return self.__axes_svg["axis"].children[5].children

  @property
  def extra_labels(self):
    """Provides access to the list of extra labels of this plot

    :return: a list of labels, each label as a tuple ``(x, y, "text", dict)``. The ``dict`` holds kwargs with plotting style
    """
    return self.__extra_labels

  def add_extra_label(self, label_text, data_x, data_y, **kwargs):
    """Adds a new label that will be drawn in the plot.

    Besides tics labels, axis labels, etc a plot may also have extra labels, placed in arbitrary locations given
    in data coordinates. Plot object will convert these X,Y coordinates do screen coordinates using main X and Y axes

    :param label_text: text to be written in this plot
    :param data_x: - data X coordinate of a label
    :param data_y: - data y coordinate of a label
    :param kwargs: - style parameters
    :return: None
    """
    if len(kwargs) > 0:
      self.__extra_labels.append((data_x, data_y, label_text, kwargs))
    else:
      self.__extra_labels.append((data_x, data_y, label_text))

  def scale(self,scale):
    """ Scales plot
      :param scale: provides a scale
      :type scale: ``float``
    """
    self.__viewport.svg.attrs["transform"]="scale(%.1f)"%(scale)

  @property
  def data_ids(self):
    """Returns data_ids
    """
    return self.__data_ids

  @property
  def viewport(self):
    """Returns viewport
    """
    return self.__viewport

  @property
  def axes_svg(self):
    """Returns axes
        """
    return self.__axes_svg
  
  @property
  def x_range(self):
    """Returns x_range
        """
    return self.__x_range

  @property
  def y_range(self):
    """Returns y_range
        """
    return self.__y_range

  @property
  def max_x(self):
    """Returns max_x
        """
    return self.__max_x

  @property
  def max_y(self):
    """Returns max_y
        """
    return self.__max_y

  @property
  def plot_label(self):
    """Defines title (label) of this plot

      :getter: returns the label as text
      :setter: sets the new label text
      :type: ``string``
    """
    return self.__plot_label

  @plot_label.setter
  def plot_label(self,new_label):
    self.__plot_label = str(new_label)

  @property
  def plot_label_font_size(self):
    """Defines the font size used to draw title (label) of this plot

      :getter: returns the label font size
      :setter: sets the new label font size
      :type: ``float``
    """
    return self.__plot_label_font_size

  @plot_label_font_size.setter
  def plot_label_font_size(self, new_font_size):
    self.__plot_label_font_size = new_font_size

  @property
  def clip_path_name(self):
    """Defines clip_path_name of this plot

      :getter: returns the clip path name
      :setter: sets the new clip path name
      :type: ``string``
    """
    return self.__clip_path_name

  @clip_path_name.setter
  def clip_path_name(self,name):
    self.__clip_path_name = name

  @property
  def clip_path_tics(self):
    """Defines clip_path_name of this plot

      :getter: returns the clip path name
      :setter: sets the new clip path name
      :type: ``string``
    """
    return self.__clip_path_tics

  @clip_path_tics.setter
  def clip_path_tics(self,name):
    self.__clip_path_tics = name

  def draw_plot_label(self):
    """Draws a plot label - its title and all extra labels that has been added to this plot
    """ 
    y = self.__axes["U"].screen_y-(self.__axes["U"].max_screen_coordinate-self.__axes["U"].min_screen_coordinate)/10
    x = (self.__axes["U"].max_screen_coordinate - self.__axes["U"].min_screen_coordinate)/2 + self.__axes["U"].min_screen_coordinate
    self.__viewport.text("PlotLabel", x, y, self.__plot_label, fill=self.__axes["U"].stroke,font_size=self.plot_label_font_size)
    i = 0
    for xyl in self.__extra_labels:
      x = self.axes["B"].screen_coordinate(xyl[0])
      y = self.axes["L"].screen_coordinate(xyl[1])
      if len(xyl) == 4:
        self.__viewport.text("extra-"+str(i), x, y, xyl[2], **xyl[3])
      else:
        self.__viewport.text("extra-" + str(i), x, y, xyl[2])

  @property
  def axes(self):
    """Dictionary of axes in a plot - key is a letter defines axis (U,B,R,L) and Axis object is a value

       :getter: returns a dictionary holding axes objects; dictionary keys are ``B``, ``U``, ``R`` and ``L``
          for **b**\ ottom, **t**\ op, **r**\ ight and **l**\ eft axis, respectively
       :type: ``dictionary(Axis)``
    """
    return self.__axes

  def __set_range(self,miin,maax,tics=5):
    """Finds a nice tics ranges for data between miin and maax and returns it as a list
    """
    range_ = maax-miin
    range_ /= (tics-1)
    cnt = 0
    if range_ == 0:
      lista =  [maax-1,miin+1]
      if lista[-1] < maax:
        lista.append(lista[-1]+1)
      if lista[0] > miin:
        lista=[lista[0]-1]+lista
      return lista
    while range_ > 1.0:
      cnt += 1
      range_ /= 10
    zakres = [0.1,0.20,0.25,0.3,0.4,0.5,0.6,0.7, 0.75, 0.8,0.9,1.0]
    for i in zakres:
      if range_ < i:
        nice_range = i*(10**(cnt))
        break

    lista = []
    mi = nice_range*math.floor(miin/nice_range)
    for i in range(tics):
      lista.append(mi+i*nice_range)
    if lista[-1] < maax:
      lista.append(lista[-1]+nice_range)
    if lista[0] > miin:
      lista=[lista[0]-nice_range]+lista
  
    return lista

  def set_nice_range(self,x_tics=5,y_tics=5):
    """Finds a nice tics ranges for plot data
       Uses min and max data stared in Plot object
    """
    tics_x = self.__set_range(self.__min_x,self.__max_x,x_tics)
    tics_y = self.__set_range(self.__min_y,self.__max_y,y_tics)
    self.__axes.clear()
    print("ax",self.axes)
    self.clear()
    Plot.__set_axes(self.__x_screen_range[0],self.__x_screen_range[1],self.__y_screen_range[0],
              self.__y_screen_range[1],tics_x[0],tics_x[-1],tics_y[0],tics_y[-1],self.__axes,self.__axes_definition)
    formatx = "%d"
    formaty = "%d"
    for i in tics_x:
      if isinstance(i, float):
        formatx = "%.2f"
    for i in tics_y:
      if isinstance(i, float):
        formaty = "%.2f"
    

    for i in ["B","U"]:
      if i in self.__axes_definition:
        self.__axes[i].tics_at_values(tics_x,formatx)
        #self.__axes[i].tics_at_fraction([0,0.25,0.5,0.75,1.0],list(map(lambda x:'%.2f'%x,tics_x)))
    for i in ["L","R"]:
      if i in self.__axes_definition:
        self.__axes[i].tics_at_values(tics_y,formaty)
        
        #self.__axes[i].tics_at_fraction([0,0.25,0.5,0.75,1.0],list(map(lambda x:'%.2f'%x,tics_y)))


  def draw_axes(self):
    """Draws axes as an <svg> element
    """
    if self.__clip_path_tics == "":
      self.__viewport.start_group("Outer-Axis")
    else:  
      self.__viewport.start_group("Outer-Axis",clip_path=self.__clip_path_tics)
    self.__viewport.start_group("Axis")
    for ax_key in self.__axes:
      self.__axes[ax_key].draw(self.__viewport)
    self.__viewport.close_group()
    self.__viewport.close_group()

  def draw_grid(self):
    """Draws grid as an <svg> element
    """

    def draw_horizontal_grid_lines(x_from, x_to, y, style):
      for yi in y: self.__viewport.line("gr", x_from, yi, x_to, yi, **style)

    def draw_vertical_grid_lines(x, y_from, y_to, style):
      for xi in x: self.__viewport.line("gr", xi, y_from, xi, y_to, **style)

    self.__viewport.start_group("Grid")

    style = {'stroke_dasharray':4,'stroke': self.__axes['B'].stroke, 'stroke_width': self.__axes['B'].stroke_width / 3.0}
    draw_vertical_grid_lines(self.__axes['B'].big_screen_tics[1:-1], self.__axes['L'].min_screen_coordinate,
                             self.__axes['L'].max_screen_coordinate,style)
    draw_horizontal_grid_lines(self.__axes['B'].min_screen_coordinate, self.__axes['B'].max_screen_coordinate,
                               self.__axes['L'].big_screen_tics[1:-1],style)
    self.__viewport.close_group()

  def draw_legend(self):
    """Calculates legend position and size and draws it
    """
    n_rows = len(self.__legend.series)
    height = n_rows*30
    width = (self.axes["U"].max_screen_coordinate - self.axes["U"].min_screen_coordinate)/5
    print(width)
    y = self.axes["U"].screen_y +15
    x = self.axes["R"].screen_x - width - 5
    self.__legend.draw(self.__viewport,x,y,width,height)

  def prepare_data_colors(self, kwargs_dict):
    """Returns list of colors used to draw points

    This method makes the following choice:

      - if ``kwargs_dict`` does not contain ``"colors"`` key, a single color will be returned to plot all points
        the returned color will be selected from the current palette assigned to differentiate between data series
      - if ``"colors"`` provides a ``string`` that is a valid color palette name (i.e. registered in ``styles.known_color_scales``)
        the requested pallete is returned
      - if ``"colors"`` provides a ``int``, the number is interpreted as an index of a color in the data series palette;
        a single color is returned
      - if ``"colors"`` provides a ``list`` of values, a color is evaluated separately for every value using a color map
        If ``kwargs_dict`` provides ``"cmap"`` key, the requested color map is used for that purpose; otherwise
        a default ``"blues"`` map is used. In addition, when ``"cmap_reversed"`` key is set to ``True``,
        the cmap will be reversed, e.g. ``"red_blue"`` color map will become ``"blue_red"``

    The colors are defined based on what user requested by kwargs parameters passed to plotting methods
    as``bubbles()``, ``scatter()`` or ``line()``
    """
    colors = []
    if "colors" in kwargs_dict:
      color = kwargs_dict["colors"]                                   # --- get color of points from kwargs
      if isinstance(color, str) and color in known_color_scales:      # --- if this is a name of a known color palette,
        return known_color_scales[color]                              # ... just return its colors
      if isinstance(color, str): colors.append(color_by_name(color))  # --- it's color by name (e.g. "Red")
      elif isinstance(color, int) :                                   # --- it's the index of the default plotting color
        colors.append( get_color(default_plotting_colors[color % len(default_plotting_colors)]) )
      elif isinstance(color, ColorBase): colors.append(color)         # --- it's color object
      elif isinstance(color, list):                                   # --- it's Z-coordinate do get colors from color map
        min_z = min(color)
        max_z = max(color)
        cmap = kwargs_dict["cmap"] if "cmap" in kwargs_dict else "blues"    # --- get cmap to convert Z-values into colors
        if isinstance(cmap, str) :                                    # --- if cmap is a string, it must be a palette name
          cmap1 = colormap_by_name(cmap, min_z, max_z, if_reversed=("cmap_reversed" in kwargs_dict))
        else:
          cmap1 = cmap                                                # It's no a string -> assume it's a pallete by itselfs
        for z in color: colors.append(cmap1.color(z))
    else :
      colors.append( get_color(default_plotting_colors[self.__default_style_index]) )
      self.__default_style_index += 1

    return colors

  def set_min_and_max_data(self,*args):
    """Sets min and max of data_x and data_y of every series in a ``Plot``
       It will be used to set_nice_range() method.
    """
    check=False
    if self.__max_x != None:
      check=True
      old_max_x = self.__max_x
      old_max_y = self.__max_y
      old_min_x = self.__min_x
      old_min_y = self.__min_y

    if len(args) >= 2:  # X and Y (and possibly Z) are given as separate arrays
      self.__max_x = max(args[0])
      self.__max_y = max(args[1])
      self.__min_x = min(args[0])
      self.__min_y = min(args[1])
    else:
      self.__max_x = args[0][0][0]
      self.__max_y = args[0][0][1]
      self.__min_x = self.__max_x
      self.__min_y = self.__max_y

      for i in range(len(args[0])):  # there is only one array given, it holds X and Y values as rows
        self.__max_x = max(self.__max_x, args[0][i][0])
        self.__min_x = min(self.__min_x, args[0][i][0])
        self.__max_y = max(self.__max_y, args[0][i][1])
        self.__min_y = min(self.__min_y, args[0][i][1])

    if check:
      self.__max_x = max(self.__max_x, old_max_x)
      self.__min_x = min(self.__min_x, old_min_x)
      self.__max_y = max(self.__max_y, old_max_y)
      self.__min_y = min(self.__min_y, old_min_y)


  def scatter(self, *args, **kwargs):
    """Creates a scatterplot

    :Keyword Arguments ``(**kwargs)``:
        * *markersize* (``float``) --
          size of points of this scatterplot
        * *markerstyle* (``char``) --
          point type; available types are:

          * 'o' -- circle
          * 'c' -- circle (same as 'o')
          * 's' -- square
          * 't' -- triangle
          * 'r' -- rhomb

        * *colors* (``list`` [ ``string`` ], ``list`` [ ``float`` ]
          or ``list`` [ :class:`core.styles.ColorBase` ]) -- define fill color for points;
          the colors are cycled over for all points, so if the list contains a single elements, all points will have the same fill color
        * stroke (``float`` or :class:`core.styles.ColorBase` ) - stroke color
        * stroke_width (``float``) - stroke width
        * title (``string``) - title of this data series; if not provided, the word "scatter" will be used
        * *flush* (``bool``) -- if ``True``, the plot will be automatically send to HTML viewport
          have no efefct on SVG viewport; defalit is ``True``
    """
    marker_size = kwargs["markersize"] if "markersize" in kwargs else 3.0
    marker_style = kwargs["markerstyle"] if "markerstyle" in kwargs else 'c'  # circle marker style is the default

    title = kwargs["title"] if "title" in kwargs else "scatter"
    self.__data_ids.append(title)

    #  --- 'colors' array defines color of every point in a scatterplot;
    #  --- the array may be smaller that array of points; the modulo operation is used
    colors = self.prepare_data_colors(kwargs)
    self.set_min_and_max_data(*args)
    # Here we convert data X-Y coordinates to data screen coordinates; the points are also repacked to new arrays
    self.set_nice_range(5,3)
    data = DataConverter(self,*args)
    
    self.__legend.add_serie(title,marker_style,marker_size,colors[0])

    self.__viewport.start_group("Outer"+title,clip_path=self.clip_path_name,**kwargs) # self.__clip_path_name is the name of a path used to clip points in this plot

    if marker_style == 'c' or marker_style == 'o':  # Circle
      self.__viewport.circles_group(title,data.x_data, data.y_data, colors, marker_size, **kwargs)
    elif marker_style == 's' :  # Square
      self.__viewport.squares_group(title,data.x_data, data.y_data, colors, marker_size, **kwargs)
    elif marker_style == 't':  # Triangle
      self.__viewport.triangle_group(title,data.x_data,data.y_data, colors, marker_size, **kwargs)
    elif marker_style == 'r':  # Rhomb
      self.__viewport.rhomb_group(title,data.x_data,data.y_data, colors, marker_size, **kwargs)
    else :
      self.__viewport.error_msg("Unknown marker style")
    self.__viewport.close_group()

    if self.__viewport.viewport_name() == "HTML" and kwargs.get("flush", True):
      self.__viewport.close()

  def bubbles(self, *args, **kwargs):
    """Creates a bubble chart

    Bubble chart displays three dimensions of data. Radius of each bubble is proportional to the square root
    of Z value of each point

    :param ``*args``: data to be plotted; see ``DataConverter.__init__()`` documentation

    :Keyword Arguments ``(**kwargs)``:
        * *markersize* (``float``) --
          a value used to scale radius of each bubbles

        * *colors* (``list`` [ ``string`` ], ``list`` [ ``float`` ]
          or ``list`` [ :class:`core.styles.ColorBase` ]) -- define fill color for points;
          the colors are cycled over for all points, so if the list contains a single elements, all points will have the same fill color
        * stroke (``float`` or :class:`core.styles.ColorBase` ) - stroke color
        * stroke_width (``float``) - stroke width
        * title (``string``) - title of this data series; if not provided, the word "bubble chart" will be used
    """

    title = kwargs["title"] if "title" in kwargs else "bubble chart"
    self.__data_ids.append(title)

    # --- Here we convert data X-Y coordinates to data screen coordinates; the points are also repacked to new arrays
    data = DataConverter(self, *args)
    self.__max_x = data.max_x
    self.__max_y = data.max_y

    # --- Prepare size of each circle based on its Z value
    marker_factor = kwargs["markersize"] if "markersize" in kwargs else 3.0
    marker_size = []
    for v in data.z_data:
      marker_size.append(sqrt(v) * marker_factor)

    #  --- 'colors' array defines color of every bubble;
    if not "colors" in kwargs: # if no colors provided, use Z values
      kwargs = dict(**kwargs, colors=data.z_data)
    #  --- the array may be smaller that array of points; the modulo operation is used
    colors = self.prepare_data_colors(kwargs)

    # --- self.clip_path_name is the name of a path used to clip points in this plot
    self.__viewport.start_group("Outer" + title, clip_path=self.clip_path_name)
    self.__viewport.circles_group(title, data.x_data, data.y_data, colors, marker_size, **kwargs)
    self.__viewport.close_group()

    if self.__viewport.viewport_name() == "HTML" and kwargs.get("flush", True):
        self.__viewport.close()

  def line(self, *args, **kwargs):
    """Creates a line plot

    Line plot displays data conected with lines. 

    :Keyword Arguments ``(**kwargs)``:

        * *colors* (``list`` [ ``string`` ], ``list`` [ ``float`` ]
          or ``list`` [ :class:`core.styles.ColorBase` ]) -- define fill color for points;
          the colors are cycled over for all points, so if the list contains a single elements, all points will have the same fill color
        * stroke (``float`` or :class:`core.styles.ColorBase` ) - stroke color
        * width (``float``) - stroke width
        * title (``string``) - title of this data series; if not provided, the word "line" will be used
    """

    # --- colors to draw a line
    colors = self.prepare_data_colors(kwargs)
    title = kwargs["title"] if "title" in kwargs else "line"
    width = kwargs["width"] if "width" in kwargs else 2.0

    data = DataConverter(self,*args)

    self.__viewport.start_group("LineGroup",stroke=colors[self.__default_style_index % len(colors)].__str__(), stroke_width=width)
    for i in range (len(data.x_data)-1) :
        self.__viewport.line(title + ":" + str(i),data.x_data[i],data.y_data[i],data.x_data[i+1],data.y_data[i+1],stroke=colors[self.__default_style_index % len(colors)].__str__(), stroke_width=width)
        
    self.__viewport.close_group()

    if self.__viewport.viewport_name() == "HTML" and kwargs.get("flush", True):
        self.__viewport.close()

  def bars(self, *args, **kwargs):
    """Creates a bar plot

    :Keyword Arguments ``(**kwargs)``:

        * *colors* (``list`` [ ``string`` ], ``list`` [ ``float`` ]
          or ``list`` [ :class:`core.styles.ColorBase` ]) -- define fill color for points;
          the colors are cycled over for all points, so if the list contains a single elements, all points will have the same fill color
        * stroke (``float`` or :class:`core.styles.ColorBase` ) - stroke color
        * width (``float``) - width of each  bar (in data units!)
        * title (``string``) - title of this data series; if not provided, the word "bars" will be used
    """

    # --- colors to draw a line
    colors = self.prepare_data_colors(kwargs)
    title = kwargs["title"] if "title" in kwargs else "bars"
    width = kwargs["width"] if "width" in kwargs else \
        (self.axes['B'].max_data_value-self.axes['B'].min_data_value) / 100.0
    width = self.axes['B'].screen_coordinate(width) - self.axes['B'].screen_coordinate(0)

    # --- backup drawing style parameters
    kwargs['fill'] = kwargs.get("color",colors[self.__default_style_index % len(colors)])
    data = DataConverter(self,*args)

    self.__viewport.start_group("BarsGroup", **kwargs)
    for i in range(len(data.x_data)):
      self.viewport.rect(title + ":" + str(i), data.x_data[i], data.y_data[i], width,
                         self.__axes["B"].screen_y - data.y_data[i], **kwargs)
    self.__viewport.close_group()
    if self.__viewport.viewport_name() == "HTML" and kwargs.get("flush", True):
        self.__viewport.close()

  def boxes(self, *args, **kwargs):

    # --- colors to draw a line
    colors = self.prepare_data_colors(kwargs)
    title = kwargs["title"] if "title" in kwargs else "boxes"
    kwargs['width'] = kwargs["width"] if "width" in kwargs else 15.0
    # --- backup drawing style parameters
    kwargs['fill'] = kwargs.get("color","white")
    kwargs['stroke_width'] = kwargs.get("stroke_width", 1)
    kwargs['stroke'] = kwargs.get("stroke","black")

    if len(args) == 1 :
      data = args[0] # the passed data is a 2D array, each dimension having (x), min, q1, q2, q3, max; x is optional
    else :
      data = args   # the passed data is a bunch of 1D arrays, having (x), min, q1, q2, q3, max; x is optional
    width = kwargs.get("box_width", 10)
    self.__viewport.start_group("BoxesGroup",**kwargs)
    median_style = """stroke-width:%s; stroke:%s;""" % (kwargs['stroke_width'] * 3.0, kwargs['stroke'])
    circle_style = """stroke-width:0; fill:%s;""" % kwargs['stroke']
    for i_box in range (len(data)) :
      if len(data[i_box]) < 6 : data[i_box].insert(0, i_box + 1)
      x = self.axes['B'].screen_coordinate(data[i_box][0])
      q1 = self.axes['L'].screen_coordinate(data[i_box][2])
      q2 = self.axes['L'].screen_coordinate(data[i_box][3])
      q3 = self.axes['L'].screen_coordinate(data[i_box][4])
      ymin = self.axes['L'].screen_coordinate(data[i_box][1])
      ymax = self.axes['L'].screen_coordinate(data[i_box][5])
      # --- box
      self.viewport.rect(title + "-b-" + str(i_box), x - width * 0.5, q3, width, (q1 - q3))
      # --- median line
      self.viewport.line(title + "-l-" + str(i_box), x - width * 0.5, q2,  x + width * 0.5, q2, style=median_style)
      # --- middle circle
      self.viewport.circle(title + "-c-" + str(i_box), x,  q2, width * 0.1, style=circle_style)
      # --- top whisker
      self.viewport.line(title + "-t-" + str(i_box), x, ymax,  x, q3)
      self.viewport.line(title + "-t-" + str(i_box), x - width * 0.5, ymax,  x + width * 0.5, ymax)
      # --- down whisker
      self.viewport.line(title + "-d-" + str(i_box), x - width * 0.5, ymin,  x + width * 0.5, ymin)
      self.viewport.line(title + "-d-" + str(i_box), x, ymin,  x, q1)

    self.__viewport.close_group()

    if self.__viewport.viewport_name() == "HTML" and kwargs.get("flush", True):
        self.__viewport.close()
