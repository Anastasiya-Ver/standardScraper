The Problem
---------------------------------------------------------------------------------------------------
One of the most important tenants in jazz is to listen, listen, listen.  The best way to learn standards is to listen, the best way to improve phrasing or rhythm or ideas is listening, the most important thing to do WHILE PLAYING is to listen.  If you're like me and want to get better at jazz and know how to (hint: it's to listen), you are fully ready to dive into the world of swing-era, bebop, cool, etc. albums and listen away.  The question remains though, listen to what?

Albums and discographies are great for listening to a specific musician or genre, but the main issue lies in "horizontal" listening.  Say I want to learn a new standard, "Black Coffee", and want to hear some different renditions of that famous song.  Searching "Black Coffee" on Spotify or Youtube will give me a lot of people playing a song named Black Coffee, any song with that common name, not necessarily the standard.  And even if you do get the standard to pop up, they're all recent recordings, good luck finding anything before 2010.

This project is born out of my desire to just have an easy way to listen to a lot of covers of one song, and especially older versions.  I wanted a way to just plug in one song and instantly have easy access to as many renditions as I can handle.  This project is taking steps towards that goal, and in some ways is already there.

Installation
-------------------------------------------------------------------------------------------------------
This isn't really in installation form, and I haven't tried it anywhere but my own machine, but if you want to try it out go ahead.  You'd need python and, since this is in command line only form right now, to point venv at standardScraper/venv/Scripts/activate (I think the necessary libraries download with this file and will load?).  You will also need to set up a MongoDB account (it's easy), start a cluster, and either create an environmental variable named MONGODB_LINK and point it to the "connect link" you will get from MongoDB, or to edit line 5 in pymongo_get_database.py from 

	CONNECTION_STRING = os.getenv("MONGODB_LINK")
  
  to
  
  CONNECTION_STRING = "{{{{put the connect link you got in here}}}}}"
  
Like I said, not really in installation form.  Might work though.  After this (and allowing your own/any IP address through MongoDB's website under Network Access), the final step is to create a database in MongoDB named "standards" (no quotes).  After all this, you just need to activate the venv and run "python main.py" in command line and it should start chugging.

Use consciously and don't overwhelm the site.  I am going to add some sort of buffering mechanism at some point so it doesn't cause too much strain, but at the time being try to only do about 100 new downloads an hour.  The program does cap the new versions you can add to the first 95 (this will later change).

Planned Developments
-----------------------------------------------------------------------------------------------------------

- Add metadata.  It's already being saved onto the database, I just need to figure out how to attach it during the download
- Fix the capping mechanism
- Make into a website or app to centralize the database (every user shares one database --> easier downloads, faster time, less strain)
- Will need to add a feature to allow you to manually reselect the target song if it automatically selects wrong.  
    This program generally chooses the correct song to download from, but not always ("Out of Nowhere" is broken).  This is because it always chooses the first result   that comes up from searching your query.  Before selecting quantity, should have a "does this look right" with title, original composer, and date of release.
- Add album release date to metadata
- Figure out a better way to do track titles
- Queue system for mass-downloading standards.  There's only like 100 commonly heard standards and maybe a total of maybe 400, 500 you'll ever hear, so queuing a list of standards to download in the program's downtime will help with speed and manage strain better.  Would be user provided or taken from online lists.

Far Far Future Developments
-----------------------------------------------------------------------------------------
One thing I noticed is that a lot of songs saved onto SHS do have youtube versions, but they aren't crowd-provided, so the youtube link is not saved onto SHS.  If you search the song, album, and author manually you will generally find it, but my scraper has no way to do this.  What might be cool is to automatically search those three parameters and automatically check the songs that come up to see if they seem appropriate.  This would hypothetically take a youtube search API to gather results, but automatically checking if they're accurate is much more difficult.  Might look into the feasibility of training a ML algorithm specifically on each standard, so this would be a selective feature and also really hard to implement.  It would be cool though.

Notes
----------------------------------------------------------------------------------------
It seems that, as a flaw of the sample set, most standards that are downloaded are sung, not instrumental.  I am considering solutions to add in more instrumentalists (like the "Far Far Future Developments" seen above).

I am also not expecting anyone to use this.  
