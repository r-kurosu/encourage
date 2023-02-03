import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials

UA_infra = "https://docs.google.com/spreadsheets/d/1NqGG-FQHLYsIPZRq-Ju0INEc-V12PXcLauyq103TmkM/edit#gid=686231199"

def get_authenticated_service():
    # # OAuth2認証を使用してGoogleアカウントにアクセス
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(credentials)

    return client


def access_ss(client):
    # # スプレッドシートのURLまたはIDを指定してスプレッドシートを開く
    spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1NqGG-FQHLYsIPZRq-Ju0INEc-V12PXcLauyq103TmkM/edit#gid=686231199')

    # # シート名またはインデックスでワークシートを取得
    worksheet = spreadsheet.worksheet("【触らない】会員データ")

    return worksheet


def get_no_apply_entors():
    client = get_authenticated_service()
    worksheet = access_ss(client)
    
    
    # # 全てのセルの値を取得し、dfに格納
    all_data = worksheet.get_all_values()
    df = pd.DataFrame(all_data[2:], columns=all_data[1])
    df = df.drop(df.columns[20:], axis=1)

    # mask = df.iloc[:, 16] == 'いいえ' # 16列目の「申請済み」が「はい」以外の行を抽出
    # df_no_apply_list = df[mask]
    mask = df.iloc[:, 16] == 'はい' # 16列目の「申請済み」が「はい」以外の行を抽出
    df_no_apply_list = df[~mask]
    df_no_apply_list = df_no_apply_list.reset_index(drop=True)

    no_apply_entors = df_no_apply_list.iloc[:, 3].tolist()
    print(no_apply_entors)

    return no_apply_entors


def get_all_entors():
    client = get_authenticated_service()
    worksheet = access_ss(client)
    
    # # 全てのセルの値を取得し、dfに格納
    all_data = worksheet.get_all_values()
    df = pd.DataFrame(all_data[2:], columns=all_data[1])
    df = df.drop(df.columns[4:], axis=1)

    all_entors = df.iloc[:, 3].tolist()
    print(all_entors)
    print(len(all_entors))
    
    return all_entors


def output_mail_list(mail_list):
    client = get_authenticated_service()
    spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1NqGG-FQHLYsIPZRq-Ju0INEc-V12PXcLauyq103TmkM/edit#gid=686231199')
    worksheet = spreadsheet.worksheet("mail_list")
    worksheet.clear()
    
    for target in mail_list:
        worksheet.append_row([target[0], target[1]])
    
    return


def output_25entors_list(entors_list, sheet_name):
    client = get_authenticated_service()
    spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1NqGG-FQHLYsIPZRq-Ju0INEc-V12PXcLauyq103TmkM/edit#gid=686231199')
    worksheet = spreadsheet.worksheet(sheet_name)
    worksheet.clear()
    
    worksheet.append_row(entors_list)
    
    return


if __name__ == '__main__':
    # get_no_apply_entors()
    get_all_entors()