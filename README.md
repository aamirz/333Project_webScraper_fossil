# The Princeton Prowler Web-Scraper

The PP Web-Scraper is an automated system for pulling publication data from
various Princeton online publications into a local repository. The Web-Scraper
also acts as a formatter for the Princeton Prowler database - it formats the
number of topics in the database, the publication metadata, and the topics that
are associated with each publication. The Web-Scraper then populates with the
database with all old Daily Princetonian articles as well as any avaialable from
the Nassau Weekly, etc.

On the Amazon AWS EC2 instance, the Web-Scraper is configured to run hourly via
the cron utility, which is a UNIX system level daemon that handles the
automation of tasks. Note that the call to the datetime UNIX utility in
`masterRun.sh` is configured specifically for Linux (the arguments for getting
yesterday's date are different on Mac OS). The cron utility is configured as
follows:

$ `crontab -e`
