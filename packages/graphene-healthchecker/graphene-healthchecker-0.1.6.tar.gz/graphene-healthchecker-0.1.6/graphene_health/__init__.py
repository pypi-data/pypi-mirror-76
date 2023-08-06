from flask import Flask
from healthcheck import HealthCheck, EnvironmentDump
from .config import config


app = Flask(__name__)
health = HealthCheck()
envdump = EnvironmentDump()

app.config.update(dict(config))
