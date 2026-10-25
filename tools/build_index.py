#!/usr/bin/env python3
"""Writes index.json from skins/*/info.json (run by the GitHub action - don't edit index.json by hand)."""
import hashlib, json, os

RAW = "https://raw.githubusercontent.com/KiruTheProot-Creative/EmulonX-Skins/main/"
skins = []
for name in sorted(os.listdir("skins")):
    folder = os.path.join("skins", name)
    try:
        info = json.load(open(os.path.join(folder, "info.json"), encoding="utf-8"))
        data = open(os.path.join(folder, "skin.emxd"), "rb").read()
    except Exception:
        continue
    skins.append({
        "id": name,
        "name": info.get("name", name),
        "author": info.get("author", ""),
        "description": info.get("description", ""),
        "version": info.get("version", "1.0"),
        "skin": RAW + f"skins/{name}/skin.emxd",
        "preview": RAW + f"skins/{name}/preview.png",
        "size": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    })
skins.sort(key=lambda s: s["name"].lower())
with open("index.json", "w", encoding="utf-8") as f:
    json.dump({"format": "emulonx-skins", "version": 1, "skins": skins}, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(f"{len(skins)} skins")
