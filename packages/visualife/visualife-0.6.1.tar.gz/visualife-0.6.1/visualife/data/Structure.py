class Structure:
    """
    Holds data for a single biomolecular structure, obtained e.g. from a PDB file
    """

    def __init__(self):
        """Creates an empty structure, initiates its data structures"""
        self.__atoms = []
        self.__residues = []
        self.__chains = []

    @property
    def atoms(self):
        return self.__atoms

    @property
    def chains(self):
        return self.__chains

    @property
    def residues(self):
        return self.__residues

