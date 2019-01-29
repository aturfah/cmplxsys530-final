# Contributing

## Git Branching Structure
### Features, Bugs, & Enhancements in Dev
- Branches are to be made off of `master`, and upon completion of a feature pulled into `dev`
- `dev` is to be pulled into `master` when a release is ready to be deployed
### Bugs in Master
- Branches are to be made off of `master`
- Upon completion, seperate pull requests are to be issued into `dev` and `master`

## Creating Issues and Pull Requests
Minus very small things (ex" updating `requirements.txt`), all changes should have corresponding issue(s) and pull request(s). These should follow the templates specified in the `docs/` directory.

## Issue & Pull Request Labels
The labels on issues and PRs help identify the nature of the work that needs to be done. The labels are broken up into four main categories: flags, scope, status, and type. Except for `status` labels, the issue and its corresponding pull request(s) should share the same labels. The status, type, and scope labels are all necessary labels for an issue.

### Flag Labels
Labels prefixed with `flag` are meant to indicate some special meaning about an issue. These can be `high priority` issues, `duplicate` issues, etc. 

### Scope Labels
Labels prefixed with `scope` identify which part of the codebase this issue will affect. A single issue should _only_ hae a single scope; ie: Engine Logic and Agent Logic should be broken up into seperate issues and Pull Requests. The main scopes are `agent logic`, `engine logic`, and `ladder logic`, as these are the three fundamental parts of the simulations. Anything else (interface, documentation, etc) should have the `misc` scope applied.

### Status Labels
Labels prefixed with `status` indicate the current state of an issue; is work on it under active development (`in progress`), ready to be worked on (`pending`) or `blocked` by another issue?

### Type Labels
Labels prefixed with `type` indicate what type of work is to be done. This admittedly isn't always apparent from the start. For example, if in order for a new feature to be implemented a seperate chunk of code needs to be rewritten, does this count as `refactor` or `new feature`? These are meant to provide some idea of the code thats going to be written, and guage its impact (one would be worried if a `type:refactor` issue was being pulled in without significant testing).
