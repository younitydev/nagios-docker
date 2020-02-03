#!/usr/bin/perl -w
#############################################
# Convert host.cfg from nagios in a CSV?    #
# Debian requires .deb:libnagios-object-perl#
#############################################
# vdominguez 2012

use strict;
use lib qw( ./lib ../lib);
use Nagios::Config;
use Nagios::Object::Config;
use Data::Dumper;

Nagios::Object::Config->strict_mode(1);

my $file = $ARGV[0] or die "Need a host.cfg file\n";

my $obj = undef;
$obj = Nagios::Object::Config->new();
$obj->parse($file);

if ($ARGV[1] =~ m/-d/) {
    print Dumper($obj), "\n";
} else {
    my $hosts = $obj->all_objects_for_type("Nagios::Host");
    if (scalar(@$hosts) == 0) {
#        print "No hosts have yet been defined\n";
    } else {
        foreach my $host (@$hosts) {
           printf $host->host_name . ";" . $host->address . "\n";
       }
   }
}
