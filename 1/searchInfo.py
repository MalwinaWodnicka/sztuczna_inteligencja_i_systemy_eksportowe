class Info:
    def __init__(self):
        self.searching_time = None
        self.visited_states = None
        self.processed_states = None
        self.max_depth_recursion = None
        self.length_found = None

    # settery
    def set_searching_time(self, searching_time):
        self.searching_time = searching_time

    def set_visited_states(self, visited_states):
        self.visited_states = visited_states

    def set_processed_states(self, processed_states):
        self.processed_states = processed_states

    def set_max_depth_recursion(self, max_depth_recursion):
        self.max_depth_recursion = max_depth_recursion

    def set_length_found(self, length_found):
        self.length_found = length_found

    # gettery
    def get_searching_time(self):
        return self.searching_time

    def get_visited_states(self):
        return self.visited_states

    def get_processed_states(self):
        return self.processed_states

    def get_max_depth_recursion(self):
        return self.max_depth_recursion

    def get_length_found(self):
        return self.length_found

    def __str__(self):
        return (
            "Długość znalezionego rozwiązania: " + str(self.length_found) +
            "\nLiczba stanów odwiedzonych: " + str(self.visited_states) +
            "\nLiczba stanów przetworzonych: " + str(self.processed_states) +
            "\nMaksymalna osiągnięta głębokość rekursji: " + str(self.get_max_depth_recursion()) +
            "\nCzas trwania procesu obliczeniowego w milisekundach: " + str(self.searching_time)
        )
