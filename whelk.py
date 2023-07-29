import argparse
import pathlib
from commenttool import CommentTool
import toml
from collections import OrderedDict
from mako.template import Template
import glob
import sys
import os


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputfile", help="path to file to process", nargs='+')
    parser.add_argument("-o", "--outputfolder", help="path to schelp file folder")
    parser.add_argument("-v", "--verbose", help="print strings which do not parse as valid toml (generates a lot of ouput!)", action="store_true")
    args = parser.parse_args()

    if not args.inputfile:
        print("Error. Must specify an input file!")
        sys.exit(1)

    if not args.outputfolder:
        print("Error. Must specify an existing output folder!")
        sys.exit(2)

    # check arguments
    input_files = []
    for file in args.inputfile:
        file = os.path.expanduser(file)
        escaped = glob.escape(file)
        if escaped != file:
            globbed = [pathlib.Path(p) for p in glob.glob(file)]
            input_files.extend(globbed)
        else:
            input_files.append(pathlib.Path(file))

    output_file_folder = pathlib.Path(os.path.expanduser(args.outputfolder))
    if not output_file_folder.exists():
        print(f"Error! folder {output_file_folder} doesn't exist!")
        return

    for input_file_path in input_files:
        # print(f"{input_file_path = }")
        if not input_file_path.exists():
            print(f"Error! file {input_file_path} doesn't exist!")
            return

        # calculate output file name from input file and output folder
        path_to_output_file = output_file_folder.joinpath(input_file_path.name).with_suffix(".schelp")
        # print(f"{path_to_output_file = }")

        print(f"{str(input_file_path)} => {str(path_to_output_file)}")

        c = CommentTool()

        # concatenate all comments that parse as valid toml into one long string
        concatenated_comments = ""
        with open(input_file_path, "r") as f:
            file_contents = f.read()
            comments = c.comments(file_contents)
            for comment in comments:
                try:
                    comment = comment[2:-2]  # strip /* and */
                    toml.loads(comment)
                    concatenated_comments = concatenated_comments + comment
                except Exception as e:
                    if args.verbose:
                        print(f"{e}")
                        print(comment)
                    pass  # ignore invalid comments

        # parse the concatenated string as a toml document
        parsed_toml = toml.loads(concatenated_comments, _dict=OrderedDict)

        # render to schelp using a mako template
        template_path = pathlib.Path(get_script_path()).joinpath("template/schelptemplate.mako")
        # print(f"{str(template_path) = }")
        schelp_template = Template(filename=str(template_path))

        # write result to file
        with open(path_to_output_file, "w") as f:
            # print(f"writing to {path_to_output_file = }")
            f.write(schelp_template.render(data=parsed_toml))


if __name__ == "__main__":
    main()
