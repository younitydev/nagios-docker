#!/usr/bin/perl
##################
## CSV  Format  ##
## Delimiter ;  ##
##################
######################################################
###                                                ###
###    name;ip_contador                            ###
###                                                ###
######################################################
# you should change the template in the end of this script
# vdominguez 2012

use strict;
#use warnings;

my $file = $ARGV[0] or die "Need to get CSV file on the command line\n";
open(my $data, '<', $file) or die "Could not open '$file' $!\n";

# my %config;
#
# while (my $line = <$data>) {
#     chomp $line;
#     print $line;
#     for my $field ($line =~ /(?:"[^"]*"|[^:])+/g) {
#       my ($key, $val) = split /,/, $field, 2;
#       ($config{$key} = $val // '') =~ s/"([^"]*)"/$1/;
#     }
#
# use Data::Dumper;
# print Data::Dumper->Dump([\%config], ['*config']);


while (my $line = <$data>) {
  chomp $line;
  print $line;
  my @fields = split /,/ , $line;
  if ($fields[0] && $fields[1] && $field[2]) {
    my $hosts = create_host_in_file ($fields[0],$fields[1],$fields[2]);
    print $hosts;
  }
}

# sub create_host_in_file {
#  my $host_name=shift;
#  my $host_alias=shift;
#  my $host_address=shift;
#
#  my $template = <<END;
#
# define host {
#         host_name                       $host_name
#         alias                           $host_alias
#         address                         $host_address
#         use                             HostGeneric
# #        check_command                   process-service-perfdata
# #        event_handler                   process-service-perfdata
# #        notification_period             none
# #        check_command                   process-service-perfdata
# #        event_handler                   process-service-perfdata
# #        notification_period             none
# #        contact_groups                  sistemasdist-Grupo
# }
