# Health Economic Modeling Hub

A Python-powered health economics modeling platform with a React frontend. Build and analyze decision trees, Markov models, and partitioned survival models (PSM) for cost-effectiveness analysis.

## Features

- **Decision Tree Models**: Model clinical pathways with branching decisions
- **Markov Models**: Simulate disease progression over time with state transitions
- **Partitioned Survival Models (PSM)**: Oncology-focused survival analysis
- **Cost-Effectiveness Analysis**: Calculate ICERs, NMB, and other health economic metrics
- **Sensitivity Analysis**: Deterministic (DSA) and Probabilistic (PSA) sensitivity analysis
- **Interactive Visualizations**: Charts for CEA curves, tornado diagrams, and survival overlays

## Technology Stack

### Backend (Python)
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM for database management
- **NumPy & SciPy**: Scientific computing for health economics calculations
- **Pandas**: Data manipulation and analysis

### Frontend (React)
- **React 18**: Modern React with hooks
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework with red, white, and black color scheme
- **Radix UI**: Accessible component primitives
- **Recharts**: Composable charting library

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- npm or yarn

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
copy .env.example .env
```

3. Initialize the database:
```bash
python -c "from backend.database import init_db; init_db()"
```

4. Start the Python backend server:
```bash
python server.py
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Install Node.js dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Running the Application

1. **Start the Backend** (in one terminal):
```bash
python server.py
```

2. **Start the Frontend** (in another terminal):
```bash
npm run dev
```

3. Open your browser and navigate to `http://localhost:5173`

## Building for Production

### Backend
```bash
# The Python backend runs as-is, but for production:
# - Use a production WSGI server like gunicorn
# - Configure a production database (PostgreSQL recommended)
# - Set DEBUG=False in .env
pip install gunicorn
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend
```bash
npm run build
```

The built files will be in the `dist` directory, ready for deployment.

## Project Structure

```
Health Economic Modeling Hub/
├── backend/                    # Python backend
│   ├── calculations/          # Health economics calculation modules
│   │   ├── decision_tree.py  # Decision tree calculations
│   │   ├── markov.py         # Markov model calculations
│   │   ├── psm.py            # Partitioned survival model
│   │   └── health_econ.py    # Core health economics functions
│   ├── routes/               # API route definitions
│   │   ├── projects.py       # Project management endpoints
│   │   ├── decision_tree.py  # Decision tree endpoints
│   │   ├── markov.py         # Markov model endpoints
│   │   ├── psm.py            # PSM model endpoints
│   │   └── calculations.py   # Calculation endpoints
│   ├── main.py               # FastAPI application entry point
│   ├── database.py           # Database configuration
│   ├── models.py             # SQLAlchemy models
│   └── schemas.py            # Pydantic schemas
├── src/                       # React frontend
│   ├── api/                  # API client
│   ├── components/           # React components
│   ├── pages/                # Page components
│   └── utils/                # Utility functions
├── server.py                 # Python server entry point
├── requirements.txt          # Python dependencies
├── package.json              # Node.js dependencies
└── README.md                 # This file
```

## API Endpoints

### Projects
- `GET /api/projects` - List all projects
- `POST /api/projects` - Create a new project
- `GET /api/projects/{id}` - Get project details
- `PATCH /api/projects/{id}` - Update a project
- `DELETE /api/projects/{id}` - Delete a project

### Decision Trees
- `GET /api/decision-tree` - List decision trees
- `POST /api/decision-tree` - Create a decision tree
- `POST /api/decision-tree/{id}/calculate` - Run calculations

### Markov Models
- `GET /api/markov` - List Markov models
- `POST /api/markov` - Create a Markov model
- `POST /api/markov/{id}/calculate` - Run Markov simulation

### PSM Models
- `GET /api/psm` - List PSM models
- `POST /api/psm` - Create a PSM model
- `POST /api/psm/{id}/calculate` - Run PSM calculations

### Calculations
- `POST /api/calculations/icer` - Calculate ICER
- `POST /api/calculations/nmb` - Calculate Net Monetary Benefit
- `POST /api/calculations/dsa` - Perform DSA
- `POST /api/calculations/psa` - Perform PSA
- `POST /api/calculations/ceac` - Calculate CEAC

## Color Scheme

The application uses a red, white, and black color scheme:
- **Primary Red**: #DC2626 (Red-600)
- **Background**: White (#FFFFFF)
- **Text**: Black (#000000)
- **Sidebar**: Black background with red accents
- **Accents**: Various shades of red for emphasis

## Development

### Adding New Models

1. Create model in `backend/models.py`
2. Create Pydantic schemas in `backend/schemas.py`
3. Implement calculations in `backend/calculations/`
4. Add API routes in `backend/routes/`
5. Update frontend API client in `src/api/base44Client.js`

### Database Migrations

When changing models, create a migration:
```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

## Support

For issues and questions, please refer to the documentation or contact the development team.

## License

This project is proprietary software. All rights reserved.
