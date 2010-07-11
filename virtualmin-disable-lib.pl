# Functions for scheduled disable

BEGIN { push(@INC, ".."); };
eval "use WebminCore;";
&init_config();
%access = &get_module_acl();
&foreign_require("at");
&foreign_require("virtual-server");
$api_cmd = &virtual_server::get_api_helper_command();

# get_disable_at_command(&domain)
# Returns the at job that disables some domain, if any
sub get_disable_at_command
{
local ($d) = @_;
local ($job) = grep { $_->{'realcmd'} eq $api_cmd." disable-domain --domain ".
					 $d->{'dom'} } &at::list_atjobs();
return $job;
}

1;

