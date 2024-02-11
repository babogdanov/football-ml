class FuzzyElement:
    def __init__(self, name, type, u, a, b, ):
        self.name = name
        self.mu = self._calculate_membership(u, a,b, type) 
        self.type = type
        self.u = u

    def _calculate_membership(self,u, a, b, type):
     if type == 'G':
         if u < a:
             return 0
         if u > b:
             return 1
         return (u - a) / (b - a)
     if type == 'L':
         if u < a:
             return 1
         if u > b:
             return 0
         return (b - u) / (b - a)
     
     def __str__(self):
         return "Name: {}, type: {} u: {}, mu: {}".format(self.name, self.type, self.u, self.mu)