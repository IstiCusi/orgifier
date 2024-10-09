# VimWiki to Neorg Converter

This script converts VimWiki files to Neorg format. It handles the conversion of
headers, links, and code blocks, preserving the directory structure and properly
formatting the content to adhere to Neorg syntax. The script recursively processes
the files and creates corresponding Neorg files in the specified output directory.

## Usage

To run the script, ensure you have Python and the necessary dependencies installed.

### Requirements

- Python 3.x
- `regex` module

You can install the necessary dependencies with:

```
pip install regex
```

### Example Execution

To convert VimWiki files from `~/.vimwiki/` to Neorg files in `~/.notes/`, run the following:

```python
# Example execution
convert_vimwiki_to_neorg("~/.vimwiki/", "~/.notes/")
```

This will recursively traverse the VimWiki directory and convert each `.wiki` file to Neorg format.

### License

This project is licensed under the MIT License. See the LICENSE file for more details.

### Author

Stephan Strauss
