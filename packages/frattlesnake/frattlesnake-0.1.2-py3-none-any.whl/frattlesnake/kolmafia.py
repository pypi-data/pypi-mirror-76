from typing import Any, Callable, Optional
from os import path
from urllib import request
import json
import jnius_config

JAR_LOCATION = "./kolmafia.jar"
JENKINS_JOB_URL = "https://ci.kolmafia.us/job/Kolmafia/lastSuccessfulBuild/"


def download_kolmafia(location: str):
    with request.urlopen(JENKINS_JOB_URL + "/api/json") as response:
        data = json.loads(response.read().decode())
        jar_url = JENKINS_JOB_URL + "artifact/" + data["artifacts"][0]["relativePath"]
        request.urlretrieve(jar_url, filename=location)


class KoLmafia:
    def __init__(self, location: str = JAR_LOCATION):
        if path.isfile(location) is False:
            download_kolmafia(location)

        jnius_config.set_classpath(location)

        from jnius import autoclass

        self.autoclass = autoclass
        

    def __getattr__(self, key) -> Any:
        path = "net.sourceforge.kolmafia."
        if key.endswith("Request"):
            path += "request."
        elif key.endswith("Database"):
            path += "persistence."
        elif key.endswith("Manager"):
            path += "session."
        elif key == "Preferences":
            path += "preferences."
        elif key == "Interpreter":
            path += "textui."

        path += key

        return self.autoclass(path)

km = KoLmafia()