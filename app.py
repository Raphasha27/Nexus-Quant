from fastapi import FastAPI

app = FastAPI(
    title="Nexus-Quant",
    description="Quantitative Trading & Market Analytics Engine",
    version="0.1.0",
)

@app.get("/")
def root():
    return {
        "service": "Nexus-Quant",
        "version": "0.1.0",
        "status": "operational",
        "docs": "/docs",
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
