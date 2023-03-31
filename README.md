# Mathguro 

The mathguro repository is a math tutor that helps senior highschool students in solving Pre-Calculus lessons, such as Conic Sections and Non-Linear Equations 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

1. **Python (v3.9+)** - This project was developed on version 3.9
2. **Open AI Account** - This project uses Open AI in one of its features and needed the Key for it to be run.

## Installing 

To run the application you need to make sure that the prerequisites is already installed in your local machine.

Once that is finished, It is recommended to create a Python virtual environment to isolate packages required by this project from the main environment to prevent any breaking changes to your other python projects

1. Start by installing Python 3.9+ and creating a virtual environment using `venv` or `conda`.
    - Install Python 3.9+
     - Create your `mathguro` conda environment:
        ```bash
        > conda create -n mathguro python=3.9
        ```
    - Activate your `mathguro` conda environment:
        ```bash
        > conda activate mathguro
        ```

2. After installing Python 3.9+, you can install the required python packages by running this in the project root directory

   ```bash
   $ pip install -r requirements.txt
   ```
## Running the Application

To run the GUI application, simply run this on the project root directory.

```bash
    > python controller.py
```

or press the shortcut key for run code (Ctrl + Alt + n)