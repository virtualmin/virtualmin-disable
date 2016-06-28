#!/usr/local/bin/perl
# Show form to setup scheduled disable
use strict;
use warnings;
our (%text, %in);

require 'virtualmin-disable-lib.pl';
&ReadParse();
my $d = &virtual_server::get_domain($in{'dom'});
$d || &error($text{'edit_edomain'});
no warnings "once";
&virtual_server::can_disable_domain($d) ||
	&error($virtual_server::text{'edit_ecannot'});
use warnings "once";

&ui_print_header(&virtual_server::domain_in($d), $text{'edit_title'}, "");

print &ui_form_start("save.cgi");
print &ui_hidden("dom", $in{'dom'});
print &ui_table_start($text{'edit_header'}, undef, 2);

# Current state
print &ui_table_row($text{'edit_state'},
	$d->{'disabled'} ? "<font color=red>$text{'edit_disabled'}</font>"
			 : $text{'edit_enabled'});

# Current time
print &ui_table_row($text{'edit_now'},
	&make_date(time(), 0, "dd/mon/yyyy"));

# When to disable
my $job = &get_disable_at_command($d);
my @tm;
if ($job) {
	@tm = localtime($job->{'date'});
	}
else {
	@tm = localtime(time() + 24*60*60);
	}
print &ui_table_row($text{'edit_when'},
	&ui_radio_table("when", $job ? 1 : 0,
		[ [ 0, $text{'edit_never'} ],
		  [ 1, $text{'edit_date'},
		    &ui_date_input($tm[3], $tm[4]+1, $tm[5]+1900,
				   "day", "month", "year")." ".
		    $text{'edit_time'}." ".
		    &ui_textbox("hour", sprintf("%2.2d", $tm[2]), 2).":".
		    &ui_textbox("minute", sprintf("%2.2d", $tm[1]), 2) ] ]));

print &ui_table_end();
print &ui_form_end([ [ undef, $text{'save'} ] ]);

&ui_print_footer("/", $text{'index'});

