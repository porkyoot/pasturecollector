# Cobblemon Pasture Loot Generator

![Cobblemon Pasture](pack.png)

This script generates loot tables in `.json` format for Minecraft from `.csv` raw data. It is designed for the [Cobblemon Pasture Collector](https://modrinth.com/mod/cobblemon-pasturecollector) mod.

## What It Does

The Cobblemon Pasture Loot Generator reads data from CSV files and creates corresponding JSON files for Minecraft loot tables. It processes Pokémon drops and assigns item IDs based on a predefined dictionary, ensuring that the generated loot tables are accurate and consistent.

## How to Use the Script

### Prerequisites

1. **Install Visual Studio Code (VS Code)**:
   - Download and install VS Code from [here](https://code.visualstudio.com/).

2. **Install Python**:
   - Download and install Python from [here](https://www.python.org/downloads/).

3. **Install Jupyter Notebook Extension for VS Code**:
   - Open VS Code.
   - Go to the Extensions view by clicking the Extensions icon in the Activity Bar on the side of the window or by pressing `Ctrl+Shift+X`.
   - Search for "Jupyter" and install the Jupyter extension.

### Setting Up the Environment

1. **Clone the Repository**:
   - Clone the repository to your local machine using the following command:
     ```sh
     git clone <repository-url>
     ```

2. **Navigate to the Project Directory**:
   - Open a terminal and navigate to the project directory:
     ```sh
     cd Cobblemon-Pasture-Loot-Generator
     ```

3. **Install Required Libraries**:
   - Open the `gen.ipynb` file in VS Code.
   - Run the following cell to install the required libraries:
     ```python
     %pip install --upgrade pip
     %pip install jupyter pandas
     ```

### Running the Script

1. **Open the Jupyter Notebook**:
   - Open the `gen.ipynb` file in VS Code.

2. **Run the Cells**:
   - Run each cell in the notebook sequentially to execute the script. This will read the CSV files and generate the corresponding JSON files in the specified output directory.

### CSV File Structure

- **drops.csv**: Contains the Pokémon drops data.
- **rolls.csv**: Contains the rarity chances data.
- **cobblemon_items.csv**: Contains the Cobblemon items data.
- **minecraft_items.csv**: Contains the Minecraft items data.

### Output

The generated JSON files will be saved in the `data/pasturecollector/loot_tables/gameplay/pasture_collector/species/` directory.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Cobblemon Pasture Collector](https://modrinth.com/mod/cobblemon-pasturecollector) mod for providing the inspiration and data for this project.