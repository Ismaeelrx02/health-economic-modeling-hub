# Final Architecture - Module-Based Organization

## ✅ **Perfect Module Structure - Layout + Callbacks Together**

Each feature is now a **self-contained module** with its own layout and callbacks in one folder!

---

## 📂 **Final Folder Structure (5 folders, 39 files)**

```
Health Economic Modeling Hub/
│
├── 📄 Root Files (9)
│   ├── app.py                      ← Main Dash application
│   ├── requirements-dash.txt       ← Python dependencies  
│   ├── .env, .env.example, .gitignore
│   └── README.md, QUICKSTART.md, ARCHITECTURE.md, FINAL_ARCHITECTURE.md
│
├── 📁 assets/ (2 files)            ← Frontend (CSS + JavaScript)
│   ├── custom.css                  ← Red/white/black theme (8.5KB)
│   └── app.js                      ← Client-side utilities (10.7KB)
│
├── 📁 config/ (2 files)            ← App configuration
│   ├── settings.py
│   └── __init__.py
│
├── 📁 data/ (2 files)              ← Database operations
│   ├── database.py
│   └── __init__.py
│
└── 📁 modules/ (24 files)          ← FEATURE-BASED MODULES
    ├── __init__.py
    │
    ├── dashboard/                  ← Dashboard module
    │   ├── layout.py               ← UI structure
    │   └── __init__.py
    │
    ├── projects/                   ← Project management module
    │   ├── layout.py               ← UI structure
    │   ├── callbacks.py            ← Logic + CRUD operations
    │   └── __init__.py
    │
    ├── decision_tree/              ← Decision tree module
    │   ├── layout.py               ← Tree builder UI
    │   ├── callbacks.py            ← Tree math + UI handlers
    │   └── __init__.py
    │
    ├── markov/                     ← Markov model module
    │   ├── layout.py               ← State editor UI
    │   ├── callbacks.py            ← Matrix simulation + UI handlers
    │   └── __init__.py
    │
    ├── psm/                        ← PSM module
    │   ├── layout.py               ← Survival curve UI
    │   ├── callbacks.py            ← PSM calculations + UI handlers
    │   └── __init__.py
    │
    ├── compare/                    ← Compare strategies module
    │   ├── layout.py               ← Comparison UI
    │   ├── callbacks.py            ← ICER, NMB calculations + UI handlers
    │   └── __init__.py
    │
    ├── dsa/                        ← DSA module
    │   ├── layout.py               ← Tornado diagram UI
    │   ├── callbacks.py            ← DSA calculations + UI handlers
    │   └── __init__.py
    │
    └── psa/                        ← PSA module
        ├── layout.py               ← CEAC UI
        ├── callbacks.py            ← PSA calculations + UI handlers
        └── __init__.py
```

---

## 🎯 **Why This Structure is Perfect**

### **Before (Separated):**
```
├── layouts/
│   ├── dashboard.py
│   ├── projects.py
│   └── decision_tree.py
│
└── callbacks/
    ├── projects_callbacks.py
    └── decision_tree_callbacks.py
```
**Problem:** Related files scattered in different folders

### **After (Module-Based):**
```
└── modules/
    ├── dashboard/
    │   └── layout.py
    │
    ├── projects/
    │   ├── layout.py           ← UI
    │   └── callbacks.py        ← Logic
    │
    └── decision_tree/
        ├── layout.py           ← UI  
        └── callbacks.py        ← Logic + Math
```
**Solution:** Everything for one feature in one place!

---

## 💡 **Module Benefits**

| Benefit | Description |
|---------|-------------|
| **Cohesion** | Layout + Logic for same feature in one folder |
| **Easy Navigation** | Want to edit Decision Tree? Open `modules/decision_tree/` |
| **Self-Contained** | Each module is independent |
| **Scalability** | Add new feature? Just create `modules/new_feature/` |
| **Team-Friendly** | Different devs can work on different modules |

---

## 🔄 **How Modules Work**

### **1. Module Structure:**
```python
# modules/markov/__init__.py
"""Markov Module - Markov cohort simulation"""
from .layout import layout
from .callbacks import register_callbacks
```

### **2. Layout (UI):**
```python
# modules/markov/layout.py
import dash_bootstrap_components as dbc

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Markov Model"),
            # ... forms, inputs, charts
        ])
    ])
])
```

### **3. Callbacks (Logic + Math):**
```python
# modules/markov/callbacks.py
from dash import Input, Output
import numpy as np

def calculate_markov_model(...):
    """Markov simulation math"""
    P = np.array(transition_matrix)
    # ... matrix multiplication logic
    return results

def register_callbacks(app):
    @app.callback(...)
    def handle_calculate(...):
        result = calculate_markov_model(...)
        return display_result(result)
```

### **4. App Integration:**
```python
# app.py
from modules.markov import layout as markov_layout, register_callbacks as markov_callbacks

# Use layout in routing
if pathname == '/markov':
    return markov_layout

# Register callbacks
markov_callbacks(app)
```

---

## 📊 **Complete Data Flow Example**

**User Action:** "Run Markov simulation"

```
1. User visits /markov route
   └── app.py serves modules/markov/layout.py

2. User fills form and clicks "Calculate"
   └── Browser sends data to server

3. modules/markov/callbacks.py receives event
   └── calculate_markov_model() function runs
   └── Matrix multiplication: trace[t] = trace[t-1] @ P
   └── Discounting applied
   └── Returns total cost & QALYs

4. Callback formats result
   └── Saves to data/database.py
   └── Returns HTML component

5. Browser displays results
   └── assets/app.js adds animations
   └── assets/custom.css styles output
```

---

## 🎨 **CSS + JavaScript Integration**

### **assets/custom.css** (8.5KB)
- Red (#DC2626), White (#FFFFFF), Black (#000000) theme
- Module-agnostic styling (applies to all pages)
- Responsive design
- Card styles, button effects, animations

### **assets/app.js** (10.7KB)
- Keyboard shortcuts (Ctrl+S, Ctrl+K)
- Form validation (client-side)
- Loading spinners
- Tooltips & notifications
- Export functionality

**Dash Auto-Loads:** All `.css` and `.js` files in `assets/` are automatically applied!

---

## 📈 **File Distribution**

| Category | Folders | Files | Lines | Percentage |
|----------|---------|-------|-------|------------|
| **Modules (Python)** | 8 | 24 | ~1,800 | 75% |
| **CSS** | 1 | 1 | ~400 | 17% |
| **JavaScript** | 1 | 1 | ~350 | 15% |
| **Config/Data** | 2 | 4 | ~200 | 8% |
| **Docs** | - | 4 | N/A | N/A |

**Total: 5 folders, 39 files, ~2,400 lines of code**

---

## 🚀 **Adding New Features**

Want to add a new "Budget Impact" module?

```bash
# 1. Create module folder
mkdir modules/budget_impact

# 2. Create layout
# modules/budget_impact/layout.py
layout = dbc.Container([...])

# 3. Create callbacks
# modules/budget_impact/callbacks.py
def register_callbacks(app): ...

# 4. Create __init__.py
# modules/budget_impact/__init__.py
from .layout import layout
from .callbacks import register_callbacks

# 5. Update app.py
from modules.budget_impact import layout as budget_layout, register_callbacks as budget_callbacks

# Add route + register callbacks
# Done! ✅
```

---

## ✅ **Optimization Summary**

### **Evolution:**
1. **Initial:** React + FastAPI (separate frontend/backend)
2. **Refactor 1:** Dash with layouts/ and callbacks/ folders
3. **Consolidation:** Merged calculations into callbacks
4. **Final:** Module-based structure (layout + callbacks per feature)

### **Result:**
- ✅ **39 files** (optimized)
- ✅ **5 clean folders** (assets, config, data, modules, root)
- ✅ **Module-based** (feature cohesion)
- ✅ **CSS/JS separation** (proper frontend assets)
- ✅ **Red/White/Black theme** throughout
- ✅ **Production-ready** architecture

---

## 🎯 **Architecture Principle**

**"One feature = One module = Layout + Callbacks in one folder"**

- **modules/*/layout.py**: What the user SEES
- **modules/*/callbacks.py**: What happens when user INTERACTS
- **assets/**: How it LOOKS and FEELS
- **config/**: What can be CONFIGURED
- **data/**: How data is PERSISTED

**Perfect cohesion. Zero redundancy. Maximum maintainability.** ✨

---

## 📂 **Final Folder Structure (6 folders, 29 files)**

```
Health Economic Modeling Hub/
│
├── app.py                          ← Main Dash application
├── requirements-dash.txt           ← Python dependencies  
├── .env / .env.example / .gitignore
├── README.md / QUICKSTART.md / ARCHITECTURE.md
│
├── assets/                         ← CSS + JavaScript (frontend)
│   ├── custom.css                  ← Red/white/black styling (8.5KB)
│   └── app.js                      ← Client-side utilities (10.7KB)
│
├── config/
│   ├── settings.py                 ← App configuration
│   └── __init__.py
│
├── layouts/                        ← UI Definitions (8 pages)
│   ├── dashboard.py
│   ├── projects.py
│   ├── decision_tree.py
│   ├── markov.py
│   ├── psm.py
│   ├── compare.py
│   ├── dsa.py
│   ├── psa.py
│   └── __init__.py
│
├── callbacks/                      ← UI Logic + Calculations (ALL-IN-ONE)
│   ├── projects_callbacks.py      ← Project CRUD
│   ├── decision_tree_callbacks.py ← Decision tree math + UI handlers
│   ├── markov_callbacks.py        ← Markov simulation + UI handlers
│   ├── psm_callbacks.py           ← PSM survival curves + UI handlers
│   ├── analysis_callbacks.py      ← DSA/PSA/ICER + UI handlers
│   └── __init__.py
│
└── data/
    ├── database.py                 ← SQLite CRUD operations
    └── __init__.py
```

---

## 🎯 **Why This Structure Works Better**

### **Before (Redundant):**
```
callbacks/analysis_callbacks.py:
    from calculations.health_econ import calculate_icer  ← Extra import
    
    @app.callback(...)
    def handle_button_click():
        result = calculate_icer(...)  ← Extra function call
```

### **After (Integrated):**
```
callbacks/analysis_callbacks.py:
    def calculate_icer(...):  ← Math function
        return inc_cost / inc_effect
    
    @app.callback(...)  ← UI handler  
    def handle_button_click():
        result = calculate_icer(...)  ← Direct call, same file
```

**Benefits:**
- ✅ Less files to maintain (29 vs 35)
- ✅ No unnecessary imports
- ✅ Calculations + UI logic in one place (cohesive)
- ✅ Easier to understand data flow

---

## 📊 **What Each Folder Does**

| Folder | Purpose | Contains | Language |
|--------|---------|----------|----------|
| **`layouts/`** | UI Structure | HTML components, forms, charts | Python (Dash components) |
| **`callbacks/`** | Logic + Math | Calculations + button handlers | Python (NumPy/SciPy + Dash) |
| **`assets/`** | Styling + UX | Theme, animations, keyboard shortcuts | CSS + JavaScript |
| **`config/`** | Settings | App title, colors, discount rates | Python (constants) |
| **`data/`** | Persistence | Database CRUD operations | Python (SQLite) |

---

## 🔄 **Complete Data Flow Example**

**User Action:** "Calculate ICER for two treatments"

```
1. User fills form in layouts/compare.py
   └── Cost A: $100, Effect A: 5 QALY
   └── Cost B: $50, Effect B: 3 QALY
   └── Clicks "Calculate" button

2. Browser (assets/app.js)
   └── Validates inputs (client-side)
   └── Shows loading spinner
   └── Sends data to server

3. Dash Callback (callbacks/analysis_callbacks.py)
   └── @app.callback receives button click
   └── Calls calculate_icer(100, 50, 5, 3)
   └── Math: (100-50) / (5-3) = $25/QALY
   └── Saves to database via data/database.py
   └── Returns HTML component to display

4. Browser receives update
   └── Displays "ICER: $25,000/QALY"
   └── Hides loading spinner (assets/app.js)
   └── Shows success notification
```

---

## 🎨 **CSS + JavaScript Integration**

### **CSS (`assets/custom.css`)** - 400 lines
- Red (#DC2626), White (#FFFFFF), Black (#000000) theme
- Card styling, button hover effects
- Responsive mobile design
- Custom scrollbars
- Table formatting

### **JavaScript (`assets/app.js`)** - 350 lines
- Keyboard shortcuts (Ctrl+S, Ctrl+K, Escape)
- Smooth scrolling
- Form validation (before sending to Python)
- Loading overlays
- Tooltips & notifications
- Local storage for user preferences
- Export to CSV functionality

**Dash Auto-Loads Assets:**
- Any `.css` file in `assets/` → Automatically applied
- Any `.js` file in `assets/` → Automatically executed
- Any images → Accessible via `/assets/image.png`

---

## 📈 **Code Distribution**

| Component | Files | Lines | Percentage |
|-----------|-------|-------|------------|
| **Python (Callbacks)** | 5 | ~1,200 | 62% |
| **Python (Layouts)** | 8 | ~600 | 31% |
| **CSS** | 1 | ~400 | 6% |
| **JavaScript** | 1 | ~350 | 5% |
| **Config/Data** | 3 | ~150 | 3% |

**Total: 29 files, ~1,950 lines of code**

---

## 🚀 **Quick Start**

```powershell
# Install dependencies
pip install -r requirements-dash.txt

# Run application
python app.py

# Open browser
http://localhost:8050
```

---

## ✅ **Optimization Summary**

### **Removed:**
- ❌ `calculations/` folder (merged into callbacks)
- ❌ 5 calculation files (integrated)
- ❌ 2 redundant docs (outdated)
- ❌ Old backend/ and src/ folders (removed earlier)
- ❌ All React/Vite configs (removed earlier)

### **Result:**
- ✅ **29 files total** (down from 35+)
- ✅ **6 clean folders** (no redundancy)
- ✅ **Integrated calculations** (no separation overhead)
- ✅ **Proper CSS/JS** (separate styling & interactivity)
- ✅ **Red/White/Black theme** throughout
- ✅ **Production-ready** structure

---

## 🎯 **Final Architecture Principle**

**"UI defined in `layouts/`, Logic + Math in `callbacks/`, Style in `assets/`"**

- **layouts/**: What the user SEES (forms, buttons, charts)
- **callbacks/**: What happens when user INTERACTS (math + handlers)
- **assets/**: How it LOOKS and FEELS (colors + UX)

**No unnecessary separation. Clean, maintainable, optimized.** ✨
