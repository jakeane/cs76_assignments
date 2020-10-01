# PA1: FoxProblem
# Jack Keane

class FoxProblem:
    def __init__(self, start_state=(3, 3, 1)):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)
        self.traverses = [(1, 0), (0, 1), (1, 1), (2, 0), (0, 2)]

    def is_safe(self, state):
        # determine animals on each bank
        west_chickens = state[0]
        west_foxes = state[1]
        east_chickens = self.start_state[0] - west_chickens
        east_foxes = self.start_state[1] - west_foxes

        # check if numbers within correct range [0,num animal]
        if not (0 <= west_chickens <= self.start_state[0]
                and 0 <= east_chickens <= self.start_state[0]
                and 0 <= west_foxes <= self.start_state[1]
                and 0 <= east_foxes <= self.start_state[1]):
            return False

        # check if chickens will get eaten
        if (west_chickens > 0 and west_foxes > west_chickens):
            return False
        if (east_chickens > 0 and east_foxes > east_chickens):
            return False

        return True

    # get successor states for the given state
    def get_successors(self, state):
        successors = []

        for traverse in self.traverses:
            # if boat on west bank, animals will be leaving west bank
            # thus, animals are subtracted from state
            if state[2] == 1:
                succ_state = (state[0] - traverse[0],
                              state[1] - traverse[1], 0)
            # if boat on east bank, animals will be arriving to west bank
            # thus, animals are added to state
            else:
                succ_state = (state[0] + traverse[0],
                              state[1] + traverse[1], 1)

            if self.is_safe(succ_state):
                successors.append(succ_state)

        return successors

    def goal_test(self, state):
        return state == self.goal_state

    def __str__(self):
        string = "Chickens and foxes problem: " + str(self.start_state)
        return string


# A bit of test code

if __name__ == "__main__":
    test_cp = FoxProblem((5, 4, 1))
    print(test_cp.get_successors((5, 4, 1)))
    print(test_cp)
