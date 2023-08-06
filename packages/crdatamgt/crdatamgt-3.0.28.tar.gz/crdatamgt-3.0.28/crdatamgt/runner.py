import os
import sys

import yaml
from yaml.scanner import ScannerError

from crdatamgt.helpers import logger, write_yaml
from crdatamgt.project import project_load

log = logger(name="__main__")

import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


def process_data():
    def represent_none(self, _):
        return self.represent_scalar("tag:yaml.org,2002:null", "")

    yaml.add_representer(type(None), represent_none)

    try:
        with open("parameters.yaml", "r") as stream:
            try:
                data_loaded = yaml.safe_load(stream)
                project_load(**data_loaded)
            except TypeError as e:
                log.critical(
                    f"We were unable to read the files -- Possible your parameters file is wrong \n {e}"
                )
                os.startfile(os.path.join(os.getcwd(), "parameters.yaml"))
                sys.exit(0)
            except ScannerError as e:
                log.critical(
                    f"Your YAML file is not properly formated - Likley missing a space BEFORE your file-path\n Example "
                    f"-> RESULTS DIRECTORY: R:\Shared Drive <- Is proper \n{e}"
                )
                sys.exit(0)
            except:
                e = sys.exc_info()[0]
                log.critical(f"A more subtle error :: {e}")
                raise(e)
                sys.exit(0)

    except FileNotFoundError as e:
        log.info("File not found\n     {}".format(e))
        data_loaded = write_yaml()
        with open("parameters.yaml", "w") as outfile:
            yaml.dump(data_loaded, outfile, default_flow_style=False)
        os.startfile(os.path.join(os.getcwd(), "parameters.yaml"))
