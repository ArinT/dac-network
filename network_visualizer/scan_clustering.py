#!/usr/bin/env python
import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.settings')
import Queue
import math
import argparse
import pickle
# from unidecode import unidecode
# from network_visualizer.models import Citations, Papers, Authors, Works

MIN_NEIGHBORS = 2
STRUCTURAL_SIMILARITY_THRESHOLD = .5

# enum adapted from http://stackoverflow.com/questions/702834/whats-the-common-practice-for-enums-in-python
class Label:
	Unlabeled, Core, Hub, Outlier, NonMember = range(5)

def structural_similarity(set1, set2):
	intersection = set1.intersection(set2)
	union = set1.union(set2)
	return float(len(intersection)) / math.sqrt(float(len(union)))

class Network(object):
	def __init__(self):
		self.network_dict = {}
		self.names = {}	

	# Returns a set of the neighbors of n_id (either paperid or authorid)
	# This isn't the formal definition of neighbors, it doesn't include the actual node
	def neighbors(self, n_id):
		return self.network_dict[n_id]

	# Returns a set of the similar neighbors of the node
	# Rectifies the difference of formal definition of neighbors
	def similar_neighbors(self, n_id):
		n_set = self.neighbors(n_id)
		ret = set()
		n_set.add(n_id)
		for n in n_set:
			n_set2 = self.neighbors(n)
			n_set2.add(n)
			if structural_similarity(n_set, n_set2) >= STRUCTURAL_SIMILARITY_THRESHOLD:
				ret.add(n)
		return ret

	# Returns a list of all of the network_ids
	def network_ids(self):
		return self.network_dict.keys()

	# Returns the name of the network item with the id n_id
	def name(self, n_id):
		return self.names[n_id]

class AuthorNetwork(Network):
	def __init__(self, up_to_year = 0):
		super(AuthorNetwork, self).__init__()
		works = Works.objects.all()
		if up_to_year != 0:
			papers = Papers.objects.filter(year__lte=up_to_year)
			works = works.filter(paperid__in=papers)
		for author in Authors.objects.all():
			aid = author.authorid
			self.names[aid] = unidecode(author.authorname)
			rel_works = works.filter(authorid=aid).values("paperid")
			neighbors = works.filter(paperid__in=rel_works)
			ret = set()
			for n in neighbors:
				ret.add(n.authorid)
			ret.discard(aid)
			self.network_dict[aid] = ret

class CitationNetwork(Network):
	def __init__(self, up_to_year = 0):
		super(CitationNetwork, self).__init__()
		papers = Papers.objects.all()
		if up_to_year != 0:
			papers = Papers.objects.filter(year__lte=up_to_year)
		for paper in papers:
			pid = paper.paperid
			self.names[pid] = unidecode(paper.title)
			targets = Citations.objects.filter(sourcepaperid=pid)
			sources = Citations.objects.filter(targetpaperid=pid)
            # Only have to filter sources, targets are necessarily before the up_to_year
			sources = sources.filter(sourcepaperid__in=papers)
			ret = set()
			for target in targets:
				ret.add(target.targetpaperid)
			for source in sources:
				ret.add(source.sourcepaperid)
			self.network_dict[pid] = ret

class ClusterIDGenerator(object):
	def __init__(self):
		self._id = 0

	def generate_id(self):
		self._id += 1
		return self._id	

	def num_clusters(self):
		return self._id

def generate_networks():
	network = CitationNetwork()
	pickle.dump(network, open("static/pickles/citation_network.p", "wb"))
	network = AuthorNetwork()
	pickle.dump(network, open("static/pickles/author_network.p", "wb"))
	current_year = 2014
	for i in range(2002, current_year + 1):
		network = CitationNetwork(up_to_year=i)
		pickle.dump(network, open("static/pickles/citation_network_" + str(i) + ".p", "wb"))
		network = AuthorNetwork(up_to_year=i)
		pickle.dump(network, open("static/pickles/author_network_" + str(i) + ".p", "wb"))

def load_network(network_type, year=0):
	# Hack necessary to load pickle outside of normal module
	main_module = sys.modules["__main__"]
	sys.modules["__main__"] = sys.modules[__name__]
	if network_type != "author" and network_type != "citation":
		return None
	file_str = "static/pickles/" + network_type + "_network"
	if year != 0:
		file_str += "_" + str(year)
	file_str += ".p"
	the_pickle = pickle.load(open(file_str, "rb"))
	sys.modules["__main__"] = main_module
	return the_pickle


# Returns if a paper is a core
# If the paper is unlabeled, we label it either a core or nonmember
def is_core(network, n_id):
	label = labels[n_id]
	if label == Label.Unlabeled:
		# Label the paper either a core or a nonmember
		m = network.similar_neighbors(n_id)
		if len(m) >= MIN_NEIGHBORS:
			labels[n_id] = Label.Core
			return True
		else:
			labels[n_id] = Label.NonMember 
			return False
	elif label == Label.Core:
		return True
	else:
		return False

def main(min_neighbors, structural_similarity_threshold, network_type, up_to_year=0):
	network = load_network(network_type, up_to_year)
	if network is None:
		return []

	global STRUCTURAL_SIMILARITY_THRESHOLD
	STRUCTURAL_SIMILARITY_THRESHOLD = structural_similarity_threshold
	global MIN_NEIGHBORS
	MIN_NEIGHBORS = min_neighbors
	global labels
	labels = {}
	cluster_ids = {}

	for n_id in network.network_ids():
		labels[n_id] = Label.Unlabeled
		cluster_ids[n_id] = 0

	n_ids = labels.keys()
	gen = ClusterIDGenerator()
	for n_id in n_ids:
		# Check if paper is a Core
		# NB: The is_core method labels the paper for us if it is unlabeled (we don't have to do it here)
		if labels[n_id] == Label.Unlabeled and is_core(network, n_id):
			new_id = gen.generate_id()
			cluster_ids[n_id] = new_id
			neighbors = Queue.Queue()
			for n in network.similar_neighbors(n_id):
				neighbors.put(n)
			while not neighbors.empty():
				y = neighbors.get()
				labels[y] = Label.Core
				R = network.similar_neighbors(y)
				cluster_ids[y] = new_id
				for x in R:
					if labels[x] == Label.NonMember:
						cluster_ids[x] = new_id
						labels[x] = Label.Core
					if labels[x] == Label.Unlabeled:
						neighbors.put(x)

	for n_id in n_ids:
		if labels[n_id] == Label.NonMember:
			n_set = network.neighbors(n_id)
			if len(n_set) == 0:
				labels[n_id] = Label.Outlier
			else:
				"""cluster_id = cluster_ids[list(n_set)[0]]
				for n in n_set:
					if cluster_ids[n] != cluster_id:
						labels[n_id] = Label.Hub
						break"""
				first_cluster = -1
				for n in n_set:
					if first_cluster > 0 and cluster_ids[n] > 0 and first_cluster != cluster_ids[n]:
						labels[n_id] = Label.Hub
						break
					if first_cluster < 1 and cluster_ids[n] > 0:
						first_cluster = cluster_ids[n]
				if labels[n_id] != Label.Hub:
					labels[n_id] = Label.Outlier

	clusters = {}
	for i in xrange(1, gen.num_clusters() + 1):
		clusters[i] = []
	# 0 is outliers
	clusters[0] = []
	# -1 is hubs
	clusters[-1] = []
	for n_id in n_ids:
		if cluster_ids[n_id] > 0:
			clusters[cluster_ids[n_id]].append(n_id)
		elif labels[n_id] == Label.Hub:
			clusters[-1].append(n_id)
		else:
			clusters[0].append(n_id)

	return clusters

def get_cluster_idxs(clusters):
	cluster_idxs = {}
	for key in clusters:
		if key < 1:
			continue
		for n_id in clusters[key]:
			cluster_idxs[n_id] = key
	return cluster_idxs


if __name__ == "__main__":
	# generate_networks()
	parser = argparse.ArgumentParser(description="Run SCAN algorithm")
	parser.add_argument("min_neighbors", help="The minimum neighbor parameter for SCAN", type=int)
	parser.add_argument("similarity_threshold", help="The structural similarity threshold for SCAN", type=float)
	parser.add_argument("network_type", help="The network to run SCAN on", choices=["author", "citation"])
	parser.add_argument("--up_to_year", help="A year to limit the data", type=int, choices=range(2002,2015))
	args = parser.parse_args()
	if args.up_to_year:
		main(args.min_neighbors, args.similarity_threshold, args.network_type, args.up_to_year)
	else:
		main(args.min_neighbors, args.similarity_threshold, args.network_type)

"""with open("SCAN_results_citation_4_22.txt", "a") as f:
	for i in xrange(1, gen.num_clusters() + 1):
		f.write("Cluster " + str(i) + "\n")
		for n_id in clusters[i]:
			f.write(network.name(n_id) + "\n")
		f.write("\n")
	f.write("Hubs\n")
	for n_id in clusters[-1]:
		f.write(network.name(n_id) + "\n")
	f.write("\nOutliers\n")
	for n_id in clusters[0]:
		f.write(network.name(n_id) + "\n")"""






















