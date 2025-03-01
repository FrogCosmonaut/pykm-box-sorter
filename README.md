# Pokémon Emerald Box Sorter 🎮✨
Automatically organize your Pokémon boxes to match pokedex order!

## 📌 Overview
Pokémon Emerald Box Sorter is a tool that reorders Pokémon in PC boxes to match the sorting logic used in pokedex. This ensures a cleaner, more organized box layout for easy viewing and transfer between save editors.

## 🚀 Features
✅ Sorts Pokémon by National Dex number
✅ Supports Pokémon Emerald .sav files (Gen 3, GBA)  
✅ Simple CLI for quick use  
✅ User-friendly GUI for non-technical users  
✅ Preserves save integrity (doesn't affect other data)  
✅ Open-source & customizable  

## 🛠️ Installation
### 1️⃣ Install via Python (Recommended)
Clone the repository:

```sh
git clone https://github.com/FrogCosmonaut/pykm-box-sorter.git
cd pykm-box-sorter
```

Install dependencies:

```sh
pip install -r requirements.txt
```

Run the sorter:

```sh
python cli.py my_save.sav sorted_save.sav
```

### 2️⃣ Run the GUI Version
For a graphical interface, run:

```sh
python gui.py
```

## 🖥️ Usage
### CLI (Command Line)

```sh
python cli.py <input_save.sav> <output_save.sav>
```

Example:

```sh
python cli.py emerald.sav sorted_emerald.sav
```

### GUI (Graphical Interface)
1. Open `gui.py`
2. Select your Pokémon Emerald save file (`.sav`)
3. Choose an output location
4. Click **"Sort Boxes"** – Done! 🎉

## ⚙️ Planned Features
🔹 Support for Ruby/Sapphire/FireRed/LeafGreen  
🔹 More sorting options (Level, OT, Shininess)  
🔹 Standalone .exe version  

## 📝 Contributing
Want to help improve the tool? Fork the repo, make changes, and submit a pull request!

## 💖 Support & Credits
This tool is inspired by PKHeX and built with `pkmn-save` for save file parsing. Special thanks to the Pokémon research & ROM hacking community!
