# Ckttools

This repository contains tools to analyze and manipulate circuits for my research. There are no guarentees on if these things will work for you or be useful to you.

## Installing

## Tools

### v2bench

Converts a circuit from a verilog format the a bench format.

Usage: `python3 ckttools/v2bench.py [-o OUTPUT_FILE] verilog_file`

### EasyLock

Adds configurable logic locking to a circuit.

Usage: `python3 ckttools/easylock.py --config CONFIG_FILE [-o OUTPUT_FILE] verilog_file`

The configuration file is a YAML file that contains information on how and where to add logic locking. The basic format is shown below:

```
---
name: A description of the config file
passes:
  - name: Pass 1
    locking-type: antisat
    integration:
      net-type: output
    number-keys: 6
  - name: Pass 2
    locking-type: sarlock
    integration:
      net-type: previous
    number-keys: 4
    primary-input-start: continuous
```

The top scope of the config file contains two items: `name` and `passes`. The `name` only serves as documentation and is intended to describe what the configuration file does. The `passes` item contains how to add locking to the circuit. Each pass adds a single instance of locking to the circuit. For example, if you do two passes with Anti-SAT locking, you will have two separate Anti-SAT blocks, which are each integrated into the circuit at different locations.

Each pass has several options available, some of which are required, and some of which are only used by certain locking techniques. The `name` option is again just for documentation. The `locking-type` determines which locking technique to use and must match a type listed in `ckttools/locking/definitions.yaml`. The `integration` option determines where the locking is placed in the circuit and can take many different values. For locking schemes that use primary inputs (Anti-SAT, SARLock, etc.), the `primary-input-start` option determines which primary inputs should be used.

As stated above, the `integration` option can take on of several values. More accurately, the list of value insertion nets starts with all nets in the circuit, and each new option listed under the `integration` node filters that list. Then, after all filters are applied, a net is randomly selected from the remaining nets. Some commonly used filters are:
 * `net-type`: can be `output` or `previous. Output selects all outputs, while previous selects the output from the previous pass.
 * `net-name`: can specify a net name if you want it to always be on that net
 * `interference`: force the locking to either be indirectly, directly, or have no iterference with another pass. This option also has children options that need more explanation.

### SAT Attack

Runs a SAT attack against a logic locked circuit.

### v2svg

Creates an .svg diagram of a circuit.
