# How to Use the Unified Calculator Notebook

**For beginners - Step-by-step guide**

---

## Table of Contents
1. [Basic Jupyter Notebook Concepts](#basic-concepts)
2. [Opening the Notebook](#opening-the-notebook)
3. [Understanding the Notebook Structure](#notebook-structure)
4. [Running Cells](#running-cells)
5. [Using the Interactive Widgets](#using-widgets)
6. [Getting Results](#getting-results)
7. [Common Tasks](#common-tasks)

---

## Basic Concepts

### What is a Cell?
A **cell** is a box that contains either:
- **Code** (Python commands) - has `In [ ]:` on the left
- **Markdown** (documentation/text) - displays formatted text

### Cell States
- **Empty cell** (`In [ ]:`) - Not run yet
- **Running cell** (`In [*]:`) - Currently executing
- **Completed cell** (`In [1]:`, `In [2]:`, etc.) - Has been run (number shows execution order)

### Two Modes
- **Command Mode** (blue border) - Navigate, delete cells, etc. Press `Esc` to enter
- **Edit Mode** (green border) - Type/edit code. Press `Enter` to enter

---

## Opening the Notebook

1. **Open JupyterLab:** Go to `http://workhorse.local/jupyter/lab/`
2. **Login:** Enter your Jupyter token (get with: `docker exec jupyter jupyter server list`)
3. **Navigate:** In the file browser (left sidebar), go to:
   - `work` → `og-ai-inference-research` → `tools`
4. **Open:** Double-click `unified-calculator.ipynb`

---

## Notebook Structure

The notebook has **10 cells** numbered 0-9:

- **Cell 0:** Documentation (markdown - just read it)
- **Cell 1:** Install packages (code - run once)
- **Cell 2:** Import libraries (code - run once)
- **Cell 3:** Load data files (code - run once)
- **Cell 4:** Calculation functions (code - run once)
- **Cell 5:** Create interactive widgets (code - run once)
- **Cell 6:** Calculation button (code - run once)
- **Cell 7:** Results display (code - run once)
- **Cell 8:** Export function (code - run once)
- **Cell 9:** Empty (can be ignored)

---

## Running Cells

### Method 1: Run One Cell at a Time (Recommended for First Time)

1. **Click on a cell** to select it (you'll see a blue or green border)
2. **Run the cell** using one of these methods:
   - Press `Shift + Enter` (runs cell and moves to next)
   - Press `Ctrl + Enter` (runs cell and stays on it)
   - Click the "Run" button in the toolbar (play icon ▶)
   - Use menu: `Run` → `Run Selected Cells`

3. **Wait for it to finish** - You'll see `In [*]:` change to `In [1]:` when done

### Method 2: Run All Cells at Once

1. Click `Run` in the menu bar
2. Select `Run All Cells`
3. Wait for all cells to execute (this may take 30-60 seconds)

**⚠️ Important:** Always run cells **in order** (Cell 1 → Cell 2 → Cell 3, etc.)

---

## Using the Interactive Widgets

After running Cells 1-5, you'll see **interactive input forms** appear below Cell 5.

### How to Use Widgets:

1. **Find the input section** - Scroll down below Cell 5
2. **You'll see several input fields:**
   - **Dropdown menus** - Click to see options, click to select
   - **Number inputs** - Click in the box, type a number, press Enter
   - **Sliders** - Click and drag, or click on the number and type
   - **Checkboxes** - Click to check/uncheck

### Example: Setting GPU Configuration

1. **GPU Count:** 
   - Find the "GPU Count" slider or number input
   - Drag the slider OR click the number and type `8`
   - Press Enter

2. **GPU Type:**
   - Find the "GPU Type" dropdown
   - Click it to see options (H100, A100, etc.)
   - Click on your choice (e.g., "H100")

3. **GPU Power:**
   - Find the "GPU Power (W)" input
   - Click in the box
   - Type `700` (or your value)
   - Press Enter

### Example: Setting Generator Configuration

1. **Manufacturer:**
   - Find "Generator Manufacturer" dropdown
   - Click and select (e.g., "Caterpillar")

2. **Model:**
   - Find "Generator Model" dropdown
   - Click and select (e.g., "CG260")

3. **Rated Power:**
   - Find "Generator Rated Power (kW)" input
   - Type `260` (or your value)
   - Press Enter

### Continue for All Inputs

Fill in all the inputs you need:
- GPU Configuration
- Generator Configuration  
- Operational Parameters (islanded, black start, etc.)
- Data Logistics (if using that calculator)

---

## Getting Results

### Step 1: Fill in All Inputs
Make sure all your desired inputs are set using the widgets.

### Step 2: Click the Calculate Button
1. Scroll down to find the **"Calculate"** button (usually a big blue button)
2. **Click it** - This runs all the calculations
3. **Wait** - You'll see `In [*]:` appear while it's calculating

### Step 3: View Results
After clicking Calculate, **Cell 7** will display results:
- Scroll down to see the results dashboard
- You'll see:
  - Generator Risk Assessment
  - BESS Sizing Recommendation
  - GPU-Generator Compatibility
  - Data Logistics Cost Comparison
  - Cost Summary
  - Charts/Visualizations

---

## Common Tasks

### Selecting a Cell
- **Click anywhere in the cell** - This selects it
- **Blue border** = Command mode (can navigate with arrow keys)
- **Green border** = Edit mode (can type/edit)

### Moving Between Cells
- **Arrow keys** (Up/Down) - Move to previous/next cell
- **Click** on any cell to jump to it

### Editing a Cell
1. **Click in the cell** (green border appears)
2. **Type or edit** the code/text
3. **Press Shift + Enter** to run it

### Adding a New Cell
- **Click between cells** (you'll see a blue line)
- Press `A` (above) or `B` (below) in Command Mode
- OR click the "+" button in toolbar

### Deleting a Cell
1. **Select the cell** (click on it)
2. Press `D` twice (or `DD`) in Command Mode
3. OR use menu: `Edit` → `Delete Cells`

### Stopping a Running Cell
- Press the **"Stop"** button (square icon) in toolbar
- OR press `Ctrl + C` in the cell

### Restarting the Kernel
If things get stuck or you want to start fresh:
1. Click `Kernel` in menu bar
2. Select `Restart Kernel...`
3. Confirm
4. **Re-run all cells** from the beginning

### Saving Your Work
- **Auto-saves** - JupyterLab saves automatically
- **Manual save:** Press `Ctrl + S` or click the save icon (disk) in toolbar

---

## Step-by-Step: First Time Setup

### Initial Setup (Do This Once)

1. **Open the notebook** (see "Opening the Notebook" above)

2. **Run Cell 1** (Install packages):
   - Click on Cell 1
   - Press `Shift + Enter`
   - Wait for "✓ All dependencies ready!" message

3. **Run Cell 2** (Import libraries):
   - Click on Cell 2 (or it auto-advances)
   - Press `Shift + Enter`
   - Wait for "✓ All libraries imported successfully!"

4. **Run Cell 3** (Load data):
   - Press `Shift + Enter`
   - Check for any error messages
   - Should show "✓ Data loaded successfully"

5. **Run Cell 4** (Load functions):
   - Press `Shift + Enter`
   - No output expected (functions are loaded)

6. **Run Cell 5** (Create widgets):
   - Press `Shift + Enter`
   - **Widgets appear below** - This is your input form!

### Using the Calculator (Every Time)

1. **Fill in inputs** using the widgets (see "Using the Interactive Widgets" above)

2. **Run Cell 6** (if needed - usually auto-runs):
   - This sets up the Calculate button

3. **Click "Calculate"** button:
   - Scroll down to find it
   - Click it
   - Wait for calculations to finish

4. **View results** in Cell 7:
   - Scroll down to see the dashboard
   - Review all sections

5. **Export results** (optional):
   - Run Cell 8
   - Follow prompts to export to CSV

---

## Troubleshooting

### "Widgets don't appear"
- Make sure you ran Cell 5
- Scroll down below Cell 5
- Try refreshing the page (F5)

### "Calculate button doesn't work"
- Make sure you ran Cell 6
- Check that all required inputs are filled
- Look for error messages in red

### "Results don't show"
- Make sure you clicked "Calculate"
- Check Cell 7 for error messages
- Try running Cell 7 again

### "Cells won't run"
- Check if kernel is running (top right should show "Python 3")
- Try restarting kernel: `Kernel` → `Restart Kernel`
- Re-run cells from the beginning

### "I made a mistake"
- **Undo:** `Ctrl + Z` (in Edit Mode)
- **Restart:** `Kernel` → `Restart Kernel` → Re-run cells
- **Edit cell:** Click in cell, edit, run again

---

## Keyboard Shortcuts Reference

### Command Mode (Blue Border) - Press `Esc` first
- `Enter` - Enter Edit Mode
- `Shift + Enter` - Run cell, move to next
- `Ctrl + Enter` - Run cell, stay on cell
- `A` - Insert cell above
- `B` - Insert cell below
- `D, D` - Delete cell
- `Z` - Undo cell deletion
- `M` - Change to Markdown cell
- `Y` - Change to Code cell
- `↑` / `↓` - Move to previous/next cell

### Edit Mode (Green Border) - Press `Enter` first
- `Esc` - Enter Command Mode
- `Shift + Enter` - Run cell
- `Ctrl + Enter` - Run cell, stay on cell
- `Tab` - Code completion
- `Ctrl + S` - Save notebook

---

## Visual Guide

### What You'll See:

```
┌─────────────────────────────────────┐
│ File  Edit  View  Run  Kernel  ... │  ← Menu Bar
├─────────────────────────────────────┤
│ [▶] [⏸] [⏹] [↻]  [💾]  ...        │  ← Toolbar
├──────────┬──────────────────────────┤
│          │  Cell 0: Documentation   │
│ File     │  ┌─────────────────────┐ │
│ Browser  │  │ # Unified Calculator│ │
│          │  │ ...                 │ │
│ work/    │  └─────────────────────┘ │
│  └─og-   │                          │
│    └─... │  Cell 1: Install        │
│          │  ┌─────────────────────┐ │
│          │  │ !pip install ...   │ │
│          │  └─────────────────────┘ │
│          │                          │
│          │  ... (more cells) ...   │
│          │                          │
│          │  ════════════════════   │
│          │  INPUT WIDGETS:          │
│          │  ┌─────────────────────┐ │
│          │  │ GPU Count: [8]     │ │
│          │  │ GPU Type: [H100 ▼] │ │
│          │  │ ...                 │ │
│          │  └─────────────────────┘ │
│          │  [Calculate] Button     │
│          │                          │
│          │  RESULTS (after click): │
│          │  ┌─────────────────────┐ │
│          │  │ Generator Risk: ... │ │
│          │  │ BESS: ...           │ │
│          │  └─────────────────────┘ │
└──────────┴──────────────────────────┘
```

---

## Quick Start Checklist

- [ ] Opened notebook in JupyterLab
- [ ] Ran Cell 1 (install packages)
- [ ] Ran Cell 2 (import libraries)
- [ ] Ran Cell 3 (load data)
- [ ] Ran Cell 4 (load functions)
- [ ] Ran Cell 5 (create widgets)
- [ ] Filled in all input widgets
- [ ] Clicked "Calculate" button
- [ ] Viewed results in dashboard
- [ ] (Optional) Exported results to CSV

---

## Need More Help?

- **JupyterLab Documentation:** https://jupyterlab.readthedocs.io/
- **Notebook Basics:** https://jupyter-notebook.readthedocs.io/
- **Check for errors:** Look for red text in cells
- **Restart if stuck:** `Kernel` → `Restart Kernel`

---

**Remember:** Always run cells in order, and wait for each one to finish before running the next!

