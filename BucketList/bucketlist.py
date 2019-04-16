class BucketList():
    '''
    Defines properties and methods for each bucket list
    '''

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.activities = []
        self.no_of_activities = len(self.activities)

    def add_activity(self, activity):
        '''Adds an activity to a certain bucketlist '''
        self.activities.append(activity)
        return True
