#!/usr/local/bin/perl
# Create or remote scheduled disable at job

require 'virtualmin-disable-lib.pl';
use Time::Local;
&error_setup($text{'save_err'});
&ReadParse();
$d = &virtual_server::get_domain_by("dom", $in{'dom'});
$d || &error($text{'edit_edomain'});
&virtual_server::can_disable_domain($d) ||
	&error($virtual_server::text{'edit_ecannot'});
$job = &get_disable_at_command($d);

if ($in{'when'}) {
	# Validate date and time
	eval { $date = timelocal(0, $in{'minute'}, $in{'hour'},
                         $in{'day'}, $in{'month'}, $in{'year'}-1900) };
	$@ && &error($text{'save_edate'});
	$date > time() || &error($text{'save_edate2'});
	if ($job) {
		&at::delete_atjob($job->{'id'});
		}
	&clean_environment();
	$api_cmd = &virtual_server::get_api_helper_command();
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

