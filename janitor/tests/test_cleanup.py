import yaml

def test_yaml_config_exists():

    with open("config/settings.yaml", "r") as file:
        config = yaml.safe_load(file)

    assert config is not None


def test_required_tags_exist():

    with open("config/settings.yaml", "r") as file:
        config = yaml.safe_load(file)

    required_tags = config["required_tags"]

    assert "Project" in required_tags
    assert "Environment" in required_tags
    assert "Owner" in required_tags
    assert "ManagedBy" in required_tags