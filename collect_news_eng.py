from lxml import html
import os
import sys
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
import requests
import textwrap

# when adding your own course to this list, add the website to this following list, add the course and corresponding
# function to "courses_dict" and simply write the function that parses that web-site, making sure to call
# writeOut with the proper parameters

# list of course web-sites
ppj = 'http://poincare.matf.bg.ac.rs/~nemanja_micovic/ppj.html'
vi = 'http://poincare.matf.bg.ac.rs/~nemanja_micovic/vi.html'
oop = 'http://poincare.matf.bg.ac.rs/~nemanja_micovic/oop.html'
pp = 'http://www.programskijezici.matf.bg.ac.rs/ProgramskeParadigmeI.html#5_tab'
pbp = 'http://poincare.matf.bg.ac.rs/~nikola_ajzenhamer/kursevi/pbp.html'
pbp_p = 'http://poincare.matf.bg.ac.rs/~nina/PBP19.html'
p2 = 'http://poincare.matf.bg.ac.rs/~nina/P2.html'


# the news_log file tracks the number of news loaded when the program was used last
# the format of the news_log file is course_name_abbreviation:number_of_news_previously_loaded;
def createLogFile():
    f = open(news_log, "w")
    s = ''

    for x in courses_dict.keys():
        s += str(x) + "=0;"

    f.write(s[:-1])
    f.close()


def writeOut(course_name, current_news_count, news_list, course_website):
    if course_name in news_count_dict.keys():
        previous_news_count = int(news_count_dict[course_name])
    else:
        print("Course isn't supported.")
        return

    print('Course website: ' + course_website)

    if current_news_count >= previous_news_count:
        to_write = current_news_count - previous_news_count
    else:
        to_write = len(news_list) - 1

    news_count_dict[course_name] = current_news_count

    if to_write == 0:
        print("No unread news\n")
    elif to_write == 1:
        print("There is 1 new notification\n")
    else:
        print('There are ' + str(to_write) + ' new notifications:\n')

    for entry in news_list[0:to_write]:
        text = entry.split('\n')
        for x in text:
            print(textwrap.fill(x, width=120))


def hasDefault():
    if os.path.isfile(default_log):
        default_file = open(default_log)
        default_courses = default_file.read()
        default_courses = default_courses.split(",")
        to_print = []
        for item in default_courses:
            item = item.upper()
            if item in courses_dict.keys():
                to_print.append(item)
            elif item == '':
                continue
            else:
                default_file.close()
                print("Corrupted " + default_log + ", printing all available news")
                clearDefault()
                to_print = list(courses_dict.keys())

        for item in to_print:
            callFetch(item)

        default_file.close()
        return True
    return False


def callFetch(which):
    which = which.upper()
    if which == 'PP':
        courses_dict[which](pp, "PP")
    elif which == 'PBP':
        courses_dict[which](pbp, "PBP")
    else:
        # case where there are multiple web-sites with a uniform structure
        courses_dict[which]()


# the format for the file where the default query is saved is course1,course2,...
def saveDefault():
    # don't ask to save as default, if it is already the default query
    if os.path.isfile(default_log):
        default_file = open(default_log)
        default_courses = default_file.read()
        default_courses = default_courses.split(",")
        set_courses = []
        for c in default_courses:
            c = c.upper()
            if c in courses_dict.keys():
                set_courses.append(c.lower())
            elif item == '':
                continue

        set_courses = set(set_courses)

        default_file.close()

        if sorted(set_courses) == sorted(course_query):
            return

    while not used_default and len(course_query) > 1:
        print('\nSave query as default? [y/n]')
        response = input()
        if response in ['y', 'yes', 'Y', 'YES']:
            default = ''
            for x in course_query:
                default = default + x + ','
            default_file = open(default_log, 'w')
            default_file.write(default[:-1])
            default_file.close()
            break
        elif response in ['n', 'no', 'N', 'NO']:
            break


def clearDefault():
    if os.path.isfile(default_log):
        os.remove(default_log)


# PPJ, VI, and OOP have the same html structure
def fetchPPJ():
    s = "PPJ"
    Micovic(ppj, s)


def fetchVI():
    s = "VI"
    Micovic(vi, s)


def fetchOOP():
    s = "OOP"
    Micovic(oop, s)


def fetchPP(course_website, course_name):
    page = requests.get(course_website)
    tree = html.fromstring(page.content)

    news_list = []

    print(('  ' + course_name + '  ').center(110, '*'))
    i = 1  # number of news

    while True:
        # the loop checks for elements containing distinct news, and as soon as it can't find the next one
        # it exits the loop
        li = tree.xpath('//div[@id="obavestenja"]//div[' + str(i) + ']/text()')

        if not li:
            break

        header = tree.xpath('//div[@id="obavestenja"]//div[' + str(i) + ']//h4/text()')

        complete = ''
        for x in header:
            complete = complete + str(x)
        complete = complete + '\n'

        # collecting text from all the different element types found
        news_text = tree.xpath(
            '//div[@id="obavestenja"]//div[' + str(i) + ']/text() | //div[@id="obavestenja"]//div[' + str(
                i) + ']//p/text()'
            + ' | //div[@id="obavestenja"]//div[' + str(i) + ']//a/@href | //div[@id="obavestenja"]//div[' + str(
                i) + ']//p//strong/text()'
            + ' | //div[@id="obavestenja"]//div[' + str(i) + ']//b/text()')

        for x in news_text:
            complete = complete + x.strip() + ' '
        complete = complete + '\n\n'
        news_list.append(str(complete))

        i = i + 1

    i = i - 1
    writeOut(course_name, i, news_list, course_website)


# PBP_P and P2 have the same html structure
def fetchPBP_p():
    s = "PBP_P"
    Nina(pbp_p, s)


def fetchP2():
    s = "P2"
    Nina(p2, s)


def fetchPBP(course_website, course_name):
    page = requests.get(course_website)
    tree = html.fromstring(page.content)

    news_list = []

    print((' ' + course_name + ' ').center(80, '*'))
    i = 1  # number of news
    while True:

        li = tree.xpath('//body/div/div/div/div/div[@class="card-body"][' + str(i) + ']/text()')
        if not li:
            break

        date = tree.xpath('//body/div/div/div/div/div[@class="card-body"][' + str(i) + ']/h5/text()')

        complete = str(date) + '\n'

        news_text = tree.xpath('//body/div/div/div/div/div[@class="card-body"][' + str(i) + ']/p/text()')

        for x in news_text:
            complete = complete + x.strip() + ' '
        complete = complete + '\n\n'
        news_list.append(str(complete))

        i = i + 1

    i = i - 1
    writeOut(course_name, i, news_list, course_website)


def Micovic(course_website, course_name):
    page = requests.get(course_website)
    tree = html.fromstring(page.content)

    news_list = []

    print((' ' + course_name + ' ').center(80, '*'))
    i = 1  # number of news
    while (1):
        li = tree.xpath('//*[@id="news"]/div/ul/li[' + str(i) + ']/text()')
        if not li:
            break

        header = tree.xpath('//*[@id="news"]/div/ul/li[' + str(i) + ']//span/text() | //*[@id="news"]/div/ul/li[' + str(
            i) + ']//h6/text()')

        complete = ''
        for x in header:
            complete = complete + str(x)
        complete = complete + '\n'

        news_text = tree.xpath(
            '//*[@id="news"]/div/ul/li[' + str(i) + ']//p/text() | //*[@id="news"]/div/ul/li[' + str(
                i) + ']//p//a/@href | //*[@id="news"]/div/ul/li[' + str(
                i) + ']//p//strong/text()')

        for x in news_text:
            complete = complete + x + ' '
        complete = complete + '\n\n'
        news_list.append(str(complete))

        i = i + 1

    i = i - 1
    writeOut(course_name, i, news_list, course_website)


def Nina(course_website, course_name):
    page = requests.get(course_website)
    tree = html.fromstring(page.content)

    news_list = []

    print((' ' + course_name + ' ').center(80, '*'))
    i = 1  # number of news

    while True:
        li = tree.xpath('//blockquote/ul/li[' + str(i) + ']/text()')
        if not li:
            break

        complete = ''

        news_text = tree.xpath('//blockquote/ul/li[' + str(i) + ']/text() | //blockquote/ul/li[' + str(
            i) + ']//a/@href | //blockquote/ul/li[' + str(i) + ']//*/text()')

        for x in news_text:
            complete = complete + x + ' '
        complete = complete + '\n\n'
        news_list.append(str(complete))

        i = i + 1

    i = i - 1
    writeOut(course_name, i, news_list, course_website)


# names of the files in which data is saved
news_log = "news_log.txt"  # number of news read in the previous program call
default_log = "default.txt"  # user's default course list when there are no additional command line arguments


# command line argument that resets the no-argument call of the program so it writes all available course news
clear_default_flag = '-c'

# dictionary of courses and their corresponding functions
courses_dict = {
    'PPJ': fetchPPJ,
    'VI': fetchVI,
    'OOP': fetchOOP,
    'PP': fetchPP,
    'PBP': fetchPBP,
    'PBP_P': fetchPBP_p,
    'P2': fetchP2
}

if not os.path.isfile(news_log):
    createLogFile()

os.chmod(news_log, S_IWUSR | S_IREAD)
if os.path.isfile(default_log):
    os.chmod(default_log, S_IWUSR | S_IREAD)

log_file = open(news_log, "r")
log = log_file.read()
news_count_dict = {}
try:
    for item in log.split(';'):
        course, count = item.split('=')
        news_count_dict[course] = count
except:
    print("Invalid " + news_log + ", created a new one.")
    log_file.close()
    os.remove(news_log)
    createLogFile()
    log_file = open(news_log, "r")
    log = log_file.read()
    createLogFile()
    for item in log.split(';'):
        course, count = item.split('=')
        news_count_dict[course] = count

used_default = False
course_query = sys.argv
erase_default = False

if len(course_query) == 1:
    if not hasDefault():
        for x in courses_dict.keys():
            callFetch(x)
    else:
        used_default = True
else:
    course_query = set(course_query[1:])
    for argument in course_query:
        if argument.upper() not in courses_dict.keys():
            if argument.upper() == clear_default_flag.upper():
                erase_default = True
                clearDefault()
                continue
            print("Wrong argument or course not supported")
            supported = ""
            for course in courses_dict.keys():
                supported = supported + str(course) + ','
            print("Supported courses: " + supported[:-1])
            sys.exit()

    if erase_default:
        course_query.remove(clear_default_flag.lower())

    if not course_query:
        course_query = set(courses_dict.keys())
        used_default = True

    for argument in course_query:
        callFetch(argument)

saveDefault()

log_file.close()
log_file = open(news_log, "w")
log_str = ''

for x in news_count_dict.keys():
    log_str += x + "=" + str(news_count_dict[x]) + ";"

log_file.write(log_str[:-1])
log_file.close()

os.chmod(news_log, S_IREAD | S_IRGRP | S_IROTH)
if os.path.isfile(default_log):
    os.chmod(default_log, S_IREAD | S_IRGRP | S_IROTH)
