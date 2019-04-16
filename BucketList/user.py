class User():
    '''
    Defines properties and methods foe each user
    '''
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.bucketlists = {}
        self.logged_in = False