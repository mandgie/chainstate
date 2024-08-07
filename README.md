# Chainstate

[![PyPI version](https://badge.fury.io/py/chainstate.svg)](https://badge.fury.io/py/chainstate)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/chainstate.svg)](https://pypi.org/project/chainstate/)

Chainstate is a powerful and intuitive Python library for implementing state machines. It provides a flexible and easy-to-use framework for defining, managing, and transitioning between states in your applications, with built-in support for sharing data between states.

## Features

- Simple and intuitive API for defining states and transitions
- Built-in context for sharing data between states
- Error handling for common state machine issues
- Extensible design allowing for custom state behaviors
- Logging support for easy debugging and monitoring
- Type hinting for improved code readability and IDE support

## Installation

Install Chainstate using pip:

```bash
pip install chainstate
```

## Quick Start

Here's a simple example to get you started with Chainstate:

```python
from chainstate import Chain, State, EndState

class GreetingState(State):
    def action(self):
        print("Hello! How can I assist you today?")
        self.context.data['user_name'] = input("Please enter your name: ")
    
    def next_state(self):
        return FarewellState

class FarewellState(EndState):
    def action(self):
        user_name = self.context.data.get('user_name', 'Guest')
        print(f"Thank you for using our service, {user_name}. Goodbye!")

# Create and run the chain
chain = Chain()
chain.add_state(GreetingState)
chain.add_state(FarewellState)
chain.set_initial_state(GreetingState)
chain.run()
```

This example creates a simple two-state chain that greets the user, asks for their name, and then says farewell using the stored name.

## Detailed Usage

### Defining States

To create a state, inherit from the `State` class and implement the `action` and `next_state` methods:

```python
class MyState(State):
    def action(self):
        # Perform the state's action
        print("Performing MyState action")
        # Store data in the context
        self.context.data['my_key'] = 'my_value'
    
    def next_state(self):
        # Return the next state class
        return NextState
```

### Creating a Chain

Use the `Chain` class to manage your states:

```python
chain = Chain()
chain.add_state(MyState)
chain.add_state(NextState)
chain.set_initial_state(MyState)
```

### Running the Chain

Execute the state machine using the `run` method:

```python
chain.run()
```

### Using the Context

The `context` attribute allows you to store and retrieve data that can be shared between states:

```python
class StateA(State):
    def action(self):
        self.context.data['shared_value'] = 42
    
    def next_state(self):
        return StateB

class StateB(State):
    def action(self):
        value = self.context.data.get('shared_value')
        print(f"Received value from previous state: {value}")
```

## Advanced Features

### Error Handling

Chainstate provides built-in error handling for common issues:

- `InitialStateNotSetError`: Raised when trying to run a chain without setting an initial state.
- `StateTransitionError`: Raised when a state transition is invalid or when a state's `next_state` method is not implemented.

### Logging

Chainstate uses Python's built-in logging module. You can configure logging to suit your needs:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Use Case: Customer Support Chatbot

Let's implement a simple customer support chatbot using Chainstate:

```python
from chainstate import Chain, State, EndState

class GreetingState(State):
    def action(self):
        print("Bot: Hello! How can I assist you today?")
        self.context.data['user_input'] = input("You: ")
    
    def next_state(self):
        user_input = self.context.data['user_input'].lower()
        if 'order' in user_input:
            return OrderState
        elif 'refund' in user_input:
            return RefundState
        else:
            return GeneralInfoState

class OrderState(State):
    def action(self):
        print("Bot: I can help you with your order. What's your order number?")
        order_number = input("You: ")
        self.context.data['order_number'] = order_number
        print(f"Bot: I've found your order {order_number}. It will be delivered in 2 days.")
    
    def next_state(self):
        return FarewellState

class RefundState(State):
    def action(self):
        print("Bot: I'm sorry to hear you need a refund. Please provide your order number.")
        order_number = input("You: ")
        self.context.data['refund_order'] = order_number
        print(f"Bot: I've initiated a refund for order {order_number}. It will be processed in 3-5 business days.")
    
    def next_state(self):
        return FarewellState

class GeneralInfoState(State):
    def action(self):
        print("Bot: For general inquiries, please visit our FAQ page at www.example.com/faq")
    
    def next_state(self):
        return FarewellState

class FarewellState(EndState):
    def action(self):
        if 'order_number' in self.context.data:
            print(f"Bot: Is there anything else I can help you with regarding your order {self.context.data['order_number']}? (yes/no)")
        elif 'refund_order' in self.context.data:
            print(f"Bot: Is there anything else I can help you with regarding your refund for order {self.context.data['refund_order']}? (yes/no)")
        else:
            print("Bot: Is there anything else I can help you with? (yes/no)")
        
        response = input("You: ")
        if response.lower() == 'yes':
            return GreetingState
        else:
            print("Bot: Thank you for using our service. Have a great day!")

# Run the chatbot
chain = Chain()
chain.add_state(GreetingState)
chain.add_state(OrderState)
chain.add_state(RefundState)
chain.add_state(GeneralInfoState)
chain.add_state(FarewellState)
chain.set_initial_state(GreetingState)
chain.run()
```

This chatbot uses Chainstate to manage different conversation flows based on user input, demonstrating how state machines can be used to create interactive and responsive systems. The context is used to store and retrieve information across different states, allowing for a more personalized interaction.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.