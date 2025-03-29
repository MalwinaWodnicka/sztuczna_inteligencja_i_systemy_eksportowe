class info:
    def __init__(self):
        self.searchingTime = None
        self.visitedStates = None
        self.processedStates = None
        self.maxDepthRecursion = None
        self.duration = None
        self.lengthFound = None

    # settery
    def setSearchingTime(self, searchingTime):
        self.searchingTime = searchingTime

    def setVisitedStates(self, visitedStates):
        self.visitedStates = visitedStates

    def setProcessedStates(self, processedStates):
        self.processedStates = processedStates

    def setMaxDepthRecursion(self, maxDepthRecursion):
        self.maxDepthRecursion = maxDepthRecursion

    def setDuration(self, duration):
        self.duration = duration

    def setLengthFound(self, lengthFound):
        self.lengthFound = lengthFound

    # gettery
    def getSearchingTime(self):
        return self.searchingTime

    def getVisitedStates(self):
        return self.visitedStates

    def getProcessedStates(self):
        return self.processedStates

    def getMaxDepthRecursion(self):
        return self.maxDepthRecursion

    def getDuration(self):
        return self.duration

    def getLengthFound(self):
        return self.lengthFound

    def __str__(self):
        return (str(self.lengthFound) + "\n" + str(self.visitedStates) + "\n" + str(self.processedStates) + "\n"
                + str(self.searchingTime) + "\n" + str(self.maxDepthRecursion) + "\n" + str(self.duration))


