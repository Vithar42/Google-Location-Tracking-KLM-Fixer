If you are logged into a google account that has location tracking data this link, https://maps.google.com/locationhistory/b/0/kml?startTime=978307200000&endTime=1416268800000 will download a KML file that lets you look at that data from january first 2000 threw today Novemeber 18th 2014.  That kml file is uselss since it in many cases has to much data.  This Python Scryps corrects the file and makes a new kml file that is usable.  

To change the end date to something other I used this website to produce a unix date. http://www.aelius.com/njh/unixtime/?y=2001&m=1&d=1&h=0&i=0&s=0 Though you hvae to add 000 to the end of the unix date for the link above to work.  No idea why, but thats how it is...


This was created as I wanted to extract and view all of my data from googles locationhistory and not just the 30 days it allows by default.  http://www.reddit.com/r/technology/comments/2mmzr2/6_links_that_will_show_you_what_google_knows/ gets creddit for sparking the idea.
