Description:

A URL shortener akin to tinyurl or bit.ly

Requirements:

The only two requirements are perl,
and a copy of the sqlite3 dbd 
driver.

Installation:

1. Copy the ushort directory to the root of your web server.
2. Make sure the active UID which runs the CGI process has write permissions to ushort.
3. Ensure all requests redirect to "ushort/index.cgi?name=<request>".

The last step depends on your web server. If using Apache, mod_rewrite can 
accomplish this. The corresponding rewrite rule is 

"RewriteRule ^([^/]*)$ /ushort/index.cgi?name=$1"

Adding Links:

A link can be shortened using the addlink.html page

Licence:

Code is licensed under the GPLV3, which can be found
here http://www.gnu.org/licenses/gpl.html
