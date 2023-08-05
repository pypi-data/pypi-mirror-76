"""This module implements SOIL's Command LIne Interface"""
import sys
import os
import json
import getpass
import zipfile
from json import JSONDecodeError    # Flake8...
import subprocess   # nosec
import virtualenv   # type: ignore
import requests


class SoilCli():
    """Implements the CLI object, containing configuartion and functionalities"""

    def __init__(self) -> None:
        """Initializes the instance and loads configuration"""
        self.env = dict()
        self.options = dict()   # type: ignore
        self.config = dict()
        self.paths = dict()
        self.paths['venv'] = '.venv'
        try:
            config_file = open(os.path.expanduser('~/.soil/soil.conf'), 'r')
            self.config = json.loads(config_file.read())
            config_file.close()
        except (IOError, JSONDecodeError):
            if sys.argv[1] != "configure":
                try:
                    os.rename(os.path.expanduser('~/.soil/soil.conf.bak'), os.path.expanduser('~/.soil/soil.conf'))
                except IOError:
                    print("Can not load soil configuration. Plase run soil configure to configure it.")
                    sys.exit()
        try:
            env_file = open(os.path.expanduser('~/.soil/soil.env'), 'r')
            self.env = json.loads(env_file.read())
            env_file.close()
        except (IOError, JSONDecodeError):
            if sys.argv[1] != "configure":
                try:
                    os.rename(os.path.expanduser('~/.soil/soil.conf.bak'), os.path.expanduser('~/.soil/soil.conf'))
                except IOError:
                    print("Can not load soil environment. Plase run soil configure to initialize it.")
                    sys.exit()

    def __save_environment(self) -> None:
        """Saves the environment keys to a file, backing it up to prevent data loss"""
        os.rename(os.path.expanduser('~/.soil/soil.env'), os.path.expanduser('~/.soil/soil.env.bak'))
        env_file = open(os.path.expanduser('~/.soil/soil.env'), 'w')
        env_file.write(json.dumps(self.env, indent=4, sort_keys=True))
        env_file.close()
        os.remove(os.path.expanduser('~/.soil/soil.env.bak'))

    def __save_configuration(self) -> None:
        """Saves the configuration keys to a file, backing it up to prevent data loss"""
        os.rename(os.path.expanduser('~/.soil/soil.conf'), os.path.expanduser('~/.soil/soil.conf.bak'))
        env_file = open(os.path.expanduser('~/.soil/soil.conf'), 'w')
        env_file.write(json.dumps(self.config, indent=4, sort_keys=True))
        env_file.close()
        os.remove(os.path.expanduser('~/.soil/soil.conf.bak'))

    def execute(self, cmd, args) -> object:     # type: ignore
        """Fills the options dict and returns the function to execute."""
        try:
            self.options = dict.fromkeys(args, 1)
            command = getattr(self, cmd, lambda: print("Invalid command!"))
            # Call the method as we return it
            return command()
        except TypeError:
            print("Invalid command!")

    def help(self) -> None:
        """Prints help"""
        commands = ["configure",
                    "init",
                    "login",
                    "install"]
        for command in commands:
            print(command + ": " + getattr(self, command).__doc__)

    def configure(self) -> None:
        """
        Allows the user to provide the configuration parameters interactively and stores them into a file
        """
        try:
            os.makedirs(os.path.expanduser('~/.soil/'))
        except FileExistsError:
            # directory already exists
            pass

        try:

            if "--reset" in self.options:
                try:
                    os.rename(os.path.expanduser('~/.soil/soil.conf'), os.path.expanduser('~/.soil/soil.conf.bak'))
                    os.rename(os.path.expanduser('~/.soil/soil.env'), os.path.expanduser('~/.soil/soil.env.bak'))
                except FileNotFoundError:
                    print("Seems there is no previous configuration. Performing a clean config...")
                    self.options.pop('--reset', None)

            config_file = open(os.path.expanduser('~/.soil/soil.conf'), 'x')
            self.config["soil_url"] = input("Enter url of your soil instance: ")  # nosec - Input is safe in python3
            auth_url_msg = "Enter authentication provider URL: [https://auth.amalfianalytics.com] "
            self.config["auth_url"] = input(auth_url_msg)   # nosec - Input is safe in python3
            if self.config["auth_url"] == "":
                self.config["auth_url"] = "https://auth.amalfianalytics.com"
            self.config["auth_app_id"] = input("Enter your application id: ")  # nosec - Input is safe in python3
            self.config["auth_api_key"] = input("Enter your API key: ")  # nosec - Input is safe in python3
            config_file.write(json.dumps(self.config, indent=4, sort_keys=True))
            config_file.close()

            # Create the environment file
            env_file = open(os.path.expanduser('~/.soil/soil.env'), 'x')
            env_file.write("{\n}")
            env_file.close()

            if "--reset" in self.options:
                os.remove(os.path.expanduser('~/.soil/soil.conf.bak'))
                os.remove(os.path.expanduser('~/.soil/soil.env.bak'))

        except FileExistsError:
            if "--reset" not in self.options:
                print("Soil already configured (Use --reset to reconfigure):\n")
                for option, value in self.config.items():
                    print(option + ": " + value)
                print()

    def login(self) -> None:
        """
        Authenticates to the authentication backend and stores the credentials (JWT) in the environment
        """
        print(f"Authenticating to {self.config['auth_url']}...")
        username = input("Username: ")  # nosec - Input is safe in python3
        password = getpass.getpass()

        request_json = {'loginId': username, 'password': password, 'applicationId': self.config['auth_app_id']}

        # print(request_json)

        resp = requests.post(self.config['auth_url']+"/api/login",
                             # headers={"Authorization: " + self.config['api_key']},
                             headers={'Authorization': self.config['auth_api_key']},
                             json=request_json)

        if resp.status_code == 200 or resp.status_code == 202:
            self.env["auth"] = json.loads(resp.content)
            self.__save_environment()
            print('Successfully logged in as ' + self.env['auth']['user']['username'] + "!")
        elif resp.status_code == 404:
            print("The user was not found or the password was incorrect.")
            self.login()

    def init(self) -> None:
        """
        Initializes the current directory as a SOIL project by placing all the directory structure and
        creating a python virtual environment
        """
        if os.path.isfile('./soil.yml'):
            print("Already initialized")
            sys.exit()
        else:
            with zipfile.ZipFile(os.path.dirname(os.path.realpath(__file__))+'/template.zip', 'r') as template_zip:
                template_zip.extractall('./')
            # create and activate the virtual environment
            virtualenv.cli_run([self.paths["venv"]])

    def install(self) -> None:
        """
        Invokes current project's virtual environment pip to install th provided packages.
        Also updates requirements.txt
        """
        if not os.path.exists(self.paths['venv']):
            print("This folder is not initalized as a soil project. Please run soil init to initialize it.")
            sys.exit()
        packages = list(self.options.keys())
        for package in packages:
            subprocess.check_call(['.venv/bin/python', "-m", "pip", "install", package])    # nosec
        f = open('requirements.txt', 'w')
        f.write(os.popen(self.paths['venv'] + '/bin/pip freeze').read())    # nosec
        f.close()


def main() -> None:
    """ main method"""
    try:
        cli = SoilCli()
        if len(sys.argv) > 1:
            cli.execute(sys.argv[1], sys.argv[2:])
        else:
            cli.help()
    except KeyboardInterrupt:
        print("\nExit")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0) # NOQA # pylint: disable=protected-access


if __name__ == "__main__":
    main()
