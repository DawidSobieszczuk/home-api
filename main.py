from sanic import Sanic
from sanic import response

from config import Config
from database import Database

sanic = Sanic("AssistantAPI")
config = Config("config.yaml")
db = Database(config.mysql_host, config.mysql_port, config.mysql_database, config.mysql_user, config.mysql_password)

@sanic.get("/")
async def index(request):
    return response.json({"status": "ok"})

if __name__ == "__main__":
    sanic.run(host="0.0.0.0", port=8000, debug=False)