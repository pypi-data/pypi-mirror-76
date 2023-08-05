from postal.core.utils import shell


help = "Rebuild and restart stack"

def arguments(parser):
    pass

def main(args):
    shell(f'docker-compose -p {args.stack} -f {args.compose} down --remove-orphans')
    shell(f'docker-compose -p {args.stack} -f {args.compose} build')
    shell(f'docker-compose -p {args.stack} -f {args.compose} up -d --force-recreate')
