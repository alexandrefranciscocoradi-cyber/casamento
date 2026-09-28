#!/usr/bin/env python3
"""Gera o payload Pix (copia e cola) e o QR Code para o site."""

from pathlib import Path

try:
    import qrcode
except ImportError:
    raise SystemExit("qrcode nao instalado: python -m pip install qrcode")

BASE = Path(__file__).resolve().parent
OUT = BASE / "assets" / "pix" / "pix.jpeg"


def crc16(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


def field(id_: str, value: str) -> str:
    size = str(len(value.encode("utf-8"))).zfill(2)
    return id_ + size + value


KEY = "5541987849665"  # chave Pix (telefone +55 (41) 98784-9665)

merchant_account = field("00", "BR.GOV.BCB.PIX") + field("01", KEY)
payload = (
    "000201"
    + field("26", merchant_account)
    + field("52", "0000")
    + field("53", "986")
    + field("58", "BR")
    + field("59", "ALEXANDRE FRANCISCO CORAD")
    + field("60", "SAO PAULO")
    + field("62", field("05", "***"))
    + "6304"
)

crc = crc16(payload.encode("latin-1"))
payload += format(crc, "04X").upper()

print("Payload:", payload)

img = qrcode.make(payload, error_correction=qrcode.constants.ERROR_CORRECT_M)
img.save(OUT)
print("QR salvo em:", OUT)