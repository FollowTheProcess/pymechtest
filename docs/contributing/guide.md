# Contributing to pymechtest

I've tried to structure pymechtest to make it nice and easy for people to contribute. Here's how to go about doing it! :smiley:

First, see the [help] section for some general info on how you can help pymechtest.

## Developing

If you want to fix a bug, improve the docs, add tests, add a feature or any other type of direct contribution to pymechtest: here's how you do it!

**To work on pymechtest you'll need python >=3.7**

### Step 1: Fork pymechtest

The first thing to do is 'fork' pymechtest. This will put a version of it on your GitHub page. This means you can change that fork all you want and the actual version of pymechtest still works!

To create a fork, go to the pymechtest [repo] and click on the fork button!

### Step 2: Clone your fork

Navigate to where you do your development work on your machine and open a terminal

**If you use HTTPS:**

```shell
git clone https://github.com/<your_github_username>/pymechtest.git
```

**If you use SSH:**

```shell
git clone git@github.com:<your_github_username>/pymechtest.git
```

**Or you can be really fancy and use the [GH CLI]**

```shell
gh repo clone <your_github_username>/pymechtest
```

HTTPS is probably the one most people use!

Once you've cloned the project, cd into it...

```shell
cd pymechtest
```

This will take you into the root directory of the project.

Now add the original pymechtest repo as an upstream in your forked project:

```shell
git remote add upstream https://github.com/FollowTheProcess/pymechtest.git
```

This makes the original version of pymechtest 'upstream' but not 'origin'. Basically, this means that if your working on it for a while and the original project has changed in the meantime, you can do:

```shell
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
```

This will (in order):

* Checkout the main branch of your locally cloned fork
* Fetch any changes from the original project that have happened since you forked it
* Merge those changes in with what you have
* Push those changes up to your fork so your fork stays up to date with the original.

*Good practice is to do this before you start doing anything every time you start work, then the chances of you getting conflicting commits later on is much lower!*

### Step 3: Create the Environment

Before you do anything, you'll want to set up your virtual environment...

```shell
python3 -m venv .venv
```

This creates a virtual environment (called .venv)

Now, activate your environment...

```shell
# macOS and Linux
source .venv/bin/activate

# Windows
.\.venv.\Scripts.\Activate.ps1
```

To check it worked, use:

```shell
# macOS and Linux
which pip

# Windows
Get-Command pip
```

It should say...

```shell
some/directory/pymechtest/.venv/bin/pip
```

If it shows this, it's worked! :tada:

### Step 4: Install the Dependencies

Now you need to install pymechtest locally (in editable format: `-e`) including all it's dependencies.

That's as easy as:

```shell
pip install -e .[dev]

# If you use zsh, you may have to escape the square brackets
pip install -e .\[dev\]

# Or you can use the makefile
make dev
```

Side note: If you're on mac (uses zsh by default) and you have to escape the square brackets. Try setting this in your `~/.zshrc`:

```shell
# in ~/.zshrc
# Means you don't have to escape square brackets
unsetopt nomatch
```

I mention that here because it took me **AGES** to find that! :unamused:

### Step 5: Do your thing

**Always checkout a new branch before changing anything**

```shell
git checkout -b <name-of-your-bugfix-or-feature>
```

So if I was going to fix a bug with the yield strength calculation I would do something like:

```shell
git checkout -b yield-strength-bugfix
```

Now you're ready to start working!

*Remember! pymechtest aims for high test coverage. If you implement a new feature, make sure to write tests for it! Similarly, if you fix a bug, it's good practice to write a test that would have caught that bug so we can be sure it doesn't reappear in the future!*

pymechtest uses [nox] for automated testing, building the docs, formatting and linting etc. So when you've made your changes, just run:

```shell
nox
```

And it will tell you if something's wrong!

### Step 6: Commit your changes

Once you're happy with what you've done, add the files you've changed:

```shell
git add <changed-file(s)>

# Might be easier to do
git add -A

# But be wary of this and check what it's added is what you wanted..
git status
```

Commit your changes:

```shell
git commit

# Now write a good commit message explaining what you've done and why.
```

While you were working on your changes, the original project might have changed (due to other people working on it). So first, you should rebase your current branch from the upstream destination. Doing this means that when you do your PR, it's all compatible:

```shell
git pull --rebase upstream main
```

Now push your changes to your fork:

```shell
git push origin <your-branch-name>
```

### Step 7: Create a Pull Request

Now go to the original pymechtest [repo] and create a Pull Request. Make sure to choose upstream repo "main" as the destination branch and your forked repo "your-branch-name" as the source.

Thats it! Your code will be tested automatically by pymechtest's CI suite and if everything passes and your PR is approved and merged then it will become part of pymechtest!

*Note: There is a good guide to open source contribution workflow [here] and also [here too]*

## Contributing to Docs

Any improvements to the documentation are always appreciated! pymechtest uses [mkdocs] with the [mkdocs-material] theme so the documentation is all written in markdown and can be found in the `docs` folder in the project root.

Because pymechtest uses [nox], things like building and serving the documentation is super easy. All you have to do is:

```shell
# Builds the docs
nox -s docs

# Or again, the makefile
make docs

# Builds and serves to localhost
nox -s docs -- serve

# makefile equivalent
make autodocs
```

*If you installed with `.[dev]` earlier, you could also just run `mkdocs build --clean` and `mkdocs serve` if you wanted*

If you use the `serve` option, you can navigate to the localhost IP address it gives you and as you make changes to the source files, it will automatically reload your browser! Automation is power! :robot:

If you add pages to the docs, make sure they are placed in the nav tree in the `mkdocs.yml` file and you're good to go!

[help]: help.md
[GH CLI]: https://cli.github.com
[nox]: https://nox.thea.codes/en/stable/
[repo]: https://github.com/FollowTheProcess/pymechtest
[here]: https://stackoverflow.com/questions/20956154/whats-the-workflow-to-contribute-to-an-open-source-project-using-git-pull-reque
[here too]: https://github.com/asmeurer/git-workflow
[mkdocs]: https://www.mkdocs.org
[mkdocs-material]: https://squidfunk.github.io/mkdocs-material/
