

def parse(arg_file):
    """
    :param arg_file: yaml file location for specifying arguments.
    :return dict of specified arguments to the script.:

    Example YAML file for arguments:
    ---
    string:
      help: Example string parameter.
      type: str
      default: 'default string'
    bool_false:
      help: Example boolean with a default of false.
      default: False
      action: 'store_true'
    bool_true:
      help: Example boolean with a default of true
      default: True
      action: 'store_false'
    list:
      help: List of n number of unnamed arguments.
      default: ''
      nargs: '*'
    """
    import argparse
    from pydoc import locate
    import yaml
    with open(arg_file, 'r') as y:
        data = yaml.load(y, Loader=yaml.FullLoader)
        parser = argparse.ArgumentParser()
        for argument, parameters in data.items():
            if 'type' in parameters.keys():
                parameters['type'] = locate(parameters['type'])
            parser.add_argument('--' + argument, **parameters)
        return vars(parser.parse_args())
