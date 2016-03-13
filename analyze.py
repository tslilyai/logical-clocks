import glob

def frange(s, e, i=1):
    c = s
    while (i > 0 and c < e) or (i < 0 and c > e):
        yield c
        c += i

for f in glob.glob('logs/1-events-*.log'):
    norm_fname = f.split('.')[0].split('/')[1]
    parts = norm_fname.split('-')

    trial_num = parts[2].split(':')[0]
    num_events = parts[2].split(':')[1]

    logfilenames = ['logs/%d-events-%s.log' % (0, parts[2]), 'logs/%d-events-%s.log' % (1, parts[2]), 'logs/%d-events-%s.log' % (2, parts[2])]
    logs = []

    start_time = 1e60
    end_time = 0.0
    for fname in logfilenames:
        logs.append([])
        with open(fname) as f:
            first = True
            for line in f:
                if first:
                    first = False
                    continue
                line = line.strip()
                if line:
                    parts = line.split(': ')
                    gtime = float(parts[2].split('\t')[0])
                    start_time = min(start_time, gtime)
                    end_time = max(end_time, gtime)
                    lc = int(parts[-1])
                    logs[-1].append((gtime, lc))

    start_time = int(start_time * 10) / 10.0
    end_time = int(end_time * 10) / 10.0

    current_indices = [0 for _ in logs]
    drifts = []
    for gtime in frange(start_time, end_time, 0.1):
        records = [None for _ in logs]
        for i, log in enumerate(logs):
            j = 0
            for j in range(current_indices[i], len(log)):
                if log[j][0] > gtime:
                    break
                records[i] = log[j]
            current_indices[i] = j

        if all(records):
            lcs = [record[1] for record in records]
            drifts.append(max(lcs)-min(lcs))

    print 'Trial %s, %s events' % (trial_num, num_events)
    print 'Drifts:', drifts
    print 'Means:', sum(drifts)/float(len(drifts))
