class Activity():
    '''
    Defines properties and methods for each activity
    '''
    
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.status = ''
        self.category = 'pending'