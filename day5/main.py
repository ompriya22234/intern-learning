from fastapi import FastAPI

app = FastAPI()


@app.get("/about")
def about():
    return {
        "name": "Om Priya Dash",
        "course": "AI Internship training",
        "skills": [
            "Version Control using Git & GitHub",
            "Building CLI Applications with Python",
            "Creating APIs with FastAPI and Docker"
        ]
    }
