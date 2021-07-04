"""
ua_plode.py

Generic conversion script for exploded/compact Universal Anaphora format

"""

import io, os, sys, re
from glob import glob
from argparse import ArgumentParser
from collections import defaultdict

DEFAULT_HEADERS = ["ID","FORM","LEMMA","UPOS","XPOS","FEATS","HEAD","DEPREL","DEPS","MISC","IDENTITY","BRIDGING","DISCOURSE_DEIXIS","REFERENCE","NOM_SEM"]

__author__ = "Amir Zeldes"
__version__ = 0.1
__license__ = "Apache 2.0"


def add_misc(old_misc, new_anno):
    if old_misc == "_":
        return new_anno
    else:
        annos = old_misc.split("|")
        annos.append(new_anno)
        return "|".join(sorted(annos))


def implode(exploded):
    def is_token(line):
        return len(line.strip())>0 and not line.startswith("#")

    lines = exploded.strip().split("\n")
    if "# global.columns" in exploded:
        headers = [l for l in lines if "# global.columns" in l][0]
        headers = headers.split("=")[1].split()
    else:
        headers = DEFAULT_HEADERS

    # Pass 1: gather markable info
    all_anno_keys = set()
    all_tok_data = []
    max_mark_id = 1
    seen_ids = set()
    seen_ents = set()
    markid2grp = {}
    opening = []
    for l, line in enumerate(lines):
        if is_token(line):
            tok_data = []
            ent2annos = defaultdict(dict)
            fields = line.split()
            for field in fields[10:]:
                if field != "_":
                    ents = re.findall(r'(\(?[^()]+\)?|\))',field)
                    for ent in ents:

                        annos = re.sub(r'[()]','',ent).split("|")
                        annos = [a for a in annos if "=" in a]
                        annos = {a.split("=",maxsplit=1)[0]:a.split("=",maxsplit=1)[1] for a in annos}
                        if "MarkableID" in annos:
                            mark_id = annos["MarkableID"]
                            seen_ids.add(mark_id)
                            del annos["MarkableID"]
                        else:
                            while str(max_mark_id) in seen_ids:
                                max_mark_id += 1
                            mark_id = str(max_mark_id)
                            seen_ids.add(mark_id)
                        if "EntityID" in annos:
                            ent_id = annos["EntityID"]
                            del annos["EntityID"]
                            annos["GRP"] = ent_id
                            seen_ents.add(ent_id)
                        for anno in annos:
                            ent2annos[mark_id][anno] = annos[anno]
                            if anno != "GRP":
                                all_anno_keys.add(anno)
                        if ent.startswith("(") and ent.endswith(")"):  # Single token
                            ent2annos[mark_id]['__brackets__'] = "single"
                        elif ent.startswith("(") and not ent.endswith(")"):  # Opening bracket
                            opening.append(mark_id)
                            ent2annos[mark_id]['__brackets__'] = "open"
                            markid2grp[mark_id] = ent2annos[mark_id]["GRP"]
                        else:  # Closing bracket
                            ent_to_close = opening.pop()
                            ent2annos[ent_to_close]['__brackets__'] = "close"
                            ent2annos[ent_to_close]["GRP"] = markid2grp[ent_to_close]
            all_tok_data.append(ent2annos)

    # Pass 2: add entity data to conllu
    all_anno_keys = sorted(list(all_anno_keys))
    global_declaration = "# global.Entity = " + "-".join(all_anno_keys) + "-GRP"
    toknum = 0
    max_entity_id = 1
    output = []
    for l, line in enumerate(lines):
        if l == 34:
            d=3
        if is_token(line):
            fields = line.split()[:10]
            ent_data = []
            for eid in all_tok_data[toknum]:
                ent = all_tok_data[toknum][eid]
                ent_annos = []
                for key in all_anno_keys:
                    if key in ent:
                        ent_annos.append(ent[key])
                    else:
                        ent_annos.append("_")
                if "GRP" not in ent:
                    # Create new entity ID since it was omitted for this markable ID in all columns
                    while str(max_entity_id) in seen_ents:
                        max_entity_id += 1
                    ent_id = str(max_entity_id)
                    seen_ents.add(ent_id)
                    ent["GRP"] = ent_id
                ent_string = "-".join(ent_annos) + "-" + ent["GRP"]
                if ent["__brackets__"] == "single":
                    ent_string = "(" + ent_string + ")"
                elif ent["__brackets__"] == "open":
                    ent_string = "(" + ent_string
                else:
                    ent_string = ent["GRP"] + ")"
                ent_data.append(ent_string)
            if len(ent_data) > 0:
                ent_data = "Entity=" + "".join(ent_data)
                fields[-1] = add_misc(fields[-1],ent_data)
            line = "\t".join(fields)
            output.append(line)
            toknum += 1
        else:
            if "global.columns" in line:
                continue
            output.append(line.strip())
            if "newdoc id" in line:
                output.append(global_declaration)

    return "\n".join(output)


def explode(conllua):
    raise NotImplementedError("Conversion to exploded format not yet supported, aborting")


def diagnose(data):
    lines = data.strip().split("\n")
    for line in lines:
        if line.startswith("1"):  # Token line
            fields = line.split()
            if len(fields) == 10:
                return "conllua"
            elif len(fields) > 10:
                return "exploded"
    return None


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("file",help="file to convert or glob pattern of files to convert (e.g. *.conllu)")
    p.add_argument("-f","--format",choices=["exploded","conllua","auto"],default="auto",
                   help="input format; by default this is auto-detected")

    opts = p.parse_args()

    files = glob(opts.file)

    for file_ in files:
        in_data = io.open(file_,encoding="utf8").read()
        file_format = opts.format
        if opts.format == "auto":
            file_format = diagnose(in_data)
        if file_format == "exploded":
            output = implode(in_data)
        elif file_format == "conllua":
            output = explode(in_data)
        else:
            raise IOError("Invalid format for file: " + file_)

        with io.open(file_+".conv",'w',encoding="utf8",newline="\n") as f:
            f.write(output)
