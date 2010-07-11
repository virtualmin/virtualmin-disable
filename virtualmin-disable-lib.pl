# Functions for scheduled disable

BEGIN { push(@INC, ".."); };
eval "use WebminCore;";
&init_config();
%access = &get_module_acl();
&foreign_require("at");

$at_cmd = "$module_config_directory/disable.pl";

1;

