import subprocess, argparse, os

def configs():
    os.chdir('~/.config/')
    subprocess.call(['git', 'add', '.'])
    subprocess.call(['git', 'commit', '-m', 'notes'])
    subprocess.call(['git', 'push', 'origin', 'master'])
    print('Configs backup completed')
def scripts():
    os.chdir(os.path.expanduser('~/run/'))
    subprocess.call(['git', 'add', '.'])
    subprocess.call(['git', 'commit', '-m', 'notes'])
    subprocess.call(['git', 'push', 'origin', 'master'])
    print('Scripts backup completed')
def notes():
    os.chdir(os.path.expanduser('~/nts/'))
    subprocess.call(['git', 'add', '.'])
    subprocess.call(['git', 'commit', '-m', 'notes'])
    subprocess.call(['git', 'push', 'origin', 'master'])
    print('Notes backup completed')
def projects(name):
    if name:
        pass

parser = argparse.ArgumentParser(description='System backup script')
parser.add_argument('-t', default='system', help='Specify what to backup')
parser.add_argument('-p', help='If the task is to backup a project, specify wich one')
args = parser.parse_args()

if args.t == 'system':
    configs()
    scripts()
    notes()
elif args.t == 'project': projects(args.p)
elif args.t == 'configs': configs()
elif args.t == 'scripts': scripts()
elif args.t == 'notes': notes()
else: print(f'Error, no such task: {args.t}')
