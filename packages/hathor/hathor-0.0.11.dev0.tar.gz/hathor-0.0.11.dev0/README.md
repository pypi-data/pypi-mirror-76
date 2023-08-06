# Hathor

Hathor is a commandline tool that helps you combobulate vanilla-like Lua source code into
Roblox Lua compatible modules.

## Goals

The main goal of hathor is to be able to use vanilla-style imports with Roblox Lua.
This makes it so autocompletion within Lua IDEs works properly with Roblox modules.
The side effect of this is that the build output can be specialized depending on project needs.
To aide with development, hathor also includes a synchronization server that can synchronize your
scripts with Roblox Studio.

Hathor is a replacement for two older Rockit tools:
- [Zipline](https://gitlab.com/rockit-tools/zipline), a synchronization tool
- [Tulip](https://gitlab.com/rockit-tools/tulip), a source transformer tool

## Getting started
Getting started with hathor is easy. The CLI is installable through pip:

```sh
pip install --user hathor
```

or through pip, but using the git repository as source:

```sh
pip install git+https://gitlab.com/rockit-tools/hathor.git
```

Installing using the git repository should install the latest development (semi-stable) version of hathor.

### Roblox Studio Plugin
To get changes synchronized in to studio, you need to install the complementary plugin. Hathor is
compatible with the older Zipline plugin for Roblox Studio.

Link: [Zipline Synchronization plugin](https://www.roblox.com/library/3607046899/Zipline-plugin)

### Concepts
Creating a new project can be done through the hathor CLI, however you'll need to know about
some core concepts.

#### Project configuration file
Every hathor project requires a `hathor.project.yml` file to be present at its root. This file
contains all requisite configuration for a hathor project to function. An example of this can be
found in the `example_project` that is bundled with the source code.


#### Paths in the project configuration
All paths in the project configuration are:
- Relative to the project configuration file
- Unix style, meaning that the path separator is a forward slash.

#### Sources
Hathor can pull sources from multiple source directories. These should be listed under the `sources`
section of the project configuration file. The key of each source is the path to the source, while
the key/value pairs for a source are its properties. Sources can be enabled and disabled as required.

#### Build profiles
The `build` section of the project contains build profiles. A build profile specifies how your
hathor project should be built. The configuration directly under the `build` section is the `default`
build profile. However, additional profiles can be specified using the `profiles` subsection.


#### Builders
Hathor is bundled with 'builders'. These are simply functions that build your project into the
desired result. Currently hathor ships with two builder:

- `modular`: Creates a modular build, using the Hathor loader
- `copy`: Creates a 1:1 copy of your sources

#### Synchronization
The `hathor serve` command spins up a REST api for the synchronization plugin. The server will
detect changes in your defined sources and build your project in memory. Output files from the build
will be synchronized to Roblox Studio.

## Creating a new project
Creating a new project with hathor is as easy as its gets. All you have to do is:
1. Create a new project directory
2. `cd` into your project directory
2. Run `hathor init`

The `hathor init` command will prompt you with several questions, and will set up a project for you.
