class FuzzyElement:
    def __init__(self, fuzzy_config, u=None):
        self.name = fuzzy_config["name"]
        self.u = u
        self.type = fuzzy_config["type"]
        self.a, self.b = fuzzy_config["params"]["a"], fuzzy_config["params"]["b"]
        self.mu = self._calculate_membership()
        
    def set_u(self,u):
        self.u = u
        self.mu = self._calculate_membership()

    def get_name(self):
        return self.name
    
    def get_mu(self):
        return self.mu if self.mu else 0.5
    
    def _calculate_membership(self):
        if not self.u:
            return
        if self.u >= 0:
            if self.type == 'G':
                return self._get_g_score(self.a, self.b)
            else:
                return self._get_l_score(self.a, self.b)
        else:
            if self.type == 'G':
                return self._get_l_score(self.a, self.b)
            else:
                return self._get_g_score(self.a, self.b)

    def _get_g_score(self, a, b):
        if self.u < a:
            return 0
        if self.u > b:
            return 1
        return (self.u - a) / (b - a)

    def _get_l_score(self, a, b):
        if self.u < a:
            return 1
        if self.u > b:
            return 0
        return (b - self.u) / (b - a)

    def __str__(self):
        return "Name: {}, type: {} self.u: {}, mu: {}".format(self.name, self.type, self.u, self.mu)
