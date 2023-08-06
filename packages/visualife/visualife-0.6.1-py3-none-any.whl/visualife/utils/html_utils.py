from browser import html, document
from utils.text_utils import substitute_template


tooltip_style = {
    'backgroundColor': 'black',
    'color': '#fff',
    'textAlign': 'center',
    'padding': '5px 0px',
    'borderRadius': '6px',
    'visibility': 'hidden',
    'position': 'fixed'
}


def create_tooltip(id_text, tooltip_text, width, height):
    tooltip = html.DIV(tooltip_text, id=id_text,
                       style={**tooltip_style, 'height': height, 'width': width})
    return tooltip


class Menu:
    __menu_style = """
        .three_dots:after {
            content: '\\2807';
            font-size: 1.5em;
        }
        .box-shadow-menu {
          position: relative;
          padding-left: 1.25em;
        }
        .box-shadow-menu:before {
          content: "";
          position: absolute;
          left: 0;
          top: 0.25em;
          width: 1em;
          height: 0.15em;
          background: black;
          box-shadow: 
            0 0.25em 0 0 black,
            0 0.5em 0 0 black;
        }

.Menu div ul li {
    width: 30px;
    background-color: white;
}

.Menu ul ul li { width: {%width%}px; }

.Menu span.dropBottom, span.dropRight {
    display: block;
    box-shadow: inset 2px 0px 0px #222;
    position: absolute;
    left: 0px;
    width: 100%;
    height: 100%;
    top: 0px;
}

.Menu span.dropBottom {
    box-shadow: inset 0px 2px 0px #222;
    position: absolute;
    width: 100%;
    bottom: 0px;
}

/* exclude border from the top-most menu level */
div.Menu ul li { font-size: 120%; }
div.Menu ul li a { padding: 0px; }
div.Menu ul li span.dropBottom { box-shadow: inset 0px 0px 0px 0px; } 

.Menu ul {
    margin: 0;
    padding: 0;
    list-style: none;
}

.Menu ul ul {
    opacity: 0;
    position: absolute;
    top: 160%;
    visibility: hidden;
    transition: all .4s ease;
    -webkit-transition: all .4s ease;
}

.Menu ul ul ul { top: 0%; left: 160%; }

.Menu ul ul li:hover > ul {
    top: 0%;
    left: 100%;
    opacity: 1;
    visibility: visible;
}

.Menu ul li:hover > ul {
    opacity: 1; 
    background-color: rgba(255,255,255,0.8);
    top: 100%;
    visibility: visible;
    border: 1px solid gray;
}

.Menu ul li { 
    float: left; 
    position: relative; 
    background-color: rgba(255,255,255,0.8);
    cursor: pointer; 
    padding: 5px 15px;
    list-style: none;
}

.Menu ul ul li { float: none; }

.Menu ul a {
    text-decoration: none;  
    color: #000;
    padding: 10px 15px;
    text-align: center;
    font: 13px Tahoma, Sans-serif;
}

.Menu ul ul li:hover { background-color: rgba(200,200,200,0.8); }

    """

    def __init__(self, element_id, dict_of_menu_items, **kwargs):
        """Creates a HTML menu

        :param element_id: ID of a html DIV element that will contain this menu instance
        :param dict_of_menu_items: dictionary that contains the menu
        :param kwargs: see below

        :Keyword Arguments:
            * *style* (``string``) --
              style of "burger" icon: ``"burger`` or ``"dots"``
            * *width* (``int``) --
              width of menu in pixels
        """
        self.__element_id = element_id

        # Remove the preious menu (if there is any) before creating a new one
        document[element_id].innerHTML = ""

        replacements = {"{%width%}": str(kwargs.get("width", 170))}
        document <= html.STYLE(substitute_template(Menu.__menu_style, replacements))

        style = kwargs.get("style", "burger")
        style = "three_dots" if style == "dots" else "box-shadow-menu"
        ul1 = html.UL(id="ul-1-" + element_id)
        li1 = Menu.__create_item("", None, "dropBottom")
        li1.class_name = style
        ul1 <= li1

        li1 <= Menu.__create_list(dict_of_menu_items)
        document[element_id] <= ul1
        document[element_id].class_name += " Menu"


    @staticmethod
    def __create_item(menu_item, callback, span_class=""):

        li = html.LI(style={"list-style": "none", "margin": "0px"})
        a = html.A(menu_item, id=menu_item, href="#")
        if callable(callback):
            a.bind("click", callback)
        li <= a
        if span_class != "":
            li <= html.SPAN(Class=span_class)

        return li

    @staticmethod
    def __create_list(menu_items):

        ul = html.UL()
        for item, callback_or_submenu in menu_items.items():
            if isinstance(callback_or_submenu, dict):
                li = Menu.__create_item(item, None, "dropRight")
                li <= Menu.__create_list(callback_or_submenu)
                ul <= li
            else:
                if callback_or_submenu == "": callback_or_submenu = None
                ul <= Menu.__create_item(item, callback_or_submenu, "")

        return ul
