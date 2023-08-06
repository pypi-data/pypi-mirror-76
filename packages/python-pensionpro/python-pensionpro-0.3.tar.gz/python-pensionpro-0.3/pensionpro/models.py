class PensionProModel(object):
    _keys = set()

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)
            self._keys.add(k)
        # Add some stuff to process datetime

class Contact(PensionProModel):
    def __str__(self):
        return self.FirstName + ' ' + self.LastName
    
    def __repr__(self):
        return f'<Contact \'{self.FirstName} {self.LastName}\'>'

class Plan(PensionProModel):
    def __str__(self):
        return self.Name
    
    def __repr__(self):
        return f'<Plan \'{self.Name}\'>'

class PlanContactRole(PensionProModel):
    def __str__(self):
        return self.Id
    
    def __repr__(self):
        return f'<PlanContactRole \'{self.Id}\'>'
