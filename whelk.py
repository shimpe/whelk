import argparse
import pathlib
from commenttool import CommentTool
import toml
from collections import OrderedDict
from mako.template import Template
import glob
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputfile", help="path to file to process")
    parser.add_argument("-o", "--outputfolder", help="path to schelp file folder")
    args = parser.parse_args()

    if not args.inputfile:
        print("Error. Must specify an input file!")
        sys.exit(1)

    if not args.outputfolder:
        print("Error. Must specify an output folder!")
        sys.exit(2)

    # check arguments
    p = pathlib.Path(args.inputfile)
    input_files = p.parent.glob(p.name)
    #print(f"{list(input_files) = }")
    for input_file_path in input_files:
        print(f"{input_file_path = }")
        if not input_file_path.exists():
            print(f"Error! file {input_file_path} doesn't exist!")
            return
        output_file_folder = pathlib.Path(args.outputfolder)
        if not output_file_folder.exists():
            print(f"Error! folder {output_file_folder} doesn't exist!")
            return

        # calculate output file name from input file and output folder
        path_to_output_file = pathlib.Path(args.outputfolder).joinpath(input_file_path.name).with_suffix(".schelp")
    #   print(f"{path_to_output_file = }")
        c = CommentTool()
        concatenated_comments = ""
        with open(input_file_path, "r") as f:
            file_contents = f.read()
            # concatenate all comment sections in file
            # using only those that parse as valid toml
            comments = c.comments(file_contents)
            for comment in comments:
                try:
                    comment = comment[2:-2] # strip /* and */
                    toml.loads(comment)
                    concatenated_comments = concatenated_comments + comment
                except Exception as e:
                    #print(f"{e}")
                    pass  # ignore invalid comments

        parsed_toml = toml.loads(concatenated_comments, _dict=OrderedDict)
        schelptemplate = Template(filename='template/schelptemplate.mako')
        with open(path_to_output_file, "w") as f:
            print(f"writing to {path_to_output_file = }")
            f.write(schelptemplate.render(data=parsed_toml))

if __name__ == "__main__":
    main()