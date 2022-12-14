from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import Routers
from app.routers.users import router as users_router
from app.routers.readmes import router as readmes_router

# Workers
from app.workers.html_generator.suscriber import HTMLGeneratorSuscriber

app = FastAPI(title="Project 1 progress | Redis")

# Register middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers

app.include_router(users_router)
app.include_router(readmes_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Project 1 progress (REDIS)",
        "members": [
            {"name": "Pascual Gómez", "email": ""},
            {"name": "Sebastian Granda", "email": "sgrandag@eafit.edu.co"}
        ],
        "documentation": "/docs"
    }

# Start Workers
readme_suscriber = HTMLGeneratorSuscriber("README-SUSCRIBER")
readme_suscriber.start()