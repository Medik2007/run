import subprocess, argparse, os, tqdm, git
from git.repo import Repo

HOME = '/home/medik/'

def push(path, name, commit=None):
    try:
        repo = Repo(HOME + path)
        if repo.is_dirty():
            if commit == None: commit = name
            repo.git.add(update=True)
            repo.index.commit(commit)
            repo.git.branch("--set-upstream-to=origin/master", "master")
            origin = repo.remote(name='origin')
            origin.push()
            print(f"{name}: backup completed")
        else:
            print(f"{name}: nothing to commit")
    except git.GitCommandError as e:
        print(f"{name}: backup error\n{e}")




def configs():
    dirs = ['.apps', '.bashrc', '.xinitrc', '.config/bspwm/', '.config/sxhkd/', '.config/nvim/', '.config/polybar/', '.config/alacritty/']
    os.chdir(os.path.expanduser('~/'))
    for i in dirs:
        subprocess.call(['git', 'add', i])
    subprocess.call(['git', 'commit', '-m', 'configs'])
    subprocess.call(['git', 'push', 'origin', 'master'])
    print('Configs backup completed')

def scripts():
    push('run/', 'Scripts')

def notes():
    push('nts/', 'Notes')

def projects(name, commit):
    if name:
        os.chdir(os.path.expanduser(f'~/prj/{name}'))
        subprocess.call(['git', 'add', '.'])
        subprocess.call(['git', 'commit', '-m', commit])
        subprocess.call(['git', 'push', 'origin', 'master'])
        print(f'{name} project backup completed')
    else:
        print('Enter a valid project name')

parser = argparse.ArgumentParser(description='System backup script')
parser.add_argument('-t', default='system', help='Specify what to backup')
parser.add_argument('-s', help='Specify settings for the task')
parser.add_argument('-c', default='commit', help='Commit name')
args = parser.parse_args()

if args.t == 'system':
    configs()
    scripts()
    notes()
    print('Full system backup completed')
elif args.t == 'projects': projects(args.s, args.c)
elif args.t == 'configs': configs()
elif args.t == 'scripts': scripts()
elif args.t == 'notes': notes()
else: print(f'Error, no such task: {args.t}')
