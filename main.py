# # main.py
# # FastAPI application entry point.
# # Connects to MySQL on startup, creates tables if they don't exist,
# # and registers all API routes.

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from database import engine, test_connection, Base
# from routes.upload    import router as upload_router
# from routes.predict   import router as predict_router
# from routes.analytics import router as analytics_router

# # Create all MySQL tables automatically if they don't exist yet
# # (reads from SQLAlchemy models in models.py)
# Base.metadata.create_all(bind=engine)

# app = FastAPI(
#     title       = "AI-Based Business Growth Prediction System",
#     description = "Predict future sales using historical data and Linear Regression. Built with FastAPI + MySQL.",
#     version     = "2.0.0"
# )

# # Allow frontend (React, HTML) to call this API from any origin
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins  = ["*"],
#     allow_methods  = ["*"],
#     allow_headers  = ["*"]
# )

# # Register all route modules
# app.include_router(upload_router)
# app.include_router(predict_router)
# app.include_router(analytics_router)


# @app.on_event("startup")
# def startup():
#     """Run on server startup — test MySQL connection."""
#     test_connection()


# @app.get("/", tags=["Health Check"])
# def root():
#     return {
#         "message": "AI-Based Growth Prediction System is running 🚀",
#         "database": "MySQL",
#         "model":    "Linear Regression",
#         "docs":     "/docs",
#         "status":   "online"
#     }
# main.py — UPGRADED
# ✅ Export route added
# ✅ Better startup messages

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth_routes import router as auth_router

from database import engine, test_connection, Base
from routes.upload    import router as upload_router
from routes.predict   import router as predict_router
from routes.analytics import router as analytics_router
from routes.export    import router as export_router   # ← NEW

# Auto-create all MySQL table

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title       = "AI-Based Business Growth Prediction System",
    description = (
        "Predict future sales using historical data.\n\n"
        "✅ Random Forest ML Model\n"
        "✅ Duplicate data prevention\n"
        "✅ Full input validation\n"
        "✅ CSV export feature"
    ),
    version = "2.0.0"
)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Register all routes
app.include_router(upload_router)
app.include_router(predict_router)
app.include_router(analytics_router)
app.include_router(export_router)    # ← NEW


@app.on_event("startup")
def startup():
    test_connection()
    print("🚀 AI Growth Prediction System v2.0 is ready!")
    print("📖 API Docs: http://127.0.0.1:8000/docs")


@app.get("/", tags=["Health"])
def root():
    return {
        "message":      "AI-Based Growth Prediction System v2.0 🚀",
        "database":     "MySQL",
        "model":        "Random Forest Regressor",
        "improvements": [
            "✅ Duplicate data prevention",
            "✅ Random Forest ML model",
            "✅ Full input validation",
            "✅ CSV export feature"
        ],
        "docs": "http://127.0.0.1:8000/docs"
    }