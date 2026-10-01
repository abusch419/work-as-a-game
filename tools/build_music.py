import re, json, sys
P = sys.argv[1]
NOTES = {"C_":0,"C#":1,"D_":2,"D#":3,"E_":4,"F_":5,"F#":6,"G_":7,"G#":8,"A_":9,"A#":10,"B_":11}
def compile_song(fname):
    lines = open(f"{P}/{fname}.asm").read().splitlines()
    prog, labels, chans, glob = [], {}, {}, None
    for ln in lines:
        ln = ln.split(";")[0].rstrip()
        if not ln.strip(): continue
        m = re.match(r"^(\S+?):+$", ln.strip())
        if m and not ln[0].isspace():
            name = m.group(1)
            if name.startswith("."): name = glob + name
            else:
                glob = name
                c = re.search(r"_Ch(\d)$", name)
                if c: chans[int(c.group(1))] = len(prog)
            labels[name] = len(prog); continue
        parts = ln.strip().split(None, 1)
        args = [a.strip() for a in parts[1].split(",")] if len(parts) > 1 else []
        args = [glob + a if a.startswith(".") else a for a in args]
        prog.append((parts[0], args))
    tempo = 256; out = {}
    for ch in (1, 2, 3):
        if ch not in chans: continue
        pc, speed, octv, stack, counters, ev, t, loopT = chans[ch], 12, 4, [], {}, [], 0.0, None
        loopIdx = None; steps = 0
        while steps < 20000:
            steps += 1
            if pc >= len(prog): break
            op, a = prog[pc]; pc += 1
            if op == "tempo": tempo = int(a[0])
            elif op == "note_type": speed = int(a[0])
            elif op == "octave": octv = int(a[0])
            elif op in ("note", "rest"):
                n = int(a[-1]); dur = n * speed * tempo / 256 / 59.7
                if op == "note": midi = 12 * (octv + 2) + NOTES[a[0]]   # octave 4 C ~ C6? tuned below
                else: midi = None
                ev.append([midi, round(dur, 4)]); t += dur
            elif op == "sound_call": stack.append(pc); pc = labels[a[0]]
            elif op == "sound_ret":
                if not stack: break
                pc = stack.pop()
            elif op == "sound_loop":
                cnt, lab = int(a[0]), labels[a[1]]
                if cnt == 0:
                    # loop start = index of first event produced at/after label: find by replay marker
                    loopIdx = lab; break
                k = pc - 1; counters[k] = counters.get(k, 0) + 1
                if counters[k] < cnt: pc = lab
                else: counters[k] = 0
        # find loop start event index: re-run marking events count when pc first reaches loopIdx
        out[ch] = {"ev": ev, "loopPc": loopIdx}
    return out, prog, chans, labels

def loop_event_index(fname):
    # second pass that records event count when program counter hits the loop label (first time, outside calls)
    lines_out, prog, chans, labels = compile_song(fname)
    res = {}
    for ch, d in lines_out.items():
        if d["loopPc"] is None: res[ch] = {"ev": d["ev"], "loop": None}; continue
        pc, stack, counters, n, hit = chans[ch], [], {}, 0, None; steps = 0
        while steps < 20000:
            steps += 1
            if pc == d["loopPc"] and hit is None and not stack: hit = n
            op, a = prog[pc]; pc += 1
            if op in ("note", "rest"): n += 1
            elif op == "sound_call": stack.append(pc); pc = labels[a[0]]
            elif op == "sound_ret": pc = stack.pop()
            elif op == "sound_loop":
                cnt, lab = int(a[0]), labels[a[1]]
                if cnt == 0: break
                k = pc - 1; counters[k] = counters.get(k, 0) + 1
                if counters[k] < cnt: pc = lab
                else: counters[k] = 0
        res[ch] = {"ev": d["ev"], "loop": hit if hit is not None else 0}
    return res

songs = {}
for key, f in [("title","titlescreen"),("route","routes1"),("battle","wildbattle"),("boss","gymleaderbattle"),("victory","defeatedwildmon")]:
    songs[key] = {str(k): v for k, v in loop_event_index(f).items()}
    print(key, {k: (len(v["ev"]), v["loop"], round(sum(e[1] for e in v["ev"]),1)) for k, v in songs[key].items()}, file=sys.stderr)
print("const SONGS=" + json.dumps(songs, separators=(",", ":")) + ";")
