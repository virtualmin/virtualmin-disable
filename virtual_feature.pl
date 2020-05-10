# Defines functions for this feature
use strict;
use warnings;
our (%text);
our $module_name;

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
return $text{'edit_header'};
}

# feature_webmin(&main-domain, &all-domains)
# Returns a list of webmin module names and ACL hash references to be set for
# the Webmin user when this feature is enabled
sub feature_webmin
{
my @doms = map { $_->{'dom'} } @{$_[1]};
if (@doms) {
        return ( [ $module_name,
                   { 'dom' => join(" ", @doms),
                     'noconfig' => 1 } ] );
        }
return ( );
}

# feature_always_links(&domain)
# Returns an array of link objects for webmin modules, regardless of whether
# this feature is enabled or not for the domain
sub feature_always_links
{
my ($d) = @_;
if (&virtual_server::can_disable_domain($d)) {
	return ( { 'mod' => $module_name,
		   'desc' => $text{'links_disable'},
		   'page' => 'edit.cgi?dom='.$d->{'id'},
		   'cat' => 'delete' });
	}
return ( );
}

1;

