import requests
import re

UNICODE_EMOJI_BASE = "https://unicode.org/Public/emoji/"

def get_latest_version():
    index = requests.get(UNICODE_EMOJI_BASE).text
    versions = re.findall(r'href="([0-9]+\.[0-9]+)/"', index)
    versions = [tuple(map(int, v.split("."))) for v in versions]
    latest = max(versions)
    return ".".join(map(str, latest))

def download_file(url):
    r = requests.get(url)
    r.encoding = "utf-8"
    return r.text.splitlines()

def parse_emoji_test(lines):
    emoji = set()
    pattern = re.compile(r";\s*(fully-qualified|minimally-qualified|unqualified)\s*#\s*(\S+)")
    for line in lines:
        m = pattern.search(line)
        if m:
            emoji.add(m.group(2))
    return emoji

def parse_sequences(lines):
    emoji = set()
    seq_pattern = re.compile(r"^([0-9A-F ]+)\s+;\s+\S+\s+#\s+(\S+)")
    for line in lines:
        m = seq_pattern.match(line)
        if m:
            cps = m.group(1).split()
            emoji.add("".join(chr(int(cp, 16)) for cp in cps))
    return emoji

def write_output(all_emoji):
    with open("emoji_merged.txt", "w", encoding="utf-8") as f:
        f.write("# MERGED UNICODE EMOJI SET\n")
        f.write("# Includes all emoji from Unicode 15.1 + 16.0 (and future versions)\n\n")
        for e in sorted(all_emoji):
            f.write(e + "\n")
    print("emoji_merged.txt created!")

if __name__ == "__main__":
    print("Detecting latest Unicode emoji version...")
    version = get_latest_version()
    print(f"Latest version detected: {version}")

    base = f"{UNICODE_EMOJI_BASE}{version}/"

    print("Downloading emoji data files...")
    emoji_test = download_file(base + "emoji-test.txt")
    emoji_sequences = download_file(base + "emoji-sequences.txt")
    emoji_zwj = download_file(base + "emoji-zwj-sequences.txt")
    emoji_variation = download_file(base + "emoji-variation-sequences.txt")

    print("Parsing files...")
    set_test = parse_emoji_test(emoji_test)
    set_seq = parse_sequences(emoji_sequences)
    set_zwj = parse_sequences(emoji_zwj)
    set_var = parse_sequences(emoji_variation)

    all_emoji = set_test | set_seq | set_zwj | set_var

    print(f"Total emoji collected: {len(all_emoji)}")
    write_output(all_emoji)
    print("Done!")
