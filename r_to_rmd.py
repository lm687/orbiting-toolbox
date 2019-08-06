## Notes:
## Any extra chunk options should be added after #<begin_chunk>", e.g.
## #<begin_chunk>", include=FALSE

import argparse
p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
p.add_argument('-v', '--verbose', action='store_true', default = True)
p.add_argument('-f', '--file', help='Input R file to convert to Rmd')
p.add_argument('--title', default='Document created with Python from R',
	help = 'Title of the rmd')
p.add_argument('--output', default='',
	help = 'Name of the output Rmd file')
p.add_argument('--author', default='L Morrill',
	help = 'Name of the author (to be put in header)')
p.add_argument('--date', default='2019')
args = p.parse_args()

if args.verbose:
	print('Options in R file: text, chunk, omit')

rfile = args.file
if args.output == '':
	outfile = "{}_ReadOnly.Rmd".format(args.file.strip('.R'))
else:
	outfile = "{}".format(args.output)
rmdfile = open(outfile, "w") 

rmdfile.write('''---
title: "{}"
author: "{}"
date: "{}"
output:
    html_document:
        number_sections: true
        theme: simplex
        toc: true
        toc_float: true
---\n\n'''.format(args.title, args.author, args.date)) 

rmdfile.write('This file has been created from the R script with the same name\n')

within_text = False
within_omit = False
with open(rfile) as f_rfile: 
	for line in f_rfile:
		if within_text:
			if "#<end_text>" in line:
				within_text = False
			else:
				if line == "##'\n":
					rmdfile.write('') ## line is empty; keep it
				else:
					rmdfile.write("\n{}".format(line.strip("##'").lstrip()))
		elif within_omit:
			if "#<end_omit>" in line:
				within_omit = False
		else:
			if "#<begin_chunk>" in line:
				if len(line.strip("#<begin_chunk>").strip("\n")) > 1:
					rmdfile.write("{}\n".format(line.strip("#<begin_chunk>").strip("\n")))
				else:
					rmdfile.write("```{r, cache=FALSE}\n")
			elif "#<begin_omit>" in line:
				within_omit = True
			elif "#<end_chunk>" in line:
				rmdfile.write("```\n")
			elif "#<begin_text>" in line:
				within_text = True

			else:
				rmdfile.write(line)

 
rmdfile.close() 

if args.verbose:
	print('Output file:\n\t{}'.format(outfile))
