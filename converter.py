"""
VimWiki to Neorg Converter
==========================

This script converts VimWiki files to Neorg format. It handles the conversion of
headers, links, and code blocks, preserving the directory structure and properly 
formatting the content to adhere to Neorg syntax. The script recursively processes 
the files and creates corresponding Neorg files in the specified output directory.

Author: Stephan Strauss
License: MIT License

MIT License
-----------

Copyright (c) 2024 Stephan Strauss

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os

import regex as re


def mkdir_p(path):
    """
    Creates directories recursively if they do not already exist.

    Args:
        path (str): The path to the directory to create.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def process_filename(link):
    """
    Processes the filename by replacing spaces with underscores and
    ensuring the file extension .norg.

     Args:
         link (str): The original filename or link.

     Returns:
         str: The processed filename with underscores and .norg extension.
    """
    if "." in link:
        name, ext = link.rsplit(".", 1)
    else:
        name, ext = link, "norg"

    name = name.replace(" ", "_")

    if ext != "norg":
        ext = "norg"

    return f"{name}.{ext}"


def convert_file(vimwiki_file, neorg_file):
    """
    Converts a VimWiki file to Neorg format by converting headers, links, and code blocks.

    Args:
        vimwiki_file (str): The path to the VimWiki file to convert.
        neorg_file (str): The path to save the converted Neorg file.
    """
    print(f"Converting file: {vimwiki_file}")

    with open(vimwiki_file, "r", encoding="utf-8") as input_file:
        content = input_file.read()

    converted_content = re.sub(
        r"^===\s*(.*?)\s*===", r"*** \1", content, flags=re.MULTILINE
    )
    converted_content = re.sub(
        r"^==\s*(.*?)\s*==", r"** \1", converted_content, flags=re.MULTILINE
    )
    converted_content = re.sub(
        r"^=\s*(.*?)\s*=", r"* \1", converted_content, flags=re.MULTILINE
    )

    converted_content = re.sub(
        r"\[\[(.*?)\]\]",
        lambda m: f"[{process_filename(m.group(1))}]{{{m.group(1)}}}",
        converted_content,
    )

    converted_content = re.sub(
        r"\[\[(.*?)\|(.*?)\]\]",
        lambda m: f"[{process_filename(m.group(1))}]{{{m.group(2)}}}",
        converted_content,
    )

    converted_content = re.sub(
        r"(\*+)\s*(.*?)\s*====*", r"\1 \2", converted_content, flags=re.MULTILINE
    )

    converted_content = re.sub(
        r"```(\w+)\n(.*?)```", r"@code \1\n\2\n@end", converted_content, flags=re.DOTALL
    )

    mkdir_p(os.path.dirname(neorg_file))

    with open(neorg_file, "w", encoding="utf-8") as output_file:
        output_file.write(converted_content)

    print(f"Converted file saved: {neorg_file}")


def traverse_and_convert(vimwiki_root, neorg_root):
    """
    Recursively walks through the VimWiki directory, converts each .wiki file to Neorg format,
    and saves it in the corresponding Neorg directory structure.

    Args:
        vimwiki_root (str): The root directory of the VimWiki files.
        neorg_root (str): The root directory to save the converted Neorg files.
    """
    for root, _, files in os.walk(vimwiki_root):
        for file in files:
            if file.endswith(".wiki"):
                vimwiki_file = os.path.join(root, file)
                relative_path = os.path.relpath(vimwiki_file, vimwiki_root)
                neorg_file = os.path.join(neorg_root, relative_path).replace(
                    ".wiki", ".norg"
                )
                convert_file(vimwiki_file, neorg_file)


def convert_vimwiki_to_neorg(vimwiki_root, neorg_root):
    """
    Main function to start the conversion process from VimWiki to Neorg.

    Args:
        vimwiki_root (str): The root directory of VimWiki files to convert.
        neorg_root (str): The root directory where the converted Neorg files will be saved.
    """
    if os.path.isdir(vimwiki_root) and os.path.isdir(neorg_root):
        print(f"Starting conversion from {vimwiki_root} to {neorg_root}")
        traverse_and_convert(vimwiki_root, neorg_root)
        print("Conversion completed!")
    else:
        print("One of the specified directories does not exist.")


# Example execution
#  ---> convert_vimwiki_to_neorg("~/.vimwiki/", "~/.notes/")
