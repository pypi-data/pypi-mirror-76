from visualife.core.shapes import arrow
from visualife.core.styles import get_color


class SequenceFeaturesBar:

    def __init__(self, viewport, sequence_ids=[], **kwargs):
        """Draws a sequence features widget

        :param viewport: where to draw the widget
        :param sequence_ids: a list of IDs for displayed sequences; sequences can also be added with ``add_sequence()`` method
        :param kwargs: see below

        :Keyword Arguments:
            * *arrow_fill* (``string`` or ``ColorBase``) --
              provides color to fill an arrow; arrow border will be made darker than the given fill
        """
        self.__sequence_ids = []
        self.__seq_annotations = {}
        self.__seq_kwargs = {}
        self.__viewport = viewport
        # graphics settings
        self.__margin_x = 20
        self.__arrow_width = 70
        self.__arrow_height = 10
        self.__seq_height = 20
        for si in sequence_ids:
            self.add_sequence(si, **kwargs)

    def add_sequence(self, seq_name, **kwargs):
        self.__sequence_ids.append(seq_name)
        self.__seq_annotations[seq_name] = []
        self.__seq_kwargs[seq_name] = kwargs

    def draw(self):

        n = 0
        arrow_center_x = self.__arrow_width/2.0 + self.__margin_x
        for si in self.__sequence_ids:
            n += 1
            y_step = n * self.__seq_height
            parms = self.__seq_kwargs[si]
            fill = get_color(parms.get("arrow_fill","white"))
            strk = fill.create_darker(0.3) if "arrow_fill" in parms else "black"
            arrow(self.__viewport, "arrow-%s" % si, self.__arrow_width, self.__arrow_height, self.__arrow_height, 0,
                  **dict(cx=70, cy=y_step, fill=fill, stroke=strk, stroke_width=parms.get("stroke_width", 1)))
            arrow_center_y = y_step - self.__arrow_height/2.0
            self.__viewport.text("label-%s" % si, arrow_center_x, arrow_center_y, si)
            self.__viewport.line("line-%s" % si, self.__margin_x*2 + self.__arrow_width, arrow_center_y, self.__viewport.get_width()-100, arrow_center_y)
            # self.__viewport.text("label-%s" % si, arrow_center_x, arrow_center_y, "1")
            # self.__viewport.text("last-%s" % si, self.__viewport.get_width() - 80, n * 20, str(len))

        self.__viewport.close()

    def add_annotation(self, begin, end, **kwargs):
        pass

    def clear_annotations(self):
        for key in self.__sequence_ids:
            self.__seq_annotations[key] = []
