class info:
    def __init__(self):
        self.searchingTime = None
        self.visitedStates = None
        self.processedStates = None
        self.maxDepthRecursion = None
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

    def getLengthFound(self):
        return self.lengthFound

    def __str__(self):
        return ("Długość znalezionego rozwiązania: " + str(self.lengthFound) + "\nLiczba stanów odwiedzonych: " +
                str(self.visitedStates) + "\nLiczba stanów przetworzonych: " + str(
                    self.processedStates)  + "\nCzas trwania procesu obliczeniowego w milisekundach: " + str(
                    self.searchingTime))
