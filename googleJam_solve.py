def read(n, fin):
    yield n
    for line in fin:
        yield map(int, line.strip().split())


def solve(path, outpath):
    fin = open(path)
    fout = open(outpath, 'w')
    T = int(fin.readline().strip())
    t = 0
    for key, group in groupby(fin, lambda line:len(line.strip().split())):
        if key == 1:
            n = int(group.next().strip())
        else:
            input = read(n, group)
            vs = load(input)
            t += 1
            mincut.cache.clear()
            print >>fout, "Case #%d:" % t, mincut_all(vs)
    fout.flush()
    fout.close()
