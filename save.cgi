#!/usr/local/bin/perl
# Create or remote scheduled disable at job
use strict;
use warnings;
our (%text, %in);

require 'virtualmin-disable-lib.pl';
use Time::Local;
&error_setup($text{'save_err'});
&ReadParse();
my $d = &virtual_server::get_domain($in{'dom'});
$d || &error($text{'edit_edomain'});
no warnings "once";
&virtual_server::can_disable_domain($d) ||
	&error($virtual_server::text{'edit_ecannot'});
use warnings "once";
my $job = &get_disable_at_command($d);
my $date;

if ($in{'when'}) {
	# Validate date and time
	eval { $date = timelocal(0, $in{'minute'}, $in{'hour'},
                         $in{'day'}, $in{'month'}-1, $in{'year'}-1900) };
	$@ && &error($text{'save_edate'});
	$date > time() || &error($text{'save_edate2'});
	if ($job) {
		&at::delete_atjob($job->{'id'});
		}
	&clean_environment();
	my $api_cmd = &virtual_server::get_api_helper_command();
	&at::create_atjob("root", $date,
			  $api_cmd." disable-domain --domain ".$d->{'dom'},
			  "/", undef);
	&reset_environment();
	}
else {
	# Remove the at job
	if ($job) {
		&at::delete_atjob($job->{'id'});
		}
	}

&redirect("edit.cgi?dom=$in{'dom'}");

