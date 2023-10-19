import subprocess, argparse, os, git, sys, time, threading
from git.repo import Repo

HOME = '/home/medik/'


def run(name, event):
    sys.stdout.write(f'{name}: backup...')
    sys.stdout.flush()
    while not event.is_set():
        sys.stdout.write(f'\r{name}: backup.. ')
        sys.stdout.flush()
        time.sleep(0.5)
        sys.stdout.write(f'\r{name}: backup.  ')
        sys.stdout.flush()
        time.sleep(0.5)
        sys.stdout.write(f'\r{name}: backup   ')
        sys.stdout.flush()
        time.sleep(0.5)
        sys.stdout.write(f'\r{name}: backup...')
        sys.stdout.flush()
    sys.stdout.write(f'\r{name}: backup completed')
    sys.stdout.flush()

def push(path, name, commit=None, dirs=None):
    try:
        repo = Repo(HOME + path)
        if repo.is_dirty():
            event = threading.Event()
            threading.Thread(target=run, args=(name, event)).start()
            if commit == None: commit = name
            if dirs == None:
                repo.git.add(update=True)
            else:
                for i in dirs:
                    repo.git.add()
            repo.index.commit(commit)
            repo.git.branch("--set-upstream-to=origin/master", "master")
            origin = repo.remote(name='origin')
            origin.push()
            event.set()
        else:
            print(f"{name}: nothing to commit")
            event = threading.Event()
            threading.Thread(target=run, args=(name, event)).start()
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
    if name: push(f'prj/{name}', name, commit)
    else: print('Enter a valid project name')

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
