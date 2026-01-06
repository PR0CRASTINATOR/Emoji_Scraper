import requests
import re

URLS = {
    "emoji_test": "https://unicode.org/Public/emoji/15.1/emoji-test.txt",
    "emoji_sequences": "https://unicode.org/Public/emoji/15.1/emoji-sequences.txt",
    "emoji_zwj": "https://unicode.org/Public/emoji/15.1/emoji-zwj-sequences.txt",
    "emoji_variation": "https://unicode.org/Public/emoji/15.1/emoji-variation-sequences.txt"
}

def download_files():
    data = {}
    for name, url in URLS.items():
        print(f"Downloading {name}...")
        r = requests.get(url)
        r.encoding = "utf-8"
        data[name] = r.text.splitlines()
    return data

def parse_emoji_test(lines):
    categories = {}
    current_group = None
    current_subgroup = None

    emoji_pattern = re.compile(r"; fully-qualified\s+#\s+(\S+)\s")

    for line in lines:
        if line.startswith("# group:"):
            current_group = line.replace("# group:", "").strip()
            categories[current_group] = {}
        elif line.startswith("# subgroup:"):
            current_subgroup = line.replace("# subgroup:", "").strip()
            categories[current_group][current_subgroup] = []
        elif "; fully-qualified" in line:
            match = emoji_pattern.search(line)
            if match:
                emoji = match.group(1)
                categories[current_group][current_subgroup].append(emoji)

    return categories

def parse_sequences(lines):
    sequences = []
    seq_pattern = re.compile(r"^([0-9A-F ]+)\s+;\s+\S+\s+#\s+(\S+)")

    for line in lines:
        match = seq_pattern.match(line)
        if match:
            codepoints = match.group(1).split()
            emoji = "".join(chr(int(cp, 16)) for cp in codepoints)
            sequences.append(emoji)

    return sequences

def parse_zwj(lines):
    zwj_list = []
    seq_pattern = re.compile(r"^([0-9A-F ]+)\s+;\s+\S+\s+#\s+(\S+)")

    for line in lines:
        match = seq_pattern.match(line)
        if match:
            codepoints = match.group(1).split()
            emoji = "".join(chr(int(cp, 16)) for cp in codepoints)
            zwj_list.append(emoji)

    return zwj_list

def write_output(categories, sequences, zwj_list):
    with open("emoji_archive.txt", "w", encoding="utf-8") as f:
        f.write("# COMPLETE EMOJI ARCHIVE\n")
        f.write("# Generated from Unicode 15.1 data files\n\n")

        for group, subgroups in categories.items():
            f.write(f"\n## {group}\n")
            for subgroup, emojis in subgroups.items():
                f.write(f"\n### {subgroup}\n")
                f.write(" ".join(emojis) + "\n")

        f.write("\n\n## Additional Sequences\n")
        f.write(" ".join(sequences) + "\n")

        f.write("\n\n## ZWJ Sequences\n")
        f.write(" ".join(zwj_list) + "\n")

    print("emoji_archive.txt has been created!")

if __name__ == "__main__":
    print("Starting...")
    data = download_files()
    print("Downloaded files.")
    categories = parse_emoji_test(data["emoji_test"])
    print("Parsed emoji-test.")
    sequences = parse_sequences(data["emoji_sequences"])
    print("Parsed sequences.")
    zwj_list = parse_zwj(data["emoji_zwj"])
    print("Parsed ZWJ sequences.")
    write_output(categories, sequences, zwj_list)
    print("Done!")
