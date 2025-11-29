# Database & AI Integration Guide

## 🗄️ Database Setup

### Local Development (SQLite)

The application uses SQLite by default for local development. No additional setup required!

```bash
# Initialize database (creates tables)
python scripts/init_database.py
```

### Production (PostgreSQL on Render)

1. **Add PostgreSQL Database on Render:**
   - Go to your Render dashboard
   - Click "New" → "PostgreSQL"
   - Name it (e.g., `health-econ-db`)
   - Select free plan
   - Click "Create Database"

2. **Connect to Your Web Service:**
   - In your web service settings, Render automatically provides `DATABASE_URL`
   - The app will auto-detect and use PostgreSQL

3. **Initialize Tables:**
   - After first deployment, run in Render Shell:
   ```bash
   python scripts/init_database.py
   ```

## 🤖 AI Chat Integration

### Features

- **Floating AI button** in bottom-right corner
- **Two AI providers**: OpenAI (GPT-4o-mini) and Anthropic (Claude 3.5 Sonnet)
- **Context-aware**: Expert in health economics and modeling
- **Conversation history**: Maintains context across messages
- **Real-time responses**: Direct chat interface

### Setup

1. **Get API Keys:**
   
   **OpenAI:**
   - Visit: https://platform.openai.com/api-keys
   - Create a new API key
   - Copy the key (starts with `sk-`)

   **Anthropic:**
   - Visit: https://console.anthropic.com/
   - Create a new API key
   - Copy the key (starts with `sk-ant-`)

2. **Add to Render Environment Variables:**
   - Go to your web service settings
   - Navigate to "Environment" tab
   - Add these variables:
   
   ```
   OPENAI_API_KEY=sk-your-openai-key-here
   ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
   ```

3. **Local Development (.env file):**
   
   Create a `.env` file in the project root:
   
   ```bash
   # AI Services
   OPENAI_API_KEY=sk-your-openai-key-here
   OPENAI_MODEL=gpt-4o-mini
   
   ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
   ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
   
   # Database
   DATABASE_URL=sqlite:///health_econ_hub.db
   ```

## 📊 Database Schema

### Projects Table
- **id**: Primary key
- **name**: Project name
- **description**: Project description
- **model_type**: decision_tree, markov, or psm
- **owner**: User identifier
- **tags**: JSON array of tags
- **created_at**, **updated_at**: Timestamps

### Scenarios Table
- **id**: Primary key
- **project_id**: Foreign key to projects
- **name**: Scenario name
- **is_baseline**: Boolean flag
- **model_structure**: JSON (tree nodes, states, curves)
- **costs**: JSON (annual costs, one-time costs)
- **effectiveness**: JSON (QALYs, LYs)
- **probabilities**: JSON (transition rates)

### Parameters Table
- **id**: Primary key
- **project_id**: Foreign key to projects
- **name**: Parameter name
- **category**: cost, effectiveness, probability, utility
- **base_value**, **min_value**, **max_value**: Numeric values
- **distribution**: uniform, normal, beta, gamma
- **distribution_params**: JSON parameters

### Results Table
- **id**: Primary key
- **project_id**: Foreign key to projects
- **analysis_type**: base_case, dsa, psa, comparison
- **results_data**: JSON (ICERs, NMB, costs, QALYs)
- **charts_data**: JSON (pre-computed chart data)
- **discount_rate**, **time_horizon**, **wtp_threshold**: Analysis settings

## 🔧 Usage Examples

### Database Operations

```python
from database.services import ProjectService, ScenarioService

# Create a project
project = ProjectService.create_project(
    name="My CEA Study",
    model_type="decision_tree",
    description="Comparing treatment A vs. B",
    tags=["oncology", "cea"]
)

# List all projects
projects = ProjectService.list_projects()

# Create a scenario
scenario = ScenarioService.create_scenario(
    project_id=project['id'],
    name="Standard Care",
    is_baseline=True,
    costs={"drug": 1000, "admin": 500},
    effectiveness={"qalys": 5.5}
)
```

### AI Chat Service

```python
from services.ai_service import AIService

# Initialize service (auto-detects provider from env)
ai = AIService()

# Simple question
response = ai.chat("What is a Markov cohort model?")
print(response)

# With conversation history
history = [
    {"role": "user", "content": "What is ICER?"},
    {"role": "assistant", "content": "ICER stands for..."}
]
response = ai.chat("How do I calculate it?", conversation_history=history)
```

## 🚀 Deployment Checklist

- [ ] PostgreSQL database created on Render
- [ ] `DATABASE_URL` environment variable set (automatic on Render)
- [ ] `OPENAI_API_KEY` environment variable set (optional)
- [ ] `ANTHROPIC_API_KEY` environment variable set (optional)
- [ ] Database tables initialized (`python scripts/init_database.py`)
- [ ] Application deployed and running

## 💡 Tips

1. **Start with SQLite locally**, migrate to PostgreSQL for production
2. **Both AI providers work well**, but you only need one API key
3. **OpenAI (gpt-4o-mini)** is faster and cheaper
4. **Anthropic (Claude)** provides more detailed responses
5. **Database auto-migrates** on startup (tables created if missing)

## 🆘 Troubleshooting

### Database Connection Issues

```python
# Check database URL
import os
print(os.getenv('DATABASE_URL'))

# Test connection
from database import init_db
init_db()  # Should print "Database initialized successfully"
```

### AI Chat Not Working

1. Verify API key is set:
   ```python
   import os
   print(os.getenv('OPENAI_API_KEY'))  # Should show your key
   ```

2. Check service availability:
   ```python
   from services.ai_service import AIService
   ai = AIService()
   print(ai.is_available())  # Should be True
   ```

3. Test simple query:
   ```python
   response = ai.chat("Hello!")
   print(response)
   ```

## 📚 Additional Resources

- [Render PostgreSQL Docs](https://render.com/docs/databases)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [SQLAlchemy ORM Docs](https://docs.sqlalchemy.org/)
