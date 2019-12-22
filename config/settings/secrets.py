import yaml

SECRETS = {
    'databases': None,
    'secret_key': None,
    'allowed_hosts': None,
}


def load_secrets():
    # config/settings/secrets.yml should contain correct
    # configuration for the instance running e.g. developers should
    # copy the file example provided and fill correct values for
    # development so do CI and production.
    with open('config/settings/secrets.yml') as secrets:
        conf_secrets = yaml.load(secrets.read(), Loader=yaml.SafeLoader)
    conf = {}
    conf.update(SECRETS)
    for section in conf_secrets:
        if section in conf:
            conf[section] = conf_secrets[section]
        else:
            raise ValueError(f"Invalid configuration value `{section}`")
    return conf
