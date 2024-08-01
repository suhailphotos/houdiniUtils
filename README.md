# Houdini Utils

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/houdiniUtils.git
   ```

2. **Navigate to the `houdiniUtils` Directory**:
   ```bash
   cd houdiniUtils
   ```

3. **Install the Package**:
   ```bash
   pip install .
   ```

4. **Add the Package to PYTHONPATH**:
   Ensure your `houdiniUtils` package is in the Python path. Add the following line to your Houdini environment file (`houdini.env`):
   ```bash
   HOUDINI_PATH = /path/to/houdiniUtils;&
   ```

5. **Import the Shelf Tool in Houdini**:
   - Open Houdini.
   - Go to `Windows > Shell Tools`.
   - Import the provided `houUtils.shelf` file from `HOUDINI_USER_PREF_DIR/toolbar/`.

6. **Use the Tools**:
   - The tools should now be available in Houdini's shelf under the `houUtils` section.

## Usage

1. **Texture ID Manager**:
   - Open the `Texture ID Manager` tool from the shelf.
   - Follow the prompts to set the texture ID names.

2. **Rename Texture**:
   - Open the `Rename Texture` tool from the shelf.
   - Follow the prompts to rename texture files according to the specified patterns.

## Contributing

If you find any issues or have suggestions for improvement, please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License.
