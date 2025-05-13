from sanic import Sanic
from sanic import response

sanic = Sanic("AssistantAPI")

@sanic.get("/")
async def index(request):
    return response.json({"status": "ok"})

if __name__ == "__main__":
    sanic.run(host="0.0.0.0", port=8000, debug=False)