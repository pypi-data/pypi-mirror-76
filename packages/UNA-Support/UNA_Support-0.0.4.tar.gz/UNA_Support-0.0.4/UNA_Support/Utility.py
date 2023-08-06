import cyrtranslit
import ping, socket
import time

from pynput.keyboard import Key, Controller

def LANGRusToCyrilik(TextRUS):
    TextRUS = str(TextRUS).decode('cp1251')
    TextRUS = unicode(TextRUS).encode('utf-8')
    TextCyrylik = cyrtranslit.to_latin(TextRUS, 'ru')

    return TextCyrylik

def una_autorefresh(self):
        keyb = Controller()

        keyb.press(Key.alt)
        keyb.press(Key.tab)
        keyb.release(Key.alt)
        keyb.release(Key.tab)

        time.sleep(0.5)
        keyb.press(Key.alt)
        keyb.press('r')
        keyb.release(Key.alt)
        keyb.release('r')
        keyb.press(Key.down)
        keyb.release(Key.down)
        keyb.press(Key.up)
        keyb.release(Key.up)

def ping_addr(hostname):
    msg_except = None
    try:
        ip_res = ping.do_one(hostname, timeout=2, psize=3)
        if ip_res == None:
            res = 1
        else:
            res = 0
        return res, msg_except
    except socket.error, e:
        print("Ping error:", e)
        msg_except = "Ping error:" + str(e)
        return -1, msg_except

def extract_str(text, _from, _until ='/'):
    """
    Extragerea portiunii de text din valoarea "text" indicata in parametru

    :param text: textul din care se va extrage valoarea
        :type text: string
    :param _from: inceputul extragerii
        :type _from: string
    :param _until: sfirsitul extragerii (implicit este valoarea '/')
        :type _until: string
    :return: se returneaza textul ce se afla intre "_from" si "_until"
        :type return: par1 string (-1: nu a fost gsit inceputul), par2 string (error text or 0 succes)
    """
    try:
        text = str(text)
        _from = str(_from)
        len_from = len(_from)
        _until = str(_until)

        if text.find(_from) != -1:
            start_ = text.find(_from) + len_from
            end_ = text[start_ + 1:].find(_until) + start_ + 1
            result_str = text[start_:end_]
        else:
            result_str = '-1'
        _except = '0'
    except Exception as ex:
        result_str = 'Error'
        _except = str(ex)
        pass

    return result_str, _except