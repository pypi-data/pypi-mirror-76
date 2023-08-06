#! /usr/bin/env python

import copy
from diagrams.Diagram import *


class InteractiveNode:

    def __init__(self, node, code_snippet, **params):
        self.__code_snippet = code_snippet
        self.next_command = None
        self.__node = node
        self.__lines = []
        if "lines" in params:
            self.__lines.append(int(params["lines"]))

    def __str__(self):
        return self.__code_snippet

    @property
    def lines(self):
        return self.__lines

    @property
    def code_snippet(self): return self.__code_snippet

    @property
    def node(self):
        return self.__node

    def execute(self, global_attrs):
        exec(self.__code_snippet, global_attrs)
        return self.next_command


class InteractiveCondition(InteractiveNode):

    def __init__(self, node, code_snippet, **params):
        super().__init__(node, code_snippet, **params)
        self.__true_command = None
        self.__false_command = None

    @property
    def true_command(self):
        return self.__true_command

    @true_command.setter
    def true_command(self, true_command):
        self.__true_command = true_command

    @property
    def false_command(self):
        return self.__false_command

    @false_command.setter
    def false_command(self, false_command):
        self.__false_command = false_command

    def execute(self, global_attrs):
        result = eval(self.code_snippet, global_attrs)
        self.next_command = self.__true_command if result else self.__false_command
        return self.next_command


class InteractiveDiagram(Diagram):

    def __init__(self, viewport, id):
        super().__init__(viewport, id)
        self.__globals = {}
        self.__next_cmd = None
        self.__start_cmd = None
        self.__stop_cmd = None

    @property
    def next_command(self):
        return self.__next_cmd

    def add_start(self, **attrs):
        start_box = super().add_box("start", 80, 30, **dict(**attrs, rx=20, ry=20))
        start = InteractiveNode(start_box, "True", **attrs)
        self.__start_cmd = start
        return start

    def add_stop(self, **attrs):
        stop_box = super().add_box("stop", 80, 30, **dict(**attrs, rx=20, ry=20))
        stop = InteractiveNode(stop_box, "True", **attrs)
        self.__stop_cmd = stop
        return stop

    def add_condition(self, text, w, condition_snippet, **attrs):
        box = super().add_condition(text, w, **attrs)
        return InteractiveCondition(box, condition_snippet, **attrs)

    def add_box(self, text, w, h, code_snippet, **attrs):
        box = super().add_box(text, w, h, **attrs)
        return InteractiveNode(box, code_snippet, **attrs)

    def start(self):
        self.__next_cmd = self.__start_cmd

    def next(self, if_debug = False):
        if self.__next_cmd == self.__stop_cmd: return True
        if if_debug: print("Executing:", self.__next_cmd)
        self.__next_cmd = self.__next_cmd.execute(self.__globals)
        if if_debug: print("next will be:", self.__next_cmd)
        return False

    def has_next(self):
        return not self.__next_cmd == self.__stop_cmd

    def declare_variable(self, *names):
        for n in names:
            self.__globals[n] = ""

    def list_variables(self):
        return self.__globals.keys()

    def set_value(self, name, value):
        self.__globals[name] = value

    def get_value(self, name):
        return self.__globals.get(name, "")

    def globals_copy(self):
        return  copy.deepcopy(self.__globals)
