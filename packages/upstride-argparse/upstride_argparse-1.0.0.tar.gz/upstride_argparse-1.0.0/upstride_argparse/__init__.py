import argparse
import yaml
import os


def create_dir(path: str):
  """this function exists to be called by the argument parser, 
  to automatically create new directories
  """
  try:
    os.makedirs(path, exist_ok=True)
  except FileExistsError as e:
    # this error shouldn't happen because of exist_ok=True, but we never know
    return False
  except FileNotFoundError as e:
    return False
  return True


def str2bool(v):
  """idea from https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
  """
  if isinstance(v, bool):
    return v
  if v.lower() in ('yes', 'true', 't', 'y', '1'):
    return True
  elif v.lower() in ('no', 'false', 'f', 'n', '0'):
    return False
  else:
    raise argparse.ArgumentTypeError('Boolean value expected.')


def create_argparse(arguments, namespace='', parser=None):
  """create argparse based on the list of arguments

  Args:
      arguments (List): list of [type, name, default, help, condition] or ['namespace', name, List]
      namespace (str, optional): [description]. Defaults to ''.
      parser (argparse, optional): instance of argparse. Defaults to None.

  """

  # this function can be called recursively, we need to be able to recall if this run is the root of the recursion
  init = False
  if parser is None:
    init = True
    parser = argparse.ArgumentParser(description="")

  for argument in arguments:
    # see https://docs.python.org/3/library/argparse.html#nargs for use of nargs='?'
    # check if namespace
    if argument[0] == 'namespace':
      full_namespace = f'{namespace}.{argument[1]}' if namespace != '' else argument[1]
      create_argparse(argument[2], namespace=full_namespace, parser=parser)
      continue
    arg_name = f'--{namespace}.{argument[1]}' if namespace != '' else f'--{argument[1]}'
    help = f'{argument[3]} [default: {argument[2]}]'
    if argument[0] == bool:
      parser.add_argument(arg_name, type=str2bool, nargs='?', const=True, help=help)
      continue
    if argument[0] in [int, str, float]:
      parser.add_argument(arg_name, type=argument[0],  nargs='?', help=help)
      continue

    # at this point, argument[0] should be a string containing 'list'
    if type(argument[0]) != str or 'list' not in argument[0]:
      raise TypeError(f'{argument[0]} is not a correct data type')

    custom_type = argument[0].split('[')[1][:-1]
    if custom_type == 'bool':
      parser.add_argument(arg_name, type=str2bool, nargs='*', help=help)
      continue
    if custom_type in ['int', 'str', 'float']:
      d = {
          'int': int,
          'str': str,
          'float': float
      }
      custom_type = d[custom_type]
      parser.add_argument(arg_name, type=custom_type, nargs='*', help=help)
      continue

    raise TypeError(f'{argument[0]} is not a correct data type')
  if init:
    return parser.parse_args()


def init_parameters(arguments):
  # define the parameter dict with all values to None
  parameters = {}
  for argument in arguments:
    if argument[0] != 'namespace':
      parameters[argument[1]] = None
    else:
      sub_parameters = init_parameters(argument[2])
      parameters[argument[1]] = sub_parameters
  return parameters


def merge_dict(parameters, arguments):
  for key in arguments:
    if parameters[key] is None:
      parameters[key] = arguments[key]
    elif type(parameters[key]) == dict:
      merge_dict(parameters[key], arguments[key])
    else:
      raise Exception("this line shouldn't be excecuted, please check the code")


def read_yaml_config(yaml_file, parameters):
  with open(yaml_file, 'r') as file:
    content = yaml.safe_load(file)
    merge_dict(parameters, content)


def check_and_add_defaults(arguments, parameters):
  # Lastly, if a variable is defined nowhere, then use the default value
  for argument in arguments:
    if argument[0] == 'namespace':
      if argument[1] not in parameters:
        parameters[argument[1]] = {}
      parameters[argument[1]] = check_and_add_defaults(argument[2], parameters[argument[1]])
    else:
      if argument[1] not in parameters or parameters[argument[1]] == None:
        parameters[argument[1]] = argument[2]
      # Now check for additional conditions
      if len(argument) == 5:
        if not argument[4](parameters[argument[1]]):
          raise ValueError("condition for parameter {} not satisfied by value {}".format(argument[1], parameters[argument[1]]))
  return parameters


def parse_cmd(arguments):
  # init parameters dict, read command line and conf file
  parameters = init_parameters(arguments)
  args = create_argparse(arguments)
  if "yaml_config" in vars(args) and vars(args)["yaml_config"] is not None:
    for conf_file in args.yaml_config:
      read_yaml_config(conf_file, parameters)
  # Overwrite config using args
  for key in vars(args):
    if key == "yaml_config" or vars(args)[key] is None:
      continue
    parameters = add_value_in_param(parameters, key, vars(args)[key])
  parameters = check_and_add_defaults(arguments, parameters)
  return parameters


def add_value_in_param(parameters, key, value):
  """
  """
  if '.' not in key:
    parameters[key] = value
  else:
    key_split = key.split('.')
    parameters[key_split[0]] = add_value_in_param(parameters[key_split[0]], '.'.join(key_split[1:]), value)
  return parameters
