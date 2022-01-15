% if 'general' in data and 'title' in data['general']:
TITLE:: ${data['general']['title']}
% else:
TITLE:: FIXME (no title specified)
% endif
% if 'general' in data and 'summary' in data['general']:
summary:: ${data['general']['summary']}
% else:
summary:: FIXME (no summary specified)
% endif
% if 'general' in data and 'categories' in data['general']:
categories:: ${data['general']['categories']}
% else:
categories:: FIXME (no categories specified)
% endif
% if 'general' in data and 'related' in data['general']:
related:: ${data['general']['related']}
% else:
related:: FIXME (no related classes specified)
% endif

% if 'general' in data and 'description' in data['general']:
DESCRIPTION::
${data['general']['description']}
% else:
DESCRIPTION::
(FIXME no long description specified)
% endif


% if 'classmethod' in data:
CLASSMETHODS::

% for method in data['classmethod']:
METHOD:: ${method}
% if 'description' in data['classmethod'][method]:
${data['classmethod'][method]['description']}

% else:
(FIXME class method has no description yet)

% endif
% if 'args' in data['classmethod'][method]:
% for argument in data['classmethod'][method]['args']:
ARGUMENT:: ${argument}
${data['classmethod'][method]['args'][argument]}

% endfor
% endif
% if 'returns' in data['classmethod'][method] and 'what' in data['classmethod'][method]['returns']:
returns:: ${data['classmethod'][method]['returns']['what']}
% else:
returns:: the class ${data['general']['title']} itself

% endif
% endfor
% endif

% if 'method' in data:
INSTANCEMETHODS::

% for method in data['method']:
METHOD:: ${method}
% if 'description' in data['method'][method]:
${data['method'][method]['description']}

% else:
(FIXME instance method has no description yet)

% endif
% if 'args' in data['method'][method]:
% for argument in data['method'][method]['args']:
ARGUMENT:: ${argument}
${data['method'][method]['args'][argument]}

% endfor
% endif
% if 'returns' in data['method'][method] and 'what' in data['method'][method]['returns']:
returns:: ${data['method'][method]['returns']['what']}
% else:
returns:: this instance of ${data['general']['title']}

% endif
% endfor
% endif

EXAMPLES::

code::
% if 'examples' in data and 'what' in data['examples']:
${data['examples']['what']}
% else:
(FIXME add some example code)
% endif
::
