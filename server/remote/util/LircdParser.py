import fileinput, glob, re, os

def parse(conf):
	"""
	Parse the lircd.conf config file and create a dictionary.
	"""
	# Open the config file and directory
	conflist = [conf]
	if os.path.isdir(conf):
		conflist = glob.glob(conf+"/*.conf")  #open lircd.conf.d comfig directory
	conf = fileinput.input(conflist, mode='r')

	remote_name = None
	codes_section = False
	raw_codes_section = False

	remotes = {}

	for l in conf:
		# Convert (multiple) tabs to spaces
		l = re.sub(r'[ \t]+', ' ', l)
		# Remove comments
		l = re.sub(r'#.*', '', l)
		# Remove surrounding whitespaces
		l = l.strip()

		# Look for a 'begin remote' line
		if l == 'begin remote':
			# Got the start of a remote definition
			remote_name = None
			codes_section = False
			raw_codes_section = False

		elif not remote_name and l.startswith('name '):
			# Got the name of the remote
			remote_name = l.split(' ')[1]
			if remote_name not in remotes:
				remotes[remote_name] = {
					'name': remote_name,
					'codes':[], 
					'filepath': conf.filename(),
					'filename': os.path.basename(conf.filename()),
				}

		elif remote_name and l == 'end remote':
			# Got to the end of a remote definition
			remote_name = None

		elif remote_name and l == 'begin codes':
			codes_section = True

		elif remote_name and l == 'end codes':
			codes_section = False

		elif remote_name and l == 'begin raw_codes':
			raw_codes_section = True

		elif remote_name and l == 'end raw_codes':
			raw_codes_section = False

		elif remote_name and codes_section:
			fields = l.split(' ')
			remotes[remote_name]['codes'].append(fields[0])

		elif remote_name and raw_codes_section:
			fields = l.split(' ')
			if len(fields) >= 2 and fields[0] == 'name':
				remotes[remote_name]['codes'].append(fields[1])
	conf.close()
	return remotes


if __name__ == "__main__":
    lirc = parse('/etc/lirc/lircd.conf.d/')
    print(lirc)
