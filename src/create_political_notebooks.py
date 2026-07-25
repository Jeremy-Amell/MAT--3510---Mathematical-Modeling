"""Generate Q1-Q7 notebooks for the political opinion dynamics scenario."""
import json, pathlib, uuid

OUT = pathlib.Path(__file__).parent.parent / "notebooks"
OUT.mkdir(exist_ok=True)

def nb(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3 (ipykernel)",
                           "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11.0"}
        },
        "nbformat": 4, "nbformat_minor": 5
    }

def md(src):
    return {"cell_type": "markdown", "id": uuid.uuid4().hex[:8],
            "metadata": {}, "source": src}

def code(src):
    return {"cell_type": "code", "execution_count": None, "id": uuid.uuid4().hex[:8],
            "metadata": {}, "outputs": [], "source": src}

# Shared preamble — specific case stated at the top of every notebook
CASE_MD = md([
    "**Specific case:** $p_X = 0.4$,\\; $p_Y = 0.3$,\\; $p_Z = 0.3$\n",
    "\n",
    "where $p_X$ = Republican, $p_Y$ = Democrat, $p_Z = 1 - p_X - p_Y$ = Independent.\n",
    "All analysis below uses this starting state.\n",
])

STEP_SRC = [
    "def step(px, py):\n",
    "    \"\"\"One discrete time step.  pz = 1 - px - py is derived.\"\"\"\n",
    "    pz = 1 - px - py\n",
    "    xy = px * max(py - px, 0)   # X -> Y\n",
    "    xz = px * max(pz - px, 0)   # X -> Z\n",
    "    yx = py * max(px - py, 0)   # Y -> X\n",
    "    yz = py * max(pz - py, 0)   # Y -> Z\n",
    "    zx = pz * max(px - pz, 0)   # Z -> X\n",
    "    zy = pz * max(py - pz, 0)   # Z -> Y\n",
    "    return px + (-xy - xz + yx + zx), py + (-yx - yz + xy + zy)\n",
]

# ─── Q1: Equilibrium Points ───────────────────────────────────────────────────
q1 = nb([
    CASE_MD,
    md([
        "## Question 1 — Find the Equilibrium Points\n",
        "\n",
        "An equilibrium is a state $(p_X, p_Y, p_Z)$ where no net switching occurs:\n",
        "$\\Delta p_X = 0$ and $\\Delta p_Y = 0$ simultaneously.\n",
        "\n",
        "Using the identity $x\\max(y-x,0) - y\\max(x-y,0) = (x-y)\\min(x,y)$,\n",
        "the update equations reduce to:\n",
        "\n",
        "$$\\Delta p_X = (p_X - p_Y)\\min(p_X, p_Y) + (p_X - p_Z)\\min(p_X, p_Z) = 0$$\n",
        "\n",
        "$$\\Delta p_Y = (p_Y - p_X)\\min(p_Y, p_X) + (p_Y - p_Z)\\min(p_Y, p_Z) = 0$$\n",
        "\n",
        "Both conditions are satisfied when one or more variables are equal or equal to zero.\n",
        "Working through all cases yields **seven equilibrium points**:\n",
        "\n",
        "| # | $(p_X,\\; p_Y,\\; p_Z)$ | Description |\n",
        "|:-:|:---------------------:|:------------|\n",
        "| 1 | $(1,\\; 0,\\; 0)$ | X (Republican) dominates |\n",
        "| 2 | $(0,\\; 1,\\; 0)$ | Y (Democrat) dominates |\n",
        "| 3 | $(0,\\; 0,\\; 1)$ | Z (Independent) dominates |\n",
        "| 4 | $(\\tfrac{1}{3},\\; \\tfrac{1}{3},\\; \\tfrac{1}{3})$ | Three-way equal split |\n",
        "| 5 | $(\\tfrac{1}{2},\\; \\tfrac{1}{2},\\; 0)$ | X–Y two-party tie |\n",
        "| 6 | $(\\tfrac{1}{2},\\; 0,\\; \\tfrac{1}{2})$ | X–Z two-party tie |\n",
        "| 7 | $(0,\\; \\tfrac{1}{2},\\; \\tfrac{1}{2})$ | Y–Z two-party tie |\n",
        "\n",
        "Starting from the specific case $(p_X, p_Y, p_Z) = (0.4, 0.3, 0.3)$,\n",
        "$p_X$ is the largest, so the system converges to **equilibrium 1: X wins**.",
    ]),
    code(
        STEP_SRC + [
            "\n",
            "# ── Specific case: simulate to confirm convergence ──\n",
            "px, py = 0.4, 0.3\n",
            "for t in range(200):\n",
            "    px, py = step(px, py)\n",
            "print(f'After 200 steps: px={px:.6f}, py={py:.6f}, pz={1-px-py:.6f}')\n",
            "print('=> converges to X (Republican) wins')\n",
        ]
    ),
    code([
        "# ── Verify delta = 0 at all seven equilibria ──\n",
        "equilibria = [\n",
        "    (1.0,  0.0,  '(1,    0,    0)   X wins'),\n",
        "    (0.0,  1.0,  '(0,    1,    0)   Y wins'),\n",
        "    (0.0,  0.0,  '(0,    0,    1)   Z wins'),\n",
        "    (1/3,  1/3,  '(1/3, 1/3, 1/3)  Equal split'),\n",
        "    (0.5,  0.5,  '(1/2, 1/2,  0)   X-Y tie'),\n",
        "    (0.5,  0.0,  '(1/2,  0,  1/2)  X-Z tie'),\n",
        "    (0.0,  0.5,  '(0,   1/2, 1/2)  Y-Z tie'),\n",
        "]\n",
        "\n",
        "print(f\"{'Equilibrium':<32}  dpx          dpy\")\n",
        "print('-' * 60)\n",
        "for px0, py0, name in equilibria:\n",
        "    nx, ny = step(px0, py0)\n",
        "    print(f\"{name:<32}  {nx-px0:+.2e}   {ny-py0:+.2e}\")\n",
    ]),
])

# ─── Q2: Jacobian Matrices ────────────────────────────────────────────────────
q2 = nb([
    CASE_MD,
    md([
        "## Question 2 — Jacobian Matrix at Each Equilibrium\n",
        "\n",
        "The system is a 2-D discrete map $F(p_X, p_Y) = (p_X + \\Delta p_X,\\; p_Y + \\Delta p_Y)$\n",
        "with $p_Z = 1 - p_X - p_Y$.  The Jacobian is:\n",
        "\n",
        "$$J = DF\\big|_{\\text{eq}} = I + \\frac{\\partial(\\Delta p_X,\\, \\Delta p_Y)}{\\partial(p_X,\\, p_Y)}\\bigg|_{\\text{eq}}$$\n",
        "\n",
        "Because the update rule contains $\\max$ terms, it is **piecewise linear**.\n",
        "The Jacobian is evaluated analytically in the dominant region near each equilibrium.\n",
        "\n",
        "The specific case $(p_X, p_Y, p_Z) = (0.4, 0.3, 0.3)$ converges to **equilibrium 1**\n",
        "$(p_X, p_Y, p_Z) = (1, 0, 0)$, so **J1** is the relevant Jacobian for this case.\n",
    ]),
    code([
        "import numpy as np\n",
        "\n",
        "# Analytical Jacobians — variable ordering: (p_X, p_Y); p_Z = 1 - p_X - p_Y\n",
        "\n",
        "J1 = np.array([[0., 0.], [0., 0.]])          # (1,   0,   0)  X wins  <-- specific case\n",
        "J2 = np.array([[0., 0.], [0., 0.]])          # (0,   1,   0)  Y wins\n",
        "J3 = np.array([[0., 0.], [0., 0.]])          # (0,   0,   1)  Z wins\n",
        "J4 = np.array([[2., 0.], [0., 2.]])          # (1/3,1/3,1/3) Equal split\n",
        "J5 = np.array([[ 1.,-1.], [-1., 1.]])        # (1/2,1/2, 0)  X-Y tie\n",
        "J6 = np.array([[ 2., 1.], [ 0., 0.]])        # (1/2, 0, 1/2) X-Z tie\n",
        "J7 = np.array([[ 0., 0.], [ 1., 2.]])        # (0, 1/2,1/2)  Y-Z tie\n",
        "\n",
        "labels = [\n",
        "    '(1,   0,   0)   X wins  [specific case]',\n",
        "    '(0,   1,   0)   Y wins',\n",
        "    '(0,   0,   1)   Z wins',\n",
        "    '(1/3,1/3, 1/3)  Equal split',\n",
        "    '(1/2,1/2,  0)   X-Y tie',\n",
        "    '(1/2, 0,  1/2)  X-Z tie',\n",
        "    '(0,  1/2, 1/2)  Y-Z tie',\n",
        "]\n",
        "\n",
        "for name, J in zip(labels, [J1,J2,J3,J4,J5,J6,J7]):\n",
        "    print(f'Equilibrium {name}:')\n",
        "    print(f'  J = | {J[0,0]:+5.1f}  {J[0,1]:+5.1f} |')\n",
        "    print(f'      | {J[1,0]:+5.1f}  {J[1,1]:+5.1f} |')\n",
        "    print()\n",
    ]),
])

# ─── Q3: Eigenvalues (Code 5.6 style) ────────────────────────────────────────
q3 = nb([
    CASE_MD,
    md([
        "## Question 3 — Eigenvalues of Each Jacobian\n",
        "\n",
        "Following Code 5.6:\n",
        "\n",
        "```python\n",
        "from pylab import *\n",
        "eig([[1, 1], [1, 0]])\n",
        "```\n",
        "\n",
        "we apply `eig` to each Jacobian from Question 2.\n",
        "The specific case $(p_X, p_Y, p_Z) = (0.4, 0.3, 0.3)$ converges to\n",
        "the X-wins equilibrium, so the first result is the one directly relevant.\n",
    ]),
    code([
        "from pylab import *\n",
        "\n",
        "Js = [\n",
        "    ([[0., 0.], [0., 0.]],    '(1,   0,   0)   X wins  [specific case]'),\n",
        "    ([[0., 0.], [0., 0.]],    '(0,   1,   0)   Y wins'),\n",
        "    ([[0., 0.], [0., 0.]],    '(0,   0,   1)   Z wins'),\n",
        "    ([[2., 0.], [0., 2.]],    '(1/3,1/3, 1/3)  Equal split'),\n",
        "    ([[ 1.,-1.],[-1., 1.]],   '(1/2,1/2,  0)   X-Y tie'),\n",
        "    ([[ 2., 1.],[ 0., 0.]],   '(1/2, 0,  1/2)  X-Z tie'),\n",
        "    ([[ 0., 0.],[ 1., 2.]],   '(0,  1/2, 1/2)  Y-Z tie'),\n",
        "]\n",
        "\n",
        "for J, name in Js:\n",
        "    vals, _ = eig(J)\n",
        "    print(f'Equilibrium {name}:  lambda = {[round(v.real,4) for v in vals]}')\n",
    ]),
])

# ─── Q4: Stability Discussion ─────────────────────────────────────────────────
q4 = nb([
    CASE_MD,
    md([
        "## Question 4 — Stability of Each Equilibrium Point\n",
        "\n",
        "For a **discrete-time map**, stability is determined by eigenvalue magnitude:\n",
        "\n",
        "- $|\\lambda| < 1$ → **stable** (nearby orbits converge)\n",
        "- $|\\lambda| > 1$ → **unstable** (nearby orbits diverge)\n",
        "- $\\lambda = 0$ → **super-stable** (collapse in finite steps)\n",
        "\n",
        "*(For continuous ODEs the criterion is $\\text{Re}(\\lambda) < 0$; here it is $|\\lambda| < 1$.)*\n",
        "\n",
        "| Equilibrium | Eigenvalues | Classification |\n",
        "|:------------|:-----------:|:--------------|\n",
        "| $(1,\\; 0,\\; 0)$ — X wins | $0,\\; 0$ | **Stable attractor** (super-stable) |\n",
        "| $(0,\\; 1,\\; 0)$ — Y wins | $0,\\; 0$ | **Stable attractor** (super-stable) |\n",
        "| $(0,\\; 0,\\; 1)$ — Z wins | $0,\\; 0$ | **Stable attractor** (super-stable) |\n",
        "| $(\\tfrac{1}{3},\\tfrac{1}{3},\\tfrac{1}{3})$ — Equal split | $2,\\; 2$ | **Unstable** (repeller) |\n",
        "| $(\\tfrac{1}{2},\\tfrac{1}{2},0)$ — X–Y tie | $0,\\; 2$ | **Unstable saddle** |\n",
        "| $(\\tfrac{1}{2},0,\\tfrac{1}{2})$ — X–Z tie | $0,\\; 2$ | **Unstable saddle** |\n",
        "| $(0,\\tfrac{1}{2},\\tfrac{1}{2})$ — Y–Z tie | $0,\\; 2$ | **Unstable saddle** |\n",
        "\n",
        "**For the specific case $(p_X, p_Y, p_Z) = (0.4, 0.3, 0.3)$:**  \n",
        "$p_X$ is the largest, so the system converges to the X-wins equilibrium $(1, 0, 0)$.\n",
        "Both eigenvalues equal zero — this is a **super-stable attractor**.\n",
        "The Jacobian maps every nearby perturbation to zero in a single linear step,\n",
        "meaning X's lead is self-reinforcing and the outcome is locked in quickly.\n",
        "\n",
        "### General discussion\n",
        "\n",
        "**Corner states (equilibria 1–3)** are the only truly stable outcomes.\n",
        "All eigenvalues are zero, so every nearby initial condition converges\n",
        "rapidly to whichever option started with the plurality — winner-takes-all.\n",
        "\n",
        "**Equal split (equilibrium 4)** has both eigenvalues equal to $2 > 1$:\n",
        "a pure repeller. Any slight imbalance is doubled each step and the\n",
        "system moves away toward one of the corners.\n",
        "\n",
        "**Two-option ties (equilibria 5–7)** are **saddle points** with $\\{0, 2\\}$.\n",
        "The $\\lambda=0$ direction is stable (the third option is drained to zero);\n",
        "the $\\lambda=2$ direction is unstable (any asymmetry between the tied pair\n",
        "doubles each step until one wins).",
    ]),
])

# ─── Q5: Why Z (Independent) state is not feasible ───────────────────────────
q5 = nb([
    CASE_MD,
    md([
        "## Question 5 — Why Is an All-Z (Independent) State Not Feasible?\n",
        "\n",
        "The model shows that $(p_X, p_Y, p_Z) = (0, 0, 1)$ is a mathematically stable\n",
        "equilibrium (eigenvalues both zero). Starting from the specific case\n",
        "$(0.4, 0.3, 0.3)$, $p_Z = 0.3$ is the smallest, so the system moves *away*\n",
        "from the Z-wins state — $p_X$ takes over. Even so, the Z-wins basin exists\n",
        "for initial conditions where $p_Z > p_X$ and $p_Z > p_Y$.\n",
        "\n",
        "In practice, however, an all-Independent outcome is not feasible:\n",
        "\n",
        "1. **Independents are not a coherent bloc.** Being \"Independent\" means absence\n",
        "   of party affiliation, not a shared platform. In real elections, self-identified\n",
        "   Independents split between X and Y candidates and do not converge on a single\n",
        "   Independent option.\n",
        "\n",
        "2. **No governing majority.** A 100% Independent electorate has no unified agenda.\n",
        "   Governance requires an organized majority, which a purely Independent population\n",
        "   cannot provide.\n",
        "\n",
        "3. **Structural barriers.** Winner-take-all elections and ballot-access rules\n",
        "   structurally favor the two established parties — features the model ignores.\n",
        "\n",
        "4. **Model homogeneity assumption.** The model treats all $p_Z$ voters as\n",
        "   equivalent and equally responsive. In reality, voter identities are heterogeneous\n",
        "   and partisan affiliations are sticky.\n",
        "\n",
        "The all-Z state is a mathematical artifact of the model's symmetry;\n",
        "real-world factors make it politically infeasible.",
    ]),
])

# ─── Q6: First major cause of change ─────────────────────────────────────────
q6 = nb([
    CASE_MD,
    md([
        "## Question 6 — One Major Cause of Change in Convergence State\n",
        "\n",
        "In this model the outcome is determined entirely by the **initial values**\n",
        "$(p_X, p_Y, p_Z)$ — whichever option starts highest wins.\n",
        "The specific case $(0.4, 0.3, 0.3)$ gives $p_X > p_Y = p_Z$, so X wins.\n",
        "If those starting values shifted to, say, $(0.28, 0.38, 0.34)$, Y would win instead.\n",
        "\n",
        "### Cause: A shift in initial popularity due to external events\n",
        "\n",
        "Any event that changes the initial distribution at the **start of a new cycle**\n",
        "can reverse the outcome:\n",
        "\n",
        "- **Economic conditions** — a recession shifts $p_X$ vs.\\ $p_Y$ before switching\n",
        "  dynamics begin.\n",
        "- **Scandals or policy failures** — reduce one option's initial popularity,\n",
        "  handing the plurality to the other.\n",
        "- **Candidate quality** — a strong or weak candidate changes the starting\n",
        "  distribution before the feedback loop takes over.\n",
        "\n",
        "Since the basin boundary between X winning and Y winning is the line $p_X = p_Y$\n",
        "(holding $p_Z$ fixed), even a **tiny shift** across that line reverses the winner.",
    ]),
])

# ─── Q7: Second major cause of change ────────────────────────────────────────
q7 = nb([
    CASE_MD,
    md([
        "## Question 7 — A Second Major Cause of Change in Convergence State\n",
        "\n",
        "### Cause: The size of the $p_Z$ (Independent) bloc\n",
        "\n",
        "In the specific case $(0.4, 0.3, 0.3)$, $p_Z = 0.3$ is relatively small and\n",
        "the X vs.\\ Y gap is $0.4 - 0.3 = 0.1$ — a comfortable margin.\n",
        "But consider an election where the starting distribution is $(0.32, 0.31, 0.37)$:\n",
        "$p_Z$ is now large and the X–Y gap is only $0.01$.\n",
        "An insignificant external event that moves just $0.02$ from X to Y flips\n",
        "the outcome to Y winning.\n",
        "\n",
        "A large $p_Z$ bloc makes the election **hyper-sensitive** to small differences\n",
        "between $p_X$ and $p_Y$:\n",
        "- Both $p_X$ and $p_Y$ are small relative to $p_Z$, so they are close together.\n",
        "- Any small alignment of $p_Z$ voters toward X or Y tips the balance decisively.\n",
        "- This amplifies election-to-election volatility — the same model that gave\n",
        "  X a comfortable win at $(0.4, 0.3, 0.3)$ can give Y a win at $(0.32, 0.31, 0.37)$\n",
        "  simply because $p_Z$ grew at the expense of $p_X$.\n",
        "\n",
        "High levels of electoral independence (large $p_Z$) therefore correspond to\n",
        "more competitive and unpredictable elections — consistent with observed\n",
        "patterns in periods of political dealignment.",
    ]),
])

# ─── Write all notebooks ─────────────────────────────────────────────────────
notebooks = {
    "exercise_political_opinion_question_1.ipynb": q1,
    "exercise_political_opinion_question_2.ipynb": q2,
    "exercise_political_opinion_question_3.ipynb": q3,
    "exercise_political_opinion_question_4.ipynb": q4,
    "exercise_political_opinion_question_5.ipynb": q5,
    "exercise_political_opinion_question_6.ipynb": q6,
    "exercise_political_opinion_question_7.ipynb": q7,
}

for fname, notebook in notebooks.items():
    path = OUT / fname
    with open(path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    print(f"Created {path}")
