#!/usr/bin/env perl

use DBI;
use CGI;
use strict;


#CGI Prep
my $cgi=CGI->new(<STDIN>);
my $lname=$cgi->param('name');
my $lurl=$cgi->param('url');
print $cgi->header('text/html');

my $dbh=&opendb("ttdb.sql");

#Main
redir() if($lname && !$lurl);
addlink() if($lname && $lurl);

$dbh->disconnect;

sub opendb {
	my ($dbname)=@_;
	my $newdb=(! -e $dbname);
	if(! -w ".") {
		print "Current directory is not writable, please ensure ".getpwuid($<)." can write to the current directory";
		exit 0;
	}
	if(-e $dbname && (! -w $dbname)) {
		print "Ensure ".getpwuid($<)." can write to $dbname";
		exit 0;
	} 
	my $dbh=DBI->connect("dbi:SQLite:dbname=$dbname","","", { RaiseError => 0, PrintError => 0 }) or die DBI::errstr;
	if($newdb) {
		$dbh->do("CREATE TABLE links (url text, name text NON NULL PRIMARY KEY)") or die "Unable to create links table in $dbname"; #If database is new, create links table
	}
	return $dbh;
}

sub redir { #Redirect to the url with the corresponding name
	my $getlink=$dbh->prepare("SELECT url FROM links WHERE name=?") or die DBI::errstr;
	$getlink->execute($lname);
	my @link=$getlink->fetchrow_array();
	if(@link) {
	print <<"REDIR"
		<html>
		<head>
		<meta http-equiv="Refresh" content="0; url=$link[0]" />
		</head>
		</html>
REDIR
	} else {
		print "$lname does not refer to a valid link";
	}
	exit 0;
}

sub addlink { #Add url/name pair to the database or print url it points to
	my $getlink=$dbh->prepare("SELECT url FROM links WHERE name=?") or die DBI::errstr;
	my $addlink=$dbh->prepare("INSERT INTO links VALUES (?, ?)") or die DBI::errstr;
	$getlink->execute($lname);
	my @link=$getlink->fetchrow_array();
	if(@link) {
		print "$link[0]\n";
		exit 0;
	}
	$addlink->execute($lurl, $lname) or die DBI::errstr;
	print "1";
}
