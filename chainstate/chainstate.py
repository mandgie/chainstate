import logging
from typing import Optional, Type


class InitialStateNotSetError(Exception):
    """Exception raised when the initial state is not set."""

    pass


class StateTransitionError(Exception):
    """Exception raised when there's an error in state transition."""

    pass


class ChainCompletedError(Exception):
    """Exception raised when trying to progress a completed chain."""

    pass


class Context:
    def __init__(self):
        self.data = {}


class State:
    def __init__(self):
        self.context: Optional[Context] = None

    def set_context(self, context: Context):
        self.context = context

    def on_enter(self):
        pass

    def action(self):
        pass

    def next_state(self) -> Optional[Type["State"]]:
        raise NotImplementedError("next_state method must be implemented by subclasses")


class EndState(State):
    def next_state(self) -> None:
        return None


class Chain:
    def __init__(self):
        self.states = {}
        self.current_state: Optional[State] = None
        self.context = Context()
        self.logger = logging.getLogger(__name__)
        self.__is_completed = False

    def add_state(self, state_class: Type[State]):
        state_instance = state_class()
        state_instance.set_context(self.context)
        self.states[state_class] = state_instance
        self.logger.info(f"Added state: {state_class.__name__}")

    def set_initial_state(self, state_class: Type[State]):
        if state_class in self.states:
            self.current_state = self.states[state_class]
            self.current_state.on_enter()
            self.logger.info(f"Set initial state: {state_class.__name__}")
        else:
            error_message = f"State {state_class.__name__} not found."
            self.logger.error(error_message)
            raise ValueError(error_message)

    def next(self) -> bool:
        if self.__is_completed:
            raise ChainCompletedError(
                "Chain has already reached an EndState and cannot progress further."
            )

        if self.current_state is None:
            error_message = (
                "Initial state not set. Please set the initial state before proceeding."
            )
            self.logger.error(error_message)
            raise InitialStateNotSetError(error_message)

        self.current_state.action()

        next_state_class = self.current_state.next_state()
        if next_state_class is None:
            if isinstance(self.current_state, EndState):
                self.logger.info(
                    f"Reached EndState: {self.current_state.__class__.__name__}. Chain execution complete."
                )
                self.__is_completed = True
                return False
            else:
                error_message = f"State {self.current_state.__class__.__name__} returned None unexpectedly."
                self.logger.error(error_message)
                raise StateTransitionError(error_message)
        elif next_state_class not in self.states:
            error_message = f"Next state {next_state_class.__name__} has not been added to the chain."
            self.logger.error(error_message)
            raise StateTransitionError(error_message)
        else:
            self.current_state = self.states[next_state_class]
            self.current_state.on_enter()
            self.logger.info(f"Transitioned to state: {next_state_class.__name__}")
            return True

    def run(self):
        if self.__is_completed:
            raise ChainCompletedError(
                "Chain has already completed execution and cannot be run again without resetting."
            )

        if self.current_state is None:
            error_message = (
                "Initial state not set. Please set the initial state before running."
            )
            self.logger.error(error_message)
            raise InitialStateNotSetError(error_message)

        self.logger.info("Starting chain execution")
        try:
            while self.next():
                pass
            self.logger.info("Chain execution completed successfully")
        except StateTransitionError as e:
            self.logger.error(f"Chain execution failed: {str(e)}")
            raise
        except ChainCompletedError:
            self.logger.info("Chain has already completed execution")

    def reset(self):
        self.current_state = None
        self.__is_completed = False
        self.context.data.clear()
        self.logger.info("Chain has been reset")

    @property
    def is_completed(self) -> bool:
        return self.__is_completed
