from nltk.corpus import wordnet as wn
import csv
class adjective():
	def __init__(self,filename,adjectives):
		self.filename=filename
	  	self.adjectives=adjectives
		self.seed_list=[]
		self.pos=0
		self.neg=0

	def file_write(self):
		sead_file=open(self.filename,'w')
		#print(self.seed_list);
		writer = csv.writer(sead_file, delimiter=' ',quotechar='|', quoting= csv.QUOTE_MINIMAL )
		for row in self.seed_list:
			writer.writerow(row)

	def file_read(self):
		sead_file=open(self.filename,'r')
		csv_read= csv.reader(sead_file,delimiter=' ')
		for row in csv_read:
			self.seed_list.append(row)

	def orientation(self):
		print(self.adjectives)
		while(1):
			size1=len(self.seed_list)
			for row in self.adjectives:
				self.search()
			size2=len(self.seed_list)
			if(size1==size2):
				break

		return [self.pos,self.neg]

	def search(self):
		self.pos=0;
		self.neg=0;
		flag=[0]*(len(self.adjectives)+5)
		for row in self.adjectives:
			for r in self.seed_list:
				if(r[0]==row):
					if(int(r[1])==-1):
						self.neg+=1
					else:
				 		self.pos+=1
					flag[self.adjectives.index(row)]=1
					break;


		for row in self.adjectives:
			if(flag[self.adjectives.index(row)]==1):
				continue;
			for r in self.seed_list:
				if(self.syn_search(r[0],row)):
					self.pos+=1
					self.seed_list.append([row,r[1]])
					break
				elif(self.ant_search(r[0],row)):
					self.neg+=1
					self.seed_list.append([row,str(-1* int(r[1]))] )
					break;

	def syn_search(self,seed_word,adjective):
		for ss in wn.synsets(seed_word):
			for sim in ss.lemmas():
				if(sim.name()==adjective):
					return 1
		return 0;


	def ant_search(self,seed_word,adjective):
		for ss in wn.synsets(seed_word):
			for sim in ss.lemmas():
				if(sim.antonyms()):
					if(sim.antonyms()[0].name()==adjective):
						return 1
					elif(self.syn_search(sim.antonyms()[0].name(),adjective)):
						return 1
		return 0;



filename='seed_list.csv'
adjectiv= ['beautiful','concrete','quick','worse','cheap','good','nice','excellent','slow']
cl=adjective(filename,adjectiv)
cl.file_read()
[pos,neg]=cl.orientation()
cl.file_write()
print(pos,neg)
