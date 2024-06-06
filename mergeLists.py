import os
import xml.etree.ElementTree as ET
from pathlib import Path

SHARED_NAME = "Shared.SpellLists.lsx"
SPELL_LIST_FOLDER = os.path.dirname(os.path.realpath(__file__)) + os.sep + "SpellLists" + os.sep
TARGET_FOLDER = os.path.dirname(os.path.realpath(__file__)) + os.sep + "Ilariel_A5EAdapted" + os.sep + "Public" + os.sep + "Ilariel_A5EAdapted" + os.sep + "Lists"+ os.sep
SPELLS_FOLDER = "Spells"


def ensure_folder_exists(path : Path,folder_name : str) -> None:
    folder = path / folder_name
    if not folder.exists():
        folder.mkdir()


def merge_spell_xml_into(shared_path : Path, merge_target_path : Path, merged_out_path : Path) -> None:
    with shared_path.open() as shared_source:
        src_doc = ET.parse(shared_source)
        src_spell_list_nodes = src_doc.find(".//node[@id='root']")[0].findall("node");
        
        src_spell_lists = {}

        for node in src_spell_list_nodes:
            key = node.find(".//attribute[@id='Comment']").attrib["value"]
            valueString = node.find(".//attribute[@id='Spells']").attrib["value"]
            src_spell_lists[int(key)] = valueString


        with merge_target_path.open() as merge_target_source:
            merge_target_doc = ET.parse(merge_target_source)
            merge_target_list_nodes = merge_target_doc.find(".//node[@id='root']")[0].findall("node")
            counter = 0;
            for node in merge_target_list_nodes:
                merge_string = src_spell_lists.get(counter,None)
                if merge_string != None:
                    spell_list_node = node.find(".//attribute[@id='Spells']")
                    value = spell_list_node.attrib["value"]
                    if len(value.strip()) > 0:
                        spell_list_node.attrib["value"] = ";".join((value,merge_string))
                    else:
                        spell_list_node.attrib["value"] = merge_string
                counter += 1
            with merged_out_path.open("wb") as target_file:
                merge_target_doc.write(target_file,"UTF-8",True)
            


def main():
    #Spell lists
    targetRoot = Path(TARGET_FOLDER)
    ensure_folder_exists(targetRoot, SPELLS_FOLDER)
    targetRoot = targetRoot / SPELLS_FOLDER
    for subfolder in Path(SPELL_LIST_FOLDER).iterdir():
        ensure_folder_exists(targetRoot,subfolder.name)
        targetFolder = targetRoot / subfolder.name
        sources = [x for x in subfolder.iterdir() if x.name != SHARED_NAME]
        sharedSpells = subfolder / SHARED_NAME
        assert(sharedSpells.exists())
        for source_path in sources:
            merge_spell_xml_into(sharedSpells,source_path,targetFolder / source_path.name)



if __name__ == "__main__":
    main()