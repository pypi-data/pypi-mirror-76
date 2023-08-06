from sys import argv, stderr, stdout
import io


class ScoreFile:
    """Score file is a tabular data format, originally used by Rosetta to store energy values

    This class loads ``.sc`` / ``.fsc`` (these two are identical) and ``.fasc`` files;
    saves ``.sc``

    """

    field_width = 8

    def __init__(self, **kwargs):
        """Creates an empty object

        :param kwargs: see below

        :Keyword Arguments:
            * *skip_columns* (``list(string)``) --
              when loading data from a file, skip columns given their names
            * *rename_columns* (``list(tuple(string,string)``) --
              when loading data from a file, rename given columns
        """
        self.__annotated_sequence = None
        self.__sequence = None
        self.__columns = {}
        self.__n_rows = 0
        self.__skip_from_facs = []
        self.__rename_column = []
        if "skip_columns" in kwargs:
            for col_name in kwargs["skip_columns"]: self.__skip_from_facs.append(col_name)

        if "rename_columns" in kwargs:
            for pair in kwargs["rename_columns"]: self.__rename_column.append(pair)

    @property
    def n_rows(self):
        """
        Provides the number of data entries (rows) in this scorefile
        :return: number of rows
        """
        return self.__n_rows

    def read_score_file(self, fname):
        """Reads data in the Rosetta's score-file format

        :param fname: input file name or input data as multi-line string
        :return: None
        """

        if fname.find('\n') > 0 :       # --- it's data, not a file
            stream = io.StringIO(fname)
        else:
            stderr.write("Reading in " + fname + "\n")
            stream = open(fname)
        self.__read_score_file_data(stream)

    def column(self, col_name):
        """Returns a column by its name

        :param col_name: column name
        :return: data column
        """
        return self.__columns[col_name]

    def is_relevant_column(self,col_name):
        """Returns False if column is not relevant meaning has all values identical
        """
        val = self.column(col_name)[0]
        for i in range(1, len(self.column(col_name))):
            if val != self.column(col_name)[i]:
                return True
        return False

    def merge_in(self, other_sf):
        """Merges data from ``other_sf`` into this object

        Columns from ``other_sf`` object will be added to rows of this object for these rows where ``tag`` columns
        hold the same row names
        :param col_name: column name
        :return: None
        """
        for col_name in other_sf.column_names():
            if col_name not in self.__columns:
                source_column = other_sf.column(col_name)
                destination_col = [0 for v in other_sf.column(col_name)]
                for other_idx, tag in enumerate(other_sf.column("tag")):
                    try:
                        idx = self.find_row(tag)
                        destination_col[idx] = source_column[other_idx]
                    except:
                        pass
                self.__columns[col_name] = destination_col

    def find_row(self, tag):
        """Find a row identified by a given tag
        :param tag: decoy / structure / data row name
        :return: row number
        """
        return self.__columns["tag"].index(tag)

    def column_names(self):
        """Provides an `iterable` of column names
        :return: names of all the data columns
        """
        return self.__columns.keys()

    def write_score_file(self, fname):
        """Writes all data stored in this object in score-file format

        :param fname: output file name or an opened stream; use None to print on stdout
        :return: None
        """

        if fname is None:
            file = stdout
        else:
            if isinstance(fname, str):
                file = open(fname, "w")
            else:
                file = fname        # Assume it's an opened stream
        if self.__sequence is not None:
            file.write("SEQUENCE: " + self.__sequence + "\n")
        file.write("SCORE:")
        for col_name in self.column_names():
            fmt = " %" + str(ScoreFile.field_width) + "s"
            file.write(fmt % col_name)
        file.write("\n")
        for i in range(self.__n_rows):
            file.write("SCORE:")
            for col_name in self.column_names():
                v = self.__columns[col_name][i]
                if isinstance(v, int):
                    fmt = " %"+str(ScoreFile.field_width)+"d"
                    file.write(fmt % v)
                elif isinstance(v, float):
                    fmt = " %"+str(ScoreFile.field_width)+".2f"
                    file.write(fmt % v)
                else:
                    fmt = " %"+str(ScoreFile.field_width)+"s"
                    file.write(fmt % v)
            file.write("\n")

    def read_fasc_file(self, fname):
        """Reads a file in `.fast` (JSON) format

        :param fname: input file name
        :return: None
        """
        data = []
        for line in open(fname): data.append(eval(line.strip()))
        for col_name in data[0].keys():
            if col_name not in self.__skip_from_facs:
                self.__columns[col_name] = []
        for d in data:
            self.__n_rows += 1
            for col_name in self.column_names():
                if col_name not in self.__skip_from_facs:
                    self.__columns[col_name].append(d[col_name])
        # --- rename columns
        for pair in self.__rename_column:
            self.__columns[pair[1]] = self.__columns[pair[0]]
            del(self.__columns[pair[0]])

    def __read_score_file_data(self, file):

        line = file.readline()
        while not line.startswith("SCORE:"):
            if line.startswith("SEQUENCE"):
                tokens = line.split()
                if len(tokens) > 1: self.__sequence = tokens[1]
            if line.startswith("ANNOTATED SEQUENCE:"):
                tokens = line.split()
                if len(tokens) > 1: self.__annotated_sequence = tokens[2]
            line = file.readline()
        col_names = line.strip().split()[1:]
        for col_name in col_names:
            if col_name not in self.__skip_from_facs:
                self.__columns[col_name] = []
        for line in file:
            tokens = line.strip().split()[1:]
            self.__n_rows += 1
            for key, val in zip(col_names, tokens):
                if key not in self.__skip_from_facs:
                    try:
                        self.__columns[key].append(int(val))
                    except:
                        try:
                            self.__columns[key].append(float(val))
                        except:
                            self.__columns[key].append(val)


def combine_score_files(*args, **kwargs):
    """Reads a number of score files and combines them by merging rows of the same tag

    :param args: a list of score file names
    :param kwargs: see constructor (``__init__()`` method)
    :return: a ``ScoreFile`` object
    """
    sf = ScoreFile(**kwargs)
    if args[0].endswith(".fasc"):
        sf.read_fasc_file(args[0])
    else:
        sf.read_score_file(args[0])
    for fname in args[1:]:
        sfi = ScoreFile(**kwargs)
        if fname.endswith(".fasc"):
            sfi.read_score_file(fname)
        else:
            sfi.read_score_file(fname)
        sf.merge_in(sfi)
    return sf


if __name__ == "__main__" :

    sf = combine_score_files("out-2.fsc", *argv[1:],
            skip_columns=["pdb_name", "decoy", "nstruct", "angle_constraint", "atom_pair_constraint", "chainbreak",
                            "dslf_ca_dih", "dslf_cs_ang", "dslf_ss_dih", "dslf_ss_dst", "ref", "dihedral_constraint",
                            "model", "rmsd"],
            rename_columns=[("filename", "tag")])
    sf.write_score_file("out.fsc")
