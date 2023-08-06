mgmr(1)

# NAME

mgmr - Merge merge requests in a GitLab instance

# SYNOPSIS

*mgmr* [options] <MRNUM...>

# OPTIONS

*--version*
	Show version number and quit

*-h, --help*
	Show help message and quit

*--token* <TOKEN>
	GitLab Personal Access Token

*-c, --config* <CONFIG>
	Full path to configuration directory

*-n, --dry-run*
	Show which merge requests mgmr would try to merge

*--timeout* <TIMEOUT>
	Set timeout for making calls to the gitlab API

*--save*
	If any value option is passed, save it to configuration

*--write*
	Write any value option passed to configuration and then exit

*--remote* <REMOTE>
	Which remote to operate on

*-q, --quiet*
	Print only the json with the results or in case of an unrecoverable error

*-v, --verbose*
	Print results and recovered errors

*-w, --wait*
	Interval between pings to GitLab to see if Merge Request was rebased

*--reset-project-id*
	Remove project-id file in cache, required when the GitLab project changes its internal-id

*--clean-cached-branches*
	Remove dangling references in branch cache (empty files and ones without a local branch)

# DESCRIPTION

mgmr is a python3 script that allows an user to merge merge requests in any
GitLab instance.

It makes uses of an ini-format configuration file to store the url of the
instance and the personal access token used to interact with the GitLab API of
the hosted instance. And it uses information stored in the git repository in
the form of remotes to guess which GitLab instance it should interact with.

# EXAMPLES

The following show examples of how to use the different options that mgmr
provides, note that almost all options can be mixed and match as you please:

## Merging lots of merge requests

```
mgmr 1 2 3
```

## Use another configuration file

```
mgmr --config=/path/to/temporary/configuration
```

## Permanently switching to a new token

```
mgmr --token=NewTokenSoNice --overwrite
```

## Merge via branch name (branch in this case is named foo)

```
mgmr foo
```

## Remove stale branch files (branch files that have no local branch)

```
mgmr --clean-cached-branches
```

; TODO: write about	the loop we use to merge multiple MRs

# SEE ALSO

*mkmr-config(7)*, *mkmr-remotes(7)*, *mkmr-cache(7)*

# AUTHORS

Maintained by Leo <thinkabit.ukim@gmail.com>
