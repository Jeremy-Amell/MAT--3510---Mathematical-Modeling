from pylab import plot, show

# Coefficients (change these to explore other linear recurrences)
a = 1.0   # multiplies x_{t-1}
b = 1.0   # multiplies y_{t-1}

def simulate(n_steps=30):
    # initial conditions: x0 = 1, x1 = 1
    x = 1.0   # current x_t (starts as x1)
    y = 1.0   # current y_t (y1 = x0)
    result = [1.0, 1.0]  # store x0, x1

    for t in range(2, n_steps):
        x_next = a * x + b * y
        y_next = x
        result.append(x_next)
        x, y = x_next, y_next

    return result

# Run simulation and plot
seq = simulate(n_steps=30)
plot(seq, marker='o')
show()
