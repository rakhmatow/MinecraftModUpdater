import yaml
import requests
import json
import os

mod_directory = "mods"


def downloadMod(item):
    res = requests.get(f"{modrinth_api_url}/project/{item}/version")

    if not res.ok:
        print(f"{item} not found!")
        return

    mod_versions_data = json.loads(res.content)

    mod_version_to_download = ""
    for mod_version in mod_versions_data:
        if mc_version in mod_version["game_versions"]:
            mod_version_to_download = mod_version
            break

    mod_file = requests.get(mod_version_to_download["files"][0]["url"]).content
    filename = mod_version_to_download["files"][0]["filename"]
    open(filename, "wb").write(mod_file)


if __name__ == "__main__":
    if not os.path.exists(mod_directory):
        os.mkdir(mod_directory)

    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

    mods_to_download = config["mods"]
    mc_version = config["mc_version"]
    modrinth_api_url = config["modrinth_api"]

    os.chdir(mod_directory)

    for item in mods_to_download:
        downloadMod(item)
