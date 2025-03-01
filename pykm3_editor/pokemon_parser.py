from dataclasses import dataclass
from typing import Dict

from .utils import (
    int_to_bytes,
    bytes_to_str,
    bytes_to_int
)


@dataclass
class BasePokemon:
    personality_value: int
    ot_id: int
    nickname: str
    language: int
    misc_flags: int
    ot_name: str
    markings: int
    unused: int
    data: Dict

    @classmethod
    def from_bytes(cls, data: bytes):
        entry = cls.parse_pokemon(data)
        return cls(
            personality_value=entry["Personality"],
            ot_id=entry["OT ID"],
            nickname=entry["Nickname"],
            language=entry["Language"],
            misc_flags=entry["Misc. Flags"],
            ot_name=entry["OT Name"],
            markings=entry["Markings"],
            unused=entry["????"],
            data=entry["Data"]
        )

    @staticmethod
    def parse_pokemon(entry: bytes) -> dict:      
        personality = bytes_to_int(entry[0x0: 0x0 + 4])
        ot_id = bytes_to_int(entry[0x04: 0x04 + 4])

        BasePokemon.set_ot_and_personality(ot_id, personality)

        return {
            "Personality": personality,
            "OT ID": ot_id,
            "Nickname": bytes_to_str(entry[0x08: 0x08 + 10]),
            "Language": bytes_to_int(entry[0x12: 0x12 + 1]),
            "Misc. Flags": bytes_to_int(entry[0x13: 0x13 + 1]),
            "OT Name": bytes_to_str(entry[0x14: 0x14 + 7]),
            "Markings": bytes_to_int(entry[0x1B: 0x1B + 1]),
            "Checksum": bytes_to_int(entry[0x1C: 0x1C + 2]),
            "????": bytes_to_int(entry[0x1E: 0x1E + 2]),
            "Data": BasePokemon.parse_pokemon_data(entry[0x20: 0x20 + 48])
        }

    @classmethod
    def set_ot_and_personality(cls, ot_id: int, personality: int):
        """Set the OT ID and Personality Value for the class."""
        cls.ot_id = ot_id
        cls.personality_value = personality

    @staticmethod
    def decrypt_pokemon_data(data: bytes) -> bytes:
        decryption_key = BasePokemon.ot_id ^ BasePokemon.personality_value
        decrypted_data = bytearray()

        for i in range(0, 48, 4):
            chunk = bytes_to_int(data[i:i+4])
            decrypted_chunk = chunk ^ decryption_key
            decrypted_data += int_to_bytes(decrypted_chunk, 4)

        return decrypted_data

    @staticmethod
    def parse_pokemon_data(data: bytes) -> dict:
        decrypted_data = BasePokemon.decrypt_pokemon_data(data)
        pokemon_data = {}
        order = BasePokemon.personality_value % 24
        order_dict = {
            0: "GAEM",  1: "GAME",  2: "GEAM",  3: "GEMA",  4: "GMAE",  5: "GMEA",
            6: "AGEM",  7: "AGME",  8: "AEGM",  9: "AEMG", 10: "AMGE", 11: "AMEG",
            12: "EGAM", 13: "EGMA", 14: "EAGM", 15: "EAMG", 16: "EMGA", 17: "EMAG",
            18: "MGAE", 19: "MGEA", 20: "MAGE", 21: "MAEG", 22: "MEGA", 23: "MEAG"
        }

        for i, x in enumerate(order_dict[order]):
            sub_data = decrypted_data[i*12:i*12+12]
            match x:
                case "G":
                    growth_data = pokemon_data['Growth'] = {}
                    growth_data['Species'] = bytes_to_int(sub_data[0:1])
                    growth_data['Item Held'] = bytes_to_int(sub_data[2:3])
                    growth_data['Experience'] = bytes_to_int(sub_data[4:7])
                    growth_data['PP bonuses'] = bytes_to_int(sub_data[8:9])
                    growth_data['Friendship'] = bytes_to_int(sub_data[9:10])
                    growth_data['Unused'] = bytes_to_int(sub_data[10:11])
                case "A":
                    attacks_data = pokemon_data['Attacks'] = {}
                    attacks_data['Move 1'] = bytes_to_int(sub_data[0:1])
                    attacks_data['Move 2'] = bytes_to_int(sub_data[2:3])
                    attacks_data['Move 3'] = bytes_to_int(sub_data[4:5])
                    attacks_data['Move 4'] = bytes_to_int(sub_data[6:7])
                    attacks_data['PP 1'] = bytes_to_int(sub_data[8:8])
                    attacks_data['PP 2'] = bytes_to_int(sub_data[9:9])
                    attacks_data['PP 3'] = bytes_to_int(sub_data[10:10])
                    attacks_data['PP 4'] = bytes_to_int(sub_data[11:11])
                case "E":
                    evs_and_cond_data = pokemon_data['EVs & Condition'] = {}
                    evs_and_cond_data['HP EV'] = bytes_to_int(sub_data[0:0])
                    evs_and_cond_data['Attack EV'] = bytes_to_int(sub_data[1:1])
                    evs_and_cond_data['Defense EV'] = bytes_to_int(sub_data[2:2])
                    evs_and_cond_data['Speed EV'] = bytes_to_int(sub_data[3:3])
                    evs_and_cond_data['Special Attack EV'] = bytes_to_int(sub_data[4:4])
                    evs_and_cond_data['Special Defense EV'] = bytes_to_int(sub_data[5:5])
                    evs_and_cond_data['Coolness'] = bytes_to_int(sub_data[6:6])
                    evs_and_cond_data['Beauty'] = bytes_to_int(sub_data[7:7])
                    evs_and_cond_data['Cuteness'] = bytes_to_int(sub_data[8:8])
                    evs_and_cond_data['Smartness'] = bytes_to_int(sub_data[9:9])
                    evs_and_cond_data['Thoughness'] = bytes_to_int(sub_data[10:10])
                    evs_and_cond_data['Feel'] = bytes_to_int(sub_data[11:11])
                case "M":
                    misc_data = pokemon_data['Miscellaneous'] = {}
                    misc_data['Pokérus status'] = bytes_to_int(sub_data[0:0])
                    misc_data['Met location'] = bytes_to_int(sub_data[1:1])
                    misc_data['Origins info'] = bytes_to_int(sub_data[2:3])
                    misc_data['IVs, Egg and Ability'] = bytes_to_int(sub_data[4:4])
                    misc_data['Ribbons and Obedience'] = bytes_to_int(sub_data[5:7])

        return pokemon_data
    
    def __str__(self):
        species = {self.data['Growth']['Species']}
        return f"Species: {species} - Nickname: {self.nickname}"
    
    def __repr__(self):
        return f"BasePokemon({self.__str__()})"