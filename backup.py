import argparse, os, git, sys, time, threading
from git.repo import Repo

HOME = '/home/medik/'
CONFIGS = ['.apps', '.bashrc', '.xinitrc', '.config/bspwm/', '.config/sxhkd/', '.config/nvim/', '.config/polybar/', '.config/alacritty/']


def run(name, event):
    sys.stdout.write(f'{name}: Backup   ')
    sys.stdout.flush()
    while not event.is_set():
        time.sleep(0.5)
        sys.stdout.write(f'\r{name}: Backup.  ')
        sys.stdout.flush()
        time.sleep(0.5)
        sys.stdout.write(f'\r{name}: Backup.. ')
        sys.stdout.flush()
        time.sleep(0.5)
        sys.stdout.write(f'\r{name}: Backup...')
        sys.stdout.flush()
        time.sleep(0.5)
        sys.stdout.write(f'\r{name}: Backup   ')
        sys.stdout.flush()

def push(path, name, commit=None, dirs=None):
    try:
        repo = Repo(HOME + path)
        if repo.is_dirty():
            event = threading.Event()
            running =  threading.Thread(target=run, args=(name, event))
            running.start()
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
            running.join()
            print(f'\r{name}: Backup completed')
        else:
            print(f"{name}: Nothing to commit")
    except git.InvalidGitRepositoryError:
        print(f'{name}: This folder has no git repository: {HOME + path}')
    except git.NoSuchPathError:
        print(f'{name}: Folder not found: {HOME + path}')
    except git.GitCommandError as e:
        print(f"{name}: Error\n{e}")


parser = argparse.ArgumentParser(description='System backup script')
parser.add_argument('-t', default='system', help='Specify what to backup')
parser.add_argument('-s', help='Specify settings for the task')
parser.add_argument('-c', default='commit', help='Commit name')
args = parser.parse_args()


if args.t == 'system':
    push('/', 'Configs', dirs=CONFIGS)
    push('run/', 'Scripts')
    push('nts/', 'Notes')
    print('System backup completed')

elif args.t == 'projects': 
    if args.s: push(f'prj/{args.s}', args.s, args.c)
    else:
        for i in os.scandir(HOME + 'prj/'):
            if i.is_dir():
                push(f'prj/{i.name}', i.name, i.name)
        print('Projects backup completed')

elif args.t == 'configs': push('/', 'Configs', dirs=CONFIGS)
elif args.t == 'scripts': push('run/', 'Scripts')
elif args.t == 'notes': push('nts/', 'Notes')
else: print(f'Error, no such task: {args.t}')
