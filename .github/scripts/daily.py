"""Her gün (ve gece/gündüz geçişinde) README ile oda görselini yeniler."""
import datetime
import os
import re
from pathlib import Path

import content
import room

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
ROOM = ROOT / "assets" / "oda.svg"
TR = datetime.timezone(datetime.timedelta(hours=3))


def replace_block(src, name, body):
    block = f"<!-- {name}:START -->\n{body}\n<!-- {name}:END -->"
    return re.sub(rf"<!-- {name}:START -->.*?<!-- {name}:END -->", lambda _m: block, src, flags=re.S)


def main():
    now = datetime.datetime.now(TR)
    if os.environ.get("TODAY"):
        now = datetime.datetime.fromisoformat(os.environ["TODAY"]).replace(tzinfo=TR)
    night = now.hour >= 19 or now.hour < 7
    if os.environ.get("PHASE"):
        night = os.environ["PHASE"] == "night"
    day = now.date().toordinal()

    poet, lines = content.POEMS[day % len(content.POEMS)]
    poem = f"*{poet}*\n\n" + "<br>\n".join(lines)
    saying, meaning = content.SAYINGS[(day * 7) % len(content.SAYINGS)]
    quote = f"> 💬 **{saying}**\n>\n> <sub>Atasözü · {meaning}</sub>"

    src = README.read_text()
    src = replace_block(src, "POEM", poem)
    src = replace_block(src, "QUOTE", quote)
    README.write_text(src)

    variant = room.VARIANTS[day % len(room.VARIANTS)]
    ROOM.parent.mkdir(exist_ok=True)
    ROOM.write_text(room.build(now.date(), night, variant))
    print(f"{now:%Y-%m-%d %H:%M} gece={night} aktivite={variant} şiir={poet}")


if __name__ == "__main__":
    main()
