# Defines functions for this feature

require 'virtualmin-disable-lib.pl';

sub feature_check
{
if (&foreign_installed("at", 1) != 2) {
	return $text{'check_eat'};
	}
return undef;
}

# feature_name()
# Returns a short name for this feature
sub feature_name
{
return $text{'feat_name'};
}

# feature_always_links(&domain)
# Returns an array of link objects for webmin modules, regardless of whether
# this feature is enabled or not
sub feature_always_links
{
local ($d) = @_;
return ( { 'mod' => $module_name,
	   'desc' => $text{'links_disable'},
	   'page' => 'edit.cgi?dom='.$d->{'id'},
	   'cat' => 'delete' });
}

1;

