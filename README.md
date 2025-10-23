# Closest Pair of Points Visualizer

An interactive visualization tool for the Divide and Conquer algorithm that finds the closest pair of points in 2D space.

## What It Does

This program visualizes the **Closest Pair Problem**: Given n points in a 2D plane, find the two points with the minimum distance between them.

Instead of checking every possible pair (which takes O(n²) time), this implementation uses a **Divide and Conquer** approach that runs in O(n log n) time.

### How the Algorithm Works

1. **Divide**: Sort points by x-coordinate and split them into left and right halves
2. **Conquer**: Recursively find the closest pair in each half
3. **Combine**: Check a narrow "strip" along the dividing line for pairs that might be closer

### What You'll See

- **Blue points**: Left side of the current division
- **Red points**: Right side of the current division
- **Gray points**: Points not in the current recursion level
- **Green dashed line**: The dividing line (midpoint)
- **Yellow strip**: The region being checked for cross-boundary pairs (width = 2δ)
- **Yellow circles with orange lines**: Base case - checking all pairs with brute force
- **Purple/Orange stars**: Points currently being compared in the strip
- **Right panel**: Shows detailed information about each step

## Installation

### Requirements
- Python 3.7 or higher
- matplotlib
- numpy

### Setup

1. Clone or download this repository

2. Install dependencies:
```bash
pip install matplotlib numpy
```

## Usage

### Run the Visualizer
```bash
python visualizer.py
```

### Controls

- **→** (Right Arrow): Go to next step
- **←** (Left Arrow): Go to previous step
- **Close Window**: Exit

### Using Your Own Points

Edit the `points` list at the bottom of `visualizer.py`:
```python
if __name__ == "__main__":
    # Add your own points here as (x, y) tuples
    points = [
        (2, 3), (12, 30), (40, 50), (5, 1), (12, 10),
        (3, 4), (15, 18), (20, 25), (30, 35), (25, 20)
    ]
    
    visualizer = ClosestPairVisualizer()
    min_dist = visualizer.show_step_by_step(points)
```

### Generate Random Points
```python
import random

# Generate 15 random points between 0 and 100
points = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(15)]

visualizer = ClosestPairVisualizer()
min_dist = visualizer.show_step_by_step(points)
```

## Understanding the Visualization

### Step Types

- **divide**: Shows how points are split into left and right halves
- **base_case**: Shows brute force comparison when ≤3 points remain (orange lines between all pairs)
- **combine**: Shows results returned from left and right recursive calls
- **strip**: Shows the narrow region being checked for cross-boundary pairs
- **checking**: Shows individual point comparisons in the strip

### Information Panel

The right side shows:
- Current step type and recursion depth
- Points in the current working set
- Left side minimum distance
- Right side minimum distance  
- Current delta (δ) - the minimum distance found so far
- Strip points being checked
- Base case details (pairs checked and distances)
- Current comparison details

## Files

- `visualizer.py` - Main visualization program with algorithm implementation
- `MDP.py` - Core algorithm implementation (if separated)
- `requirements.txt` - Python package dependencies
- `README.md` - This file

## License
```
MIT License

Copyright (c) 2025 [Aidan Jiang]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
