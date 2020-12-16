# Output file format:
# numStrokes
# (then for each stroke)
# brush_name brush_color.r brush_color.g brush_color.b brush_color.a brush.size stroke.scale + numPoints
# (for each point in the stroke)
# x y z qx qy qz qa timestamp
# Note that x y z are in metres

import os, sys

# Tilt Brush Toolkit only works with Python 2
# if sys.version[0] != '2':
	# sys.exit('ERROR: Must use python2 for tilt-brush-toolkit!')
	
# Assuming that https://github.com/googlevr/tilt-brush-toolkit has been downloaded and 
# the environment variable TILT_BRUSH_TOOLKIT_ROOT points to its location

sys.path.append(os.path.join(os.environ['TILT_BRUSH_TOOLKIT_ROOT'], 'Python'))

from tiltbrush.tilt import Tilt


def main():
	
	if len(sys.argv) <= 1:
		sys.exit("Quitting: no input file provided!")

	fin = sys.argv[1]
	print('Reading from file ' + fin)
	
	t = Tilt(fin)
	sketch = t.sketch
	strokes = sketch.strokes
	
	#assert strokes[0].has_stroke_extension('scale'), "Strokes need to have 'scale' attribute to figure out real-world scale!"
	assert strokes[0].has_cp_extension('timestamp'), "Points need to have 'timestamp' attribute to figure out drawing speed!"
	
	if len(sys.argv) >= 3:
		foutName = sys.argv[2]
	else:
		foutName = os.path.abspath(fin) + '.dat'
	
	print('Writing to file ' + foutName)
	sys.stdout.flush()
	
	gnMap = {}
	with open('./guid_name_map.txt') as f:
		for line in f:
			words = line.split('\t')
			assert len(words)==4, line
			gnMap[words[1]] = [words[0], words[2], words[3][:-1]];
	
	numIgnored = 0 # Count number of strokes we ignore 

	with open(foutName, 'w') as fout:
		fout.write(str(len(strokes)) + '\n')
		for stroke in strokes:
			brushDescKey = t.metadata['BrushIndex'][stroke.brush_idx]
			# Ignore strokes declared to be effect brushes and/or animated brushes
			if gnMap[brushDescKey][1]=='Effect' or gnMap[brushDescKey][2]=='Anim':
				numIgnored = numIgnored + 1
				continue

			# Missing scale attribute
			try: 
				str(stroke.scale)
			except: 
				stroke.scale = 1.0
				
			fout.write(gnMap[brushDescKey][0] + ' ' + gnMap[brushDescKey][1] + ' ')
			fout.write(str(stroke.brush_color[0]) + ' ' + str(stroke.brush_color[1]) + ' ' + str(stroke.brush_color[2]) + ' ' + str(stroke.brush_color[3]) + ' ')
			fout.write(str(stroke.brush_size/10) + ' ' + str(stroke.scale) + ' ' + str(len(stroke.controlpoints)) + '\n')
			
			for pt in stroke.controlpoints:
				fout.write(str(pt.position[0]/10) + ' ' + str(pt.position[1]/10) + ' ' + str(pt.position[2]/10) + ' ')
				fout.write(str(pt.orientation[0]) + ' ' + str(pt.orientation[1]) + ' ' + str(pt.orientation[2]) + ' ' + str(pt.orientation[3]) + ' ')
				fout.write(str(stroke.get_cp_extension(pt, 'timestamp')) + '\n')
	
	# Adjust strokes count accordingly 
	with open(foutName) as f:
		lines = f.readlines()
		lines[0] = str(len(strokes) - numIgnored) + "\n"
	with open(foutName, "w") as f:
		f.writelines(lines)

if __name__ == "__main__":
	main()				