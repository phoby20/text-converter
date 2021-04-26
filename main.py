import os,sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from bs4 import BeautifulSoup
import codecs
import shutil


cnt = 0
home_path = ''
output = ''
before_text = ''
after_text = ''


def readWrite(file_path, outputFile, *args):
    global before_text
    global after_text
    edit_list = []
    # find_starting = 'https://shuppanbunka.heteml.jp/'
    # find_ending = 'https://shuppanbunka.heteml.net/'
    find_starting = before_text
    find_ending = after_text

    with open(file_path, 'r', encoding=args[0], errors='ignore') as f:
        fl = f.read()
        result_list = fl.split('\n')
        for item in result_list:
            if find_starting in item:
                # cnt += 1
                item = item.replace(find_starting, find_ending)
            edit_list.append(item)
    # 실제파일 생성하기
    with open(outputFile, mode='w', encoding=args[0]) as l:
        for line in edit_list:
            l.write(line)
            l.write('\n')



def ChangeText(dir, filename):
    global cnt
    file_path = os.path.join(dir, filename)
    outputFile = os.path.join(output, filename)

    find_starting = before_text
    find_ending = after_text
    edit_list = []

    name, ext = os.path.splitext(filename)
    if ext == '.dwt':
        readWrite(file_path, outputFile, 'utf-8')
    elif ext == '.html':
        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                fl = f.read()
                soup = BeautifulSoup(fl, 'html.parser')
                soup_pretty = soup.prettify()
                result_list = soup_pretty.split('\n')
                for item in result_list:
                    if find_starting in item:
                        # print(file_path, item)
                        cnt += 1
                        item = item.replace(find_starting, find_ending)
                    edit_list.append(item)
            # 실제파일 생성하기
            with open(outputFile, mode='w', encoding='utf-8') as l:
                for line in edit_list:
                    l.write(line)
                    l.write('\n')
        except UnicodeDecodeError:
            shutil.copyfile(file_path, outputFile)
    elif ext == '.pm':
        readWrite(file_path, outputFile, 'utf-8')
    elif ext == '.css':
        readWrite(file_path, outputFile, 'utf-8')
    elif ext == '.jpg' or ext == '.mp4' or ext == '.flv' or ext == '.swf' or ext == '.gif' or ext == '.jpeg':
        shutil.copyfile(file_path, outputFile)
    elif ext == '.png':
        shutil.copyfile(file_path, outputFile)
        print(file_path, outputFile)
    else:
        try:
            readWrite(file_path, outputFile, 'cp932')
        except UnicodeDecodeError:
            shutil.copyfile(file_path, outputFile)

# フォルダ指定の関数
def dirdialog_clicked():
    global home_path
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = filedialog.askdirectory(initialdir = iDir)

    home_path = iDirPath
    entry1.set(iDirPath)

# ファイル指定の関数
def dirdialog_clicked2():
    global output
    iDir2 = os.path.abspath(os.path.dirname(__file__))
    iDirPath2 = filedialog.askdirectory(initialdir=iDir2)
    output = iDirPath2
    entry2.set(iDirPath2)

# # ファイル指定の関数
# def filedialog_clicked():
#     fTyp = [("", "*")]
#     iFile = os.path.abspath(os.path.dirname(__file__))
#     iFilePath = filedialog.askopenfilename(filetype = fTyp, initialdir = iFile)
#     entry2.set(iFilePath)

# 実行ボタン押下時の実行関数
def conductMain():
    global before_text
    global after_text
    text = ""

    dirPath = entry1.get()
    dirPath2 = entry2.get()
    dirPath3 = entry3.get()
    before_text = dirPath3
    dirPath4 = entry4.get()
    after_text = dirPath4
    # filePath = entry2.get()

    for (path, dirs, files) in os.walk(home_path):
        for file in files:
            new_path = os.path.join(path, file)
            ChangeText(path, file)
    print('変更数：', cnt)
    if cnt:
        text += "変更完了" + "\n"
        text += "変更数：" + str(cnt)
    if text:
        messagebox.showinfo("info", text)

def exit():
    sys.exit()
if __name__ == "__main__":

    # rootの作成
    root = Tk()
    root.title("ファイル内の文字変換tool")
    root.resizable(width=False, height=False)

    # Frame0の作成
    frame0 = ttk.Frame(root, padding=10)
    frame0.grid(row=0, column=1, sticky=E)

    # Frame1の作成
    frame1 = ttk.Frame(root, padding=10)
    frame1.grid(row=2, column=1, sticky=E)

    # 「フォルダ参照」ラベルの作成
    IDirLabel = ttk.Label(frame1, text="原本フォルダ：", padding=(5, 2))
    IDirLabel.pack(side=LEFT)

    # 「フォルダ参照」エントリーの作成
    entry1 = StringVar()
    IDirEntry = ttk.Entry(frame1, textvariable=entry1, width=30)
    IDirEntry.pack(side=LEFT)

    # 「フォルダ参照」ボタンの作成
    IDirButton = ttk.Button(frame1, text="参照", command=dirdialog_clicked)
    IDirButton.pack(side=LEFT)

    # Frame2の作成
    frame2 = ttk.Frame(root, padding=10)
    frame2.grid(row=3, column=1, sticky=E)

    # Frame3の作成
    frame3 = ttk.Frame(root, padding=10)
    frame3.grid(row=4, column=1, sticky=E)

    # Frame4の作成
    frame4 = ttk.Frame(root, padding=10)
    frame4.grid(row=5, column=1, sticky=E)

    # Frame0の作成
    frame0 = ttk.Frame(root, padding=10)
    frame0.grid(row=0, column=1, sticky=W)
    context = ttk.Label(frame0, text="本toolはテキストファイル内の文字を変換するtoolです。\n 原本フォルダ内の全てのファイルを検索して「変更後の文字」に変換し、\n保存先フォルダにコピーを保存します。"
                                     "\n「変更前の文字」に該当されないファイルがある場合はそのままコピーされます。", anchor=W)
    context.pack(side=RIGHT)


    # 「ファイル参照」ラベルの作成
    IFileLabel = ttk.Label(frame2, text="保存先フォルダ：", padding=(5, 2))
    IFileLabel.pack(side=LEFT)

    # 「フォルダ参照2」エントリーの作成
    entry2 = StringVar()
    IFileEntry = ttk.Entry(frame2, textvariable=entry2, width=30)
    IFileEntry.pack(side=LEFT)

    # 「ファイル参照」ボタンの作成
    IFileButton = ttk.Button(frame2, text="参照", command=dirdialog_clicked2)
    IFileButton.pack(side=LEFT)

    before_moji_label = ttk.Label(frame3, text="変更前の文字：")
    before_moji_label.pack(side=LEFT)

    # 「フォルダ参照3」エントリーの作成
    entry3 = StringVar()
    IDirEntry3 = ttk.Entry(frame3, textvariable=entry3, width=45)
    IDirEntry3.pack(side=LEFT)


    after_moji_label = ttk.Label(frame4, text="変更後の文字：")
    after_moji_label.pack(side=LEFT)

    # 「フォルダ参照4」エントリーの作成
    entry4 = StringVar()
    IDirEntry4 = ttk.Entry(frame4, textvariable=entry4, width=45)
    IDirEntry4.pack(side=LEFT)


    # Frame5の作成
    frame5 = ttk.Frame(root, padding=10)
    frame5.grid(row=6, column=1, sticky=E)
    copyright = ttk.Label(frame5, text="ver1.0 by kwansung" + "\n" + "制作日：2021.04.26")
    copyright.pack(side=LEFT)

    # Frame6の作成
    frame6 = ttk.Frame(root, padding=10)
    frame6.grid(row=7,column=1,sticky=W)

    # 実行ボタンの設置
    button1 = ttk.Button(frame6, text="実行", command=conductMain)
    button1.pack(fill = "x", padx=50, side = "left")

    # キャンセルボタンの設置
    button2 = ttk.Button(frame6, text=("閉じる"), command=exit)
    button2.pack(fill = "x", padx=50, side = "left")

    root.mainloop()