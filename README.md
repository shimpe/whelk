![logo](https://github.com/shimpe/whelk/blob/main/image/whelk.png?raw=true)

# whelk
***whelk*** is a python3 tool to extract schelp files (supercollider help files) from supercollider documents.
It can be used to generate documentation for quarks directly from the source code of the quarks.

The current specification is very much in alpha state and while the general approach will not change, some minor details could be changed in the future.
Note: whelk does not check for syntax errors, so double check the generated documentation for any unexpected problems.

# dependencies
whelk depends on a python3 implementation (https://github.com/uiri/toml) of the markup language TOML (https://github.com/toml-lang/toml) with support for remembering the correct ordering of key-value pairs, and on the templating language mako (https://www.makotemplates.org/)

```
pip install toml
pip install mako
```

# usage

## Get an overview of commmand line options
```
python3 whelk.py -h 
```
## Process single file 

The schelp file will have the same name (but with .schelp extension) as the .sc or .scd file you pass to -i
Note that the output folder should exist already.

```
python3 whelk -i path/to/Classes/SomeFile.sc -o path/to/HelpSource/Classes/
```

## Process entire folder of files via wildcards

The schelp files will have the same name as the .sc or .scd file it was extracted from, but with extension .schelp
A ~ character will be expanded to the user folder. The output folder should exist already.

```
python3 whelk.py -i path/to/Classes/*.sc -o path/to/HelpSource/Classes/
```

## Process multiple folders of files via wildcards

All .schelp files need to end up in the same folder.

```
python3 whelk.py -i path/to/Classes/*.sc path/to/Classes/tests/*.sc -o path/to/HelpSource/Classes/
```

## Examining problems
Note if you generated new .schelp files, they will not yet be indexed by the help system. You can force a reindexation of the docs by calling
```smalltalk
SCDoc.indexAllDocuments
```
in scide.

To check for problems with the embedded documentation, there are a few things you can do:
1. If you pass the option --verbose to whelk, it will print to the terminal all comments that it couldn't parse as valid toml. You can then judge if you intended those comments to be part of the documentation or not.
2. After generating the documentation in .schelp format, try to load it in scide and watch the post window for errors.
3. After generating the documentation in .schelp format, try to load it in scide and look in the help text for red flags, like methods which are listed as undocumented whereas you remember adding docs for them, or missing code examples which you are sure you added.

## Some examples to see the syntax

### Setting up the general properties
General properties to be defined are 
* title
* summary
* categories
* related
* description
```
/*
[general]
title = "ScMidiKnob"
summary = "a bidirectional midi knob"
categories = "Midi Utils"
related = "Classes/ScMsgDispatcher, Classes/ScMidiTextField, Classes/ScNumericControl, Classes/ScMidiSlider, Classes/ScMidiControlChangeDumper"
description = '''
ScMidiKnob models a bidirectional MIDI knob. The knob updates when updates are received from the midi device. If the knob is modified in the UI, the new values are sent to the midi device.
'''
*/
```
### Documenting a member variable
To document a member variable, you can give
* a description can be given under a section title with the form [method.<name_of_the_member_variable>]
* under the section title [method.<name_of_the_member_variable>.returns] you can describe the expected type of the variable
```
/*
[method.muted]
description='''
A boolean to indicate that the knob is muted. When a knob is muted,
it doesn't send values to the midi device when the user rotates the knob.
The knob will still update its displayed value if control changes are received from the midi device though.
'''
[method.muted.returns]
what = "a boolean"
*/
var <>muted;
``` 
### Documenting a class method
To document a class method, you can give
* a description, under a section title [classmethod.<name_of_the_class_method>]
* [optionally] each of the arguments, under a section title [classmethod.<name_of_the_class_method>.args]
* [optionally] the return value, under a section title [classmethod.<name_of_the_class_method>.returns]
```
/*
[classmethod.new]
description = "New creates a new ScMidiKnob"
[classmethod.new.args]
unique_name = "unique name, a string, must be unique over all bidirectional midi controls in your program"
gui_name = "gui name, a string, needn't be unique over all bidirectional midi controls in your program - part of label"
msgDispatcher = "an ScMsgDispatcher, the object that knows all bidirectional midi controls in your program, and that performs midi communication"
[classmethod.new.returns]
what = "a new ScMidiKnob"
*/
*new {
  | unique_name, gui_name, msgDispatcher |
  ^super.new.init(unique_name, gui_name, msgDispatcher);
}
```
### Documenting an instance method
To document an instance method, you can give
* a description, under a section title [method.<name_of_the_instance_method>]
* [optionally] each of the arguments, under a section title [method.<name_of_the_instance_method>.args]
* [optionally] the return value, under a section title [method.<name_of_the_instance_method>.returns]
```
/*
[method.asLayout]
description = '''
Convenience method that sets up the guiknob, guilabel, guilearnbutton and guimutebutton and returns them into a VLayout
'''
[method.asLayout.args]
show_label = "show the label above the midi control (default: true)"
show_learn_button = "show the learn button under the midi control (default:true)"
show_mute_button = "show the mute button under the midi control (default:true)"
learn_label = "text to display on the learn button (default: \"Learn\")"
mute_label = "text to display on the mute button (default: \"Mute\")"
[method.asLayout.returns]
what = "a VLayout containing a label (optional), a knob, and two buttons (optional)"
*/
asLayout {
		| show_label=true, show_learn_button=true, show_mute_button=true, learn_label="Learn", mute_label="Mute"|
		// ...
		^VLayout(*list_of_controls);
	}
```
### Adding example code
To embed an example in the schelp file you can add an [examples] section. The name of the key is not important.
You can add multiple keys under the [examples] section and they will all be included in the schelp file.
```
/*
[examples]
what = '''
(
var slider1, slider2, knob1, textfield;
var msgDispatcher;

// create a midi msg dispatcher
// the msg dispatcher is responsible for learning and sending information to from midi device
msgDispatcher = ScMsgDispatcher();
msgDispatcher.connect("Rev2", "Rev2 MIDI 1");

// create some controls, passing in a unique id, a ui label and the midi msg dispatcher as argument
slider1 = ScMidiSlider("SLIDER 1", "slider", msgDispatcher);
// set up the slider to listen to pitch bending msgs on midi channel 0
slider1.prebindBend(0);

// create a second slider
slider2 = ScMidiSlider("SLIDER 2", "slider", msgDispatcher);
// add a custom handler that will be invoked when values are received from the midi device
slider2.registerReceiveHandler({
	| dispatcher, control, src, chan, num, val |
	src.debug(control.uniquename + "src ");
	chan.debug(control.uniquename + "chan");
	num.debug(control.uniquename + "num ");
	val.debug(control.uniquename + "val ");
});

// create a knob
knob1 = ScMidiKnob("KNOB 1", "knob", msgDispatcher);

// create a textfield
textfield = ScMidiTextField("TF", "text", msgDispatcher);

// make a window,
w = Window("Midi fader", Rect(100, 500, 400, 400));
w.layout_(HLayout(
	slider1.asLayout(show_label:false, show_mute_button:false, learn_label:"L"),
	slider2.asLayout,
	knob1.asLayout,
	textfield.asLayout(show_mute_button:false),
	nil));
w.front;

// clean up when clicking ctrl+. (or cmd+.)
CmdPeriod.doOnce({
	msgDispatcher.cleanUp;
	Window.closeAll
});

)
'''
*/
```
### adding a test
Whelk can also extract testing code from your comments. This can be useful for quickly recording small tests and things you try out as you develop your code,
without requiring a context switch between writing code and writing test code.

Testing code differs from example code because it is extracted to a unit test. Testing code is not added to the generated .schelp documentation because 
it has to be written as a method and therefore cannot be copy/pasted and run directly inside the supercollider IDE.

Whelk will extract the tests to a subfolder ```autogenerated_doctests``` at the location of the .sc file that is being processed. 
Note that the ```autogenerated_doctests``` folder could be automatically deleted, so it's best not to add manually written tests in that same folder.

The name of the file (equal to the name of the class) in which the test code will be saved is part of the toml header: e.g. by writing
```[doctests.MtlDegreeTests]```, a file ```MtlDegreeTests.sc``` will be generated, containing a class ```MtlDegreeTests : UnitTest { ... }```.
If the name doesn't start with a capital, whelk will transform it into a capital because supercollider class names must start with a capital.

In the example below, a test named ```test_degree``` will be generated in a class ```MtlDegreeTests``` in the file 
```Classes/autogenerated_doctest/MtlDegreeTests.sc```). You can add multiple tests in a single file. 

**Beware:** It's up to the user to make sure that different .sc files specify different classnames/filenames otherwise 
tests in one .sc file can overwrite tests specified in another .sc file.

```
/*
[doctests.MtlDegreeTests]
test_degree = '''
var d1 = MtlDegree(5, 3, \score, \onebased);
var d2 = MtlDegree(4, 3, \score, \zerobased);
var d3 = MtlDegree(2, 3, \score, \onebased);
this.assertEquals(d1.degree_value(\onebased), 5, "d1_degree_value_onebased");
this.assertEquals(d1.degree_value(\zerobased), 4, "d1_degree_value_zerobased");
this.assertEquals(d1.degree_kind, \score, "d1_degree_kind");
this.assertEquals(d1.equave, 3, "d1_equave");
this.assert(d1 == d2, "compare onebased to zerobased");
this.assert(d3 < d2, "smaller than");
this.assert(d2 > d3, "greater than");
'''
*/
```
### basic and literal strings strings
in TOML syntax, 
* basic strings are enclosed in quotes. In basic strings certain characters can be escaped with a backslash.
```"this is a string \n with an embedded newline"```
* literal strings are enclosed in single quotes. In literal strings no escaping occurs. What you see is what you get. This also means that there is literally no way to print a single quote using a literal string.
```'this is a literal string \n and despite first appearance no newline is embedded'```
* basic multiline strings are enclosed in three double quotes. In basic multiline strings, certain characters can be escaped with backslash.
```
"""
this is a 
basic 
multiline string
"""
```
* literal multiline strings are enclosed in three single quotes. In literal multiline strings, again no escaping occurs, so in a multiline literal string it's not possible to print three successive single quotes.
```
''' this
is a 
multiline
string
'''
```
```
