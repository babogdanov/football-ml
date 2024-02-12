weights = {
    'yellowCards': 0.2,
    'redCards': 0.2,
    'points': 1,
    "goals": 1,
    'possession': 0.2,
}

class FuzzyDecisionNode:
    def __init__(self, fuzzy_element, yes_node=None, no_node=None):
        self.fuzzy_element = fuzzy_element
        self.yes_node = yes_node
        self.no_node = no_node
        self.weight = weights[fuzzy_element.get_name()]
        
    def evaluate(self, standing, fit=0.5):
        name = self.fuzzy_element.get_name()
        #print(standing, name )
       # print(standing[name] )

        self.fuzzy_element.set_u(standing[name])
        #print(name, standing[name])
        conf = self.fuzzy_element.get_mu() * self.weight * 2
        # print(self.fuzzy_element, confidence, conf)
        if self.fuzzy_element.get_mu() > 0.5:
            if self.yes_node:
                return self.yes_node.evaluate(standing, (fit * conf + 0.1))
            return fit * conf
        else:
            if self.no_node:
                return self.no_node.evaluate(standing, fit * (1 - conf + 0.1))
            return fit * (1 - conf)
