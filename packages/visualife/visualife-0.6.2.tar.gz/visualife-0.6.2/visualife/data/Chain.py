class Chain:
    def __init__(self, chainid):
        self.__chain_id = chainid
        self.__residues = []
        self.__owner = None

    def __str__(self):
        return "%s" % (self.__chain_id)

    @property
    def residues(self):
        return self.__residues

    @property
    def chain_id(self):
        return self.__chain_id

    @chain_id.setter
    def chain_id(self,new_id):
        self.__chain_id = new_id

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, new_owner):
        self.__owner = new_owner




