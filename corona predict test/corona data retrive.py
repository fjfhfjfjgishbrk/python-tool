import requests
from bs4 import BeautifulSoup
import datetime
import plotly.graph_objects as go
import time as t
from scipy.optimize import curve_fit
import numpy as np


def sum_list(list, start, end):
    sum = 0
    for i in range(start, end):
        sum += list[i]
    return sum


def exponential(x, a, b):
    return a * np.exp(b * x)


def log_function(x, a, b):
    return a * np.log(x) + b


def growth_rate(t, a, b, type):
    if type == "log":
        return 1 / log_function(t, a, b) * a / t
    return 1 / exponential(t, a, b) * a * b * np.exp(b * t)


def best_function(x, a, b, c, type):
    if type == "log":
        return log_function(x, a, b)
    else:
        return exponential(x, a, b) + c


def abs_sum(list):
    list_sum = 0
    for i in list:
        list_sum += abs(i)
    return list_sum


# ---------- CONSTANTS ----------

daysToSearch = 60
daysToAverage = 7
growthRateAverageDays = 50
serialInterval = 4.7
predictionDays = 100
sigma_range = 20
sigma_intensity = 0.11

# ---------------------------------

time = datetime.datetime.now()
oneDay = datetime.timedelta(days=1)
time = time - oneDay
total_cases = []
dates = []
averageTime = []

for a in range(daysToSearch):
    time_start = int(round(t.time() * 1000))
    res = requests.get(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/" + time.strftime(
            "%m-%d-%Y") + ".csv")
    soup = BeautifulSoup(res.text, "html.parser")

    raw_data = soup.text.strip().split("\n")
    raw_data.pop(0)
    countries_cases = {}
    for countries in raw_data:
        i = countries.split(",")
        for j in i:
            if len(j) == 0:
                continue
            elif j[0] == " ":
                i.remove(j)
        if i[3] not in countries_cases:
            countries_cases[i[3]] = int(i[7])
        else:
            countries_cases[i[3]] += int(i[7])
    total_cases.append(countries_cases)
    dates.append(time.strftime("%y-%m-%d"))
    daysLeft = daysToSearch - a - 1
    averageTime.append(int(round(t.time() * 1000)) - time_start)
    if len(averageTime) > 15:
        averageTime.pop(0)
    print("Data from " + time.strftime("%m-%d-%Y") + " retrieved, " + str(daysLeft) + " days left, estimated time "
                                                                                      "left: " + str(round(sum(
        averageTime) / len(averageTime) * daysLeft / 1000, 4)) + "s")
    time = time - oneDay

new_cases_graph = go.Figure()
total_cases_graph = go.Figure()
prediction_graph = go.Figure()

total_dates = dates.copy()

for i in range(daysToAverage - 1):
    dates.pop()
dates = dates[::-1]

predict_days = []
prediction_date = datetime.datetime.now()

for i in range(predictionDays):
    predict_days.append(prediction_date)
    prediction_date += oneDay

country_searched = []

while True:

    print("---------------------------------------------------")
    while True:
        country_to_search = input("Type country to search: ")
        if country_to_search in list(total_cases[0].keys()):
            break
        else:
            print("Country not found.")

    # graphing new cases
    add_cases = []

    for i in range(0, daysToSearch - 1):
        add_cases.append(total_cases[i][country_to_search] - total_cases[i + 1][country_to_search])

    average_days = []

    for i in range(1, len(add_cases) - daysToAverage + 2):
        average_days.append(round(sum_list(add_cases, i - 1, i + daysToAverage - 1) / 3))

    average_days = average_days[::-1]

    new_cases_graph.add_bar(
        x=dates,
        y=average_days,
        name=country_to_search
    )

    # graphing total cases

    country_total_cases = []

    for i in range(len(add_cases)):
        country_total_cases.append(total_cases[i][country_to_search])

    graph_sigma = np.ones(len(country_total_cases))
    for i in range(sigma_range):
        graph_sigma[-sigma_range+i] = pow(1 + sigma_intensity, i)
        graph_sigma[sigma_range-i] = pow(1 - sigma_intensity, i)

    # calculate best curve fit (Ae^bt)

    # test with constant

    exp_country_total_cases = country_total_cases.copy()
    for i in range(len(exp_country_total_cases)):
        exp_country_total_cases[i] -= country_total_cases[-1] - 3

    exp_pars, exp_cov = curve_fit(f=exponential, xdata=range(len(country_total_cases), 0, -1),
                                  ydata=country_total_cases,
                                  p0=[1, 0],
                                  bounds=(-np.inf, np.inf),
                                  sigma=graph_sigma)
    exp_stdevs = np.sqrt(np.diag(exp_cov))
    exp_res = country_total_cases - exponential(range(len(country_total_cases), 0, -1), *exp_pars)
    exp_const = 0

    # calculate best curve fit (b + a * ln(t))

    log_pars, log_cov = curve_fit(f=log_function, xdata=range(len(country_total_cases), 0, -1),
                                  ydata=country_total_cases,
                                  p0=[1, 1],
                                  bounds=(-np.inf, np.inf),
                                  sigma=graph_sigma)
    log_stdevs = np.sqrt(np.diag(log_cov))
    log_res = country_total_cases - log_function(range(len(country_total_cases), 0, -1), *log_pars)

    # choose best fit

    if abs_sum(exp_res) < abs_sum(log_res):
        best_pars = exp_pars
        best_stdevs = exp_stdevs
        best_const = exp_const
        best_type = "exp"
    else:
        best_pars = log_pars
        best_stdevs = log_stdevs
        best_const = 0
        best_type = "log"

    print(abs_sum(exp_res), abs_sum(log_res))

    time_growth_rate = []
    for i in range(1, growthRateAverageDays + 1):
        time_growth_rate.append(
            growth_rate(len(country_total_cases) - growthRateAverageDays + i, *best_pars, best_type))
    average_growth_rate = sum(time_growth_rate) / growthRateAverageDays
    double_time = np.log(2) / average_growth_rate
    reproduction_number = np.exp(average_growth_rate * serialInterval)
    print("Reproduction number: {0}".format(reproduction_number))
    print("Double time: {0}".format(double_time))

    total_cases_graph.add_trace(go.Scatter(
        x=total_dates,
        y=country_total_cases,
        name=country_to_search,
        connectgaps=True,
        line=dict(shape="spline"),
        hovertext="Reproduction number: {0}\n Double time: {1} days".format(round(reproduction_number, 4),
                                                                            round(double_time))
    ))

    # prediction graph

    prediction_date = datetime.datetime.now()

    predict_avg_cases = []
    predict_max = []
    predict_min = []
    hover_text = []

    for i in range(1, predictionDays + 1):
        predict_avg_cases.append(round(best_function(daysToSearch + i, *best_pars, best_const, best_type)))
        predict_max.append(round(best_function(daysToSearch + i, *(best_pars + best_stdevs), best_const, best_type)))
        predict_min.append(round(best_function(daysToSearch + i, *(best_pars - best_stdevs), best_const, best_type)))
        hover_text.append("Max: {0}, Min: {1}".format(round(best_function(daysToSearch + i, *(best_pars + best_stdevs), best_const, best_type)),
                                                      round(best_function(daysToSearch + i, *(best_pars - best_stdevs), best_const, best_type))))

    prediction_graph.add_trace(go.Scatter(
        x=predict_days,
        y=predict_avg_cases,
        name=country_to_search,
        connectgaps=True,
        line=dict(shape="spline", dash="dot"),
        hovertext=hover_text
    ))

    prediction_graph.add_trace(go.Scatter(
        x=predict_days + predict_days[::-1],
        y=predict_max + predict_min[::-1],
        fill='toself',
        name="{0} cases range".format(country_to_search),
    ))

    print("Added " + country_to_search)
    country_searched.append(country_to_search)
    print("Total countries: " + ", ".join(country_searched))
    askDone = input("Type 'd' if done or type anything else to add country: ")
    if askDone == "d":
        break

new_cases_graph.show()
total_cases_graph.show()
prediction_graph.show()
