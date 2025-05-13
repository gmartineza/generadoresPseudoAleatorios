from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QSpinBox, QLabel

class PRNGSelector:
    """Manages PRNG method selection and parameter forms."""
    
    # Define available PRNG methods and their parameters
    METHODS = {
        "Von Neumann": {
            "params": {
                "n": "Number of random numbers",
                "d": "Number of digits",
                "x1": "Initial number"
            }
        },
        "Fibonacci": {
            "params": {
                "n": "Number of random numbers",
                "x0": "First seed",
                "x1": "Second seed",
                "m": "Module"
            }
        },
        "Mixed Congruential": {
            "params": {
                "n": "Number of random numbers",
                "x0": "Initial seed",
                "a": "Multiplier",
                "c": "Additive constant",
                "m": "Module"
            }
        },
        "Additive Congruential": {
            "params": {
                "n": "Number of random numbers",
                "x0": "Initial seed",
                "c": "Additive constant",
                "m": "Module"
            }
        },
        "Multiplicative Congruential": {
            "params": {
                "n": "Number of random numbers",
                "x0": "Initial seed",
                "a": "Multiplier",
                "m": "Module"
            }
        }
    }

class ParameterForm(QWidget):
    """Base class for parameter input forms."""
    
    def __init__(self, params):
        super().__init__()
        self.layout = QFormLayout(self)
        self.spinboxes = {}
        
        # Create spinboxes for each parameter
        for param, description in params.items():
            spinbox = QSpinBox()
            spinbox.setMinimum(1)
            spinbox.setMaximum(999999)
            self.spinboxes[param] = spinbox
            self.layout.addRow(f"{param} ({description}):", spinbox)
    
    def get_values(self):
        """Get current parameter values."""
        return {param: spinbox.value() for param, spinbox in self.spinboxes.items()} 