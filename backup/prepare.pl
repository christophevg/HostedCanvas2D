#!/usr/bin/perl

use Text::CSV;

open my $diagrams, ">Diagram.csv" or die $!;
open my $versions, ">DiagramVersion.csv" or die $!;
open my $accounts, ">Account.csv" or die $!;

# helpers for listing accounts
my %seen  = ();
my %users = ();
open my $users, "users.tsv" or die $!;  
while( <$users> ) {
  chomp;
  my ( $account, $email ) = split /\t/;
  # remove gmail.com to allow them to login through openid
  $email =~ s/\@gmail\.com$//;
  $users{$account} = $email;
}
close $users;

my $csv = Text::CSV->new( { binary => 1, eol => "\012" } );

# starting point for IDs for this upload
my $num = 50000;

while(<>) {
  chomp;
  # replace NULL markers in entire input
  $_ =~ s/\\N//g;
  
  my ( $id, $name, $src, $width, $height, $author, $descr, $tags, $created, 
       $updated, $views, $edits, $voteup, $votedown, $notes, $visibility, 
       $status ) = split /\t/;

  # we don't use the 'unknown' user account anymore
  $author = "" if $author eq "unknown";

  # convert dates
  $created =~ s/^([0-9\-]+) ([0-9:]+)\..*$/$1T$2/;
  $updated =~ s/^([0-9\-]+) ([0-9:]+)\..*$/$1T$2/;

  # owner == initial author
  my $owner = $author;

  # convert src
  $src =~ s/(\\r)?\\n/\n/g;

  # diagrams
  $csv->print( $diagrams, [ $id, $created, $updated, 
                            $owner, $author, $name, 
                            $src, $width, $height, 
                            $descr, $notes, $tags, 
                            $views, $edits, $voteup, $votedown, 
                            $visibility, $status ] );

  # diagramversions
  $csv->print( $versions, [ $num++, $id, $created, $updated, 
                            $owner, $author, $name, 
                            $src, $width, $height, 
                            $descr, $notes, $tags, 
                            $views, $edits, $voteup, $votedown, 
                            $visibility, $status ] );
                           
  # accounts
  $csv->print( $accounts, [ $author, $users{$author} ] ) 
    if ! $seen{$author} and $author ne "" and $users{$author} ne "";
  $seen{$author} = 1;
}

close $diagrams;
close $versions;
close $accounts;
