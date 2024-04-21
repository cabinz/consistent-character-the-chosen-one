import argparse
import yaml


def config2args(path):
    with open(path, 'r') as file:
        yaml_data = yaml.safe_load(file)
    parser = argparse.ArgumentParser(description="Generate args from config")
    for key, value in yaml_data.items():
        parser.add_argument(f'--{key}', type=type(value), default=value)
    
    args = parser.parse_args([])
        
    return args

def log_print(text, log=None):
    SPLIT_LN = "###########################################################################"
    if log is None:
        print()
        print(SPLIT_LN)
        print(SPLIT_LN)
        print(text)
        print(SPLIT_LN)
        print(SPLIT_LN)
        print()
    else:
        log.info(SPLIT_LN)
        log.info(SPLIT_LN)
        log.info(text)
        log.info(SPLIT_LN)
        log.info(SPLIT_LN)
        