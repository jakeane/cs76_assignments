class CSPNode:

    def __init__(self, name, domain, neighbors):
        self.name = name
        self.domain = domain
        self.neighbors = neighbors

    def __str__(self):
        output = ""

        output += "Name: {}".format(self.name)
        output += "\n\tDomain: {}".format(self.domain)
        output += "\n\tNeightbors: "
        for neighbor in self.neighbors:
            output += "{}, ".format(neighbor.name)

        return output
