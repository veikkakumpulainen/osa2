from urllib import request
from project import Project
import tomli


class ProjectReader:
    def __init__(self, url):
        self._url = url

    def get_project(self):

        content = request.urlopen(self._url).read().decode("utf-8")

        toml_dict = tomli.loads(content)
        

        # Oikea polku tietoihin
        poetry_data = toml_dict.get("tool", {}).get("poetry", {})

        name = poetry_data.get("name", "Unknown")
        description = poetry_data.get("description", "")
        license = poetry_data.get("license", "")
        authors = poetry_data.get("authors", [])
        dependencies = list(poetry_data.get("dependencies", {}).keys())

        dev_dependencies = []
        dev_group = poetry_data.get("group", {}).get("dev", {}).get("dependencies", {})
        if dev_group:
            dev_dependencies = list(dev_group.keys())

        return Project(name, description, license, authors, dependencies, dev_dependencies)
