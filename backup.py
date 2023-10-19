import subprocess, argparse, os, git, sys, time, threading
from git.repo import Repo

HOME = '/home/medik/'
CONFIGS = ['.apps', '.bashrc', '.xinitrc', '.config/bspwm/', '.config/sxhkd/', '.config/nvim/', '.config/polybar/', '.config/alacritty/']


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
        time.sleep(0.5)

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
                    repo.git.add(i)
            repo.index.commit(commit)
            repo.git.branch("--set-upstream-to=origin/master", "master")
            origin = repo.remote(name='origin')
            origin.push()
            event.set()
            sys.stdout.write(f'\r{name}: backup completed')
            sys.stdout.flush()
        else:
            print(f"{name}: nothing to commit")
    except git.GitCommandError as e:
        print(f"{name}: backup error\n{e}")

parser = argparse.ArgumentParser(description='System backup script')
parser.add_argument('-t', default='system', help='Specify what to backup')
parser.add_argument('-s', help='Specify settings for the task')
parser.add_argument('-c', default='commit', help='Commit name')
args = parser.parse_args()

if args.t == 'system':
    push('/', 'Configs', dirs=CONFIGS)
    push('run/', 'Scripts')
    push('nts/', 'Notes')
    print('Full system backup completed')
elif args.t == 'projects': 
    if args.s: push(f'prj/{args.s}', args.s, args.c)
    else: print('Enter a valid project name')
elif args.t == 'configs': push('/', 'Configs', dirs=CONFIGS)
elif args.t == 'scripts': push('run/', 'Scripts')
elif args.t == 'notes': push('nts/', 'Notes')
else: print(f'Error, no such task: {args.t}')
