import subprocess, argparse, os

def configs():
    dirs = ['r/', '.apps', '.bashrc', '.xinitrc', '.config/bspwm/', '.config/sxhkd/', '.config/nvim/', '.config/polybar/', '.config/alacritty/']
    os.chdir(os.path.expanduser('~/'))
    for i in dirs:
        subprocess.call(['git', 'add', i])
    subprocess.call(['git', 'commit', '-m', 'configs'])
    subprocess.call(['git', 'push', 'origin', 'master'])
    print('Configs backup completed')

def scripts():
    os.chdir(os.path.expanduser('~/run/'))
    subprocess.call(['git', 'add', '.'])
    subprocess.call(['git', 'commit', '-m', 'scripts'])
    subprocess.call(['git', 'push', 'origin', 'master'])
    print('Scripts backup completed')

def notes():
    os.chdir(os.path.expanduser('~/nts/'))
    subprocess.call(['git', 'add', '.'])
    subprocess.call(['git', 'commit', '-m', 'notes'])
    subprocess.call(['git', 'push', 'origin', 'master'])
    print('Notes backup completed')

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
parser.add_argument('-p', help='If the task is to backup a project, specify wich one')
parser.add_argument('-c', default='commit', help='Commit name')
args = parser.parse_args()

if args.t == 'system':
    configs()
    scripts()
    notes()
    print('Full system backup completed')
elif args.t == 'projects': projects(args.p, args.c)
elif args.t == 'configs': configs()
elif args.t == 'scripts': scripts()
elif args.t == 'notes': notes()
else: print(f'Error, no such task: {args.t}')
