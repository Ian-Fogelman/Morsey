from flask import Flask, render_template, request
from flask import url_for

#from redis import Redis, RedisError
import os
import socket
import sqlite3
import time

app = Flask(__name__ , static_url_path='/static', static_folder="static")

def create():
    db_path = r'Morsey.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS MorseTable
            (Id INTEGER PRIMARY KEY,PlainText,CipherText, MsgDT)""")
    conn.commit()  # commit needed
    c.close()

def insert(pt,ct):
    db_path = r'Morsey.db'
    conn = sqlite3.connect(db_path)
    dt = time.strftime("%m/%d/%Y %H:%M:%S")
    c = conn.cursor()
    c.execute("""INSERT INTO MorseTable (PlainText, CipherText, MsgDT)
              values('""" + str(pt) + """','""" + str(ct) + """', '""" + dt + """')""")
    conn.commit()  # commit needed
    c.close()


def returnrecs():
    db_path = r'Morsey.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    #create()
    #insert()
    #conn.commit()  # commit needed
    sql = "SELECT * FROM MorseTable"
    recs = c.execute(sql)
    top = '<table>'

    for row in recs:
        print(row)
        top = top + '<td>'+ str(row[0]) + '<td>'
    c.close()
    bottom = '</table>'
    print(top + bottom)
    return top + bottom


def decodeMorse(morse_code):
    ans = ''
    D = {'.-': 'A',
         '-...': 'B',
         '-.-.': 'C',
         '-..' : 'D',
         '.' : 'E',
         '..-.' : 'F',
         '--.' : 'G',
         '....' : 'H',
         '..' : 'I',
         '.---' : 'J',
         '-.-' : 'K',
         '.-..' : 'L',
         '--' : 'M',
         '-.' : 'N',
         '---' : 'O',
         '.--.' : 'P',
         '--.-' : 'Q',
         '.-.' : 'R',
         '...' : 'S',
         '-' : 'T',
         '..-' : 'U',
         '...-' : 'V',
         '.--' : 'W',
         '-..-' : 'X',
         '-.--' : 'Y',
         '--..' : 'Z',
         '.----' : '1',
         '..---' : '2',
         '...--' : '3',
         '....-' : '4',
         '.....' : '5',
         '-....' : '6',
         '--...' : '7',
         '---..' : '8',
         '----.' : '9',
         '-----' : '0',
         '...---...' : 'SOS',
         '-.-.--' : 'EE',
         '-.-.--' : '!',
         '.-.-.-' : '.'}
    mcs = list(morse_code.split(' '))
    i = 0
    codeind = False
    for x in mcs:
        if(x == '|'):
            ans = ans + ' '
        elif(x == ' '):
            ans = ans + ' '
            codeind = True
        elif(x != ''):
            ans = ans + D[x]
            codeind = True
        elif(x == '' and (i + 1) < len(mcs) and mcs[i + 1] == '' and codeind == True):
            ans = ans + ' '
        i = i + 1
    if(ans[-1:] == ' '):
        ans = ans[:-1]
    return ans



def encodeMorse(plain_text):
    ans = ''
    D = {'A' : '.-',
         'B' : '-...',
         'C' : '-.-.',
         'D' : '-..',
         'E' : '.',
         'F' : '..-.',
         'G' : '--.',
         'H' : '....',
         'I' : '..',
         'J' : '.---',
         'K' : '-.-',
         'L' : '.-..',
         'M' : '--',
         'N' : '-.',
         'O' : '---',
         'P' : '.--.',
         'Q' : '--.-',
         'R' : '.-.',
         'S' : '...',
         'T' : '-',
         'U' : '..-',
         'V' : '...-',
         'W' : '.--',
         'X' : '-..-',
         'Y' : '-.--',
         'Z' : '--..',
         '1' : '.----',
         '2' : '..---',
         '3' : '...--',
         '4' : '....-',
         '5' : '.....',
         '6' : '-....',
         '7' : '--...',
         '8' : '---..',
         '9' : '----.',
         '0' : '-----',
         'SOS' : '...---...',
         'EE' : '-.-.--',
         '!' : '-.-.--',
         '.' : '.-.-.-'}
    #mcs = list(plain_text.split(' '))
    mcs = [*plain_text]
    i = 0
    codeind = False
    for x in mcs:
        if(x == ' '):
            ans = ans + ' | '
            codeind = True
        elif(x != ''):
            ans = ans + D[x.upper()] + ' '
            codeind = True
        elif(x == '' and (i + 1) < len(mcs) and mcs[i + 1] == '' and codeind == True):
            ans = ans + ' '
        i = i + 1
    if(ans[-1:] == ' '):
        ans = ans[:-1]
    return ans

X = decodeMorse(".-")
morse_code = ".-"
@app.route('/hello/<user>')
def hello_name(user):
   return render_template('hello.html', name = user)

@app.route('/history/')
def history():
    ##myhisttable = returnrecs()
    db_path = r'Morsey.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = "SELECT * FROM MorseTable"
    recs = c.execute(sql)
    myhisttable = []
    for row in recs:
        #print(row)
        myhisttable.append(row)
    c.close()

    return render_template('history.html', histtable = myhisttable)


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/encode/<plaintext>')
def encode_message(plaintext):
   a = encodeMorse(plaintext)
   b = plaintext
   return render_template('encode.html', morsecode = a, originaltext = b)


@app.route('/encode/<plaintext>', methods=['POST'])
def encode_messageB(plaintext):
   plaintext = request.form['mcode']
   a = encodeMorse(plaintext)
   b = plaintext
   insert(a, b)
   return render_template('encode.html', morsecode = a, originaltext = b)



@app.route('/decode/<morsecode>')
def decode_message(morsecode):
   a = decodeMorse(morsecode)
   b = morsecode
   return render_template('decode.html', morsecode = a, originaltext = b)


@app.route('/decode/<morsecode>', methods=['POST'])
def decode_messageB(morsecode):
   morsecode = request.form['mcode']
   a = decodeMorse(morsecode)
   b = morsecode
   insert(a,b)
   return render_template('decode.html', morsecode = a, originaltext = b)

#http://localhost/sidebar
@app.route("/sidebar")
def sidebar():
    return render_template('sidebar.html')

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
