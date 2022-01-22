# whelk
***whelk*** is a python3 tool to extract schelp files (supercollider help files) from supercollider documents.
It can be used to generate documentation for quarks directly from the source code of the quarks.

The current specification is very much in alpha state and while the general approach will not change, some minor details could be changed in the future.

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

The schelp file will have the same name as the .sc or .scd file you pass to -i
```
python3 whelk -i path/to/Classes/SomeFile.sc -o path/to/HelpSource/Classes/
```

## Process entire folder of files via wildcards

The schelp files will have the same name as the .sc or .scd file it was extracted from, but with extension .schelp
Note that if you use wildcards in a command line shell like bash, you need to include the path in quotes "" to avoid
that the shell already expands the wildcard.

```
python3 whelk.py -i "path/to/Classes/*.sc" -o path/to/HelpSource/Classes/
```

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
### basic and literal strings strings
in TOML syntax, 
* basic strings are enclosed in quotes. In basic strings certain characters can be escaped with a backslash.
```"this is a string"```
* literal strings are enclosed in single quotes. In literal strings no escaping occurs. What you see is what you get. This also means that there is literally no way to print a single quote using a literal string.
* ```'this is a literal string'```
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
