import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

# ============================================================================
# DISTANCE AND BRUTE FORCE FUNCTIONS
# ============================================================================

def distance(p1, p2):
    """Calculate Euclidean distance between two points"""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def bruteForce(coords):
    """Find minimum distance by checking all pairs (for small inputs)"""
    minDis = float('inf')
    pairs_checked = []
    
    if len(coords) == 1:
        return minDis, pairs_checked
    
    for i in range(len(coords) - 1):
        for j in range(i + 1, len(coords)):
            dist = distance(coords[i], coords[j])
            pairs_checked.append((coords[i], coords[j], dist))
            minDis = min(dist, minDis)
    
    return minDis, pairs_checked


# ============================================================================
# VISUALIZER CLASS
# ============================================================================

class ClosestPairVisualizer:
    def __init__(self):
        self.steps = []
        self.all_points = []  # Store all points for consistent display
        
    def record_step(self, coords, midpoint_x, left_coords, right_coords, 
                   curr_min, strip, checking_point=None, checking_with=None, 
                   depth=0, step_type="divide", leftmin=None, rightmin=None,
                   base_case_pairs=None):
        """Save a snapshot of the algorithm's current state"""
        self.steps.append({
            'coords': coords.copy(),
            'midpoint': midpoint_x,
            'left': left_coords.copy() if left_coords else [],
            'right': right_coords.copy() if right_coords else [],
            'delta': curr_min,
            'strip': strip.copy() if strip else [],
            'checking': checking_point,
            'checking_with': checking_with,
            'depth': depth,
            'type': step_type,
            'leftmin': leftmin,
            'rightmin': rightmin,
            'base_case_pairs': base_case_pairs if base_case_pairs else []
        })
    
    def MDP(self, coords, depth=0):
        """Modified Closest Pair algorithm that records steps"""
        n = len(coords)
        
        # BASE CASE: 3 or fewer points
        if n <= 3:
            result, pairs = bruteForce(coords)
            self.record_step(coords, None, [], [], result, [], 
                           depth=depth, step_type="base_case",
                           base_case_pairs=pairs)
            return result
        
        # DIVIDE STEP
        midpoint = n // 2
        midpoint_x = coords[midpoint][0]
        
        left_coords = coords[0:midpoint]
        right_coords = coords[midpoint:n]
        
        # Record the division
        self.record_step(coords, midpoint_x, left_coords, right_coords, 
                       float('inf'), [], depth=depth, step_type="divide")
        
        # CONQUER STEP: Recursively solve left and right
        leftmin = self.MDP(left_coords, depth=depth+1)
        rightmin = self.MDP(right_coords, depth=depth+1)
        
        # Get minimum from both sides
        curr_min = min(leftmin, rightmin)
        
        # Record after getting results from both sides
        self.record_step(coords, midpoint_x, left_coords, right_coords, 
                       curr_min, [], depth=depth, step_type="combine",
                       leftmin=leftmin, rightmin=rightmin)
        
        # COMBINE STEP: Build the strip
        strip = []
        for coord in coords:
            if abs(coords[midpoint][0] - coord[0]) <= curr_min:
                strip.append(coord)
        
        strip = sorted(strip, key=lambda p: p[1])
        
        # Record strip formation
        self.record_step(coords, midpoint_x, left_coords, right_coords, 
                       curr_min, strip, depth=depth, step_type="strip",
                       leftmin=leftmin, rightmin=rightmin)
        
        # Check all points in the strip
        for i in range(len(strip) - 1):
            for j in range(i + 1, min(i + 8, len(strip))):
                if strip[j][1] - strip[i][1] >= curr_min:
                    break
                
                # Record this comparison
                self.record_step(coords, midpoint_x, left_coords, right_coords,
                               curr_min, strip, strip[i], strip[j], 
                               depth=depth, step_type="checking",
                               leftmin=leftmin, rightmin=rightmin)
                
                dist = distance(strip[i], strip[j])
                if dist < curr_min:
                    curr_min = dist
        
        return curr_min
    
    def visualize(self, step_idx, ax_plot, ax_info):
        """
        Draw a single step of the algorithm
        
        ax_plot: Left subplot for the main visualization
        ax_info: Right subplot for the information panel
        """
        if step_idx >= len(self.steps):
            step_idx = len(self.steps) - 1
        
        step = self.steps[step_idx]
        
        # Clear both subplots
        ax_plot.clear()
        ax_info.clear()
        
        # ====================================================================
        # LEFT SIDE: MAIN PLOT
        # ====================================================================
        
        # Extract all x and y coordinates
        all_x = [p[0] for p in self.all_points]
        all_y = [p[1] for p in self.all_points]
        
        # Determine which points are left, right, or neither in current step
        left_set = set(step['left'])
        right_set = set(step['right'])
        
        # Plot ALL points, colored based on current left/right division
        for point in self.all_points:
            if point in left_set:
                # Blue for left side
                ax_plot.scatter(point[0], point[1], c='blue', s=100, 
                              zorder=3, alpha=0.7)
            elif point in right_set:
                # Red for right side
                ax_plot.scatter(point[0], point[1], c='red', s=100, 
                              zorder=3, alpha=0.7)
            else:
                # Gray for points not in current recursion level
                ax_plot.scatter(point[0], point[1], c='gray', s=50, 
                              zorder=2, alpha=0.3)
        
        # DRAW MIDLINE
        if step['midpoint'] is not None:
            y_min, y_max = min(all_y) - 1, max(all_y) + 1
            ax_plot.axvline(x=step['midpoint'], color='green', linestyle='--', 
                          linewidth=2, alpha=0.7, label='Midline')
        
        # DRAW STRIP
        if step['delta'] != float('inf') and step['midpoint'] is not None:
            y_min, y_max = min(all_y) - 1, max(all_y) + 1
            strip_left = step['midpoint'] - step['delta']
            strip_right = step['midpoint'] + step['delta']
            
            rect = patches.Rectangle(
                (strip_left, y_min),
                step['delta'] * 2,
                y_max - y_min,
                linewidth=2, 
                edgecolor='orange',
                facecolor='yellow', 
                alpha=0.2, 
                label='Strip'
            )
            ax_plot.add_patch(rect)
        
        # HIGHLIGHT BASE CASE with yellow background
        if step['type'] == 'base_case':
            if len(step['coords']) > 0:
                base_x = [p[0] for p in step['coords']]
                base_y = [p[1] for p in step['coords']]
                
                # Draw a yellow circle around base case points
                for point in step['coords']:
                    circle = patches.Circle(point, radius=1.5, 
                                          facecolor='yellow', 
                                          edgecolor='gold',
                                          linewidth=3,
                                          alpha=0.4, 
                                          zorder=1)
                    ax_plot.add_patch(circle)
                
                # Draw lines between all pairs in base case
                for p1, p2, dist in step['base_case_pairs']:
                    ax_plot.plot([p1[0], p2[0]], [p1[1], p2[1]],
                               'orange', linewidth=2, linestyle='-', 
                               alpha=0.8, zorder=4)
                    
                    # Show distance on the line
                    mid_x = (p1[0] + p2[0]) / 2
                    mid_y = (p1[1] + p2[1]) / 2
                    ax_plot.text(mid_x, mid_y, f'{dist:.2f}', 
                               fontsize=9, color='orange', fontweight='bold',
                               bbox=dict(boxstyle='round', 
                                       facecolor='white', alpha=0.9))
        
        # HIGHLIGHT POINTS BEING COMPARED in strip
        if step['checking'] is not None:
            ax_plot.scatter(step['checking'][0], step['checking'][1], 
                          c='purple', s=300, marker='*', zorder=5, 
                          edgecolors='black', linewidths=2)
            
            if step['checking_with'] is not None:
                ax_plot.scatter(step['checking_with'][0], 
                              step['checking_with'][1],
                              c='orange', s=300, marker='*', zorder=5,
                              edgecolors='black', linewidths=2)
                
                # Draw line between them
                ax_plot.plot([step['checking'][0], step['checking_with'][0]],
                           [step['checking'][1], step['checking_with'][1]],
                           'purple', linewidth=2, linestyle=':', alpha=0.7)
                
                # Show distance
                dist = distance(step['checking'], step['checking_with'])
                mid_x = (step['checking'][0] + step['checking_with'][0]) / 2
                mid_y = (step['checking'][1] + step['checking_with'][1]) / 2
                ax_plot.text(mid_x, mid_y, f'd={dist:.2f}', 
                           fontsize=10, color='purple', fontweight='bold',
                           bbox=dict(boxstyle='round', 
                                   facecolor='white', alpha=0.8))
        
        # TITLE
        delta_str = f"{step['delta']:.2f}" if step['delta'] != float('inf') else "∞"
        step_type_str = step.get('type', 'unknown')
        ax_plot.set_title(f'Step {step_idx + 1}/{len(self.steps)} | '
                        f'Type: {step_type_str} | Delta: {delta_str}', 
                        fontsize=12, fontweight='bold')
        
        # Legend outside the plot
        ax_plot.legend(loc='upper left', fontsize=9, 
                      bbox_to_anchor=(0, 1), framealpha=0.9)
        
        ax_plot.grid(True, alpha=0.3)
        ax_plot.set_aspect('equal', adjustable='box')
        
        # Set consistent plot limits
        x_min, x_max = min(all_x) - 3, max(all_x) + 3
        y_min_plot = min(all_y) - 3
        y_max_plot = max(all_y) + 3
        ax_plot.set_xlim(x_min, x_max)
        ax_plot.set_ylim(y_min_plot, y_max_plot)
        
        ax_plot.set_xlabel('X coordinate', fontsize=10)
        ax_plot.set_ylabel('Y coordinate', fontsize=10)
        
        # ====================================================================
        # RIGHT SIDE: INFORMATION PANEL
        # ====================================================================
        
        ax_info.axis('off')  # Turn off axes for info panel
        
        # Build information text
        info_lines = []
        info_lines.append("=" * 35)
        info_lines.append(f"STEP {step_idx + 1} INFO")
        info_lines.append("=" * 35)
        info_lines.append("")
        
        info_lines.append(f"Step Type: {step_type_str.upper()}")
        info_lines.append(f"Recursion Depth: {step['depth']}")
        info_lines.append("")
        
        # Current working set
        info_lines.append(f"Points in current level: {len(step['coords'])}")
        if len(step['coords']) <= 10:
            for i, p in enumerate(step['coords']):
                info_lines.append(f"  {i+1}. {p}")
        info_lines.append("")
        
        # Left side info
        info_lines.append(f"LEFT SIDE (Blue):")
        info_lines.append(f"  Count: {len(step['left'])}")
        if step['leftmin'] is not None:
            if step['leftmin'] == float('inf'):
                info_lines.append(f"  Min distance: ∞")
            else:
                info_lines.append(f"  Min distance: {step['leftmin']:.4f}")
        if len(step['left']) <= 5 and len(step['left']) > 0:
            for p in step['left']:
                info_lines.append(f"    {p}")
        info_lines.append("")
        
        # Right side info
        info_lines.append(f"RIGHT SIDE (Red):")
        info_lines.append(f"  Count: {len(step['right'])}")
        if step['rightmin'] is not None:
            if step['rightmin'] == float('inf'):
                info_lines.append(f"  Min distance: ∞")
            else:
                info_lines.append(f"  Min distance: {step['rightmin']:.4f}")
        if len(step['right']) <= 5 and len(step['right']) > 0:
            for p in step['right']:
                info_lines.append(f"    {p}")
        info_lines.append("")
        
        # Current delta
        info_lines.append(f"CURRENT DELTA (δ):")
        if step['delta'] == float('inf'):
            info_lines.append(f"  ∞ (not computed yet)")
        else:
            info_lines.append(f"  {step['delta']:.4f}")
        info_lines.append("")
        
        # Strip info
        if len(step['strip']) > 0:
            info_lines.append(f"STRIP:")
            info_lines.append(f"  Points in strip: {len(step['strip'])}")
            if len(step['strip']) <= 8:
                for p in step['strip']:
                    info_lines.append(f"    {p}")
            info_lines.append("")
        
        # Base case specific info
        if step['type'] == 'base_case':
            info_lines.append(f"BASE CASE TRIGGERED!")
            info_lines.append(f"  Points: {len(step['coords'])}")
            info_lines.append(f"  Using brute force")
            if step['base_case_pairs']:
                info_lines.append(f"  Pairs checked: {len(step['base_case_pairs'])}")
                for p1, p2, dist in step['base_case_pairs']:
                    info_lines.append(f"    {p1} ↔ {p2}: {dist:.4f}")
            if step['delta'] != float('inf'):
                info_lines.append(f"  RETURNING: {step['delta']:.4f}")
            else:
                info_lines.append(f"  RETURNING: ∞")
        
        # Checking info
        if step['checking'] is not None and step['checking_with'] is not None:
            info_lines.append(f"COMPARING:")
            info_lines.append(f"  Point 1: {step['checking']}")
            info_lines.append(f"  Point 2: {step['checking_with']}")
            dist = distance(step['checking'], step['checking_with'])
            info_lines.append(f"  Distance: {dist:.4f}")
        
        # Display the text
        info_text = "\n".join(info_lines)
        ax_info.text(0.05, 0.95, info_text, 
                    transform=ax_info.transAxes,
                    fontsize=9, 
                    verticalalignment='top',
                    fontfamily='monospace',
                    bbox=dict(boxstyle='round', 
                            facecolor='lightyellow', 
                            alpha=0.8))
    
    def show_step_by_step(self, points):
        """Main function to run the algorithm and show interactive visualization"""
        # Store all points for consistent display
        self.all_points = sorted(points, key=lambda p: p[0])
        
        # Run the algorithm
        result = self.MDP(self.all_points, depth=0)
        
        # Print summary
        print(f"Minimum distance found: {result:.4f}")
        print(f"Total steps recorded: {len(self.steps)}")
        print("\nStep breakdown:")
        for i, step in enumerate(self.steps):
            print(f"  Step {i+1}: {step['type']:12s} "
                  f"(depth {step['depth']}, {len(step['coords'])} points)")
        
        # Create figure with two subplots
        # Width ratio: plot gets 65%, info panel gets 35%
        fig, (ax_plot, ax_info) = plt.subplots(1, 2, figsize=(18, 8),
                                                gridspec_kw={'width_ratios': [65, 35]})
        
        current_step = [0]
        
        def update(val):
            """Redraw the visualization when step changes"""
            self.visualize(current_step[0], ax_plot, ax_info)
            plt.draw()
        
        def on_key(event):
            """Handle keyboard input"""
            if event.key == 'right' and current_step[0] < len(self.steps) - 1:
                current_step[0] += 1
                update(None)
            elif event.key == 'left' and current_step[0] > 0:
                current_step[0] -= 1
                update(None)
        
        fig.canvas.mpl_connect('key_press_event', on_key)
        
        # Show the first step
        self.visualize(0, ax_plot, ax_info)
        
        # Add instructions
        fig.text(0.5, 0.02, 
                'Use LEFT/RIGHT arrow keys to navigate | '
                f'Minimum distance: {result:.4f}', 
                ha='center', fontsize=12, style='italic', weight='bold',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
        
        plt.tight_layout(rect=[0, 0.03, 1, 1])
        plt.show()
        
        return result


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    points = [
        (2, 3), (12, 30), (40, 50), (5, 1), (12, 10),
        (3, 4), (15, 18), (20, 25), (30, 35), (25, 20)
    ]
    
    visualizer = ClosestPairVisualizer()
    min_dist = visualizer.show_step_by_step(points)
"""
## Key Library Explanations

### `matplotlib.pyplot` (imported as `plt`)
The main plotting interface:
- `plt.figure()` - Creates a new window/figure
- `plt.clf()` - Clear the current figure
- `plt.gca()` - Get Current Axes (the drawing area)
- `plt.show()` - Display the window
- `plt.draw()` - Refresh the display
- `plt.figtext()` - Add text to the figure
- `plt.tight_layout()` - Automatically adjust spacing

### `axes` object (`ax`)
The drawing area where we plot:
- `ax.scatter(x, y, ...)` - Plot points
- `ax.plot(x_list, y_list, ...)` - Draw lines
- `ax.axvline(x, ...)` - Draw vertical line
- `ax.text(x, y, text, ...)` - Add text at position
- `ax.set_title()` - Set title
- `ax.set_xlabel()` / `ax.set_ylabel()` - Label axes
- `ax.set_xlim()` / `ax.set_ylim()` - Set axis ranges
- `ax.legend()` - Show legend
- `ax.grid()` - Show grid

### `matplotlib.patches`
For drawing shapes:
- `patches.Rectangle()` - Creates a rectangle
- `ax.add_patch()` - Adds the shape to the plot

## Expected Output

With 10 points, you should now see **~20-30 steps**:
```
Total steps recorded: 27
Step breakdown:
  Step 1: divide       (depth 0, 10 points)
  Step 2: divide       (depth 1, 5 points)
  Step 3: divide       (depth 2, 2 points)
  Step 4: base_case    (depth 3, 2 points)
  Step 5: base_case    (depth 3, 3 points)
  Step 6: strip        (depth 2, 2 points)
  ...

  """