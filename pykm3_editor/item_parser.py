from dataclasses import dataclass

from .utils import bytes_to_int

ITEM_BYTE_LENGTH = 4

@dataclass
class Item:
    item_id: int
    item_name: str
    item_quantity: int

    @classmethod
    def from_bytes(cls, data: bytes, security: bool = False, security_key: int = 0):
        item_id = bytes_to_int(data[:2])
        item_name = ITEM_ID_TO_NAME[item_id]
        item_quantity = bytes_to_int(data[2:])
        if security:
            item_quantity = cls.decrypt_qty(item_quantity, security_key)
        return cls(item_id, item_name, item_quantity)
    
    @staticmethod
    def decrypt_qty(item_quantity, security_key):
        """Must be XORed with the lower 16 bits of the security key to yield the true value."""
        return item_quantity ^ (security_key & 0xFFFF)


ITEM_ID_TO_NAME = {
    0: "Nothing", 1: "Master Ball", 2: "Ultra Ball", 3: "Great Ball", 4: "Poké Ball", 5: "Safari Ball", 6: "Net Ball", 7: "Dive Ball", 8: "Nest Ball", 9: "Repeat Ball",
    10: "Timer Ball", 11: "Luxury Ball", 12: "Premier Ball", 13: "Potion", 14: "Antidote", 15: "Burn Heal", 16: "Ice Heal", 17: "Awakening", 18: "Parlyz Heal", 19: "Full Restore",
    20: "Max Potion", 21: "Hyper Potion", 22: "Super Potion", 23: "Full Heal", 24: "Revive", 25: "Max Revive", 26: "Fresh Water", 27: "Soda Pop", 28: "Lemonade", 29: "Moomoo Milk",
    30: "EnergyPowder", 31: "Energy Root", 32: "Heal Powder", 33: "Revival Herb", 34: "Ether", 35: "Max Ether", 36: "Elixir", 37: "Max Elixir", 38: "Lava Cookie", 39: "Blue Flute",
    40: "Yellow Flute", 41: "Red Flute", 42: "Black Flute", 43: "White Flute", 44: "Berry Juice", 45: "Sacred Ash", 46: "Shoal Salt", 47: "Shoal Shell", 48: "Red Shard", 49: "Blue Shard",
    50: "Yellow Shard", 51: "Green Shard", 52: "unknown", 53: "unknown", 54: "unknown", 55: "unknown", 56: "unknown", 57: "unknown", 58: "unknown", 59: "unknown", 60: "unknown",
    61: "unknown", 62: "unknown", 63: "HP Up", 64: "Protein", 65: "Iron", 66: "Carbos", 67: "Calcium", 68: "Rare Candy", 69: "PP Up", 70: "Zinc", 71: "PP Max",
    72: "unknown", 73: "Guard Spec.", 74: "Dire Hit", 75: "X Attack", 76: "X Defend", 77: "X Speed", 78: "X Accuracy", 79: "X Special", 80: "Poké Doll", 81: "Fluffy Tail",
    82: "unknown", 83: "Super Repel", 84: "Max Repel", 85: "Escape Rope", 86: "Repel", 87: "unknown", 88: "unknown", 89: "unknown", 90: "unknown", 91: "unknown",
    92: "unknown", 93: "Sun Stone", 94: "Moon Stone", 95: "Fire Stone", 96: "Thunderstone", 97: "Water Stone", 98: "Leaf Stone", 99: "unknown", 100: "unknown", 101: "unknown",
    102: "unknown", 103: "TinyMushroom", 104: "Big Mushroom", 105: "unknown", 106: "Pearl", 107: "Big Pearl", 108: "Stardust", 109: "Star Piece", 110: "Nugget",
    111: "Heart Scale", 112: "unknown", 113: "unknown", 114: "unknown", 115: "unknown", 116: "unknown", 117: "unknown", 118: "unknown", 119: "unknown", 120: "unknown",
    121: "Orange Mail", 122: "Harbor Mail", 123: "Glitter Mail", 124: "Mech Mail", 125: "Wood Mail", 126: "Wave Mail", 127: "Bead Mail", 128: "Shadow Mail", 129: "Tropic Mail", 130: "Dream Mail",
    131: "Fab Mail", 132: "Retro Mail", 133: "Cheri Berry", 134: "Chesto Berry", 135: "Pecha Berry", 136: "Rawst Berry", 137: "Aspear Berry", 138: "Leppa Berry", 139: "Oran Berry", 140: "Persim Berry",
    141: "Lum Berry", 142: "Sitrus Berry", 143: "Figy Berry", 144: "Wiki Berry", 145: "Mago Berry", 146: "Aguav Berry", 147: "Iapapa Berry", 148: "Razz Berry", 149: "Bluk Berry", 150: "Nanab Berry",
    151: "Wepear Berry", 152: "Pinap Berry", 153: "Pomeg Berry", 154: "Kelpsy Berry", 155: "Qualot Berry", 156: "Hondew Berry", 157: "Grepa Berry", 158: "Tamato Berry", 159: "Cornn Berry", 160: "Magost Berry",
    161: "Rabuta Berry", 162: "Nomel Berry", 163: "Spelon Berry", 164: "Pamtre Berry", 165: "Watmel Berry", 166: "Durin Berry", 167: "Belue Berry", 168: "Liechi Berry", 169: "Ganlon Berry", 170: "Salac Berry",
    171: "Petaya Berry", 172: "Apicot Berry", 173: "Lansat Berry", 174: "Starf Berry", 175: "Enigma Berry", 176: "unknown", 177: "unknown", 178: "unknown", 179: "BrightPowder", 180: "White Herb",
    181: "Macho Brace", 182: "Exp. Share", 183: "Quick Claw", 184: "Soothe Bell", 185: "Mental Herb", 186: "Choice Band", 187: "King's Rock", 188: "SilverPowder", 189: "Amulet Coin", 190: "Cleanse Tag",
    191: "Soul Dew", 192: "DeepSeaTooth", 193: "DeepSeaScale", 194: "Smoke Ball", 195: "Everstone", 196: "Focus Band", 197: "Lucky Egg", 198: "Scope Lens", 199: "Metal Coat", 200: "Leftovers",
    201: "Dragon Scale", 202: "Light Ball", 203: "Soft Sand", 204: "Hard Stone", 205: "Miracle Seed", 206: "BlackGlasses", 207: "Black Belt", 208: "Magnet", 209: "Mystic Water", 210: "Sharp Beak",
    211: "Poison Barb", 212: "NeverMeltIce", 213: "Spell Tag", 214: "TwistedSpoon", 215: "Charcoal", 216: "Dragon Fang", 217: "Silk Scarf", 218: "Up-Grade", 219: "Shell Bell",
    220: "Sea Incense", 221: "Lax Incense", 222: "Lucky Punch", 223: "Metal Powder", 224: "Thick Club", 225: "Stick", 226: "unknown", 227: "unknown", 228: "unknown", 229: "unknown",
    230: "unknown", 231: "unknown", 232: "unknown", 233: "unknown", 234: "unknown", 235: "unknown", 236: "unknown", 237: "unknown", 238: "unknown", 239: "unknown", 240: "unknown",
    241: "unknown", 242: "unknown", 243: "unknown", 244: "unknown", 245: "unknown", 246: "unknown", 247: "unknown", 248: "unknown", 249: "unknown", 250: "unknown",
    251: "unknown", 252: "unknown", 253: "unknown", 254: "Red Scarf", 255: "Blue Scarf", 256: "Pink Scarf", 257: "Green Scarf", 258: "Yellow Scarf", 259: "Mach Bike", 260: "Coin Case", 261: "Itemfinder",
    262: "Old Rod", 263: "Good Rod", 264: "Super Rod", 265: "S.S. Ticket", 266: "Contest Pass", 267: "unknown", 268: "Wailmer Pail", 269: "Devon Goods", 270: "Soot Sack", 271: "Basement Key",
    272: "Acro Bike", 273: "Pokéblock Case", 274: "Letter", 275: "Eon Ticket", 276: "Red Orb", 277: "Blue Orb", 278: "Scanner", 279: "Go-Goggles", 280: "Meteorite",
    281: "Rm. 1 Key", 282: "Rm. 2 Key", 283: "Rm. 4 Key", 284: "Rm. 6 Key", 285: "Storage Key", 286: "Root Fossil", 287: "Claw Fossil", 288: "Devon Scope", 289: "TM01",
    290: "TM02", 291: "TM03", 292: "TM04", 293: "TM05", 294: "TM06", 295: "TM07", 296: "TM08", 297: "TM09", 298: "TM10",
    299: "TM11", 300: "TM12", 301: "TM13", 302: "TM14", 303: "TM15", 304: "TM16", 305: "TM17", 306: "TM18", 307: "TM19", 308: "TM20",
    309: "TM21", 310: "TM22", 311: "TM23", 312: "TM24", 313: "TM25", 314: "TM26", 315: "TM27", 316: "TM28", 317: "TM29", 318: "TM30",
    319: "TM31", 320: "TM32", 321: "TM33", 322: "TM34", 323: "TM35", 324: "TM36", 325: "TM37", 326: "TM38", 327: "TM39", 328: "TM40",
    329: "TM41", 330: "TM42", 331: "TM43", 332: "TM44", 333: "TM45", 334: "TM46", 335: "TM47", 336: "TM48", 337: "TM49", 338: "TM50",
    339: "HM01", 340: "HM02", 341: "HM03", 342: "HM04", 343: "HM05", 344: "HM06", 345: "HM07", 346: "HM08", 347: "unknown", 348: "unknown",
    349: "Oak's Parcel", 350: "Poké Flute", 351: "Secret Key", 352: "Bike Voucher", 353: "Gold Teeth", 354: "Old Amber", 355: "Card Key", 356: "Lift Key", 357: "Helix Fossil", 358: "Dome Fossil",
    359: "Silph Scope", 360: "Bicycle", 361: "Town Map", 362: "VS Seeker", 363: "Fame Checker", 364: "TM Case", 365: "Berry Pouch", 366: "Teachy TV", 367: "Tri-Pass",
    368: "Rainbow Pass", 369: "Tea", 370: "MysticTicket", 371: "AuroraTicket", 372: "Powder Jar", 373: "Ruby", 374: "Sapphire", 375: "Magma Emblem", 376: "Old Sea Map"
}

ITEM_NAME_TO_ID = {v: k for k, v in ITEM_ID_TO_NAME.items()}