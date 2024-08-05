import pytest
from chainstate import Chain, State, EndState, InitialStateNotSetError


class GreetingState(State):
    def on_enter(self):
        print("Entering Greeting State")

    def action(self):
        print("Hello! How can I assist you today?")
        self.context.data["greeting_done"] = True
        self.context.data["guide"] = True

    def next_state(self):
        return EndState


class EndState(EndState):
    def action(self):
        print(f"{self.__class__.__name__} is an end state. No further transitions.")


def test_chainstate():
    chain = Chain()
    chain.add_state(GreetingState)
    chain.add_state(EndState)
    chain.set_initial_state(GreetingState)
    chain.run()

    assert chain.context.data["greeting_done"] is True


def test_chainstate_no_initial_state():
    chain = Chain()
    chain.add_state(GreetingState)
    chain.add_state(EndState)
    with pytest.raises(InitialStateNotSetError):
        chain.run()
