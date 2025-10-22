import argparse, pathlib, sys

def main():
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("args", nargs="*")
    p.add_argument("--in", dest="in_", action="append") 
    p.add_argument("--out")
    args, _ = p.parse_known_args()

    paths = []
    if args.in_:
        paths += args.in_
    paths += [a for a in args.args if not a.startswith("-")]

    ok = True
    for s in paths:
        pth = pathlib.Path(s)
        if not pth.exists():
            print(f"[rollup] warn: path not found: {pth}", file=sys.stderr)
        else:
            print(f"[rollup] using: {pth}")

    print("[rollup] shim: done")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
