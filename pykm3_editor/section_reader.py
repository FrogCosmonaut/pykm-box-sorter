import struct
from dataclasses import dataclass, asdict
from typing import ClassVar

from .pokemon_parser import BasePokemon
from .item_parser import Item
from .constants import (
    GAME_NAMES,
    GAME_OFFSETS
)
from .utils import (
    clip,
    bytes_to_int,
    bytes_to_str,
    int_to_bytes
)

class BaseSection:
    offsets: dict = GAME_OFFSETS
    data: bytes = None
    security_key: ClassVar[int] = 0
    game_code: ClassVar[int] = 0

    @classmethod
    def from_bytes(cls, data: bytes):
        return cls(data)

    @classmethod
    def set_security_key(cls, value: int):
        cls.security_key = value
    
    @classmethod
    def set_game_code(cls, value: int):
        cls.game_code = value
    
    def get_data(self, key: str) -> bytes:
        if self.data is None or self.game_code is None:
            raise ValueError('Data or game_code not defined')
        
        offset, size = self.offsets[key][self.game_code]
        return self.data[offset:offset+size]

class TrainerInfoSection(BaseSection):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.get_game_code(self.get_data('game_code'))
        self.get_security_key(self.get_data('security_key'))
        self.player_name = bytes_to_str(self.get_data('player_name'))
        self.player_gender = bytes_to_int(self.get_data('player_gender'))
        self.unused = bytes_to_int(self.get_data('unused'))
        self.trainer_id = bytes_to_int(self.get_data('trainer_id'))
        self.tid_secret = bytes_to_int(self.get_data('tid_secret'))
        self.time_played = self.get_time_played(self.get_data('time_played'))
        self.options = self.get_options(self.get_data('options'))

    def get_game_code(self, data: bytes):
        self.game_code = clip(bytes_to_int(data), 0, 2)
        self.game_name = GAME_NAMES[self.game_code]
        BaseSection.set_game_code(self.game_code)
    
    def get_security_key(self, data: bytes):
        self.security_key = bytes_to_int(data)
        BaseSection.set_security_key(self.security_key)
        
    def get_time_played(self, data: bytes) -> tuple:
        hours, minutes = bytes_to_int(data[0:1]), data[2]
        seconds, frames = data[3], data[4]
        return (hours, minutes, seconds, frames)
    
    def get_options(self, data: bytes) -> list:
        button_mode = data[0]
        text_speed = data[1]
        sound = data[2]
        return [button_mode, text_speed, sound]

    def __repr__(self):
        return (f"TrainerInfoSection(game_code={self.game_code}, "
                f"security_key={self.security_key}, "
                f"player_name={self.player_name}, "
                f"player_gender={self.player_gender}, "
                f"trainer_id={self.trainer_id}, "
                f"tid_secret={self.tid_secret}, "
                f"time_played={self.time_played})")

class TeamItemsSection(BaseSection):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.team_size = bytes_to_int(self.get_data('team_size'))
        self.team_pokemon_list = self.get_pokemon_list()
        self.money =  self.get_money()
        self.coins = self.get_coins()
        self.pc_items = self.get_items(self.get_data('pc_items'), security=False)
        self.item_pocket = self.get_items(self.get_data('item_pocket'))
        self.key_item_pocket = self.get_items(self.get_data('key_item_pocket'))
        self.ball_item_pocket = self.get_items(self.get_data('ball_item_pocket'))
        self.tm_case = self.get_items(self.get_data('tm_case'))
        self.berry_pocket = self.get_items(self.get_data('berry_pocket'))

    def get_pokemon_list(self) -> list:
        data = self.get_data('team_pokemon_list')
        pokemon_list = []
        for i in range(0, 600, 100):
            pokemon = BasePokemon.from_bytes(data[0+i:0+i + 100])
            pokemon_list.append(pokemon)
        return pokemon_list

    def get_money(self) -> int:
        """Must be XORed with the security key to yield the true value."""
        data = self.get_data('money')
        return bytes_to_int(data) ^ self.security_key
    
    def get_coins(self) -> int:
        """Must be XORed with the lower two bytes of the security key to yield the true value."""
        data = self.get_data('coins')
        lower_two_bytes = self.security_key & 0xFFFF
        return bytes_to_int(data) ^ lower_two_bytes
    
    def get_items(self, data: bytes, security: bool=True):
        item_len = 4
        item_list = []
        for i in range(0, len(data), item_len):
            item_data = data[0x00 + i:0x00 + i + item_len]
            item = Item.from_bytes(item_data, security=security, security_key=self.security_key)
            item_list.append(item)
        return item_list

    def __repr__(self):
        return (f"TeamItemsSection(team_size={self.team_size}, "
                f"money={self.money}, coins={self.coins}, "
                f"pc_items={len(self.pc_items)}, item_pocket={len(self.item_pocket)}, "
                f"key_item_pocket={len(self.key_item_pocket)}, ball_item_pocket={len(self.ball_item_pocket)}, "
                f"tm_case={len(self.tm_case)}, berry_pocket={len(self.berry_pocket)})")

class GameStateSection(BaseSection):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.mirage_island_value = bytes_to_int(self.get_data('mirage_island_value'))

    def __repr__(self):
        return (f"GameStateSection(mirage_island_value={self.mirage_island_value})")
    
    def __str__(self):
        return (f"Mirage Island Value: {self.mirage_island_value}\n")

class GameSpecificDataSection(BaseSection):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.rival_name = bytes_to_str(self.get_data('rival_name'))

    def __repr__(self):
        return (f"GameSpecificDataSection(rival_name={self.rival_name})")
    
    def __str__(self):
        return (f"Rival Name: {self.rival_name}\n")

class PCBufferSection(BaseSection):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.current_pc_box = bytes_to_int(self.get_data('current_pc_box'))
        self.box_names = self.get_box_names(self.get_data('box_names'))
        self.box_wallpapers = self.get_box_wallpapers(self.get_data('box_wallpapers'))
        self.pc_boxes_pokemon_list = self.get_pc_pokemons(self.get_data('pc_boxes_pokemon_list'))

    def get_box_names(self, data: bytes) -> list[str]:
        box_length = len(data) // 14
        box_names = []
        for i in range(0, len(data), box_length):
            box_name = bytes_to_str(data[0+i:0+i+box_length])
            box_names.append(box_name)
        return box_names

    def get_box_wallpapers(self, data: bytes) -> list[int]:
        wallpaper_names = []
        for i in range(0, len(data)):
            wallpaper_name = data[0+i]
            wallpaper_names.append(wallpaper_name)
        return wallpaper_names

    def get_pc_pokemons(self, data: bytes) -> dict:
        pc_data = {}
        box_len = 2400
        pk_len = 80

        for i in range(14):
            pc_data[f"Box {i}"] = {
                "Box Name": self.box_names[i],
                "Box Wallpaper": self.box_wallpapers[i],
                "Pokemons": []
            }
            box_pokemons = data[box_len*i:box_len*i+box_len]
            pokemon_entries = [box_pokemons[x:x+pk_len] for x in range(0, box_len, pk_len)]
            pc_data[f"Box {i}"]["Pokemons"] = [BasePokemon.from_bytes(e) for e in pokemon_entries]

        return pc_data
    
    def __repr__(self):
        return (f"PCBufferSection(current_pc_box={self.current_pc_box!r}, "
                f"box_names={self.box_names!r}, box_wallpapers={self.box_wallpapers!r}, "
                f"pc_boxes_pokemon_list={self.pc_boxes_pokemon_list!r})")

    def __str__(self):
        return (f"PC Buffer Section:\n"
                f"Current PC Box: {self.current_pc_box}\n"
                f"Box Names: {self.box_names}\n"
                f"Box Wallpapers: {self.box_wallpapers}\n"
                f"PC Boxes Pokémon List: {self.pc_boxes_pokemon_list}")

@dataclass
class SaveSection:
    id: int | list[int]
    data: bytes
    checksum: int
    signature: int
    save_index: int

    def to_dict(self):
        return asdict(self)

class SectionReader:
    SECTION_SIZE = 0x1000  # 4KB
    SECTION_DATA_SIZE = 0x0FF4
    SIGNATURE = 0x08012025
    SAVE_A_OFFSET = (0x00, 0xE000)
    SAVE_B_OFFSET = (0xE000, 0x1C000)

    def __init__(self, save_data: bytes):
        self.data = save_data
        self.sections = self.load_sections()

    def get_section_by_id(self, section_id: int) -> BaseSection:
        if section_id not in SECTION_ID_TO_CLASS:
            raise ValueError(f'Section ID {section_id} not found.')
        section_class = SECTION_ID_TO_CLASS[section_id]
        if section_id >= 5:
            section_bytes = self.get_full_pc_buffer()
        else:
            section_bytes = self.sections[section_id].data
        return section_class.from_bytes(section_bytes)

    def get_full_pc_buffer(self) -> bytes:
        """ Joins all PC buffer sections into one continuous data block. """
        pc_buffer_sections = [5, 6, 7, 8, 9, 10, 11, 12, 13]
        section_sizes = [3968, 3968, 3968, 3968, 3968, 3968, 3968, 3968, 2000]
        pc_data = bytearray()
        for i, section_id in enumerate(pc_buffer_sections):
            if section_id in self.sections:
                pc_data.extend(self.sections[section_id].data[0:section_sizes[i]])
            else:
                raise ValueError(f"Section {section_id} is missing.")
        return bytes(pc_data)

    def load_sections(self):
        save_a = self.data[self.SAVE_A_OFFSET[0]:self.SAVE_A_OFFSET[1]]
        # save_b = self.data[self.SAVE_B_OFFSET[0]:self.SAVE_B_OFFSET[1]]

        blocks: list[SaveSection] = []
        for offset in range(0, len(save_a), self.SECTION_SIZE):
            section_a = self.read_section(offset)
            section_b = self.read_section(self.SAVE_B_OFFSET[0] + offset)

            if self.validate_section(section_a):
                blocks.append(section_a)
            if self.validate_section(section_b):
                blocks.append(section_b)

        latest_index = max(block.save_index for block in blocks)
        latest_blocks = [b for b in blocks if b.save_index == latest_index]

        return {block.id: block for block in latest_blocks}

    def read_section(self, offset: int) -> SaveSection:
        section_data = self.data[offset:offset + self.SECTION_SIZE]
        data = section_data[:self.SECTION_DATA_SIZE]
        section_id = bytes_to_int(section_data[0x0FF4:0x0FF4 + 2])
        checksum = bytes_to_int(section_data[0x0FF6:0x0FF6 + 2])
        signature = bytes_to_int(section_data[0x0FF8:0x0FF8 + 4])
        save_index = bytes_to_int(section_data[0x0FFC:0x0FFC + 4])
        return SaveSection(section_id, data, checksum, signature, save_index)

    def validate_section(self, section: SaveSection) -> bool:
        if section.signature != self.SIGNATURE:
            return False
        return self.calculate_checksum(section.data, self.SECTION_DATA_SIZE) == section.checksum

    def calculate_checksum(self, d: bytes, s: int) -> int:
        checksum = sum(struct.unpack("<" + "I" * (s // 4), d[:s - (s % 4)]))
        return ((checksum >> 16) + (checksum & 0xFFFF)) & 0xFFFF


SECTION_ID_TO_CLASS = {
    0: TrainerInfoSection,
    1: TeamItemsSection,
    2: GameStateSection,
    3: GameSpecificDataSection,
    4: None,
    5: PCBufferSection
}