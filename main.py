from sanic import Sanic
from sanic import response

from config import Config
from database import Database

from orjson import dumps

sanic = Sanic("AssistantAPI", dumps=dumps)
config = Config("config.yaml")
db = Database(config.mysql_host, config.mysql_port, config.mysql_database, config.mysql_user, config.mysql_password)

## DB Check
def is_table_exist(name):
    results = db.query("SHOW TABLES")

    for result in results:
         table_name = list(result.values())[0]

         if name == table_name:
             return True

    return False

@sanic.get("/")
async def index(request):
    return response.json({"status": "ok"})

## DB
@sanic.get("/db/<name:str>")
async def getAll(request, name):
    if not is_table_exist(name):
        return response.json({
            "status": "failed"
        })        
    
    include_deleted = request.args.get("include_deleted")
    if(include_deleted=="true"):
        include_deleted = True
    else:
        include_deleted = False

    results = db.query(f"SELECT * FROM {name} { "" if include_deleted else "WHERE deleted_at is NULL"}")
    
    return response.json({
        "status": "ok",
        "data": results
    })

@sanic.get("/db/<name:str>/<id:int>")
async def get(request, name:str, id:int):
    if not is_table_exist(name):
        return response.json({
            "status": "failed"
        })        
    
    include_deleted = request.args.get("include_deleted")
    if(include_deleted=="true"):
        include_deleted = True
    else:
        include_deleted = False

    results = db.query(f"SHOW COLUMNS FROM {name}")
    id_field = results[0]["Field"]

    results = db.query(f"SELECT * FROM {name} WHERE {id_field} = %s { "" if include_deleted else "WHERE deleted_at is NULL"}", id)
    
    return response.json({
        "status": "ok",
        "data": results
    })

@sanic.post("/db/<name:str>")
async def create(request, name):
    if not is_table_exist(name):
        return response.json({
            "status": "failed",
            "errors": [
                { "message": "Table not found" }
            ]
        })
    
    fields = ", ".join(request.json.keys())
    values = ", ".join(f"'{v}'" for v in request.json.values())

    try:
        results = db.query(f"INSERT INTO {name} ({fields}) VALUES ({values})")
    
        return response.json({
            "status": "ok",
            "data": results
        })
    except:
        return response.json({
            "status": "failed",
            "errors": [
                { "message": "MYSQL Syntax Error" }
            ]
        })

@sanic.put("/db/<name:str>/<id:int>")
async def update(request, name, id):
    if not is_table_exist(name):
        return response.json({
            "status": "failed",
            "errors": [
                { "message": "Table not found" }
            ]
        })
    
    fields = ", ".join(f"{k} = %s" for k in request.json.keys())
    values = list(f"'{v}'" for v in request.json.values())

    results = db.query(f"SHOW COLUMNS FROM {name}")
    id_field = results[0]["Field"]

    try:
        result = db.query(f"UPDATE {name} SET {fields} WHERE {id_field} = %s", values, id)
        return response.json({
            "status": "ok",
            "data": result
        })
    except:
        return response.json({
            "status": "failed",
            "errors": [
                { "message": "MYSQL Syntax Error" }
            ]
        })

@sanic.delete("/db/<name:str>/<id:int>")
async def delete(request, name, id):
    if not is_table_exist(name):
        return response.json({
            "status": "failed",
            "errors": [
                { "message": "Table not found" }
            ]
        })

    results = db.query(f"SHOW COLUMNS FROM {name}")
    id_field = results[0]["Field"]

    result = db.query(f"UPDATE {name} SET deleted_at = NOW() WHERE {id_field} = %s", id)
    
    return response.json({
        "status": "ok",
        "data": []
    })

if __name__ == "__main__":
    sanic.run(host="0.0.0.0", port=8000, debug=False)