# Sem Dinheiro Api

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.7 or higher
- pip
- A virtual environment tool (optional, but recommended - for example, `venv`)

### Installing

First, clone this repository to your local machine using:

```bash
git clone <repo url>
```

Navigate to the project directory:

```bash
cd <project_directory>
```

It's recommended to create a virtual environment to keep the dependencies required by the project separate. You can do this by running:

```bash
python3 -m venv env
```

Activate the virtual environment:

- On Unix or MacOS, run:

  ```bash
  source env/bin/activate
  ```

- On Windows, run:

  ```cmd
  .\env\Scripts\activate
  ```

Next, install the project dependencies:

```bash
pip install -r requirements.txt
```

Now you're ready to run the project!

### Running the project

To start the server, run:

```bash
uvicorn src.main:app --reload
```
The application should be accessible at http://localhost:8000

---
