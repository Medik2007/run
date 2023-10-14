import subprocess, argparse, time

parser = argparse.ArgumentParser(description='Script that automates opening projects')
parser.add_argument('-o', help='Which project to open')
parser.add_argument('-s', help='Specify settings for project opening')
args = parser.parse_args()

def run(command):
    subprocess.Popen(command, shell=True).wait()

s = int(args.s)
if args.o == 'yp':
    if s == None: s = 1

    run((
        'alacritty -e /bin/bash -c "'
        f'bspc node -d ^{s+2} && '
        'cd ~/prj/yp && '
        'source bin/activate && '
        'cd youngplanet && '
        'python manage.py runserver && '
        '/bin/bash" &'
    ))

    run("firefox http://127.0.0.1:8000 https://chat.geekgpt.org/ &")
    time.sleep(1)
    run(f"bspc node -d ^{s+1} &")

    run((
        'cd ~/prj/yp && '
        'source bin/activate && '
        'cd youngplanet && '
        'nvim'
    ))

else:
    print(f"No such project opening script: {args.o}")
