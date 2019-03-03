#MATF news gathering

The idea behind the project is ease of access to news posted on various TA's sites, without having to check all of them manually.

The program works by parsing the corresponding web-pages, and extracting data. 
Every time the program is run, only unread news are shown. 

Not all courses and TAs are supported - some of them can't be parsed properly, if you have a suggestion on which TA I should add, contact me.

##Instructions

Run the program from the terminal or from an IDE (using the option to add command line arguments).

* If the program is run without any command line arguments, 
the script will go through all the supported websites and print the relevant information.
* To choose only specific courses, enter the corresponding course name abbreviation as a command line argument,
  * For example, if you wanted to get the news for the course
   "**P**rogramiranje **B**aza **P**odataka" and "**O**bjektno-**O**rjentisano **P**rogramiranje", 
   you'd run the program with "**python3 collect_news.py PBP OOP**"
  * You can add as many courses as you want, for example "**python3 collect_news.py PP VI PPJ PBP OOP**"
  is a valid program call
  * If one of the arguments isn't a valid course code, the program will list all the available ones and not run
  
* The program uses a file called "news_log.txt" as its source of data regarding 
what news it had previously read. Don't change the file without good reason, if you want to reset
the program's news output, delete that file.
* The program also has a feature called "default". When the program is run with command line arguments for the first time,
you will be asked whether you want to make that query your default one. If you say "yes", whenever you run the program without
command line arguments, your default courses will be listed, instead of all the available ones.
* You can change the default query by entering a different set of command line arguments, or delete the default settins by
using "-c" as a command line argument (or deleting the default.txt)