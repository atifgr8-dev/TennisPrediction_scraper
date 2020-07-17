from bs4 import BeautifulSoup
import requests
import csv
import time
import re
import pandas as pd
import os
import xlwt


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def getSoupForRequest(year, month, day, t_p, excelFile):
    sheet_name = "Tab-"+str(t_p)
    sheet1 = sheet_creator(excelFile, sheet_name)
    file_name = year + '_' + month + '_' + day + '_' + 'tab-' + str(t_p) + '.csv'
    requests_url = 'http://www.tennisprediction.com/'
    params = {
        't_p': t_p,
        'year': year,
        'month': month,
        'day': day
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }

    res = requests.get(requests_url, params=params, headers=headers)
    time.sleep(2)
    soup = BeautifulSoup(res.content, 'lxml')
    all_tables = soup.select('#main_tur')
    # print(all_tables)
    row = 1
    for table in all_tables:
        tournament_name = table.select('td#main_tit')[0].text
        # tournament_description = table.select('#main_tour')[0].text
        all_matches = table.select('tr.match')
        all_matches = list(chunks(all_matches, 2))
        all_matches1 = table.select('tr.match1')
        all_matches1 = list(chunks(all_matches1, 2))
        # pass
        print("Tournament Name:", tournament_name)
        # print("Tournament Description:", tournament_description)
        # print("\n")
        counter = 1
        match_num = 1
        for idx_1, match in enumerate(all_matches):
            print("Match#:", idx_1+1)
            match_list = []
            match_list.append(tournament_name)
            ods_list = []
            fin_perc_list = []
            for tr_idx_1, tr in enumerate(match):

                player_name = ""
                country = ""
                rank = ""

                if tr_idx_1 == 0:
                    match_time = tr.select('td.main_time')[0].text.strip()
                    match_list.append(match_time)
                    print("Match Time:", match_time)
                player_name_ctr_rank_text = tr.select('td.main_player')[0].text.strip()
                player_names_list = player_name_ctr_rank_text.split("/")
                player_names_list = [player.split('(')[0] for player in player_names_list]
                player_name = " / ".join(player_names_list)
                match_list.append(player_name)

                players_countries_1 = [_country for _country in re.findall(r'\((.*?)\)', player_name_ctr_rank_text) if _country.isalpha()]
                players_countries_1 = " / ".join(players_countries_1)
                match_list.append(players_countries_1)

                players_ranks_1 = [_rank for _rank in re.findall(r'\((.*?)\)', player_name_ctr_rank_text) if _rank.isnumeric()]
                players_ranks_1 = " / ".join(players_ranks_1)
                match_list.append(players_ranks_1)
                player_sets = tr.select('td.main_res_f, td.main_res')
                player_sets = [(set_score.text.strip()).split("(")[0] for set_score in player_sets]
                match_list.extend(player_sets)

                main_odds_m = tr.select('td.main_odds_m')[0].text
                ods_list.append(main_odds_m)


                fin_perc = tr.select('td.main_perc')[0].text
                fin_perc_list.append(fin_perc)

                print("Player Name:", player_name)
                print("Main Odds m:", main_odds_m)
                print("Countries:", players_countries_1)
                print("Ranks:", players_ranks_1)
                print()
            match_list.extend(ods_list)
            match_list.extend(fin_perc_list)
            for col_id, col in enumerate(match_list):
                sheet1.write(row, col_id, col)
            row += 1


        for idx_1, match in enumerate(all_matches1):
            print("Match#:", idx_1+1)
            match_list = []
            match_list.append(tournament_name)
            ods_list = []
            fin_perc_list = []

            for tr_idx_1, tr in enumerate(match):
                player_name = ""
                country = ""
                rank = ""
                if tr_idx_1==0:
                    match_time = tr.select('td.main_time')[0].text.strip()
                    match_list.append(match_time)
                    print("Match Time:", match_time)
                player_name_ctr_rank_text = tr.select('td.main_player')[0].text.strip()
                player_names_list = player_name_ctr_rank_text.split("/")
                player_names_list = [player.split('(')[0] for player in player_names_list]
                player_name = " / ".join(player_names_list)
                match_list.append(player_name)

                players_countries_1 = [_country for _country in re.findall(r'\((.*?)\)', player_name_ctr_rank_text) if _country.isalpha()]
                players_countries_1 = " / ".join(players_countries_1)
                match_list.append(players_countries_1)

                players_ranks_1 = [_rank for _rank in re.findall(r'\((.*?)\)', player_name_ctr_rank_text) if _rank.isnumeric()]
                players_ranks_1 = " / ".join(players_ranks_1)
                match_list.append(players_ranks_1)

                player_sets = tr.select('td.main_res_f, td.main_res')
                player_sets = [(set_score.text.strip()).split("(")[0] for set_score in player_sets]
                match_list.extend(player_sets)

                main_odds_m = tr.select('td.main_odds_m')[0].text
                ods_list.append(main_odds_m)

                fin_perc = tr.select('td.main_perc')[0].text
                fin_perc_list.append(fin_perc)

                print("Player Name:", player_name)
                print("Main Odds m:", main_odds_m)
                print("Countries:", players_countries_1)
                print("Ranks:", players_ranks_1)
            match_list.extend(ods_list)
            match_list.extend(fin_perc_list)
            for col_id, col in enumerate(match_list):
                sheet1.write(row, col_id, col)
            row += 1
            excelFile.save("Final Data File" + day +"_" + month + '.xls')

def sheet_creator(excelFile, sheet_name):
    sheet1 = excelFile.add_sheet(sheet_name)
    for col in range(10):
        sheet1.col(col).width = 3000
    sheet1.write(0, 0, "Tournament Name")
    sheet1.write(0, 1, "Time")
    sheet1.write(0, 2, "Player-1")
    sheet1.write(0, 3, "Country")
    sheet1.write(0, 4, "Rank")
    sheet1.write(0, 5, "Round-1")
    sheet1.write(0, 6, "Round-2")
    sheet1.write(0, 7, "Round-3")
    sheet1.write(0, 8, "Round-4")
    sheet1.write(0, 9, "Round-5")
    sheet1.write(0, 10, "Round-6")


    sheet1.write(0, 11, "Player-2")
    sheet1.write(0, 12, "Country")
    sheet1.write(0, 13, "Rank")
    sheet1.write(0, 14, "Round-1")
    sheet1.write(0, 15, "Round-2")
    sheet1.write(0, 16, "Round-3")
    sheet1.write(0, 17, "Round-4")
    sheet1.write(0, 18, "Round-5")
    sheet1.write(0, 19, "Round-6")
    sheet1.write(0, 20, "O-1")
    sheet1.write(0, 21, "O-2")
    sheet1.write(0, 22, "Final Perc-1")
    sheet1.write(0, 23, "Final Perc-2")
    return sheet1


if __name__ == '__main__':
    excelFile = xlwt.Workbook(encoding="utf-8")
    year = '2020'
    month = '01'
    day = '16'
    # t_p = 1
    for tp in range(1, 5):
        getSoupForRequest(year, month, day, tp, excelFile)
