Pybadges
========

What is this ?
--------------

Just a very quick and dirty Python script to generate badges for
conference attendees and speakers.

It requires a `CSV` file as input, with the following format:

    firstname,lastname,company,role,phone_number,email,id
    firstname,lastname,company,role,phone_number,email,id
    firstname,lastname,company,role,phone_number,email,id
    firstname,lastname,company,role,phone_number,email,id
    firstname,lastname,company,role,phone_number,email,id

Typically `role` can be `speaker`, `attendee`, `organizer` or something
like that.

It also requires a background image used for the badges.

Typical usage:

    ./pybadges -i input.csv -o output.pdf -b background.png


Multi-tracks usage (define 'tracks' in ./multiple-tracks.py):
		./multiple-tracks


Download QR codes:
		./download-qrcodes -i input.csv -o ./outputDirectory


Get the back badge with the QR codes:
		./pybadges_back -i input.csv -o output.pdf -b background.png



## Notes about your `csv` file:
* Capitalize necessary columns in Excel or LibreOffice :
	* LibreOffice : > Format > Text > Change case > Capitalize Every Word
* Find and Replace All to update "role" to your concerns

License
-------

Licensed under the WTFPL license, http://sam.zoy.org/wtfpl/
