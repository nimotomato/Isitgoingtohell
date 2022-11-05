import toml


def load_toml(file_path) -> dict:
    with open(file_path, "r") as f:
        data = toml.load(f)

    return data
