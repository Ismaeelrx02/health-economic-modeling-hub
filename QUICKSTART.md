# Quick Start - Dash Framework

## ⚡ Get Started in 2 Steps

### Step 1: Install Dash Dependencies
```powershell
cd "c:\Users\Iyunu\OneDrive\Documents\Health Economic Modeling Hub"
pip install -r requirements.txt
```

### Step 2: Run the Dash Application
```powershell
python app.py
```

✅ **Dash app running at http://127.0.0.1:8050**

---

## 🎯 Modular Dash Architecture

```
app.py                    # Main Dash application (START HERE!)
├── config/
│   └── settings.py      # Configuration
├── layouts/             # Modular page layouts
│   ├── dashboard.py
│   ├── projects.py
│   ├── decision_tree.py
│   ├── markov.py
│   ├── psm.py
│   ├── compare.py
│   ├── dsa.py
│   └── psa.py
├── callbacks/           # Modular callback functions
│   ├── projects_callbacks.py
│   ├── decision_tree_callbacks.py
│   ├── markov_callbacks.py
│   ├── psm_callbacks.py
│   └── analysis_callbacks.py
├── data/
│   └── database.py      # SQLite database
└── calculations/        # Health economics math
```

---

## ✨ Features

- ✅ **Plotly Dash** - Python-only, no JavaScript
- ✅ **Modular layouts** - 8 separate page modules
- ✅ **Modular callbacks** - 5 organized callback modules
- ✅ **SQLite database** - Project and model storage
- ✅ **Red/white/black theme** - Custom CSS
- ✅ **Real calculations** - NumPy/SciPy math
- ✅ **Interactive charts** - Built-in Plotly graphs

---

## 📚 Documentation

- **DASH_ARCHITECTURE.md** - Complete architecture guide
- **https://dash.plotly.com/** - Official Dash docs

---

## 🐛 Troubleshooting

### Dash won't start
```powershell
pip install -r requirements.txt --force-reinstall
```

### Import errors
Make sure you're in the project directory:
```powershell
cd "c:\Users\Iyunu\OneDrive\Documents\Health Economic Modeling Hub"
```

---

## ✅ Success Checklist

- [ ] Dash dependencies installed
- [ ] `python app.py` runs without errors
- [ ] Can access http://127.0.0.1:8050
- [ ] Dashboard displays with statistics
- [ ] Sidebar navigation works (black sidebar, red accents)
- [ ] Can navigate to all 8 pages

---

## 🚀 Next Steps

1. Open http://127.0.0.1:8050 in your browser
2. Navigate using the sidebar
3. Create a project on the Projects page
4. Build models (Decision Tree, Markov, PSM)
5. Run analyses (Compare, DSA, PSA)
6. Read **DASH_ARCHITECTURE.md** for customization

---

**Happy Modeling with Dash! 🎯**
