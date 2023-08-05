# tangoctl

[![Pypi Version](https://img.shields.io/pypi/v/tangoctl.svg)](https://pypi.python.org/pypi/tangoctl)
[![Python Versions](https://img.shields.io/pypi/pyversions/tangoctl.svg)](https://pypi.python.org/pypi/tangoctl)
[![Build Status](https://gitlab.com/tiagocoutinho/tangoctl/badges/master/pipeline.svg)](https://gitlab.com/tiagocoutinho/tangoctl/commits/master)
[![Coverage Status](https://gitlab.com/tiagocoutinho/tangoctl/badges/master/coverage.svg)](https://gitlab.com/tiagocoutinho/tangoctl/commits/master)

A CLI built for [Tango](http://tango-controls.org) system
administrators.

tangoctl aims to be to [Tango](http://tango-controls.org) what systemctl
is to to systemd.

Actions speak louder than words. Here is a video:

![tangoctl in action](./tangoctl.svg)

## Purpose

- day to day [Tango](http://tango-controls.org) maintenance
- help automate ansible, puppet or chef scripts
- prepare automated test scripts for your own software
- help write a custom [bash completion](http://www.caliban.org/bash/#completion)
  for your tool

## Features

- server operations:
  - server info
  - tree of servers
  - list of servers
  - register/unregister servers
- device operations:
  - device info
  - tree of devices
  - list of devices
  - register/unregister devices
  - execute commands
  - command info
  - read and write attributes
  - attribute info
  - read and write properties

## Installation

pip install it on your favorite python environment:

`$ pip install tangoctl`

That's it!

## Examples

```bash
# Display tree of servers:
tangoctl server tree

# Display list of devices:
tangoctl device list

# Read 'state' attribute from a device
tangoctl device attribute read -d sys/tg_test/1 -a state

# Execute command Init() on a device
tangoctl device command exec -d sys/tg_test/1 -c init

# Display 'double_spectrum' attribute information
tangoctl device attribute info -d sys/tg_test/1 -a double_spectrum

# Display list of device attributes:
tangoctl device attribute list -d sys/tg_test/1
```

### Writting a custom bash completion for your server

Imagine you have a [Tango](http://tango-controls.org) server called
*LimaCCDs* and you registered two instances in the database, maybe
using tangoctl:

```bash
tangoctl server add LimaCCDs/basler1 -d id00/limaccds/basler1
tangoctl server add LimaCCDs/pilatus1 -d id00/limaccds/pilatus1
```

To have bash auto-complete every time you type `LimaCCDs [tab]` on the
command line, place the following lines in a bash script:

```bash
# naive tango server autocomplete using tangoctl server ilist
_tango_server_complete()
{
    stype="${COMP_WORDS[0]}"
    sname="${COMP_WORDS[COMP_CWORD]}"
    echo $stype
    COMPREPLY=( $(tangoctl server ilist -t "${stype}" --instance="${sname}*") )
    return 0
}

complete -F _tango_server_complete Demo
```

and run it. Next time you type `LimaCCDs [tab]]` on the bash command line it
will offer the existing LimaCCDs instances as completion options:

```bash
$ LimaCCDs [tab]
basler1 pilatus1

$ LimaCCDs pil[tab]
pilatus1
```

Check the bash completion documentation on how to add it permanently to
your environment.

## Special thanks to

- [PyTango](https://github.com/tango-controls/pytango): Tango binding
  to python
- [click](https://github.com/pallets/click): beautiful command line
  interfaces
- [gevent](https://github.com/gevent/gevent): I/O made simple and
  efficient
- [tabulate](https://bitbucket.org/astanin/python-tabulate): ASCII
  tables
- [treelib](https://github.com/caesar0301/treelib): tree data structures
- [python prompt toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit):
  powerful interactive command line applications
