import ctypes
import oead
import zlib
from pathlib import Path

from . import actorlookup, taglookup


def sbyml_to_yml():
    startpath = Path.cwd() / Path("CookData.sbyml")
    cookdata = oead.byml.from_binary(oead.yaz0.decompress(startpath.read_bytes()))

    for recipe in cookdata["Recipes"]:
        if "Actors" in recipe:
            for combo in recipe["Actors"]:
                idx = 0
                for idx in range(len(combo)):
                    try:
                        combo[idx] = actorlookup[combo[idx].v]
                    except KeyError:
                        continue
        if "Tags" in recipe:
            for taglist in recipe["Tags"]:
                idx = 0
                for idx in range(len(taglist)):
                    try:
                        taglist[idx] = taglookup[taglist[idx].v]
                    except KeyError:
                        continue
        try:
            recipe["Recipe"] = actorlookup[recipe["Recipe"].v]
        except KeyError:
            continue

    for recipe in cookdata["SingleRecipes"]:
        if "Actors" in recipe:
            idx = 0
            for idx in range(len(recipe["Actors"])):
                try:
                    recipe["Actors"][idx] = actorlookup[recipe["Actors"][idx].v]
                except KeyError:
                    continue
        if "Tags" in recipe:
            idx = 0
            for idx in range(len(recipe["Tags"])):
                try:
                    recipe["Tags"][idx] = taglookup[recipe["Tags"][idx].v]
                except KeyError:
                    continue
        try:
            recipe["Recipe"] = actorlookup[recipe["Recipe"].v]
        except KeyError:
            continue

    endpath = Path.cwd() / Path("CookData.yml")

    if not endpath.exists():
        endpath.touch()

    endpath.write_text(oead.byml.to_text(cookdata))
