import yaml
import requests
import json
import os

mod_directory = "mods"


def downloadMod(item):
    query_params = {
        "game_versions": f'["{mc_version}"]',
        "loaders": f'["{mod_loader}"]',
    }
    res = requests.get(
        f"{modrinth_api_url}/project/{item}/version", params=query_params
    )

    if not res.ok:
        print(f"{item} not found!")
        return

    mod_versions_data = json.loads(res.content)

    if not mod_versions_data:
        print(f"{item} doesn't support {mod_loader} {mc_version}")
        return

    mod_file = mod_versions_data[0]["files"][0]

    file_url = requests.get(mod_file["url"]).content
    file_name = mod_file["filename"]
    with open(file_name, "wb") as file:
        file.write(file_url)


if __name__ == "__main__":
    if not os.path.exists(mod_directory):
        os.mkdir(mod_directory)

    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

    mods_to_download = config["mods"]
    mc_version = config["mc_version"]
    mod_loader = config["mod_loader"]
    modrinth_api_url = config["modrinth_api"]

    os.chdir(mod_directory)

    for item in mods_to_download:
        downloadMod(item)
