from widget import SequenceViewer
from utils.text_utils import consecutive_find
from utils.html_utils import Menu


class SecondaryStructureViewer(SequenceViewer):
    """Easy to use widget that displays a secondary structure of a protein

Example of the widget is given below:

    .. raw:: html

      <div id="show_secondary"></div>
      <script type="text/python">
        from widgets import SecondaryStructureViewer

        seq = SecondaryStructureViewer("show_secondary","4fia A","CCHHHHHHHHHHHHHHCEEEEEECCEEEEEECHHHHHHHHHHCCCCCCHHHHHHHHHEECCEECCCCCCCCCCHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHCCCCCCCEEHHHHHHHHHHHHHHHHHHHCCCCCCCCCHHHHHHHHHHHHHHHHHHHHHCHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHCCCCCCHHHHHHHHHHCCCCCHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHCHHHHHHHHHHHHHHHHHCCCCCHHHHHHHHHHHHHHHHHHHHHHCCCCEEEEEECCCEEECCEEECCCEEEEEEHHHHHHCCCCCCCCCCCHHHHHHCCCCCCCCCCCCCCHHHHHCCHHHHHHHHHHHHHHHHHHHEEEEECCCCCCCEEECCCEEECCCCEEEEEEC")
        seq.add_to_selection("sel1",40,80)
        seq.selection_tooltip("sel1","first region")
      </script>

It has been created by the following code:

    .. code-block:: Python

        from widgets import SecondaryStructureViewer

        seq = SecondaryStructureViewer("show_secondary","4fia A","CCHHHHHHHHHHHHHHCEEEEEECCEEEEEECHHHHHHHHHHCCCCCCHHHHHHHHHEECCEECCCCCCCCCCHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHCCCCCCCEEHHHHHHHHHHHHHHHHHHHCCCCCCCCCHHHHHHHHHHHHHHHHHHHHHCHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHCCCCCCHHHHHHHHHHCCCCCHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHCHHHHHHHHHHHHHHHHHCCCCCHHHHHHHHHHHHHHHHHHHHHHCCCCEEEEEECCCEEECCEEECCCEEEEEEHHHHHHCCCCCCCCCCCHHHHHHCCCCCCCCCCCCCCHHHHHCCHHHHHHHHHHHHHHHHHHHEEEEECCCCCCCEEECCCEEECCCCEEEEEEC")
        seq.add_to_selection("sel1",40,80)
        seq.selection_tooltip("sel1","first region")

    """

    def __init__(self, element_id, sequence_name="", ss_string="", **kwargs):
        """Creates a widget that displays a protein secondary structure

        :param element_id: ID of a html DIV element that will contain this SecondaryStructureViewer instance
        :param sequence_name: name of the secondary structure to be shown
        :param sequence: the secondary structure itself (one-letter string, HEC-code)
        :param kwargs: only parsed by the base class constructor

        """

        super().__init__(element_id, sequence_name, ss_string, **kwargs)

        Menu("menu-" + element_id,
             {"color scheme": {"clear": self.__color_sequence_event, "HEC": self.__color_sequence_event},
              "region from selection": ""
              }, width=150)

        self.color_sequence("hec_secondary")

    def detect_blocks(self, allowed_characters=['H','E','C','L']):
        """Detects secondary structure blocks (segments)

        Returns three lists, that contain helices, strands and loops (H, E and C elements)
        :param allowed_characters: defines what to be detected, e.g. ``['H','E']`` detects only helices and strands
        (``E`` for extended)
        :return: list of SSEs
        """
        H, E, C = [], [], []
        for block in consecutive_find(self.sequence, 2, allowed_characters):
            if block[2] == 'H': H.append([block[0], block[1]])
            elif block[2] == 'E': E.append([block[0], block[1]])
            elif block[2] == 'C' or block[2] == 'L' : C.append([block[0], block[1]])

        return H, E, C


        return blocks

    def __color_sequence_event(self, evt):

        what = evt.target.id
        if what == "HEC":
            self.color_sequence("hec_secondary")
        elif what == "none" or what == "clear":
            self.color_sequence("clear")
