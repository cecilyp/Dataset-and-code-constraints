# Homework 04
# [Please replace this comment with your name]


"""
*** DESCRIBE YOUR CODE ORGANIZATION HERE ***
"""


#################### PLEASE  DO NOT MODIFY CODE HERE #####################
import sys, os, string
import math, random
import csv, json
from collections import Counter
# Please do not use other imports in this homework
##########################################################################
# *** PLEASE DEFINE ANY OTHER FUNCTIONS HERE ***


def load_data(file_path):
    '''
    :param file_path: String: relative file path to the text file containing the data
    :return: List of Dictionaries: containing json dictionary of each line in the file.
    '''
    d_studies_data = []
    fp = open(file_path)
    for line in fp:
        l = json.loads(line)
        d_studies_data.append(l)

    return d_studies_data


def get_variable_lists(data):
    NP = [line['NP'] for line in data]
    PG = [line['PG'] for line in data]
    SI = [line['SI'] for line in data]
    BP = [line['BP'] for line in data]
    SFT = [line['SFT'] for line in data]
    BMI = [line['BMI'] for line in data]
    age = [line['age'] for line in data]
    cls = [line['class'] for line in data]

    return NP, PG, SI, BP, SFT, BMI, age, cls


def summary_stats(data):

    var = get_variable_lists(data)

    summary = []
    for item in var:
        stats = {}
        sm = sum(item)
        num = len(item)
        mean = sm / num
        std = st_d(mean, num, item)
        maximum = max(item)
        minimum = min(item)
        stats['MEAN'] = mean
        stats['STD'] = std
        stats['MAX'] = maximum
        stats['MIN'] = minimum
        stats['COUNT'] = num
        summary.append(stats)

    return summary


def display_summary(summary):
    var = ['NP', 'PG', 'SI', 'BP', 'SFT', 'BMI', 'age', 'class']
    print("            %2s %8s %8s %8s %8s" % ("STD", "MEAN", "MIN", "MAX", "COUNT"))
    for i, colum in enumerate(summary):
        print("%6s %8.2f %8.2f %8s %8s %8s" % (var[i],colum["STD"], colum["MEAN"], colum["MIN"], colum["MAX"], colum["COUNT"]))
    print()
    return None


def st_d(mean, length, data):
    n = 1/(length - 1)
    summation = 0
    for num in data:
        x = (mean - num) ** 2
        summation = summation + x

    return math.sqrt(n*summation)


def flag_missing_values(data):
    total_missing = 0
    si = bmi = bp = pg = sft = 0

    d_clean = []
    for d in data:
        if d['SI'] == 0:
            d['SI'] = None
            total_missing += 1
            si += 1

        if d['BMI'] == 0.0:
            d['BMI'] = None
            total_missing += 1
            bmi += 1

        if d['BP'] == 0:
            d['BP'] = None
            total_missing += 1
            bp += 1

        if d['PG'] == 0:
            d['PG'] = None
            total_missing += 1
            pg += 1

        if d['SFT'] == 0:
            d['SFT'] = None
            total_missing += 1
            sft += 1

        # print(d)
        d_clean.append(d)
    print("Total Missing: ", total_missing)
    print("SI Missing: ", si)
    print("BMI Missing: ", bmi)
    print("BP Missing: ", bp)
    print("PG Missing: ", pg)
    print("SFT Missing: ", sft, "\n")
    return d_clean,total_missing


def listwise_deletion(data):
    c_data = []
    for line in data:
        stop = False
        for key, value in line.items():
            if value is None:
                stop = True
                break
        if not stop:
            c_data.append(line)

    return c_data


def correlation_coefficient(X,Y):
    """Compute and return (as a float) the Pearson correlation coefficient
    between two lists of numbers X and Y.
    """
    sm = sum(X)
    num = len(X)
    x_mean = sm / num

    sm = sum(Y)
    num = len(Y)
    y_mean = sm / num

    sum_xy = 0
    sum_sqrd_x = 0
    sum_sqrd_y = 0
    for index in range(0, len(X)):
        sum_xy += ((X[index] - x_mean) * (Y[index] - y_mean))
        sum_sqrd_x += (X[index] - x_mean) ** 2
        sum_sqrd_y += (Y[index] - y_mean) ** 2
    return round(sum_xy / (math.sqrt(sum_sqrd_x) * math.sqrt(sum_sqrd_y)), 3)


def display_correlation_table(data):
    vars = get_variable_lists(data)
    var = ['NP', 'PG', 'SI', 'BP', 'SFT', 'BMI', 'age', 'class']
    table = []

    print("  %8s %8s %8s %8s %8s %8s %8s %8s" % (var[0], var[1], var[2], var[3], var[4], var[5], var[6], var[7]))

    for X in vars:
        row = []
        for Y in vars:
            value = correlation_coefficient(X,Y)
            row.append(value)

        table.append(row)

    for i, x in enumerate(table):
        print("%6s  %6s %8s %8s %8s %8s %8s %8s %8s" % (var[i], x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]))

    return None

# *** YOUR WORK HERE ***

d_data = load_data('diabetes_study_rz03__data.txt')

summ_dirty = summary_stats(d_data)
display_summary(summ_dirty)

flagged_data, count = flag_missing_values(d_data)
print("Number of missing values:  ",count, )
# print(len(flagged_data))
clean_data = listwise_deletion(flagged_data)
summ = summary_stats(clean_data)
# print(summ)
display_summary(summ)

display_correlation_table(clean_data)



# *** PROBLEM 3 BELOW THIS IMPORT ONLY ***
import matplotlib.pyplot as plt

d_vars = get_variable_lists(d_data)


def mean(x):
    no_none = [value for value in x if value is not None ]
    m = sum(no_none)/len(no_none)
    return m


imp = []
for i, item in enumerate(list(d_vars)):
    imp_item = []
    m = mean(item)
    for value in item:
        if value is None:
            imp_item.append(m)
        else:
            imp_item.append(value)
    imp.append(imp_item)

var = ['NP', 'PG', 'SI', 'BP', 'SFT', 'BMI', 'age', 'class']

table = []

print("  %8s %8s %8s %8s %8s %8s %8s %8s" % (var[0], var[1], var[2], var[3], var[4], var[5], var[6], var[7]))

for X in imp:
    row = []
    for Y in imp:
        value = correlation_coefficient(X,Y)
        row.append(value)

    table.append(row)

for i, x in enumerate(table):
    print("%6s  %6s %8s %8s %8s %8s %8s %8s %8s" % (var[i], x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]))


for i, item in enumerate(d_vars):
    for j, other in enumerate(d_vars):
        if i <= j:
            continue
        r = plt.plot(imp[i], imp[j],'ro', label='Marginal mean imputation')
        b = plt.plot(item, other,'bo', label='True Values')
        plt.title('%s By %s' % (var[i], var[j]))
        plt.xlabel('%s' % (var[i]))
        plt.ylabel('%s' % (var[j]))
        plt.savefig('./plots/plot_%s_%s' % (var[i], var[j]))
