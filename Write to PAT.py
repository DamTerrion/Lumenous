def write_pat (pat_file, stack):
    for line in stack:
        X = 'X'+str(round(line.x * 1000))
        Y = 'Y'+str(round(line.y * 1000))
        H = 'H'+str(round(line.height * 1000))
        W = 'W'+str(round(line.width * 1000))
        A = 'A'+str(round(line.a * 10))
        pat_file.write(X+Y+H+W+A+';\n')
    pat_file.write("$;")
