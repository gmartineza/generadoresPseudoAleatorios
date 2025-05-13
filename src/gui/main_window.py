from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, 
    QComboBox, QLabel, QStackedWidget,
    QPushButton, QTextEdit
)
from PyQt6.QtCore import Qt
from .prng_selector import PRNGSelector, ParameterForm

# Import PRNG implementations
from prng.mid_square import generate_sequence as von_neumann_generate
from prng.fibonacci import generate_sequence as fibonacci_generate
from prng.congruential_mixed import generate_sequence as mixed_generate
from prng.congruential_additive import generate_sequence as additive_generate
from prng.congruential_multiplicative import generate_sequence as multiplicative_generate

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PRNG Generator")
        self.setMinimumSize(600, 400)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create PRNG selector
        prng_label = QLabel("Select PRNG Method:")
        self.prng_selector = QComboBox()
        self.prng_selector.addItems(PRNGSelector.METHODS.keys())
        self.prng_selector.currentTextChanged.connect(self.on_method_changed)
        
        # Create stacked widget for parameter forms
        self.parameter_stack = QStackedWidget()
        
        # Create generate button
        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.on_generate)
        
        # Create results display
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setPlaceholderText("Results will appear here...")
        
        # Add widgets to layout
        layout.addWidget(prng_label)
        layout.addWidget(self.prng_selector)
        layout.addWidget(self.parameter_stack)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.results_display)
        
        # Initialize with first method
        self.on_method_changed(self.prng_selector.currentText())
    
    def on_method_changed(self, method_name):
        """Handle PRNG method selection change."""
        # Create parameter form for selected method
        params = PRNGSelector.METHODS[method_name]["params"]
        form = ParameterForm(params)
        
        # Remove all widgets from stack
        while self.parameter_stack.count():
            self.parameter_stack.removeWidget(self.parameter_stack.widget(0))
        
        # Add new form to stack
        self.parameter_stack.addWidget(form)
    
    def on_generate(self):
        """Handle generate button click."""
        # Get current parameter form
        current_form = self.parameter_stack.currentWidget()
        if not current_form:
            return
        
        # Get parameter values
        params = current_form.get_values()
        method = self.prng_selector.currentText()
        
        try:
            sequence = None  # Initialize sequence variable
            # Call appropriate PRNG method
            if method == "Von Neumann":
                sequence = von_neumann_generate(
                    n=params['n'],
                    d=params['d'],
                    x1=params['x1']
                )
            elif method == "Fibonacci":
                sequence = fibonacci_generate(
                    n=params['n'],
                    x0=params['x0'],
                    x1=params['x1'],
                    m=params['m']
                )
            elif method == "Mixed Congruential":
                sequence = mixed_generate(
                    n=params['n'],
                    x0=params['x0'],
                    a=params['a'],
                    c=params['c'],
                    m=params['m']
                )
            elif method == "Additive Congruential":
                sequence = additive_generate(
                    n=params['n'],
                    x0=params['x0'],
                    c=params['c'],
                    m=params['m']
                )
            elif method == "Multiplicative Congruential":
                sequence = multiplicative_generate(
                    n=params['n'],
                    x0=params['x0'],
                    a=params['a'],
                    m=params['m']
                )
            
            if sequence is None:
                raise ValueError("No sequence was generated")
            
            # Display results
            self.results_display.setText(
                f"Parameters: {params}\n\n"
                f"Generated sequence:\n{sequence}"
            )
        except Exception as e:
            self.results_display.setText(f"Error: {str(e)}") 