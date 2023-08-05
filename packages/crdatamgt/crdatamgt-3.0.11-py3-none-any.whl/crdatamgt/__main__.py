import os
import sys

import simplelogging
import yaml
from yaml.scanner import ScannerError

import crdatamgt

log = simplelogging.get_logger()


def main():
    def represent_none(self, _):
        return self.represent_scalar("tag:yaml.org,2002:null", "")

    yaml.add_representer(type(None), represent_none)

    try:
        with open("parameters.yaml", "r") as stream:
            try:
                data_loaded = yaml.safe_load(stream)
                crdatamgt.project.project_load(**data_loaded)
            except TypeError as e:
                log.critical(
                    "We were unable to read the files -- Possible your parameters file is wrong"
                )
                print("Please double-check your parameters.yaml document'")
                os.startfile(os.path.join(os.getcwd(), "parameters.yaml"))
            except ScannerError as e:
                log.critical(
                    f"Your YAML file is not properly formated - Likley missing a space BEFORE your file-path\n Example "
                    f"-> RESULTS DIRECTORY: R:\Shared Drive <- Is proper \n{e}"
                )
            except:
                e = sys.exc_info()[0]
                log.critical(f"A more subtle error :: {e}")

    except FileNotFoundError as e:
        log.info("File not found\n     {}".format(e))
        data_loaded = crdatamgt.helpers.write_yaml()
        with open("parameters.yaml", "w") as outfile:
            yaml.dump(data_loaded, outfile, default_flow_style=False)
        print("Please fill out the parameter.yaml document")
        os.startfile(os.path.join(os.getcwd(), "parameters.yaml"))


if __name__ == "__main__":
    main()
