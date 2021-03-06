# Functions for scheduled disable
use strict;
use warnings;
our %access;

BEGIN { push(@INC, ".."); };
eval "use WebminCore;";
&init_config();
%access = &get_module_acl();
&foreign_require("at");
&foreign_require("virtual-server");

# get_disable_at_command(&domain)
# Returns the at job that disables some domain, if any
sub get_disable_at_command
{
my ($d) = @_;
my $api_cmd = &virtual_server::get_api_helper_command();
my $re = $api_cmd." disable-domain --domain ".$d->{'dom'};
my ($job) = grep { $_->{'realcmd'} =~ /\Q$re\E/ } at::list_atjobs();
return $job;
}

1;

