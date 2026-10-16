"""Profil README'sindeki Connect Four oyunu.

Her hamle, başlığı `c4|<sütun>` olan bir Issue ile gelir. Başlık güvenilmeyen girdidir:
yalnızca sıkı bir regex ile ayrıştırılır, hiçbir zaman çalıştırılmaz.
"""
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import quote

ROWS, COLS = 6, 7
ROOT = Path(__file__).resolve().parents[2]
STATE_FILE = ROOT / "game" / "state.json"
README = ROOT / "README.md"

EMOJI = {0: "⚪", 1: "🔴", 2: "🟡"}
NUMS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]
ORDER = sorted(range(COLS), key=lambda c: abs(c - 3))

LINES = []
for r in range(ROWS):
    for c in range(COLS):
        for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
            cells = [(r + i * dr, c + i * dc) for i in range(4)]
            if all(0 <= rr < ROWS and 0 <= cc < COLS for rr, cc in cells):
                LINES.append(cells)


def new_state(stats=None):
    return {
        "board": [[0] * COLS for _ in range(ROWS)],
        "over": False,
        "result": "",
        "last": "",
        "stats": stats or {"win": 0, "loss": 0, "draw": 0},
    }


def load():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return new_state()


def save(state):
    STATE_FILE.parent.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=1) + "\n")


def valid_cols(board):
    return [c for c in ORDER if board[0][c] == 0]


def drop(board, col, p):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == 0:
            board[r][col] = p
            return r
    return None


def undo(board, col):
    for r in range(ROWS):
        if board[r][col] != 0:
            board[r][col] = 0
            return


def has_won(board, p):
    return any(all(board[r][c] == p for r, c in line) for line in LINES)


def evaluate(board):
    score = sum(3 for r in range(ROWS) if board[r][3] == 2)
    score -= sum(3 for r in range(ROWS) if board[r][3] == 1)
    for line in LINES:
        w = [board[r][c] for r, c in line]
        for p, sign in ((2, 1), (1, -1)):
            n, e = w.count(p), w.count(0)
            if n == 3 and e == 1:
                score += sign * 6
            elif n == 2 and e == 2:
                score += sign * 2
    return score


def minimax(board, depth, alpha, beta, bot_turn):
    if has_won(board, 2):
        return 100000 + depth
    if has_won(board, 1):
        return -100000 - depth
    cols = valid_cols(board)
    if not cols:
        return 0
    if depth == 0:
        return evaluate(board)
    best = -10**9 if bot_turn else 10**9
    for c in cols:
        drop(board, c, 2 if bot_turn else 1)
        val = minimax(board, depth - 1, alpha, beta, not bot_turn)
        undo(board, c)
        if bot_turn:
            best = max(best, val)
            alpha = max(alpha, val)
        else:
            best = min(best, val)
            beta = min(beta, val)
        if alpha >= beta:
            break
    return best


def bot_move(board):
    best_col, best_val = None, -10**9
    for c in valid_cols(board):
        drop(board, c, 2)
        val = minimax(board, 4, -10**9, 10**9, False)
        undo(board, c)
        if val > best_val:
            best_col, best_val = c, val
    return best_col


def render(state, repo):
    board = state["board"]
    base = f"https://github.com/{repo}/issues/new"
    body = quote("Sadece Submit new issue düğmesine bas, hamleni bot oynatır. 🎮")
    head = "| " + " | ".join(
        f"[{NUMS[c]}]({base}?title={quote(f'c4|{c + 1}')}&body={body})" for c in range(COLS)
    ) + " |"
    sep = "|" + ":-:|" * COLS
    rows = ["| " + " | ".join(EMOJI[v] for v in row) + " |" for row in board]

    if state["over"]:
        status = {
            "win": "🎉 Son oyunu bir ziyaretçi kazandı! Yeni oyun için bir sütuna tıkla.",
            "loss": "🤖 Son oyunu ben kazandım! Rövanş için bir sütuna tıkla.",
            "draw": "🤝 Son oyun berabere bitti. Yeni oyun için bir sütuna tıkla.",
        }[state["result"]]
    else:
        status = "🎮 **Sıra sende!** Bir sütun seç. 🔴 sensin, 🟡 benim."
    s = state["stats"]
    lines = [
        "<!-- C4:START -->",
        status,
        "",
        head,
        sep,
        *rows,
        "",
        f"📊 **Skor:** Ziyaretçiler **{s['win']}** · Ben **{s['loss']}** · Berabere **{s['draw']}**",
    ]
    if state["last"]:
        lines.append(f"🕹️ **Son hamle:** [{state['last']}](https://github.com/{state['last']})")
    lines.append("<!-- C4:END -->")
    text = "\n".join(lines)
    src = README.read_text()
    new = re.sub(r"<!-- C4:START -->.*?<!-- C4:END -->", lambda _m: text, src, flags=re.S)
    README.write_text(new)


def reply(text):
    path = os.environ.get("REPLY_FILE")
    if path:
        Path(path).write_text(text)
    print(text)


def main():
    repo = os.environ.get("REPO", "hoguzs/hoguzs")
    state = load()

    if "--render" in sys.argv:
        render(state, repo)
        return

    m = re.fullmatch(r"c4\|([1-7])", os.environ.get("TITLE", "").strip())
    if not m:
        reply("Bu başlığı anlayamadım. Hamle için README'deki sütun numaralarına tıkla. 🙂")
        return
    col = int(m.group(1)) - 1
    actor = os.environ.get("ACTOR", "")
    if not re.fullmatch(r"[A-Za-z0-9-]{1,39}", actor):
        actor = ""

    if state["over"]:
        state = new_state(state["stats"])
    board = state["board"]

    if board[0][col] != 0:
        reply(f"⚠️ {col + 1}. sütun dolu, başka bir sütun seçip tekrar dene.")
        return

    drop(board, col, 1)
    state["last"] = actor or state["last"]
    stats = state["stats"]

    if has_won(board, 1):
        state.update(over=True, result="win")
        stats["win"] += 1
        msg = f"🎉 {col + 1}. sütuna attığın taşla dörtlüyü tamamladın, **kazandın**! Tebrikler. Yeni oyun için README'den bir sütuna tıkla."
    elif not valid_cols(board):
        state.update(over=True, result="draw")
        stats["draw"] += 1
        msg = "🤝 Tahta doldu, oyun **berabere** bitti. Yeni oyun için README'den bir sütuna tıkla."
    else:
        bc = bot_move(board)
        drop(board, bc, 2)
        if has_won(board, 2):
            state.update(over=True, result="loss")
            stats["loss"] += 1
            msg = f"🤖 Hamleni {col + 1}. sütuna attın, ben {bc + 1}. sütuna attım ve dörtlüyü tamamladım. Bu oyunu **ben kazandım**! Rövanş için README'den bir sütuna tıkla."
        elif not valid_cols(board):
            state.update(over=True, result="draw")
            stats["draw"] += 1
            msg = "🤝 Tahta doldu, oyun **berabere** bitti. Yeni oyun için README'den bir sütuna tıkla."
        else:
            msg = f"🔴 Hamleni {col + 1}. sütuna attın, 🟡 ben {bc + 1}. sütuna attım. Sıra yine sende! README'deki tahtaya bak."

    save(state)
    render(state, repo)
    reply(msg)


if __name__ == "__main__":
    main()
