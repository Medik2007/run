import subprocess, argparse, time

parser = argparse.ArgumentParser(description='Script that automates opening projects')
parser.add_argument('-t', help='Set a task (Which project to open)')
parser.add_argument('-s', help='Specify settings for project opening')
args = parser.parse_args()

def run(command): subprocess.Popen(command, shell=True).wait()

if args.t == 'yp':
    s = int(subprocess.Popen(['bspc','query','-D','-d','--names'], stdout=subprocess.PIPE ).communicate()[0])
    if args.s != None: s = int(args.s)

    run((
        'alacritty -e /bin/bash -c "'
        f'bspc node -d {s+2} &'
        'cd ~/prj/yp &&'
        'source bin/activate &&'
        'cd youngplanet &&'
        'python manage.py runserver &&'
        '/bin/bash" &'
    ))

    run("firefox http://127.0.0.1:8000 https://gpt-chatbot.ru/chat-gpt-ot-openai-dlya-generacii-teksta &")
    time.sleep(1)
    run(f"bspc node -d {s+1} &")

    run((
        'cd ~/prj/yp && '
        'source bin/activate && '
        'cd youngplanet && '
        'nvim'
    ))

elif args.t == 'rpi':
    s = int(subprocess.Popen(['bspc','query','-D','-d','--names'], stdout=subprocess.PIPE ).communicate()[0])
    if args.s != None: s = int(args.s)
    run('feh ~/prj/lil/rpi4.jpg &')
    time.sleep(1)
    run(f"bspc node -d {s+1} &")
    run('openscad ~/prj/lil/parts/main.scad &')
    run('nvim ~/prj/lil/parts/main.scad')

else:
    print(f"Error: No such project opening script: {args.t}")
