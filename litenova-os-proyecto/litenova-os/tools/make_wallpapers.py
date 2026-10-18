#!/usr/bin/env python3
"""Genera fondos originales de LiteNova (ondas azules y paisaje).
Uso: python3 tools/make_wallpapers.py   (necesita Pillow y numpy)"""
import os
import numpy as np
from PIL import Image, ImageFilter

W, H = 1920, 1080
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "config/includes.chroot/usr/share/backgrounds/litenova")
os.makedirs(OUT, exist_ok=True)
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
u, v = x / W, y / H


def col(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float32)


def lerp(a, b, t):
    return a + (b - a) * t[..., None]


def to_img(a, blur):
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))


def waves(top, bot, glow, ribbons, seed):
    rng = np.random.default_rng(seed)
    img = lerp(col(top), col(bot), v)
    for c in ribbons:
        a = rng.uniform(.08, .16)
        f = rng.uniform(.5, .9)
        p = rng.uniform(0, 6.28)
        base = rng.uniform(.25, .85)
        th = rng.uniform(.09, .18)
        center = base + a * np.sin(f * 6.28 * u + p) + .5 * a * np.sin(1.4 * f * 6.28 * u + 2 * p) + .25 * (u - .5)
        m = np.exp(-((v - center) / th) ** 2)
        img = img + m[..., None] * col(c) * .55
    g = np.exp(-(((u - .75) / .5) ** 2 + ((v - .2) / .5) ** 2))
    img = img + g[..., None] * col(glow) * .35
    return to_img(img, 14)


def landscape():
    img = lerp(col("#1b2a63"), col("#c98fb0"), np.clip(v ** 1.6 * 1.6, 0, 1))
    moon = np.exp(-(((u - .79) * W) ** 2 + ((v - .27) * H) ** 2) / 2200)
    img = img + moon[..., None] * 255
    xs = np.linspace(0, 1, W)
    for seed, base, amp, c in [(3, .55, .09, "#223a82"), (11, .63, .07, "#162a66"), (5, .72, .05, "#0c1b45")]:
        r = np.random.default_rng(seed)
        line = np.zeros(W, np.float32)
        for k in range(1, 7):
            line += r.uniform(.4, 1) / k * np.sin(2 * np.pi * k * xs * r.uniform(.6, 1.4) + r.uniform(0, 6.28))
        mask = (v > (base + amp * line)[None, :]).astype(np.float32)
        img = img * (1 - mask[..., None]) + mask[..., None] * col(c)
    lake = (v > .78).astype(np.float32)
    water = lerp(col("#13245a"), col("#060f2b"), np.clip((v - .78) / .22, 0, 1))
    img = img * (1 - lake[..., None] * .75) + water * lake[..., None] * .75
    return to_img(img, 1.5)


waves("#050d24", "#0b1e3b", "#007bff", ["#007bff", "#4da3ff", "#1f6bff", "#0a4fd6"], 1).save(f"{OUT}/litenova-oscuro.png")
waves("#e6f0ff", "#9cc7ff", "#ffffff", ["#4da3ff", "#007bff", "#bcd9ff", "#7fb6ff"], 2).save(f"{OUT}/litenova-claro.png")
landscape().save(f"{OUT}/litenova-paisaje.png")
print("OK:", sorted(os.listdir(OUT)))
