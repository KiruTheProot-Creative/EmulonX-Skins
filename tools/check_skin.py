#!/usr/bin/env python3
"""Checks skin folders: python3 tools/check_skin.py skins/<name> [more folders]. Exits 1 if anything is wrong."""
import json, re, sys, zipfile, os

MAX_SKIN = 20 * 1024 * 1024
MAX_PREVIEW = 2 * 1024 * 1024
ALLOWED_IN_SKIN = (".json", ".png", ".jpg", ".jpeg", ".ttf", ".otf")

def check(folder):
    problems = []
    name = os.path.basename(os.path.normpath(folder))
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 48:
        problems.append(f"the folder name '{name}' may only use small letters, numbers and dashes (up to 48)")
    allowed = {"skin.emxd", "preview.png", "info.json"}
    for f in os.listdir(folder):
        if f not in allowed:
            problems.append(f"'{f}' doesn't belong here - only skin.emxd, preview.png and info.json")
    # info.json
    try:
        info = json.load(open(os.path.join(folder, "info.json"), encoding="utf-8"))
        for key in ("name", "author"):
            if not isinstance(info.get(key), str) or not info[key].strip():
                problems.append(f"info.json needs a \"{key}\"")
        for key in ("name", "author", "description", "version"):
            if key in info and (not isinstance(info[key], str) or len(info[key]) > (300 if key == "description" else 60)):
                problems.append(f"info.json: \"{key}\" is too long or not text")
    except FileNotFoundError:
        problems.append("info.json is missing")
    except Exception as e:
        problems.append(f"info.json can't be read ({e})")
    # preview
    p = os.path.join(folder, "preview.png")
    if not os.path.exists(p):
        problems.append("preview.png is missing")
    else:
        if os.path.getsize(p) > MAX_PREVIEW:
            problems.append("preview.png is bigger than 2 MB")
        if open(p, "rb").read(8) != b"\x89PNG\r\n\x1a\n":
            problems.append("preview.png isn't a PNG picture")
    # the skin itself
    s = os.path.join(folder, "skin.emxd")
    if not os.path.exists(s):
        problems.append("skin.emxd is missing")
        return problems
    if os.path.getsize(s) > MAX_SKIN:
        problems.append("skin.emxd is bigger than 20 MB")
    try:
        with zipfile.ZipFile(s) as z:
            names = z.namelist()
            if "skin.json" not in names:
                problems.append("skin.emxd has no skin.json inside - save it with Emulon X SD")
            total = 0
            for n in names:
                info_ = z.getinfo(n)
                total += info_.file_size
                if n.startswith("/") or ".." in n.split("/"):
                    problems.append(f"skin.emxd contains an unsafe file name: {n}")
                if not n.endswith("/") and not n.lower().endswith(ALLOWED_IN_SKIN):
                    problems.append(f"skin.emxd contains a file type that isn't allowed: {n}")
            if total > 128 * 1024 * 1024:
                problems.append("skin.emxd unpacks to more than 128 MB")
            if "skin.json" in names:
                j = json.loads(z.read("skin.json").decode("utf-8"))
                if j.get("format") != "emxd":
                    problems.append("skin.json isn't an Emulon X skin description")
                elif float(j.get("version", 0)) < 2:
                    problems.append("this skin uses the old format - open and save it in Emulon X SD")
    except zipfile.BadZipFile:
        problems.append("skin.emxd isn't a valid skin file")
    except Exception as e:
        problems.append(f"skin.emxd can't be read ({e})")
    return problems

if __name__ == "__main__":
    bad = False
    for folder in sys.argv[1:]:
        if not os.path.isdir(folder):
            continue
        problems = check(folder)
        if problems:
            bad = True
            print(f"{folder}:")
            for p in problems:
                print(f"  - {p}")
        else:
            print(f"{folder}: ok")
    sys.exit(1 if bad else 0)
