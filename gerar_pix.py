#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera o QR Code Pix estatico usado no site (assets/pix/pix.jpeg).

O payload (copia e cola) e mantido literalmente como foi fornecido.
"""
from pathlib import Path

try:
    import qrcode
except ImportError:
    raise SystemExit("qrcode nao instalado: python -m pip install qrcode")

BASE = Path(__file__).resolve().parent
OUT = BASE / "assets" / "pix" / "pix.jpeg"

PAYLOAD = (
    "00020126630014br.gov.bcb.pix0114+55419878496650223Lua_de_mel_da_Mai_e_Ale"
    "5204000053039865802BR5925MAIANE_REGINA_FERREIRA_SO6008CURITIBA"
    "62290525kf14qFuwCY8iHAAZHSs7cRWT863044300"
)


def main():
    img = qrcode.make(PAYLOAD, error_correction=qrcode.constants.ERROR_CORRECT_M)
    img.save(OUT)
    print("Payload:", PAYLOAD)
    print("QR salvo em:", OUT)


if __name__ == "__main__":
    main()