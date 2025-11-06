# ProjectInitTool 🤩

---
### Ever feel like initializing a project takes longer than it needs?
Will atleast I have felt so, Creating a GitHub repo, setting up the local directory, initializing git, connecting remotes... it adds up! 

**ProjectInitTool** automates all of this in one simple command, so you can start coding faster.

---

## Installation:

```bash
git clone https://github.com/kevo-1/ProjectInitTool
cd ProjectInitTool
pip install -e .

# Then run this command to set it up
project-configs
```
---
## Requirements:
- [Python 3.6+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- GitHub Personal Access Token ([How to create one](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens))
---

## How to run?
- ### Quickstart:

```bash
projectinit cool-project
```

- ### Basic Usage:
```bash
# Use your saved defaults
projectinit cool-project

# Add description
projectinit cool-project --description "Cooler description😂"

# Make it private
projectinit cool-private-project -p
```

- ### Override defaults:
```bash
# Different directory/
projectinit cool-project -d ~/SomewhereCool

# Github Token
projectinit cool-project -t ghp_token

# Make the repo public (default: private)
projectinit cool-project --public
```

- ### All Options:
```bash
projectinit < project-name > [OPTIONS]

Options:
  -d, --directory       #Base directory (overrides config)
  -t, --token           #GitHub token (overrides config)
  -p, --private         #Make repository private
  --public              #Make repository public
  --description "TEXT"  #Repository description
  --help                #Show help message
```
---

### Configurations
Run the configuration setup anytime to update your defaults:

```bash
project-config
```

This saves:
- **GitHub Token**: Never type it again
- **Base Directory**: Your default project location (e.g., `~/projects`)
- **Privacy Default**: Whether repos should be private by default

Configuration is stored in `~/.github_repo_creator.json`

---
## Custom command names

Want different command names? Edit `setup.py`:

```python
entry_points={
    'console_scripts': [
        'your-command-name=create_repo:main',
        'your-config-name=create_repo:configure',
    ],
}
```

Then reinstall:
```bash
pip install -e .
```

---

## Troubleshooting

**"Error: GitHub token required"**
- Run `project-config` to save your token
- Or set `GITHUB_TOKEN` environment variable
- Or pass `-t` flag with token

**"Error: git is not installed"**
- Install git: [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

**Command not found**
- Try: `pip install --user -e .`

---

## Example

```bash
# One-time setup
git clone https://github.com/kevo-1/ProjectInitTool
cd ProjectInitTool
pip install -e .
project-config  # setup your configurations

# Daily usage
cd ~/projects
projectinit cool-app-finalfinalfinal --description "The coolest app of them all"
cd cool-app-finalfinalfinal
# Now start coding!
```

---

## Contributing

**Since this is an open source project**
Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

---


## Author

### **Kevo**
- GitHub: [@kevo-1](https://github.com/kevo-1)

---

## Contributors

---

**Made with ❤️ to save your time**