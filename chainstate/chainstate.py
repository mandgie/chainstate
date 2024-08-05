class InitialStateNotSetError(Exception):
    """Exception raised when the initial state is not set."""

    pass


class Context:
    def __init__(self):
        self.data = {}


class State:
    def __init__(self):
        self.context = None

    def set_context(self, context):
        self.context = context

    def on_enter(self):
        pass

    def action(self):
        pass

    def next_state(self):
        return None


class EndState(State):
    def action(self):
        print(f"{self.__class__.__name__} is an end state. No further transitions.")


class Chain:
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.context = Context()

    def add_state(self, state_class):
        state_instance = state_class()
        state_instance.set_context(self.context)
        self.states[state_class] = state_instance

    def set_initial_state(self, state_class):
        if state_class in self.states:
            self.current_state = self.states[state_class]
            self.current_state.on_enter()
        else:
            raise ValueError(f"State {state_class} not found.")

    def next(self):
        if self.current_state is None:
            raise InitialStateNotSetError(
                "Initial state not set. Please set the initial state before proceeding."
            )

        self.current_state.action()
        if isinstance(self.current_state, EndState):
            print("Reached an end state. No further transitions.")
            return False

        next_state_class = self.current_state.next_state()
        if next_state_class in self.states:
            self.current_state = self.states[next_state_class]
            self.current_state.on_enter()
            return True
        else:
            raise ValueError(f"Transition to state {next_state_class} not possible.")

    def run(self):
        if self.current_state is None:
            raise InitialStateNotSetError(
                "Initial state not set. Please set the initial state before running."
            )

        while self.next():
            pass
