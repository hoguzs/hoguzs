"""Her gün ve gece/gündüz geçişinde oda görselini (tarih, aktivite) yeniler."""
import datetime
import os
from pathlib import Path

import room

ROOT = Path(__file__).resolve().parents[2]
ROOM = ROOT / "assets" / "oda.svg"
TR = datetime.timezone(datetime.timedelta(hours=3))


def main():
    now = datetime.datetime.now(TR)
    if os.environ.get("TODAY"):
        now = datetime.datetime.fromisoformat(os.environ["TODAY"]).replace(tzinfo=TR)
    night = now.hour >= 19 or now.hour < 7
    if os.environ.get("PHASE"):
        night = os.environ["PHASE"] == "night"
    day = now.date().toordinal()

    variant = room.VARIANTS[day % len(room.VARIANTS)]
    ROOM.parent.mkdir(exist_ok=True)
    ROOM.write_text(room.build(now.date(), night, variant))
    print(f"{now:%Y-%m-%d %H:%M} gece={night} aktivite={variant}")


if __name__ == "__main__":
    main()
