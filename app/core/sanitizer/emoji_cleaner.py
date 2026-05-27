import emoji
import re


def remove_emojis(text):
    return emoji.replace_emoji(text, replace='')


if __name__ == "__main__":
    sample = "🔥Marvel✨Edit🥵.mp4"

    cleaned = remove_emojis(sample)

    print(cleaned)