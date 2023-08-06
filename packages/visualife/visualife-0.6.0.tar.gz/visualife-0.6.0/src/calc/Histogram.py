#!/usr/bin/env python3
__author__ = "Dominik Gront"
__copyright__ = "UW"
__license__ = "Apache License, Version 2.0"


class Histogram:

    __N_BINS = 100
    __WIDTH = 1
    __HIST_RANGE = (-180, 180)

    def __init__(self, **kwargs):
        """Creates a new Histogram2D instance
        :param kwargs: see below
        :return: new Histogram2D instance

        :Keyword Arguments:
            * *n_bins* (``int``) -- number of bins of equal width
            * *range* (``tuple(value,value)``) -- histogram range
            * *width* (``float``) -- bin width
            * *bins* (``list[float]``) -- list of n+1 values defining n bins
            * *bin_outliers* (``bool``) -- if True, outliers will be recorded by the first and last bin of the histogram
        """

        self.__range = kwargs.get("range", Histogram.__HIST_RANGE)

        if "n_bins" in kwargs:
            self.__n_bins = kwargs("n_bins")
            self.__width = (self.__range[1] - self.__range[0])/float(self.__n_bins)
        elif "width" in kwargs:
            self.__width = kwargs["width"]
            self.__n_bins = int((self.__range[1] - self.__range[0])/float(self.__width))

        self.__data = [0 for i in range(self.n_bins)]
        self.__count_in_hist = 0
        self.__count_outliers = 0
        self.__bin_outliers = kwargs.get("bin_outliers", False)


    @property
    def width(self):
        """Width of each bins (class) of this histogram. Each bin has the same width
        :return: bin width
        """
        return self.__width

    @property
    def n_bins(self):
        """The number of bins (classes) of this histogram. Each bin has the same width
        :return: the number of bins
        """
        return self.__n_bins

    def clear(self):
        """Removes all the data from this histogram"""
        self.__data = [0 for _ in range(self.n_bins)]

    def observe(self, *points):
        """Adds observation(s) to this histogram
        :param points: ``float`` or ``list(float)`` - data to be inserted into this histogram
        :return: None
        """
        if not isinstance(points[0], list):
            points = list(points)
        else:
            points = points[0]
        for x in points:
            if x < self.__range[0]:
                if self.__bin_outliers:
                    self.__data[0] += 1
                else:
                    self.__count_outliers += 1
            elif x >= self.__range[1]:
                if self.__bin_outliers:
                        self.__data[-1] += 1
                else:
                    self.__count_outliers += 1
            else:
                x_place = int((x-self.__range[0])/self.__width)
                self.__data[x_place] += 1

    def highest_bin(self):
        """Returns the highest bin of this histogram
        :return: tuple of two: (max_bin_index, max_counts)
        """
        max_val = max(self.__data)
        max_idx = self.__data.index(max_val)
        return max_idx, max_val

    @property
    def outliers(self):
        """ Numbers of outliers that were left outside this histogram
        :return: number of outliers
        """
        return self.__count_outliers

    def counts(self, *args):
        if args:
            return self.__data[args[0]]
        return self.__count_in_hist

    def bin_from_to(self, bin_index):
        """ Returns the range of data that is included in a given bin of this histogram
        :param bin_index: index of a bin from 0 to n_bins-1 both inclusive
        :return: bin range
        """
        return self.__range[0] + bin_index * self.__width, self.__range[0] + (bin_index + 1) * self.__width

    def __str__(self):
        s = ""
        for i in range(self.__n_bins):
            r = self.bin_from_to(i)
            s += "%6.1f %6.1f : %6d\n" % (r[0], r[1], self.__data[i])
        return s

