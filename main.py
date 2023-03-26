import requests
from bs4 import BeautifulSoup


def get_web_data():
    url = "https://morsecode.world/international/morse2.html"
    web_response = requests.get(url=url)
    web_response.raise_for_status()
    web_data = web_response.text
    return web_data


def scrap_web_data():
    return BeautifulSoup(markup=get_web_data(), features="html.parser")


def get_letters_nums_data(web_data):
    letters_nums_codes_list = []
    letter_tags = web_data.find_all(name="span", class_="morse tile")
    letter_tags = letter_tags[:36]
    letters_nums_list = [letters.text for letters in letter_tags]

    morse_code = web_data.select("table tr td", )
    for morse in morse_code:
        if morse_code.index(morse) % 2 != 0:
            if len(morse.get_text().split()) == 1:
                letters_nums_codes_list.append(morse.get_text())
    letters_nums_codes_list = letters_nums_codes_list[:36]
    letters_nums_data = {char: morse for char, morse in zip(letters_nums_list, letters_nums_codes_list)}
    return letters_nums_data


def get_punctuations_data(web_data):
    values = []
    punctuation_tags = web_data.find_all("table", id="punctuation")
    for tags in punctuation_tags:
        values = tags.text.split("\n\n\n")[1:]
    punctuation_marks, punctuation_morse_code = [marks.split()[0] for marks in values], [code.split()[-1] for code in
                                                                                         values]
    punctuations_data = {char: morse for char, morse in zip(punctuation_marks, punctuation_morse_code)}
    return punctuations_data


def get_non_latin_lets_data(web_data):
    val, accent_lets, accent_lets_morse = [], [], []
    non_latin_tags = web_data.find_all("table", id="accents")
    for tag in non_latin_tags:
        val = tag.findAllNext(name="td")
    accent_lets = ["".join(x.get_text().replace("\n", "")) for x in val if val.index(x) % 2 == 0]
    accent_lets_morse = ["".join(x.get_text()) for x in val if val.index(x) % 2 > 0]
    accent_lets, accent_lets_morse = accent_lets[:17], accent_lets_morse[:17]
    accent_data = {char: morse for char, morse in zip(accent_lets, accent_lets_morse)}
    return accent_data


def morse_code_data():
    global soup
    letter_nums, punctuations, non_latin = get_letters_nums_data(soup), get_punctuations_data(
        soup), get_non_latin_lets_data(soup)
    morse_codes_data = {**letter_nums, **punctuations, **non_latin}
    return morse_codes_data


def get_user_input():
    user_request = input("What would you like to convert?: ").upper().split()
    return user_request


def convert_to_morse_code(user_word):
    morse = ""
    for words in user_word:
        for letters in words:
            morse += f"{all_morse_codes_data[letters]} "
        morse += " / "
    print(morse)


get_web_data()
soup = scrap_web_data()
all_morse_codes_data = morse_code_data()
user_requested_word = get_user_input()
convert_to_morse_code(user_requested_word)
