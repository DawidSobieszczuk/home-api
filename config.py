import yaml

class Config():
    def __init__(self, file:str):
        with open(file, "r") as config_file:
            config = yaml.safe_load(config_file)

        self.mysql_host = config["mysql"]["host"]
        self.mysql_port = config["mysql"]["port"]
        self.mysql_user = config["mysql"]["user"]
        self.mysql_password = config["mysql"]["password"]
        self.mysql_database = config["mysql"]["database"]