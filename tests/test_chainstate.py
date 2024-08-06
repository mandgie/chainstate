import pytest
from chainstate import (
    Chain,
    State,
    EndState,
    InitialStateNotSetError,
    StateTransitionError,
)


class GreetingState(State):
    def action(self):
        print("Hello! How can I assist you today?")
        self.context.data["greeting_done"] = True

    def next_state(self):
        return FinalState


class FinalState(EndState):
    def action(self):
        print("Thank you for using our service. Goodbye!")


class BrokenState(State):
    def action(self):
        print("This state is broken and will return None unexpectedly.")

    def next_state(self):
        return None


class StateWithMissingNextState(State):
    def action(self):
        print("This state transitions to a state that hasn't been added to the chain.")

    def next_state(self):
        return MissingState


class MissingState(State):
    def action(self):
        print("This state is never added to the chain.")

    def next_state(self):
        return None


class StateWithoutNextStateImplementation(State):
    def action(self):
        print("This state hasn't implemented the next_state method.")

    # Deliberately not implementing next_state method


def test_successful_chain():
    chain = Chain()
    chain.add_state(GreetingState)
    chain.add_state(FinalState)
    chain.set_initial_state(GreetingState)
    chain.run()
    assert chain.context.data["greeting_done"] is True


def test_broken_state():
    chain = Chain()
    chain.add_state(BrokenState)
    chain.set_initial_state(BrokenState)
    with pytest.raises(StateTransitionError):
        chain.run()


def test_chainstate_no_initial_state():
    chain = Chain()
    chain.add_state(GreetingState)
    chain.add_state(FinalState)
    with pytest.raises(InitialStateNotSetError):
        chain.run()


def test_missing_next_state():
    chain = Chain()
    chain.add_state(StateWithMissingNextState)
    chain.set_initial_state(StateWithMissingNextState)
    with pytest.raises(StateTransitionError) as excinfo:
        chain.run()
    assert "has not been added to the chain" in str(excinfo.value)


def test_state_without_next_state_implementation():
    chain = Chain()
    chain.add_state(StateWithoutNextStateImplementation)
    chain.set_initial_state(StateWithoutNextStateImplementation)
    with pytest.raises(NotImplementedError) as excinfo:
        chain.run()
    assert "next_state method must be implemented by subclasses" in str(excinfo.value)
