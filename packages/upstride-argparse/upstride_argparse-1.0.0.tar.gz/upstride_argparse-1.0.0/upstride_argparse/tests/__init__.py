import shutil
import os
import tempfile
import json
import yaml
import unittest
import argparse
from unittest import mock
from upstride_argparse import read_yaml_config, parse_cmd


class TestArgumentParser(unittest.TestCase):
  def test_read_yaml_config(self):
    config_dir = create_yaml_file()
    parameters = init_parameters()
    read_yaml_config(os.path.join(config_dir, "config.yml"), parameters)
    self.assertEqual(parameters['parameter_int'], 2)
    self.assertEqual(parameters['parameter_str'], "plip")
    self.assertEqual(parameters['parameter_list'], [1, 2, 3])
    self.assertEqual(parameters['parameter_bool'], True)
    self.assertEqual(parameters['parameter_dict']['parameter_int'], 3)
    shutil.rmtree(config_dir)

  @mock.patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace())
  def test_parse_empty_config(self, mock_args):
    arguments = get_arguments()
    parameters = parse_cmd(arguments)
    out_parameters = {
        "parameter_int": 0,
        "parameter_str": '',
        "parameter_list": [1, 5, 6],
        "parameter_bool": False,
        "parameter_dict": {
            "parameter_int": 5
        }
    }
    self.assertEqual(parameters, out_parameters)

  @mock.patch('argparse.ArgumentParser.parse_args',
              return_value=argparse.Namespace(**{"yaml_config": ['/tmp/testing_upstride_argparse/config.yml']}))
  def test_parse_yaml_config(self, mock_args):
    arguments = get_arguments()
    arguments.append([str, "yaml_config", "", "config file"])
    create_yaml_file_fixed_location()
    parameters = parse_cmd(arguments)
    self.assertEqual(parameters['parameter_int'], 1)
    self.assertEqual(parameters['parameter_str'], "plop")
    self.assertEqual(parameters['parameter_list'], [1, 2, 3])
    self.assertEqual(parameters['parameter_bool'], True)
    self.assertEqual(parameters['parameter_dict']['parameter_int'], 3)

  @mock.patch('argparse.ArgumentParser.parse_args',
              return_value=argparse.Namespace(**{"yaml_config": ['/tmp/testing_upstride_argparse/config.yml'], "parameter_int": -1}))
  def test_parse_yaml_mix_config(self, mock_args):
    arguments = get_arguments()
    arguments.append([str, "yaml_config", "", "config file"])
    arguments.append([str, "other_param", "test", ""])
    create_yaml_file_fixed_location()
    parameters = parse_cmd(arguments)
    self.assertEqual(parameters['parameter_int'], -1)
    self.assertEqual(parameters['parameter_str'], "plop")
    self.assertEqual(parameters['parameter_list'], [1, 2, 3])
    self.assertEqual(parameters['parameter_bool'], True)
    self.assertEqual(parameters['other_param'], "test")


def get_arguments():
  return [
      [int, "parameter_int", 0, "", lambda x: x < 2],
      [str, "parameter_str", "", ""],
      ['list[int]', "parameter_list", [1, 5, 6], ""],
      [bool, "parameter_bool", False, ""],
      ['namespace', 'parameter_dict', [
          [int, 'parameter_int', 5, '']
      ]]
  ]


def create_yaml_file():
  """Create a config yaml file and return the dir containing it for destruction
  """
  config_dir = tempfile.mkdtemp()
  yaml_content = {
      "parameter_int": 2,
      "parameter_str": "plip",
      "parameter_list": [1, 2, 3],
      "parameter_bool": True,
      "parameter_dict": {
          "parameter_int": 3
      }
  }
  with open(os.path.join(config_dir, 'config.yml'), 'w') as outfile:
    yaml.dump(yaml_content, outfile)
  return config_dir


def create_yaml_file_fixed_location():
  """Create a config yaml file in /tmp/testing_upstride_argparse
  this is needed because the mock.patch can't take variables
  """
  config_dir = '/tmp/testing_upstride_argparse'
  os.makedirs(config_dir, exist_ok=True)
  yaml_content = {
      "parameter_int": 1,
      "parameter_str": "plop",
      "parameter_list": [1, 2, 3],
      "parameter_bool": True,
      "parameter_dict": {
          "parameter_int": 3
      }
  }
  with open(os.path.join(config_dir, 'config.yml'), 'w') as outfile:
    yaml.dump(yaml_content, outfile)
  return


def init_parameters():
  parameters = {
      "parameter_int": None,
      "parameter_str": None,
      "parameter_list": None,
      "parameter_bool": None,
      "parameter_dict": {
          "parameter_int": None
      }
  }
  return parameters
