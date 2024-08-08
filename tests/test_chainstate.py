import pytest
from chainstate import (
    Chain,
    State,
    EndState,
    InitialStateNotSetError,
    StateTransitionError,
    ChainCompletedError,
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


def test_chain_completed_property():
    chain = Chain()
    chain.add_state(GreetingState)
    chain.add_state(FinalState)
    chain.set_initial_state(GreetingState)

    assert not chain.is_completed
    chain.run()
    assert chain.is_completed


def test_chain_completed_error():
    chain = Chain()
    chain.add_state(GreetingState)
    chain.add_state(FinalState)
    chain.set_initial_state(GreetingState)
    chain.run()

    with pytest.raises(ChainCompletedError):
        chain.next()


def test_chain_reset():
    chain = Chain()
    chain.add_state(GreetingState)
    chain.add_state(FinalState)
    chain.set_initial_state(GreetingState)
    chain.run()

    assert chain.is_completed
    assert chain.context.data["greeting_done"] is True

    chain.reset()
    assert not chain.is_completed
    assert chain.current_state is None
    assert "greeting_done" not in chain.context.data


def test_chain_rerun_after_reset():
    chain = Chain()
    chain.add_state(GreetingState)
    chain.add_state(FinalState)
    chain.set_initial_state(GreetingState)
    chain.run()

    chain.reset()
    chain.set_initial_state(GreetingState)
    chain.run()
    assert chain.is_completed
    assert chain.context.data["greeting_done"] is True


def test_is_completed_read_only():
    chain = Chain()
    chain.add_state(GreetingState)
    chain.add_state(FinalState)
    chain.set_initial_state(GreetingState)
    chain.run()

    assert chain.is_completed

    # Attempt to modify is_completed (should not work)
    with pytest.raises(AttributeError):
        chain.is_completed = False

    assert chain.is_completed  # Should still be True


def test_multiple_runs_without_reset():
    chain = Chain()
    chain.add_state(GreetingState)
    chain.add_state(FinalState)
    chain.set_initial_state(GreetingState)
    chain.run()

    with pytest.raises(ChainCompletedError) as excinfo:
        chain.run()

    assert "Chain has already completed execution" in str(excinfo.value)
