from subprocess import run, PIPE


def command(cmd):
    return run(cmd, shell=True, stdout=PIPE, text=True).stdout.rstrip()
