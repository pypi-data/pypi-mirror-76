import ctypes
import oead
import zlib
from pathlib import Path


def yml_to_sbyml(a):
    bigendian: bool = a.bigendian
    startpath = Path.cwd() / Path("CookData.yml")
    cookdata = oead.byml.from_text(startpath.read_text())

    for recipe in cookdata["Recipes"]:
        if "Actors" in recipe:
            for combo in recipe["Actors"]:
                idx = 0
                for idx in range(len(combo)):
                    try:
                        combo[idx] = oead.U32(
                            ctypes.c_uint32(zlib.crc32(combo[idx].encode())).value
                        )
                    except AttributeError:
                        continue
        if "Tags" in recipe:
            for taglist in recipe["Tags"]:
                idx = 0
                for idx in range(len(taglist)):
                    try:
                        taglist[idx] = oead.U32(
                            ctypes.c_uint32(zlib.crc32(taglist[idx].encode())).value
                        )
                    except AttributeError:
                        continue
        try:
            recipe["Recipe"] = oead.U32(
                ctypes.c_uint32(zlib.crc32(recipe["Recipe"].encode())).value
            )
        except AttributeError:
            continue

    for recipe in cookdata["SingleRecipes"]:
        if "Actors" in recipe:
            idx = 0
            for idx in range(len(recipe["Actors"])):
                try:
                    recipe["Actors"][idx] = oead.U32(
                        ctypes.c_uint32(zlib.crc32(recipe["Actors"][idx].encode())).value
                    )
                except AttributeError:
                    continue
        if "Tags" in recipe:
            idx = 0
            for idx in range(len(recipe["Tags"])):
                try:
                    recipe["Tags"][idx] = oead.U32(
                        ctypes.c_uint32(zlib.crc32(recipe["Tags"][idx].encode())).value
                    )
                except AttributeError:
                    continue
        try:
            recipe["Recipe"] = oead.U32(
                ctypes.c_uint32(zlib.crc32(recipe["Recipe"].encode())).value
            )
        except AttributeError:
            continue

    endpath = Path.cwd() / Path("CookData.sbyml")

    if not endpath.exists():
        endpath.touch()

    endpath.write_bytes(oead.yaz0.compress(oead.byml.to_binary(cookdata, bigendian)))
