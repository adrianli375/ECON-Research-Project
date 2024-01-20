# --- this script gets the date of extreme weather dates 
# --- where either the red/black rainstorm signal is hoisted
# --- or the Special Announcement on Flooding in the northern New Territories is issued

from datetime import datetime
import requests

def get_rainstorm_dates():
    output = []
    response = requests.get('https://www.hko.gov.hk/dps/wxinfo/climat/warndb/rstorm.dat?s=15663')
    response_text = response.text
    raw_list = response_text.split('\n')
    for item in raw_list:
        dates = get_date_from_rainstorm_raw_string(item)
        for date in dates:
            if date not in output:
                output.append(date)
    return output


def get_date_from_rainstorm_raw_string(s: str):
    sub_list = s.split('\t')
    try:
        start_year, start_month, start_date = int(sub_list[1]), int(sub_list[2]), int(sub_list[3])
        end_year, end_month, end_date = int(sub_list[6]), int(sub_list[7]), int(sub_list[8])
        start_datetime = datetime(start_year, start_month, start_date)
        end_datetime = datetime(end_year, end_month, end_date)
        return list(set([start_datetime, end_datetime]))
    except IndexError:
        return []


def get_flooding_dates():
    output = []
    response = requests.get('https://www.hko.gov.hk/dps/wxinfo/climat/warndb/nf.dat?s=14463')
    response_text = response.text
    raw_list = response_text.split('\n')
    for item in raw_list:
        dates = get_date_from_flooding_raw_string(item)
        for date in dates:
            if date not in output:
                output.append(date)
    return output


def get_date_from_flooding_raw_string(s: str):
    sub_list = s.split('\t')
    try:
        start_year, start_month, start_date = int(sub_list[0]), int(sub_list[1]), int(sub_list[2])
        end_year, end_month, end_date = int(sub_list[5]), int(sub_list[6]), int(sub_list[7])
        start_datetime = datetime(start_year, start_month, start_date)
        end_datetime = datetime(end_year, end_month, end_date)
        return list(set([start_datetime, end_datetime]))
    except ValueError:
        return []


def get_extreme_weather_date_list():
    rainstorm_date_list = get_rainstorm_dates()
    flooding_date_list = get_flooding_dates()
    return sorted(list(set(rainstorm_date_list + flooding_date_list)))
