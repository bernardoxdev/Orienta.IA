from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "status": "Orienta.IA online 🚀"
    }

if __name__ == '__main__':
    pass