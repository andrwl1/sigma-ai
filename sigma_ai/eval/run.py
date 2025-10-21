import os, sys, argparse, pathlib
from sigma_ai.cli import main as cli_main

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--tests', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--max-examples', type=int, default=None)
    p.add_argument('--judge', default=None)
    a = p.parse_args()

    out_dir = str(pathlib.Path(a.out).parent)
    provider = os.getenv('SIGMA_PROVIDER', 'openai')
    model = os.getenv('SIGMA_MODEL', '')

    argv = ['sigma', a.tests, provider]
    if model:
        argv.append(model)
    if a.max_examples is not None:
        argv += ['--max-examples', str(a.max_examples)]
    if a.judge:
        argv += ['--judge', a.judge]
    argv += ['--out-dir', out_dir]

    sys.argv = argv
    cli_main()

if __name__ == '__main__':
    main()
