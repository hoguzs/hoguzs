"""Her gün README'deki yazılımcı şakasını değiştirir."""
import datetime
import re
from pathlib import Path

README = Path(__file__).resolve().parents[2] / "README.md"

JOKES = [
    "Kod çalışıyor ama neden çalıştığını bilmiyorum. Sakın dokunma.",
    "Yazılımcıya \"Sorun ne?\" diye sorma. \"Bende çalışıyor\" der.",
    "Hata ayıklamak, katilin sen olduğun bir cinayet filminde dedektiflik yapmaktır.",
    "Bilgisayar biliminde iki zor şey vardır: önbelleği temizlemek, değişkene isim bulmak ve bir de sıfırdan başlayarak saymak.",
    "\"5 dakikalık iş\" diyen yazılımcı, 3 günlük işe başlamıştır.",
    "Commit mesajım: \"son-son-gerçekten-son-v2-düzeltildi\".",
    "Yorum satırı: Bunu yazdığımda bir tek ben ve Tanrı ne yaptığımı biliyorduk. Şimdi sadece Tanrı biliyor.",
    "Gece 3'te canlı sisteme dokunma. Ciddiyim.",
    "Hata değil, özellik.",
    "\"Bir de şunu ekler misin?\" yazılım tarihinin en tehlikeli cümlesidir.",
    "Kahvesiz kod yazılmaz. Kodsuz kahve içilir, ama tadı yok.",
    "Testler yeşil yandıysa ya her şey doğrudur ya da testi yazan çok iyimserdir.",
    "Windows'ta çalışıyor, Mac'te çalışıyor, canlıda çalışmıyor. Üçü de aynı kod.",
    "Sonsuz döngü: Kahve bitti, kod bitmedi, kahve yap, kahve bitti...",
]


def main():
    idx = datetime.date.today().toordinal() % len(JOKES)
    block = (
        "<!-- JOKE:START -->\n"
        f"> 😄 {JOKES[idx]}\n"
        "<!-- JOKE:END -->"
    )
    src = README.read_text()
    new = re.sub(r"<!-- JOKE:START -->.*?<!-- JOKE:END -->", lambda _m: block, src, flags=re.S)
    README.write_text(new)


if __name__ == "__main__":
    main()
