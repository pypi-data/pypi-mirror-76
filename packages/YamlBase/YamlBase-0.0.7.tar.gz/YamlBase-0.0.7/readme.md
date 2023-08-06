# YamlBase
[![codecov](https://codecov.io/gh/mv-yurchenko/YBase/branch/dev/graph/badge.svg)](https://codecov.io/gh/mv-yurchenko/YBase)
[![Actions Status](https://github.com/mv-yurchenko/YBase/workflows/deploy_on_master/badge.svg)](https://github.com/mv-yurchenko/YBase/actions)
[![CodeFactor](https://www.codefactor.io/repository/github/mv-yurchenko/ybase/badge)](https://www.codefactor.io/repository/github/mv-yurchenko/ybase)

This utility allows you to manage tables in a database using YAML files, which makes it faster to create and delete tables in multiple databases simultaneously

## The following databases are currently supported: 

- SQLite 

## Installation 

```shell script
pip install YamlBase
``` 

## Usage Example

To use this utility, you need 2 files, one is the configuration of new tables for the database, and the second is a file with a list of actions

File examples: 
- actions_example.yaml
- base_example.yaml
