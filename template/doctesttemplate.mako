<%!
def ensure_start_lowercase(text):
    if len(text) > 1:
        return text[0].lower() + text[1:]
    elif len(text) == 1:
        return text.lower()
    else:
        return text
%>

${classname} : UnitTest {
    *new {
     ^super.new.init();
    }

    init {
    }

% for testname in data['doctests'][keyname]:
   ${testname | ensure_start_lowercase} {
% for indented_line in data['doctests'][keyname][testname].splitlines():
      ${indented_line}
% endfor
   }
% endfor
}
