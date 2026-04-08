# MAT--3510---Mathematical-Modeling

Code from and for the MAT - 3510 - Mathematical Modeling course from Thomas Edison State University.

## PyCX In This Repo

For this setup, the PyCX library is used as `pycxsimulator`.

The two main files related to it are:

- `src/pycx_random_walk.py`: a small working PyCX example.
- `notebooks/pycx_verification.ipynb`: a quick notebook check that confirms the imports work.

## How PyCX Works

PyCX runs a simulation by calling three functions over and over:

1. `initialize()` sets the starting state of the model.
2. `observe()` draws the current state with Matplotlib.
3. `update()` moves the model forward by one step.

Then you pass those three functions into the GUI runner:

```python
import pycxsimulator

pycxsimulator.GUI(title="My Model", interval=0).start(
	[initialize, observe, update]
)
```

That line opens the PyCX control window and starts the model interface.

## Using PyCX From A Script

Use `src/pycx_random_walk.py` as the template.

### 1. Import what you need

```python
import matplotlib.pyplot as plt
import pycxsimulator
```

You usually import:

- `pycxsimulator` for the simulation GUI.
- `matplotlib.pyplot` as `plt` for drawing.
- Any math, random, NumPy, or other tools your model needs.

### 2. Write the three PyCX functions

In this repo's example:

- `initialize()` resets the walk to `(0, 0)`.
- `observe()` clears the figure and redraws the path.
- `update()` takes one random step and stores the new position.

That is the basic PyCX pattern: reset, draw, step.

### 3. Start the GUI

At the bottom of the script, run:

```python
if __name__ == "__main__":
	pycxsimulator.GUI(title="PyCX Random Walk", interval=0).start(
		[initialize, observe, update]
	)
```

Using `if __name__ == "__main__":` means the GUI only opens when you run the file directly.

### 4. Run the script

From the repo root, run:

```powershell
python src/pycx_random_walk.py
```

If VS Code is using the same Anaconda interpreter that was configured here, that is enough. If you want to use the exact interpreter that was already tested, run:

```powershell
C:/Users/jerem/anaconda3/python.exe src/pycx_random_walk.py
```

What to expect:

- A PyCX control window opens.
- A Matplotlib figure opens for the model.
- `Run`, `Step Once`, and `Reset` let you control the simulation.

## Using PyCX From A Notebook

### 1. Open the verification notebook

Open `notebooks/pycx_verification.ipynb`.

### 2. Run the code cell

Run Cell 2.

That cell checks that the notebook kernel can import:

- `pycxsimulator`
- `numpy`
- `scipy`
- `matplotlib`
- `networkx`

It also prints the exact file location for `pycxsimulator` and the path to the example script.

### 3. Run a PyCX model from the notebook

Because the notebook's working folder is `notebooks/`, the example script can be launched with:

```python
%run ../src/pycx_random_walk.py
```

Or with a shell command:

```python
!python ../src/pycx_random_walk.py
```

The model will open in a separate GUI window.

## Quick Reminder For Future Me

If you come back later and forget the flow, it is basically this:

1. Import `pycxsimulator` and `matplotlib.pyplot`.
2. Write `initialize()`, `observe()`, and `update()`.
3. Start the GUI with `pycxsimulator.GUI(...).start([initialize, observe, update])`.
4. Run the script directly, or launch it from a notebook with `%run`.

## Files To Look At

- `src/pycx_random_walk.py`
- `notebooks/pycx_verification.ipynb`
