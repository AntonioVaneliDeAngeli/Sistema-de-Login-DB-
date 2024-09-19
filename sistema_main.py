import PySimpleGUI as sg
import mysql.connector
from datetime import datetime
from time import sleep

sg.theme('Reddit')

conexao = mysql.connector.connect(host='localhost', user='root', password='', database='contas')
cursor = conexao.cursor()

def login_tela():
    layout = [[sg.Text('Login')],
    [sg.Input(key=('login'))],
    [sg.Text('Senha')],
    [sg.Input(key=('senha'))],
    [sg.Button('Logar', key='logar'), sg.Button('Criar nova conta', key='criar')],
    [sg.Text('', key=('txt'))]
    ]
    return sg.Window('Login', layout=layout, finalize=True)

def criar_conta():
    layout = [
        [sg.Text('Usuario')],
        [sg.Input(key=('user_c'))],
        [sg.Text('Senha')],
        [sg.Input(key=('senha_c'))],
        [sg.Text('Email')],
        [sg.Input(key=('email'))],
        [sg.Button('Criar conta', key='criar_conta'), sg.Button('Voltar', key=('retornar'))],
        [sg.Text('', key=('txt_c'))]
    ]
    return sg.Window('Criar conta', layout=layout, finalize=True)

def tela_main():
    layout = [
        [sg.Button('Deslogar', key=('voltar'))]
        ]
    return sg.Window('Tela', layout=layout, finalize=True)

login, criar, tela = login_tela(), None, None

while True:
    janela, eventos, valores = sg.read_all_windows()
    if eventos == sg.WIN_CLOSED:
        break
    elif eventos == 'logar':
        cursor.execute(f'select user, senha from contas where user = "{valores["login"]}"')
        resultado = cursor.fetchall()
        try:
            if resultado[0][0] == valores['login'] and resultado[0][1] == valores['senha']:
                login.hide()
                tela = tela_main()
            else:
                print("53")
                janela['txt'].update('Usuario ou senha incorretos')

        except:
            print("53")
            janela['txt'].update('Usuario ou senha incorretos')

    elif eventos == 'voltar':
        tela.hide()
        login = login_tela()

    elif eventos == 'criar':
        login.hide()
        criar = criar_conta()

    elif eventos == 'retornar':
        criar.hide()
        login = login_tela()

    elif eventos == 'criar_conta':
        cursor.execute(f'select user from contas where user = "{valores["user_c"]}"')
        resultado1 = cursor.fetchall()
        cursor.execute(f'select email from contas where user = "{valores["email"]}"')
        resultado2 = cursor.fetchall()
        try:
            if resultado1[0][0] == valores['login']:
                janela['txt_c'].update('Esse usuario ja esta em uso')
            elif resultado2[0][0] == valores['email']:
                janela['txt_c'].update('Esse email ja esta em uso')
        except:
            hoje = datetime.now()
            cursor.execute(f'insert into contas (user, senha, email, data_criacao) values ("{valores["user_c"]}", "{valores["senha_c"]}", "{valores["email"]}", "{hoje.date()}")')
            conexao.commit()
            criar.hide()
            login = login_tela()
            sg.popup_ok('Sua conta foi criada com sucesso')