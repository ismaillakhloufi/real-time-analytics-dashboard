import os
from dotenv import load_dotenv

def load_environment_variables(env_file_path=".env"):  # Adjust the path to the correct location
    """
    Load environment variables from a .env file or system environment.
    
    Args:
        env_file_path (str, optional): Path to the .env file. Defaults to "../.env".

    Returns:
        dict: A dictionary of environment variable names and their values.
    """
    # Load environment variables from the .env file (if it exists)
    if os.path.exists(env_file_path):
        load_dotenv(dotenv_path=env_file_path)
        print(f"Environment variables loaded from: {env_file_path}")
    else:
        print(f".env file not found at: {env_file_path}")
        raise FileNotFoundError(f"{env_file_path} does not exist")

    # Collect and return all loaded environment variables
    env_vars = {key: os.getenv(key) for key in os.environ.keys()}
    return env_vars
