def load_config(config_path):
    import yaml
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def setup_logging(log_file):
    import logging
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')

def save_model(model, model_path):
    import pickle
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)

def load_model(model_path):
    import pickle
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

def log_message(message):
    import logging
    logging.info(message)