from browser import document, html
from core.styles import known_color_scales, known_sequence_scales, colormap_by_name
from utils.html_utils import create_tooltip, Menu


class SequenceViewer:
    """Easy to use widget that displays an amino acid or nucleotide sequence.

Example of the widget is given below:

    .. raw:: html

      <div id="show_sequence"></div>
      <script type="text/python">
        from widgets import SequenceViewer

        seq = SequenceViewer("show_sequence","4fia A","GRVLQDVFLDWAKKYGPVVRVNVFHKTSVIVTSPESVKKFLMSTKYNKDSKMYRALQTVFGERLFGQGLVSECNYERWHKQRRVIDLAFSRSSLVSLMETFNEKAEQLVEILEAKADGQTPVSMQDMLTYTAMDILAKAAFGMETSMLLGAQKPLSQAVKLMLEGITASRNTKRKQLREVRESIRFLRQVGRDWVQRRREALKRGEEVPADILTQILKAEEGAQDDEGLLDNFVTFFIAGHETSANHLAFTVMELSRQPEIVARLQAEVDEVIGSKRYLDFEDLGRLQYLSQVLKESLRLYPPAWGTFRLLEEETLIDGVRVPGNTPLLFSTYVMGRMDTYFEDPLTFNPDRFGPGAPKPRFTYFPFSLGHRSCIGQQFAQMEVKVVMAKLLQRLEFRLVPGQRFGLQEQATLKPLDPVLCTLRPR")
        seq.add_to_selection("sel1",40,80)
        seq.selection_tooltip("sel1","first region")
      </script>

It has been created by the following code:

    .. code-block:: Python

        from widgets import SequenceViewer

        seq = SequenceViewer("show_sequence","4fia A","GRVLQDVFLDWAKKYGPVVRVNVFHKTSVIVTSPESVKKFLMSTKYNKDSKMYRALQTVFGERLFGQGLVSECNYERWHKQRRVIDLAFSRSSLVSLMETFNEKAEQLVEILEAKADGQTPVSMQDMLTYTAMDILAKAAFGMETSMLLGAQKPLSQAVKLMLEGITASRNTKRKQLREVRESIRFLRQVGRDWVQRRREALKRGEEVPADILTQILKAEEGAQDDEGLLDNFVTFFIAGHETSANHLAFTVMELSRQPEIVARLQAEVDEVIGSKRYLDFEDLGRLQYLSQVLKESLRLYPPAWGTFRLLEEETLIDGVRVPGNTPLLFSTYVMGRMDTYFEDPLTFNPDRFGPGAPKPRFTYFPFSLGHRSCIGQQFAQMEVKVVMAKLLQRLEFRLVPGQRFGLQEQATLKPLDPVLCTLRPR")
        seq.add_to_selection("sel1",40,80)
        seq.selection_tooltip("sel1","first region")

    """

    __style = """
.numbers {
    font-family: monospace;
    font-size: 13px;
    display: inline-block;
    text-align: right;
    padding-right: 5px;
    border-right: 1px solid LightGray;
    width: 40px;
}

.fasta {
    font-family: monospace;
    font-size: 13px;
    display: inline-block;
    padding-left: 5px;
    box-sizing: border-box;
    text-align: left;
    white-space: nowrap;
    cursor: pointer;
}

.top_row {
    overflow: visible;
    padding-left: 45px;
    font-family: monospace;
    font-size: 13px;
    height: 20px;
    display: flex;
    flex-direction: row;
    align-content: space-between;
}

.legend_item {
    display: flex;
    flex-direction: row;
    font: Arial;
    font-size: 15px;
    cursor: pointer;
}

.legend_item:disabled {
    color: gray;
}

.sequence-box { overflow: visible; }

.menu {
    width: 20px;
    height: 20px;
    right: 0px;
    cursor: context-menu;
}
    """

    def __init__(self, element_id, sequence_name="", sequence="", **kwargs):
        """Creates a widget that displays an amino acid or a nucleotide sequence

        :param element_id: ID of a html DIV element that will contain this SequenceViewer instance
        :param sequence_name: name of the sequence to be shown
        :param sequence: the sequence itself (one-letter string, FASTA-style without header)
        :param kwargs: see below

        :Keyword Arguments:
            * *palette_name* (``string``) --
              name of a color palette used to mark sequence regions (one color per region)
            * *sequence_colors* (``dict``) --
              name of a color scheme that is used to color a sequence. The available
              color schemes are defined in ``core/styles.py``. Each style is just a dictionary that provides
              a color (either by its name or hex) for every letter that may be found in sequence
            * *n_columns_of_ten* (``int``) --
              when the widget displays sequence, it puts a space after every 10 residues; by default there are
              50 residues in every line, divided in five 10-residues blocks; say ``n_columns_of_ten=4`` to display
              only 40 residues per line  or to  ``n_columns_of_ten=8`` if you like to have 80 residues per line
            * *onclick* (``function``) --
              provide a function that will be called at ``onclick`` event; the function must accept
              sole ``event`` object argument
            * *first_residue_id* (``int``) --
              integer index of the very first residue in the given sequence (1 by default)
        """

        self.__element_id = element_id
        self.__sequence_name = sequence_name
        self.__sequence = sequence
        self.__secondary_structure = ""
        self.__selecting_allowed = kwargs.get("selecting_allowed", False)
        self.__first_residue_id = kwargs.get("first_residue_id", 1)
        self.__chars_in_block = 10
        self.__selections = {}
        self.__selection_colors = {}
        self.__selection_cmap = None
        self.__selection_tooltips = {}
        self.__selections_palette_name = kwargs.get("palette_name", "pastel1")
        self.__selections_palette = known_color_scales[self.__selections_palette_name]
        self.__regions_shown = {}
        self.click_on_sequence_callback = self.__click_letter_default
        self.click_on_legend_callback = self.__click_on_legend_default

        self.__blocks_in_line = kwargs.get("n_columns_of_ten", 5)
        width = int(86 * self.__blocks_in_line + 10)

        document <= html.STYLE(SequenceViewer.__style)

        max_width_style = {'width': '%spx' % str(width+50), 'max-width': '%spx' % str(width+50)}
        d1 = html.DIV('', Class="sequence-box", id="SequenceViewer-"+element_id, style=max_width_style)

        width_style = {'width': '%spx' % str(width-5), 'max-width': '%spx' % str(width-5)}
        d2 = html.DIV('', Class="top_row", id="top-row-" + element_id, style=width_style)

        d2 <= html.DIV('', id="header-" + element_id, style={"width": "%dpx" % (width-40)})
        d2 <= html.DIV('', Class="menu", id="menu-" + element_id)
        d1 <= d2

        d3 = html.DIV('', style={'display': 'flex', 'flex-direction': 'row'})
        d3 <= html.DIV('', Class="numbers", id="numbers-"+element_id)
        width_style = {'width': '%spx' % str(width), 'max-width': '%spx' % str(width)}
        d3 <= html.DIV('', Class="fasta", id="fasta-"+element_id, style=width_style)
        d1 <= d3
        d1 <= html.DIV('', id="legend-box-" + element_id, style={'display': 'flex', 'flex-direction': 'row',
                    'width': '%spx' % str(width+50), 'max-width': '%spx' % str(width+50), 'flex-wrap':'wrap',
                    'padding-top':'10px'})
        document[element_id] <= d1

        Menu("menu-" + element_id,
                    {"color scheme": {
                        "clear": self.__color_sequence_event,
                        "secondary": self.__color_sequence_event,
                        "clustal":self.__color_sequence_event},
                     "region from selection": ""
                     },
                    width=150)

        self.sequence_name = sequence_name
        if len(sequence) > 0:
            self.load_sequence(sequence)

        if "sequence_colors" in kwargs:
            self.color_sequence(kwargs["sequence_colors"])

    @property
    def element_id(self):
        """Provides ID of the page element that holds this widget (parent element)

        :return: ID of the parent HTML element
        """
        return self.__element_id

    def region_legend_id(self, region_name):
        """Returns the ID of a legion legend element
        :param region_name: a region name, assigned at ``add_to_region()`` call
        :return: ID of the DOM element that holds legend for that sequence region
        """
        return "legend-box-" + self.__element_id + "-" + region_name

    @property
    def sequence_name(self):
        """
        Name of the sequence displayed by this viewer.

        :getter: returns the sequence name
        :setter: sets a new name for this sequence
        :type: string
        """
        return self.__sequence_name

    @sequence_name.setter
    def sequence_name(self, name):
        self.__sequence_name = name
        if self.__sequence_name != "":
            document["header-" + self.__element_id].innerHTML = "&gt; "+self.__sequence_name

    @property
    def sequence(self):
        """Protein / nucleotide sequence displayed by this viewer.

        :getter: Returns the sequence
        :setter: not available, use load_sequence() instead
        :type: string
        """
        return self.__sequence

    @property
    def secondary_structure(self):
        """Protein / nucleotide secondary structure - for coloring purposes only

        :getter: returns the secondary structure
        :setter: sets secondary structure string for this sequence
        :type: string
        """
        return self.__secondary_structure

    @property
    def first_residue_id(self):
        """Index of the very first residue in that sequence

        :getter: returns the index
        :setter: sets the new index value
        :type: integer
        """
        return self.__first_residue_id

    @first_residue_id.setter
    def first_residue_id(self, index):
        self.__first_residue_id = index
        self.load_sequence(self.sequence)   # Reload the sequence since numbering has been changed

    @property
    def click_on_legend_callback(self):
        """procedure called when a user clicks on a sequence's letter

        :getter: returns the callback procedure
        :setter: sets the new callback procedure for ``onclick`` event
        :type: function
        """
        return self.__click_on_legend_callback

    @click_on_legend_callback.setter
    def click_on_legend_callback(self, callback):
        self.__click_on_legend_callback = callback

    @property
    def click_on_sequence_callback(self):
        """procedure called when a user clicks on a sequence's letter

        :getter: returns the callback procedure
        :setter: sets the new callback procedure for ``onclick`` event
        :type: function
        """
        return self.__onclick_callback

    @click_on_sequence_callback.setter
    def click_on_sequence_callback(self, callback):
        self.__onclick_callback = callback

    @property
    def regions_palette(self):
        """A name of color palette used to color marked regions.

        To display more than one regions, use one of the categorical palettes defined in styles.known_color_scales,
        such as ``"tableau10"``, ``"pastel1"`` or ``"accent"``. To color residues by a real-valued property, use
        a continuous color scale such as ``"violet_red"``

        :getter: returns the  name of color palette used to color selected regions
        :setter: sets the new palette
        :type: string
        """
        return self.__selections_palette_name

    @regions_palette.setter
    def regions_palette(self, palette_name):
        if palette_name in known_color_scales:
            self.__selections_palette_name = palette_name
        self.__selections_palette = known_color_scales[self.__selections_palette_name]
        self.__selection_cmap = colormap_by_name(self.__selections_palette_name, 0.0, 1.0)

    def add_to_region(self, region_name, if_show_region=True, **kwargs):
        """Add a block of amino acids/nucleotides to a sequence region

        This method updates an existing region. If the given region name has not been used so far,
        a new region will be created

        :param region_name: name of this sequence region
        :param if_show_region: if True, the sequence region will be made visible after this change
        :param kwargs: see below

        :Keyword Arguments:
            * *color* (``string``, ``ColorBase``, ``int`` or ``list[float]``) --
              provides color for this region:
                - directly as ColorBase object
                - by color name as ``string``
                - by index of a color in the palette defined by ``regions_palette()``
                - by real values: color map will be used to color the region
              color is assigned only to newly created blocks; extending a block doesn't change its color
            * *tooltip* -- a tooltip text will be shown when mouse cursor is over the region (*mouseover* event)
            * *by_residue_id* (``bool``) -- by default is ``False``; when set to ``True``, ``pos_from`` and ``pos_to``
              will be considered residue IDs rather than indexes from 1
            * *show_in_legend* (``bool``) -- if ``True``, the region will be also listed in a legend box
            * *first_pos* (``int``) -- first residue included in this region, numbers start from 1;
              if no *last_pos* is provided, *last_pos* will be set to ``first_pos``
            * *last_pos* (``int``) -- last residue included in this region, numbers start from 1;
              if no *first_pos* is provided, *first_pos* will be set to ``last_pos``
            * *sequence* (``string``) -- a string that is the sequence fragment
        :return: None
        """
        if_legend = kwargs.get("show_in_legend", True)
        if region_name not in self.__selections:
            if "color" in kwargs:
                self.__selection_colors[region_name] = kwargs["color"]
            else:
                self.__selection_colors[region_name] = len(self.__selections)
            self.__selections[region_name] = []
            document <= create_tooltip(region_name+"-tooltip", "", 200, 10)
            if if_legend:
                clr = self.__selection_colors[region_name]
                if isinstance(clr, int):
                    color = self.__selections_palette[clr]
                elif isinstance(clr, float):
                    color = self.__selection_cmap(0)
                else:
                    color = clr
                dot = html.SPAN("&#9679;", style={'color': color, 'padding': '0px 10px 0px 20px'})
                legend_div = html.DIV("", Class="legend_item", id=self.region_legend_id(region_name))
                legend_div <= dot
                legend_div <= html.DIV(kwargs.get("tooltip", ""), id="legend-box-" + self.__element_id + "-" + region_name + "-text")
                document["legend-box-" + self.__element_id] <= legend_div
                legend_div.bind("click", self.__click_legend_dispatch)
        first = -self.__first_residue_id if "by_residue_id" in kwargs else 0
        if "sequence" in kwargs:
            pos = self.sequence.find(kwargs["sequence"])
            if pos > -1:
                pos_from = pos + 1
                pos_to = pos_from + len(kwargs["sequence"])
        elif "first_pos" in kwargs:
            pos_from = kwargs["first_pos"]
            pos_to = kwargs.get("last_pos", pos_from)
        elif "last_pos" in kwargs:
            pos_to = kwargs["last_pos"]
            pos_from = kwargs.get("first_pos", pos_to)

        self.__selections[region_name].append((pos_from+first, pos_to+first))

        if "tooltip" in kwargs:
            self.region_tooltip(region_name, kwargs["tooltip"])
        if if_show_region: self.show_region(region_name)

    def delete_region(self, region_name):
        """Permanently removes a sequence region

        If you just want to hide a region, use ``hide_region()`` instead
        :param region_name: name of a sequence region to be deleted
        :return: None
        """
        for d in [self.__selections, self.__selection_colors, self.__selection_tooltips]:
            if region_name in d:
                del(d[region_name])

    def delete_regions(self):
        """Permanently removes all regions defined for a sequence

        :return: None
        """
        for name in self.__selections: self.delete_region(name)

    def show_region(self, region_name):
        """Activates a given region

        :param region_name: name of a sequence region to be made visible
        :return: None
        """

        if region_name not in self.__selections: return

        self.__regions_shown[region_name] = True
        if isinstance(self.__selection_colors[region_name],int):
            color = [self.__selections_palette[self.__selection_colors[region_name]]]
        elif isinstance(self.__selection_colors[region_name], list):
            color = [self.__selection_cmap[f] for f in self.__selection_colors[region_name]]
        else:
            color = [self.__selection_colors[region_name]]

        id_str = "ch-" + self.__element_id + "-"
        for chunk in self.__selections[region_name]:
            for i in range(chunk[0] + 1, min(chunk[1] + 2, len(self.__sequence)+1)):
                el = document[id_str+str(i)]
                el.style.backgroundColor = str(color[i % len(color)])
                el.class_name += " "+region_name+"-tipcls"

    def hide_region(self, region_name):
        """Deactivates a given sequence region

        This method does not remove any region, it just clears the color
        :param region_name: name of a sequence region to be made cleared off
        :return: None
        """

        if region_name not in self.__selections: return

        self.__regions_shown[region_name] = False
        id_str = "ch-" + self.__element_id + "-"
        for chunk in self.__selections[region_name]:
            for i in range(chunk[0] + 1, min(chunk[1] + 2, len(self.__sequence)+1)):
                document[id_str + str(i)].style.backgroundColor = "#FFFFFF"

    def flip_region(self, region_name):
        """
        Flips region visibility: visible region will be hidden while a hidden region will be shown
        :param region_name:  name of a sequence region
        :return: None
        """
        print(region_name)
        if not self.__regions_shown[region_name]: self.show_region(region_name)
        else: self.hide_region(region_name)

    def region_tooltip(self, region_name, tooltip):
        """Sets a text that will show up in a tooltip

        The given text will be displayed in a tooltip box when a user hoovers the given sequence region
        with a mouse pointer. Use empty string to clear a tooltip

        :param region_name: name of a sequence region that needs a tooltip
        :param tooltip: tooltip text
        :return: None
        """

        self.__selection_tooltips[region_name] = tooltip
        document[region_name+"-tooltip"].innerHTML = tooltip
        el_id = "legend-box-" + self.__element_id + "-" + region_name + "-text"
        if el_id in document:
            document[el_id].innerHTML = tooltip

    def region_for_name(self, region_name):
        """ Returns a sequence region registered under a given name
        :param region_name: region name

        :return: a list of residue ranges (from, to) - both inclusive from 0, e.g. ``[(0,5),(7,20)]``
        """
        return self.__selections[region_name]

    def region_for_position(self, pos):
        """ Returns a sequence region a given residue belongs to
        :param pos: residue position from 1

        :return: a region name and  a list of ranges as in ``region_for_name()`` or None if a given residue
          doesn't belong to any region
        """
        for name, region in self.__selections.items():
            for chunk in region:
                if pos >= chunk[0] and pos <= chunk[1]:
                    return name, region
        return None, None

    def which_region_in_legend(self, evt):
        """Returns the sequence region corresponding to a legend item user clicked on.

        :param evt: event object passed by a browser, that holds the clicked element
        :return: tuple of two: sequence region name and the residues' range as a list of lists of int
        """
        for name, region in self.__selections.items():
            if evt.target.id.find(name) > -1 : return name, region
        return None, None

    def __click_letter_default(self, evt):

        if not self.__selecting_allowed: return

        aa = document["fasta-" + self.__element_id].children
        pos = self.__locate_letter(evt.target)
        if aa[pos].style.backgroundColor == "rgb(255, 255, 0)":
            aa[pos].style.backgroundColor = "#FFFFFF"
        else:
            aa[pos].style.backgroundColor = "rgb(255, 255, 0)"

    def __click_on_legend_default(self, evt):

        name, _ = self.which_region_in_legend(evt)
        if name: self.flip_region(name)

    def __click_letter_dispatch(self, evt):
        return self.click_on_sequence_callback(evt)

    def __click_legend_dispatch(self, evt):
        return self.click_on_legend_callback(evt)

    def __locate_letter(self, obj):
        i = 0
        for o in document["fasta-" + self.__element_id].children:
            if o == obj: return i
            i += 1
        return None

    def __show_tooltip(self, evt):

        class_name = evt.target.class_name
        if len(class_name) < 2 : return
        for tip_name in self.__selection_tooltips:
            if class_name.find(tip_name) > -1 :
                if len(self.__selection_tooltips[tip_name]) > 0:
                    document[tip_name + "-tooltip"].style.visibility = 'visible'
                    document[tip_name + "-tooltip"].style.top = str(evt.clientY + 20) + 'px'
                    document[tip_name + "-tooltip"].style.left = str(evt.clientX + 20) + 'px'

    def __hide_tooltips(self, evt):

        for tip_name in self.__selection_tooltips:
            document[tip_name + "-tooltip"].style.visibility = 'hidden'

    def __color_sequence_event(self, evt):
        what = evt.target.id
        print("coloring by", what)
        self.color_sequence(what)

    def color_sequence(self, color_scheme_name):

        fasta_seq = document["fasta-" + self.element_id]
        if color_scheme_name == "none" or color_scheme_name == "clear":
            for span in fasta_seq.getElementsByTagName("span"):
                span.style.color = "black"

        if color_scheme_name == "secondary" and len(self.secondary_structure)==len(self.sequence):
            ii = 0
            color_scheme = known_sequence_scales["hec_secondary"]
            for span in fasta_seq.getElementsByTagName("span"):
                if span.innerHTML == ' ' or span.innerHTML == '-' or span.innerHTML == '_':
                    continue
                ch = self.secondary_structure[ii]
                span.style.color = color_scheme.get(ch,"black")
                ii += 1

        if color_scheme_name not in known_sequence_scales:
            return
        color_scheme = known_sequence_scales[color_scheme_name]
        for span in fasta_seq.getElementsByTagName("span"):
            ch = span.innerHTML
            span.style.color = color_scheme.get(ch,"black")

    def load_sequence(self, fasta_sequence):
        """ Replaces the sequence displayed by this object with a new one

        :param fasta_sequence: a new sequence to be loaded (one-letter code)
        :return: None
        """

        n = self.__chars_in_block
        subseq = [fasta_sequence[i:i + n] for i in range(0, len(fasta_sequence), n)]
        i_block, i_row, i_char = 0, 0, 0
        document["numbers-" + self.element_id] <= html.SPAN(str(self.__first_residue_id)) + html.BR()
        id_str = "ch-" + self.__element_id + "-"
        for block in subseq:
            for ch in block:
                i_char += 1
                document["fasta-" + self.element_id] <= html.SPAN(ch, id=id_str + str(i_char))
            document["fasta-"+self.element_id] <= html.SPAN(" ")
            i_block += 1
            if i_block % self.__blocks_in_line == 0 and len(block) == self.__chars_in_block and block != subseq[-1]:
                i_row += 1
                ir = i_row * self.__chars_in_block * self.__blocks_in_line + self.__first_residue_id
                document["numbers-" + self.element_id] <= html.SPAN(str(ir)) + html.BR()
                document["fasta-" + self.element_id] <= html.BR()
        for c in document["fasta-" + self.element_id].children:
            c.bind("click", self.__click_letter_dispatch)
            c.bind("mouseover", self.__show_tooltip)
            c.bind("mouseout", self.__hide_tooltips)
