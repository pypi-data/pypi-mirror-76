mkmr-config(7)

# NAME

*mkmr-config* - Configuration for mkmr and utilities

# DESCRIPTION

The *config* file, in ini-format consists of various sections, the sections are
all named after the current directory of where the repo was initialized.

The section can also have a second name (these types of sections will be
referred as *tool-section*), which is the name of one of the tools that mkmr
provides.

sections can have the following options:

- origin -> name of the remote that refers to your fork of the repo
- upstream -> name of the remote that refers to upstream
- remote -> same as upstream, for tools that only deal with upstream

tool-sections can have the following options:

> NOTE: some options only affect certain tools, and options have different
> effects depending on the tool.

- yes (True|False)
- quiet (True|False)
- edit (True|False)
- timeout (Integer)
- wait (Integer)

# EXAMPLES

```
[aports]
origin = origin
upstream = upstream

[aports mkmr]
edit = False
yes = True

[aports mgmr]
wait = 6
```

# AUTHORS

Maintained by Leo <thinkabit.ukim@gmail.com>
