(
var report = true;
var verbose= UnitTest.brief; // or UnitTest.full
UnitTest.passVerbosity = verbose;
% for test in classnames:
${test}.run(report:report);
% endfor
)
