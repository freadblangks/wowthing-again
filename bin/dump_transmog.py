import csv
import glob
import os
import os.path
import re
import sys


CLASS_MASK = {
       1: 'warrior',
       2: 'paladin',
       4: 'hunter',
       8: 'rogue',
      16: 'priest',
      32: 'death-knight',
      64: 'shaman',
     128: 'mage',
     256: 'warlock',
     512: 'monk',
    1024: 'druid',
    2048: 'demon-hunter',
}

ARMOR_MASKS = {
    'cloth': [
        16 + 128 + 256,
    ],
    'leather': [
        8 + 1024,
        8 + 1024 + 512,
        8 + 1024 + 512 + 2048,
    ],
    'mail': [
        4 + 64,
    ],
    'plate': [
        1 + 2,
        1 + 2 + 32,
    ]
}

SLOT_MAP = {
     1: 'Head',
     3: 'Shoulders',
     5: 'Chest',
     6: 'Waist',
     7: 'Legs',
     8: 'Feet',
     9: 'Wrists',
    10: 'Hands',
    16: 'Back',
    20: 'Chest',
}

DESCRIPTION_MAP = {
     1641: 'Raid Finder',
     2015: 'Heroic',
     3859: 'Elite',
    13145: 'Mythic',
    13193: 'Normal',
    13216: 'Timewarped',
    13291: '25 Normal',
    13292: '25 Heroic',
    13293: '10 Normal',
    13301: 'Gladiator',
    13302: 'Combatant',
    13303: 'Aspirant',
    13304: 'Honor',
    13306: 'PVP Rare',
    13307: 'PVP Epic',
    13305: 'Normal', # Sunwell
    13584: 'Ember Court',
    13590: 'Campaign',
    13591: 'Renown',
    13592: "Queen's Conservatory",
    13594: 'Abominable Stitching',
    13595: 'Unity',
    13596: 'Travel Network',
    13787: 'Winterborn',
    13813: 'Path of Ascension',
    13849: "Death's Advance",
    13850: 'Korthia',
    13859: 'Renown Quartermaster',
}
DESCRIPTION_ORDER = [
    13145, # Mythic
     2015, # Heroic
    13292, # 25 Heroic
    13305, # Sunwell
    13291, # 25 Normal
    13293, # 10 Normal
    13193, # Normal
     1641, # Raid Finder
    13216, # Timewarped

     3859, # Elite
    13301, # Gladiator
    13302, # Combatant
    13304, # Honor
    13303, # Aspirant
    13307, # PVP Epic
    13306, # PVP Rare

    # 9.0 covenant
    13590, # Campaign
    13591, # Renown
    # Kyrian
    13813, # Path of Ascension
    # Necrolord
    13594, # Abominable Stitching
    13595, # Unity
    # Night Fae
    13592, # Queen's Conservatory
    13787, # Winterborn
    # Venthyr
    13584, # Ember Court
    13596, # Travel Network

    # 9.1 covenant
    13849, # Death's Advance
    13850, # Korthia
    13859, # Renown Quartermaster

    0,
]


def main():
    sets = {}
    with open(glob.glob('data/dumps/enUS/transmogset-*.csv')[0]) as csv_file:
        # Name_lang,ID,ClassMask,TrackingQuestID,Flags,TransmogSetGroupID,
        # ItemNameDescriptionID,ParentTransmogSetID,Field_8_1_0_28294_008,
        # ExpansionID,PatchIntroduced,UiOrder,ConditionID
        for row in csv.DictReader(csv_file):
            sets[int(row['ID'])] = dict(
                name=row['Name_lang'],
                class_mask=int(row['ClassMask']),
                description_id=int(row['ItemNameDescriptionID']),
                flags=int(row['Flags']),
            )

    combine = False
    item_ids = []
    set_ids = []

    if sys.argv[1] == 'c':
        combine = True
        set_ids = sys.argv[2:]
    elif sys.argv[1] == 'i':
        item_ids = sys.argv[2:]
    elif sys.argv[1] == 'm':
        # compare?items=29093:28340:27456:28398:27800:137029:27827:28268
        item_ids = sys.argv[2].split('=')[1].split(':')
    elif sys.argv[1] == 'name':
        name_res = []
        for set_name in sys.argv[2:]:
            name_res.append(re.compile(set_name.replace('*', '.*?')))
        for name_re in name_res:
            set_ids.extend(k for k, v in sets.items() if name_re.match(v['name']))
    else:
        set_ids = sys.argv[1:]

    item_ids = [int(item_id) for item_id in item_ids]
    set_ids = [int(set_id) for set_id in set_ids]

    set_items = {}
    with open(glob.glob('data/dumps/transmogsetitem-*.csv')[0]) as csv_file:
        # ID,TransmogSetID,ItemModifiedAppearanceID,Flags
        for row in csv.DictReader(csv_file):
            set_items.setdefault(int(row['TransmogSetID']), []).append(int(row['ItemModifiedAppearanceID']))

    appearances = {}
    with open(glob.glob('data/dumps/itemmodifiedappearance-*.csv')[0]) as csv_file:
        for row in csv.DictReader(csv_file):
            appearances[int(row['ID'])] = [
                int(row['ItemID']),
                int(row['ItemAppearanceID']),
                int(row['ItemAppearanceModifierID']),
            ]

    item_slot = {}
    with open(glob.glob('data/dumps/item-*.csv')[0]) as csv_file:
        for row in csv.DictReader(csv_file):
            item_slot[int(row['ID'])] = int(row['InventoryType'])

    if item_ids:
        appearance_ids = []
        modifier_appearances = {}
        for item_id in item_ids:
            print(item_id)
            for k, v in appearances.items():
                if item_id == v[0]:
                    modifier_appearances.setdefault(v[2], []).append(k)

        for modifier_id, appearance_ids in reversed(sorted(modifier_appearances.items())):
            print(f'    # modifier={modifier_id}')
            print(f'    - name: Modifier {modifier_id}')
            print_items(appearance_ids, appearances, item_slot)

    else:
        mask = sets[set_ids[0]]['class_mask']
        if mask in CLASS_MASK:
            print(f'    {CLASS_MASK[mask]}:')
        else:
            for armor_type, masks in ARMOR_MASKS.items():
                if mask in masks:
                    print(f'    {armor_type}:')
                    break

        if combine:
            set_ids.sort()
            print_set_ids = ",".join(str(s) for s in set_ids)
            print_set_name = ' / '.join(list(dict.fromkeys(sets[s]['name'] for s in set_ids)))

            print(f'    # {get_description(sets, set_ids[0])} set={print_set_ids}')
            print(f'    - name: {print_set_name}')

            appearance_ids = []
            for set_id in set_ids:
                appearance_ids.extend(set_items[set_id])

            print_items(appearance_ids, appearances, item_slot)

        else:
            sort_me = [
                (
                    DESCRIPTION_ORDER.index(sets[set_id]['description_id']),
                    get_description(sets, set_id),
                    set_id,
                ) for set_id in set_ids
            ]
            sort_me.sort()

            for (order, description, set_id) in sort_me:
                print(f'    # {description} set={set_id}')
                print(f'    - name: {sets[set_id]["name"]}')

                print_items(set_items[set_id], appearances, item_slot)


def get_description(sets, set_id):
    description_id = sets[set_id]['description_id']
    flags = sets[set_id]['flags']
    alliance = (flags & 4) > 0
    horde = (flags & 8) > 0

    description = DESCRIPTION_MAP.get(description_id, f'description={description_id}')
    if alliance and not horde:
        description = f'{description} (Alliance)'
    elif horde and not alliance:
        description = f'{description} (Horde)'

    return description

def print_items(appearance_ids, appearances, item_slot):
    ugh = {}
    for appearance_id in appearance_ids:
        if appearance_id not in appearances:
            print('      # Missing appearance', appearance_id)
            continue

        item_id, item_appearance_id, modifier_id = appearances[appearance_id]
        slot = item_slot[item_id]
        # Why are there 2 chest slots?
        if slot == 20:
            slot = 5
        ugh.setdefault(slot, set()).add(item_appearance_id)

    #print(sets[set_id])
    #print(ugh)
    print(f'      wowheadSetId:')
    print(f'      items:')
    for thing in sorted(ugh.items()):#, key=lambda u: SLOT_ORDER.index(u[0])):
        s = thing[0] < 10 and '  ' or ' '
        print(f'        {thing[0]}:{s}{" ".join(str(s) for s in sorted(thing[1]))}', '#', SLOT_MAP[thing[0]])
    print()



if __name__ == '__main__':
    main()
