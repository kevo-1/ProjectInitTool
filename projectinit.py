import argparse
import os
import sys
import subprocess
import json
from pathlib import Path
try:
    import requests
except ImportError:
    print("Error: 'requests' library is required.\n" \
            "Install it with: pip install requests")
    sys.exit(1)

CONFIG_FILE = Path.home() / ".github_repo_creator.json"


def loadConfig():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}


def saveConfig(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"Configuration saved to {CONFIG_FILE}")


def configure():
    print("Project Init Configuration\n")
    
    config = loadConfig()
    
    print("Enter your GitHub Personal Access Token")
    print("(Leave blank to keep current value)")
    token = input(f"Token [{config.get('token', 'Not set')[:10]}...]: ").strip()
    if token:
        config['token'] = token
    
    print("\nEnter default base directory for repositories")
    print("(Leave blank to keep current value)")
    default_dir = config.get('base_directory', str(Path.home() / 'projects'))
    base_dir = input(f"Base directory [{default_dir}]: ").strip()
    if base_dir:
        config['base_directory'] = base_dir
    elif 'base_directory' not in config:
        config['base_directory'] = default_dir
    
    print("\nDefault repository visibility")
    print("(Leave blank to keep current value)")
    current_private = config.get('private', False)
    private = input(f"Make repos private by default? (yes/no) [{current_private}]: ").strip().lower()
    if private in ['yes', 'y', 'true']:
        config['private'] = True
    elif private in ['no', 'n', 'false']:
        config['private'] = False
    
    saveConfig(config)
    print("\n✓ Configuration updated successfully!")
    print(f"\nCurrent settings:")
    print(f"  Token: {'Set' if config.get('token') else 'Not set'}")
    print(f"  Base directory: {config.get('base_directory')}")
    print(f"  Private by default: {config.get('private', False)}")


def runCommand(cmd, cwd=None):
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Error: {e.stderr}")
        sys.exit(1)


def createGithubRepo(token, repo_name, description="", private=False):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "name": repo_name,
        "description": description,
        "private": private
    }
    
    response = requests.post(
        "https://api.github.com/user/repos",
        headers=headers,
        json=data
    )
    
    if response.status_code == 201:
        repo_data = response.json()
        return repo_data["clone_url"], repo_data["html_url"]
    else:
        print(f"Error creating GitHub repository: {response.status_code}")
        print(response.json())
        sys.exit(1)


def setupLocalRepo(base_dir, repo_name, remote_url):
    repo_path = Path(base_dir) / repo_name
    
    if repo_path.exists():
        print(f"Error: Local directory '{repo_path}' already exists!")
        sys.exit(1)
    
    print(f"Creating directory: {repo_path}")
    repo_path.mkdir(parents=True, exist_ok=True)
    
    print("Initializing git repository...")
    runCommand("git init", cwd=repo_path)
    
    print(f"Adding remote 'origin': {remote_url}")
    runCommand(f"git remote add origin {remote_url}", cwd=repo_path)
    
    readme_path = repo_path / "README.md"
    with open(readme_path, "w") as f:
        f.write(f"# {repo_name}\n\nInitial repository setup.\n")
    
    print("Created README.md")
    
    return repo_path


def main():
    parser = argparse.ArgumentParser(
        description="Create a GitHub repository and initialize a local git repo",
        epilog="Run 'repo-config' to set default values for token and base directory"
    )
    parser.add_argument(
        "repo_name",
        help="Name of the repository to create"
    )
    parser.add_argument(
        "-d", "--directory",
        help="Base directory where the repo folder will be created (overrides config)"
    )
    parser.add_argument(
        "-t", "--token",
        help="GitHub personal access token (overrides config and GITHUB_TOKEN env var)"
    )
    parser.add_argument(
        "--description",
        default="",
        help="Repository description"
    )
    parser.add_argument(
        "-p", "--private",
        action="store_true",
        help="Make the repository private (overrides config default)"
    )
    parser.add_argument(
        "--public",
        action="store_true",
        help="Make the repository public (overrides config default)"
    )
    
    args = parser.parse_args()
    
    config = loadConfig()
    
    # (priority: arg > env > config)
    token = args.token or os.environ.get("GITHUB_TOKEN") or config.get('token')
    if not token:
        print("Error: GitHub token required.")
        print("Set it by running: repo-config")
        print("Or provide via -t/--token or GITHUB_TOKEN environment variable")
        sys.exit(1)
    
    # (priority: arg > config > current dir)
    base_dir = args.directory or config.get('base_directory', '.')
    
    # (priority: explicit flags > config > false)
    if args.public:
        private = False
    elif args.private:
        private = True
    else:
        private = config.get('private', False)
    
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: git is not installed or not in PATH")
        sys.exit(1)
    
    print(f"Creating GitHub repository: {args.repo_name}")
    print(f"Base directory: {base_dir}")
    print(f"Visibility: {'Private' if private else 'Public'}")
    
    clone_url, html_url = createGithubRepo(
        token,
        args.repo_name,
        args.description,
        private
    )
    print(f"Repository created: {html_url}")
    
    repo_path = setupLocalRepo(base_dir, args.repo_name, clone_url)
    
    print(f"\n✓ Successfully created repository!")
    print(f"  Local path: {repo_path}")
    print(f"  Remote URL: {html_url}")
    print(f"\nNext steps:")
    print(f"  cd {repo_path}")
    print(f"  git add .")
    print(f"  git commit -m 'Initial commit'")
    print(f"  git push -u origin main")


if __name__ == "__main__":
    main()