from pydub import AudioSegment
from pathlib import Path
import re


def get_songs(name_file):
    """ считывание cue файла и возврата массива всех композиций
    :param name_file: имя файла с содержинием всех композиций в mp3 файле
    :type name_file: str
    :rtype: list
    :return: array
    """
    with open(name_file, "r", encoding="cp1250") as f:
        line = f.readlines()
        line = line[3:]
        len_song = int(len(line) / 3)
        songs = []

        for number_son in range(len_song):
            son = line[number_son * 3: number_son * 3 + 3]
            son = son[1:]
            son[0] = son[0].strip()[6:].strip("\"")
            time = re.findall(r'(\d\d):(\d\d):\d\d', son[1])
            son[1] = (int(time[0][0]) * 60 + int(time[0][1])) * 1000
            songs.append(son)
    return songs


def slice(mass, file):
    """ создает обрезаные mp3 компоциции
    :param mass:
    :type mass: list
    :param file: путь к файлам без суфикса
    :type file: str
    """
    song = AudioSegment.from_mp3(file + '.mp3')
    for i in range(len(mass) - 1):
        mp = song[mass[i][1]: mass[i + 1][1]]
        mp.export(mass[i][0] + ".mp3", format="mp3")
        print("Песня {} создана".format(mass[i][0]))
    mp = song[mass[-1][1]:]
    mp.export(mass[-1][0] + ".mp3", format="mp3")


def dell_files(file):
    """ Удаляет обработанные файлы
    :param file: путь к файлам без суфикса
    :type file: str
    """
    Path.unlink(Path(file + '.mp3'))
    Path.unlink(Path(file + '.cue'))


def mv_mp3():
    """ Перемещает все созданые файлы в папку mp3 """
    path_mp3 = Path.cwd().glob("*.mp3")
    path_replace = Path.cwd().joinpath("mp3")
    for path in path_mp3:
        path.replace(path_replace / path.name)


dir_files = Path("/media/prizrak/Новый том/musik/VA - TRANCEFFECT/VA - Tranceffect (2020)")
all_mp3_files = dir_files.glob("*.cue")
for i in all_mp3_files:
    file_name = str(i.with_suffix(''))
    songs = get_songs(file_name + '.cue')
    slice(songs, file_name)
    dell_files(file_name)
    mv_mp3()
