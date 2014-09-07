## these are all the current options want_to_annotate_with = ['travel_country', 'spec_type', 'phage_type', 'phe_centre', 'r_type', 'cluster']
want_to_annotate_with = ['travel_country', 'spec_type', 'phage_type', 'phe_centre', 'cluster']

## to colour list
#to_colour = ['13167_H130700419-2', '13168_H130720555-2', '13169_H131660213-2', '13170_H131920702-2', '13171_H131960204-2', '13172_H132020501-2', '13173_H132040425-2', '13174_H132300541-2', '13175_H132460180-2', '13176_H132780266-2', '13177_H132800431-2', '13178_H132920685-2', '13179_H132940743-2', '13180_H132940744-2', '13181_H132940745-2', '13182_H132940746-2', '13183_H132940747-2', '13184_H132940748-2', '13185_H132940749-2', '13186_H132940750-2', '13187_H132940751-2', '13188_H132940752-2', '13189_H132940753-2', '13190_H132940754-2', '13191_H132940756-2', '13192_H132960590-2', '13193_H132980531-2', '13194_H133000645-2', '13195_H133000653-2', '13196_H133000654-2', '13197_H133040470-2', '13198_H133040472-2', '13199_H133040473-2', '13200_H133040474-2', '13201_H133060374-2', '13202_H133060375-2', '13203_H133060376-2', '13204_H133060377-2', '13205_H133060378-2', '13206_H133200471-2', '13207_H133220558-2', '13208_H133260293-2', '13209_H133300609-2', '13210_H133340322-2', '13211_H133380323-2', '13212_H133400611-2', '13213_H133400613-2', '13214_H133460540-2', '13215_H133480564-2']
#to_colour = ['13179_H132940743-2', '13180_H132940744-2', '13181_H132940745-2', '13182_H132940746-2', '13183_H132940747-2', '13184_H132940748-2', '13185_H132940749-2', '13186_H132940750-2', '13187_H132940751-2', '13188_H132940752-2', '13189_H132940753-2', '13190_H132940754-2', '13191_H132940756-2', '13194_H133000645-2', '13195_H133000653-2', '13196_H133000654-2', '13198_H133040472-2', '13199_H133040473-2', '13200_H133040474-2', '13209_H133300609-2', '13201_H133060374-2', '13202_H133060375-2', '13203_H133060376-2', '13204_H133060377-2', '13205_H133060378-2']
to_colour = []

colour_list = ["5845277","14714700","5054582","13393876","288103","1893860","147601","33024","3493162","9814630","103","5154520"]



def annotate_tree(attrib_dict, tree):
	fo = '/Users/flashton/annot.tree'
	with open(fo, 'w') as annotated_tree:
		with open(tree) as tree_handle:
			for line in tree_handle.readlines():
				if line.startswith('\t'):
					if not line.startswith('\ttree '):

					
						seq_id = line.strip()
	

	
						if seq_id in attrib_dict:

							annotated_tree.write('\t' + seq_id + "[&!name=\"" + seq_id + '\t' + attrib_dict[seq_id] +"\"]\n" )
	
						else:

							annotated_tree.write('\t' + seq_id + "[&!name=\"" + seq_id +"\"]\n")
	
							#print '\t' + x + "[&!name=\"" + molis_id +" "+mlva_list[molis_id] +"\"]"
					else:
						seq_id = '\t%s\n' % seq_id
						annotated_tree.write(seq_id)
				else:
					annotated_tree.write(line)
			else:
				annotated_tree.write(line)

def get_meta_data(inhandle):
	fi = open(inhandle)
	res_dict = {}
	for line in fi.readlines():
		split_line = line.strip().split('\t')
		res_dict[split_line[0]] = split_line[1]

	return res_dict

################################# main #################################

tree = '/Users/flashton/exported_tree.nexus'
inhandle = '/Users/flashton/annot'

res_dict = get_meta_data(inhandle)

annotate_tree(res_dict, tree)

