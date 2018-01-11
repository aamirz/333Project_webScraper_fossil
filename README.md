# The Princeton Prowler Web-Scraper

The PP Web-Scraper is an automated system for pulling publication data from
various Princeton online publications into a local repository. The Web-Scraper
also acts as a formatter for the Princeton Prowler database - it formats the
number of topics in the database, the publication metadata, and the topics that
are associated with each publication. The Web-Scraper then populates with the
database with all old Daily Princetonian articles as well as any avaialable from
the Nassau Weekly, etc.

## Launching to an EC2 Instance (or any Linux/UNIX based machine)

On my Amazon AWS EC2 instance (running Red Hat Linux),
the Web-Scraper is configured to run hourly via
the cron utility, which is a UNIX system level daemon that handles the
automation of tasks. Note that the call to the datetime UNIX utility in
`masterRun.sh` is configured specifically for Linux (the arguments for getting
yesterday's date are different on Mac OS). The cron utility is configured as
follows:

`$ crontab -e`    

Insert the following line into your crontab file, which tells cron to run the
Web-Scraper every hour on the 30th minute for all time, it ouputs any error
messages to the log file in the `$HOME` directory:

`30 * * * * /bin/bash ~/prowler_webScraper/masterRun.sh > ~/logfile_masterRun`

Once you add this line, exit out of the text editor (depends on your system, I
like emacs) and make sure that `masterRun.sh` has permissions by running:

`$ cd PATH_TO_WEB_SCRAPER`      
`$ chmod +x masterRun.sh`

## Summary of Shell Scripts (scraping automation)

**autoPullToday.sh** : \****Deprecated*** An intermediate testing script for
pulling articles to a local directory.

**commandOldPull.sh** : Extracts dates from an input file and then uses them
to command a pull as well as a post to the database. Writes all output (success/fail)
to a log file.

**config.sh** : Formats the database with publication metadata.
Formats the local directory (for pulling/posting) with a local
folder for all future pulls.

**masterRun.sh** : Performs pulls vial pullToday.sh for both today and yesterday. Takes today's date
as a command line argument.

**oldPull.sh** : Control for pulling old Daily Princetonian files. Two arguments
command line arguments.

**pullToday.sh** : Controls pulling/posting all of today's articles from every
publication.

**pullWeeks.sh** : \****Deprecated*** pull from a range of dates from the Prince.

**refill.sh** : \****Deprecated***  Testing script to pull old Prince data.

**runTests.sh**; **testPullPost.sh**; **testypoo.sh** : \****Deprecated***
