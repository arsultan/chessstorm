import chess, chess.engine, chess.pgn, json, sys, os
eng = chess.engine.SimpleEngine.popen_uci('/usr/games/stockfish')
eng.configure({'Threads': 2, 'Hash': 256})
SRC, OUT, PRIOR = sys.argv[1], sys.argv[2], sys.argv[3]
T = 2.5
TR = 2.0
prior = {r['n']: r for r in json.load(open(PRIOR))} if os.path.exists(PRIOR) else {}


def sc(s, turn):
    p = s.pov(turn)
    if p.is_mate():
        m = p.mate()
        return 100000 - abs(m) * 100 if m > 0 else -100000 + abs(m) * 100
    return p.score()


def unique(info, turn):
    if len(info) < 2:
        return True
    a = sc(info[0]['score'], turn); c = sc(info[1]['score'], turn)
    if a >= 90000:
        return c < 90000 or c <= a - 300
    if c >= 500:
        return a - c >= 400
    return a - c >= 150


VAL = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9}


def material(b, side):
    s = 0
    for sq, p in b.piece_map().items():
        v = VAL.get(p.piece_type, 0)
        s += v if p.color == side else -v
    return s


def acceptable(best, alt):
    if best >= 90000:
        return alt >= 90000
    if alt >= best - 100:
        return True
    return best >= 400 and alt >= 400 and alt >= best - 250


out = json.load(open(OUT)) if os.path.exists(OUT) else []
done = {r['n'] for r in out}
f = open(SRC, encoding='utf-8', errors='replace'); i = 0
while True:
    g = chess.pgn.read_game(f)
    if g is None:
        break
    i += 1
    if i in done:
        continue
    try:
        b = g.board()
    except Exception:
        out.append({'n': i, 'ok': False, 'bad': True, 'm': []}); continue
    if b.legal_moves.count() == 0 or not b.is_valid():
        out.append({'n': i, 'ok': False, 'bad': True, 'm': []}); continue
    turn = b.turn
    pr = prior.get(i)
    if pr and not pr.get('bad') and pr['ok'] and pr.get('m'):
        ok = True; first = pr['m'][0]; ev = pr.get('ev')
    else:
        info = eng.analyse(b, chess.engine.Limit(time=8), multipv=min(3, b.legal_moves.count()))
        ev = sc(info[0]['score'], turn); fm = info[0]['pv'][0]
        gap = ev - (sc(info[1]['score'], turn) if len(info) > 1 else -99999)
        forcing0 = bool(b.is_capture(fm) or b.gives_check(fm) or fm.promotion)
        ok = bool(unique(info, turn) or (gap >= 40 and forcing0 and ev >= -50) or (os.environ.get('FORCE') and gap >= 60))
        first = fm.uci() if ok else None
    rec = {'n': i, 'fen': b.fen(), 'ok': ok, 'ev': ev, 'm': [], 'a': {}}
    if ok:
        bb = b.copy(); line = [first]; bb.push(chess.Move.from_uci(first)); alts = {}
        mat0 = material(b, turn)
        seen = {b.board_fen(), bb.board_fen()}
        maxs = 4 if (ev is not None and ev >= 90000) else 3
        k = 1
        while k < maxs and not bb.is_game_over():
            rr = eng.analyse(bb, chess.engine.Limit(time=TR), multipv=max(1, min(3, bb.legal_moves.count())))
            if not rr or not rr[0].get('pv'):
                break
            rep = rr[0]['pv'][0]
            bb2 = bb.copy(); bb2.push(rep)
            if bb2.is_game_over():
                break
            info = eng.analyse(bb2, chess.engine.Limit(time=T), multipv=max(1, min(5, bb2.legal_moves.count())))
            best = sc(info[0]['score'], turn)
            floor = min(150, (ev if ev is not None else 150) - 100)
            if best < floor:
                info = eng.analyse(bb2, chess.engine.Limit(time=T * 3), multipv=max(1, min(5, bb2.legal_moves.count())))
                best = sc(info[0]['score'], turn)
            cands = []
            for x in info:
                mv = x['pv'][0]; t = bb2.copy(); t.push(mv)
                if t.board_fen() in seen:
                    continue
                cands.append((x, mv))
            if not cands:
                break
            bx, bm = cands[0]
            best = sc(bx['score'], turn)
            # prefer a natural forcing move (capture/check/promotion) if it is almost as strong
            for x, mv in cands:
                v = sc(x['score'], turn)
                nat = bb2.is_capture(mv) or bb2.gives_check(mv) or mv.promotion
                if nat and ((best >= 90000 and v >= 90000 and v >= best - 100) or (best < 90000 and v >= best - 60)):
                    bx, bm = x, mv
                    break
            if best < floor:
                break
            forcing = bb2.is_capture(bm) or bb2.gives_check(bm) or bm.promotion or best >= 90000
            gained = material(bb2, turn) - mat0
            # stop only when the combination is over: next move is quiet and material already won
            if not forcing and gained >= 2:
                break
            acc = sorted({mv.uci()[:4] for x, mv in cands[1:] if acceptable(best, sc(x['score'], turn))} - {bm.uci()[:4]})
            line += [rep.uci(), bm.uci()]
            if acc:
                alts[str(len(line) - 1)] = acc
            bb = bb2; bb.push(bm); seen.add(bb2.board_fen()); seen.add(bb.board_fen()); k += 1
        rec['m'] = line; rec['a'] = alts
    out.append(rec)
    print(i, ok, ev, ' '.join(rec['m']), rec['a'], flush=True)
    json.dump(out, open(OUT, 'w'))
eng.quit()
