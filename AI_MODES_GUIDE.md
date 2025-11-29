# AI Modes Guide

## 🤖 Three AI Operating Modes

The Health Economic Modeling Hub supports **three distinct AI modes** that you can toggle via the dropdown in the header bar.

---

## 🤝 AI-Assisted Mode (Default)

**Philosophy:** Manual control with AI suggestions

### How It Works:
- **You input** all parameters manually
- **AI provides** suggestions and recommendations
- **AI validates** your inputs and warns of issues
- **AI recommends** parameter ranges based on literature
- **You have** full control over final decisions

### Best For:
- Learning health economics modeling
- Regulatory submissions requiring full control
- Custom analyses with specific requirements
- When you want to understand every step

### Example Workflow:
```
1. You create a Markov model
2. You define states and transition probabilities
3. AI suggests: "Based on similar studies, consider transition probability range 0.1-0.3"
4. You review and adjust
5. AI validates: "Warning: Sum of probabilities from State A = 0.95, should be 1.0"
6. You fix the issue
7. You run the analysis
```

---

## ⚡ AI-Augmented Mode

**Philosophy:** AI actively helps with tasks and automates repetitive work

### How It Works:
- **AI auto-fills** common parameters from similar studies
- **AI suggests** optimal parameter values
- **AI performs** sensitivity analysis automatically
- **AI generates** interim reports
- **You review** and approve AI suggestions

### Best For:
- Rapid prototyping
- Exploratory analyses
- When you have limited time
- Routine analyses with standard assumptions

### Example Workflow:
```
1. You select "Create PSM Model"
2. AI auto-fills: survival distributions, utilities, costs from literature
3. You review pre-filled values
4. AI suggests: "Run DSA on top 5 uncertain parameters?"
5. You approve
6. AI executes DSA and generates tornado diagram
7. You review results and iterate
```

---

## 🤖 AI-Automated Mode

**Philosophy:** Full AI control with minimal user intervention

### How It Works:
- **AI performs** complete analysis pipeline
- **AI selects** appropriate models and parameters
- **AI runs** all relevant sensitivity analyses
- **AI generates** final reports and visualizations
- **You provide** only high-level objectives

### Best For:
- Quick estimates
- Preliminary analyses
- When you trust AI's judgment
- Demonstrating multiple scenarios rapidly

### Example Workflow:
```
1. You input: "Compare Treatment A vs Treatment B for Type 2 Diabetes"
2. AI selects: Markov model as most appropriate
3. AI populates: all parameters from published meta-analyses
4. AI runs: Base case, DSA, PSA, CEAC automatically
5. AI generates: Complete CEA report with ICER, NMB, cost-effectiveness plane
6. You review: final results and export report
```

---

## 🔄 Switching Between Modes

### In the Header Bar:
1. Look for "AI Mode:" dropdown (top right)
2. Select your desired mode:
   - 🤝 AI-Assisted
   - ⚡ AI-Augmented
   - 🤖 AI-Automated
3. Badge updates to show current mode
4. All modules adapt behavior instantly

### What Changes:
| Feature | Assisted | Augmented | Automated |
|---------|----------|-----------|-----------|
| **Auto-fill parameters** | ❌ | ✅ | ✅ |
| **Show suggestions** | ✅ | ✅ | ❌ (Just does it) |
| **Manual input required** | ✅ Always | ✅ Can override | ❌ Optional |
| **Auto-run analyses** | ❌ | 🟡 With approval | ✅ |
| **Generate reports** | Manual | Semi-auto | Fully auto |
| **User involvement** | High | Medium | Low |

---

## 💡 Usage Examples by Module

### Decision Tree Module:
- **Assisted:** You draw tree, AI validates structure
- **Augmented:** AI suggests common tree templates, you customize
- **Automated:** AI creates complete tree from problem description

### Markov Module:
- **Assisted:** You define states/transitions, AI checks probabilities sum to 1
- **Augmented:** AI suggests state structure, you approve and adjust
- **Automated:** AI builds entire Markov model from disease description

### PSM Module:
- **Assisted:** You input survival parameters, AI validates curve fits
- **Augmented:** AI fits curves to your data automatically
- **Automated:** AI selects best distributions and runs full analysis

### DSA Module:
- **Assisted:** You select parameters to vary, AI runs tornado
- **Augmented:** AI suggests top uncertain parameters, you approve
- **Automated:** AI identifies all uncertain parameters and runs complete DSA

### PSA Module:
- **Assisted:** You define distributions, AI validates
- **Augmented:** AI suggests distributions from literature
- **Automated:** AI runs full PSA with 1000+ iterations and generates CEAC

---

## 🎯 Recommendations

### Start with AI-Assisted if:
- New to health economics modeling
- Need regulatory-compliant documentation
- Want to learn the methodology
- Have very specific requirements

### Use AI-Augmented for:
- Day-to-day analyses
- Exploratory work
- Time-constrained projects
- Standard CEA studies

### Use AI-Automated for:
- Quick feasibility checks
- Preliminary estimates
- Demonstrating multiple scenarios
- When speed matters more than precision

---

## 🔧 Technical Implementation

### Accessing AI Mode in Callbacks:
```python
from dash import Input, State
from config.ai_mode import should_auto_fill, get_ai_mode_config

@app.callback(
    Output('result', 'children'),
    Input('calculate-btn', 'n_clicks'),
    State('ai-mode-store', 'data')
)
def calculate(n_clicks, ai_mode):
    if should_auto_fill(ai_mode):
        # Auto-fill parameters
        params = get_default_params()
    else:
        # Wait for user input
        params = get_user_params()
    
    return perform_calculation(params)
```

### Mode Configuration:
```python
from config.ai_mode import get_ai_mode_config

mode_config = get_ai_mode_config('ai-augmented')
# Returns:
# {
#   'name': 'AI-Augmented',
#   'icon': '⚡',
#   'description': '...',
#   'features': [...]
# }
```

---

## 🚀 Future Enhancements

- **Learning Mode:** AI adapts to your preferences over time
- **Custom Modes:** Define your own AI assistance levels
- **Mode Presets:** Save mode settings per project
- **AI Explanations:** See why AI made specific suggestions
- **Undo AI Actions:** Revert AI decisions easily

---

**Toggle the AI mode anytime to match your workflow needs!** 🎯
