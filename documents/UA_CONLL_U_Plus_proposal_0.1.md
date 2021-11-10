# Universal Anaphora in CoNLL-U-Plus ("CoNLL-UA-Exploded")

The following examples illustrate the proposed extensions to UD's CoNLL-U-Plus format to encode the information layers proposed in the Universal Anaphora format using separate columns for different types of information.
The description is a modification of  Amir Zeldes' proposal for a format based on the CONLL-U format, using the Misc column to encode all information ("CONLL-U-Compact"), but the examples have been reordered to  follow the same order as in the UA discussion document

## The Core Anaphoric Layers

### A corpus with only tokenization and the mandatory identity layer

(This is the same example from the GUM corpus as in Amir's proposal, but the annotations have been hand-edited by me)

  * There are no sentence breaks so numbers are sequential for entire document
  * There are no annotations, so we just include the mandatory non-anaphoric layers and use 10 columns to conform with the conll format
  * In this version of the example, coreference is indicate by co-index opening and closing brackets (on one line for single-token entities), as done in the CONLL Coreference format
  * The limitation of this format is that the only information provided about markables is their boundaries and the coreference chain they belong to. While this may also work for singletons, there is  no proviso for non-referring markables, as "Town" would be according to the ARRAU guidelines. One option is to mark such markables with empty parentheses. 
  
```
# newdoc id = GUM_voyage_tulsa
# sent_id = GUM_voyage_tulsa-1
# text = Tulsa
1	Tulsa	_	_	_	_	_	_	_	(1)

# sent_id = GUM_voyage_tulsa-2
# text = Tulsa is in the Green Country region of Oklahoma
1	Tulsa	_	_	_	_	_	_	_	(1)
2	is	_	_	_	_	_	_	_	_
3	in	_	_	_	_	_	_	_	_
4	the	_	_	_	_	_	_	_	(2
5	Green	_	_	_	_	_	_	_	_
6	Country	_	_	_	_	_	_	_	_
7	region	_	_	_	_	_	_	_	_
8	of	_	_	_	_	_	_	_	_
9	Oklahoma	_	_	_	_	_	_	_	(3) 2)
10	.	_	_	_	_	_	_	_	_

# sent_id = GUM_voyage_tulsa-3
# text = It is also called "T-town"
11	It	_	_	_	_	_	_	_	(1)
12	is	_	_	_	_	_	_	_	_
13	also	_	_	_	_	_	_	_	_
14	called	_	_	_	_	_	_	_	_
15	“	_	_	_	_	_	_	_	_
16	T-town	_	_	_	_	_	_	_	()
17	”	_	_	_	_	_	_	_	_
```

### Same example, but in SEMEVAL2010/EVALITA2012/CRAC2018 format


  * In the  format introduced for the SEMEVAL 2010 Shared Task on Multilingual coreference, and then used for EVALITA 2012 and CRAC 2018, all markables are explicitly given an identifier and represented in BIO format, and entities are marked using a symbolic identifier.
  * This format is clunkier than the format used in CONLL 2012 but more explicit.
  * We should discuss what format is preferrable, but for the moment the CRAC format is used in the rest of this document.
  * Note that following CONLL and CRAC the entity is specified with the first token of the markable, but perhaps it should be specified on the same line as the MIN

  
```
# newdoc id = GUM_voyage_tulsa
# sent_id = GUM_voyage_tulsa-1
# text = Tulsa
1	Tulsa	_	_	_	_	_	_	_	B_markable_1=set_1

# sent_id = GUM_voyage_tulsa-2
# text = Tulsa is in the Green Country region of Oklahoma
1	Tulsa	_	_	_	_	_	_	_	B_markable_2=set_1
2	is	_	_	_	_	_	_	_	_
3	in	_	_	_	_	_	_	_	_
4	the	_	_	_	_	_	_	_	B_markable_3=set_2
5	Green	_	_	_	_	_	_	_	I_markable_3
6	Country	_	_	_	_	_	_	_	I_markable_3
7	region	_	_	_	_	_	_	_	I_markable_3
8	of	_	_	_	_	_	_	_	I_markable_3
9	Oklahoma	_	_	_	_	_	_	I_markable_3@B_markable_4=set_3
10	.	_	_	_	_	_	_	_	_

# sent_id = GUM_voyage_tulsa-3
# text = It is also called "T-town"
11	It	_	_	_	_	_	_	_	B_markable_5=set_1
12	is	_	_	_	_	_	_	_	_
13	also	_	_	_	_	_	_	_	_
14	called	_	_	_	_	_	_	_	_
15	“	_	_	_	_	_	_	_	_
16	T-town	_	_	_	_	_	_	_	B_markable_6
17	”	_	_	_	_	_	_	_	_
```


### Optional core anaphoric layer: minimum span / entity heads

  * For fuzzy matching and other purposes, it can be useful to have a minimum or core span which systems must identify for each entity, as originally proposed in MUC
  * In most contexts, this will be the syntactic head of the phrase, but there are some cases in which the syntactic head according to UD is not appropriate for anaphoric purposes (e.g., in coordination) and we need some facilities in case the min span is multiple, possible discontinuous tokens 
  * Proposal: in UA exploded, a MIN column is used. In CRAC, the MIN column of a markable reported the min span for all tokens in the markable. Here, we propose a simplified notation, in which only the min words are marked.


```
# newdoc id = GUM_voyage_tulsa
# sent_id = GUM_voyage_tulsa-1
# text = Tulsa
1	Tulsa	_	_	_	_	_	_	_	B_markable_1=set_1	markable_1

# sent_id = GUM_voyage_tulsa-2
# text = Tulsa is in the Green Country region of Oklahoma
1	Tulsa	_	_	_	_	_	_	_	B_markable_2=set_1	markable_2
2	is	_	_	_	_	_	_	_	_			_
3	in	_	_	_	_	_	_	_	_			_
4	the	_	_	_	_	_	_	_	B_markable_3=set_2	_
5	Green	_	_	_	_	_	_	_	I_markable_3		_
6	Country	_	_	_	_	_	_	_	I_markable_3		_
7	region	_	_	_	_	_	_	_	I_markable_3		markable_3
8	of	_	_	_	_	_	_	_	I_markable_3		_
9	Oklahoma	_	_	_	_	_	_	I_markable_3@B_markable_4=set_3	markable_4
10	.	_	_	_	_	_	_	_	_

# sent_id = GUM_voyage_tulsa-3
# text = It is also called "T-town"
11	It	_	_	_	_	_	_	_	B_markable_5=set_1	markable_5
12	is	_	_	_	_	_	_	_	_			_
13	also	_	_	_	_	_	_	_	_			_
14	called	_	_	_	_	_	_	_	_			_	
15	“	_	_	_	_	_	_	_	_			_
16	T-town	_	_	_	_	_	_	_	B_markable_6		markable_6
17	”	_	_	_	_	_	_	_	_
```

* For multi-head words such as *New York*, all forms in  the min span are marked

```
# newdoc id = Artificial_example
# sent_id = Artificial_example-1
# text = New York is a big city
1	New	_	_	_	_	_	_	_	B_markable_1=set_1	markable_1
2	York	_	_	_	_	_	_	_	I_markable_1		markable_1
3	is	_	_	_	_	_	_	_	_ 			_
4	a	_	_	_	_	_	_	_	B_markable_2		_	
5	big	_	_	_	_	_	_	_	I_markable_2		_	
6	city	_	_	_	_	_	_	_	I_markable_2		markable_2
```

### Optional core anaphoric layer: Sem_Type

  * The Sem_Type layer provides information about the semantic type of a markable: whether it is referential or not (and in  this case, whether it is Discourse New - DN - or Discourse Old - DO), or expletive, predicative, quantifier, coordination, or some other type of non-referring expression (e.g., an idiom)
  * In CRAC, the Sem_Type argument was called REFERENCE and was specified for every token of a markable. In UA, I suggest we specify it only once - we could specify it either with the first token in a markable (the same token that contains the entity information), or with the head.


```
# newdoc id = GUM_voyage_tulsa
# sent_id = GUM_voyage_tulsa-1
# text = Tulsa
1	Tulsa	_	_	_	_	_	_	_	B_markable_1=set_1	markable_1	dn

# sent_id = GUM_voyage_tulsa-2
# text = Tulsa is in the Green Country region of Oklahoma
1	Tulsa	_	_	_	_	_	_	_	B_markable_2=set_1	markable_2	do
2	is	_	_	_	_	_	_	_	_			_		_
3	in	_	_	_	_	_	_	_	_			_		_
4	the	_	_	_	_	_	_	_	B_markable_3=set_2	_		dn
5	Green	_	_	_	_	_	_	_	I_markable_3		_		_
6	Country	_	_	_	_	_	_	_	I_markable_3		_		_
7	region	_	_	_	_	_	_	_	I_markable_3		markable_3	_
8	of	_	_	_	_	_	_	_	I_markable_3		_		_
9	Oklahoma	_	_	_	_	_	_	I_markable_3@B_markable_4=set_3	markable_4	dn
10	.	_	_	_	_	_	_	_	_				_

# sent_id = GUM_voyage_tulsa-3
# text = It is also called "T-town"
11	It	_	_	_	_	_	_	_	B_markable_5=set_1	markable_5	do
12	is	_	_	_	_	_	_	_	_			_		_
13	also	_	_	_	_	_	_	_	_			_		_
14	called	_	_	_	_	_	_	_	_			_		
15	“	_	_	_	_	_	_	_	_			_		_
16	T-town	_	_	_	_	_	_	_	B_markable_6		markable_6	predicative
17	”	_	_	_	_	_	_	_	_			_		_
```

## Basic Non-Anaphoric Layers

### Basic layers

  * We adopt the CONLL-U spec for all the basic layers up to dependency syntax - 9 layers in total, so that the Identity layer would be the 10th, MIN the 11th, and Sem_Type the 12th (Note: in CONLL Coref other layers, such as WordSense, Constituency, and Propbank, were also included before the coreference layer, we need to decide what to do about those)
  * Line space separates sentences
  * IDs restart each sentence, but unique sentence IDs can be specified (optional in conllu)
  * For more information about UD tagsets, morphological categories, etc. see https://universaldependencies.org/format.html
  
  
```
# newdoc id = GUM_voyage_tulsa
# sent_id = GUM_voyage_tulsa-1
# text = Tulsa
1	Tulsa	Tulsa	PROPN	NNP	Number=Sing	0	root	_	B_markable_1=set_1

# sent_id = GUM_voyage_tulsa-2
# text = Tulsa is in the Green Country region of Oklahoma.
1	Tulsa	Tulsa	PROPN	NNP	Number=Sing	7	nsubj	_	B_markable_2=set_1
2	is	be	AUX	VBZ	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin	7	cop	_	_
3	in	in	ADP	IN	_	7	case	_	_
4	the	the	DET	DT	Definite=Def|PronType=Art	7	det	_	B_markable_3=set_2
5	Green	Green	PROPN	NNP	Number=Sing	6	amod	_	_	I_markable_3
6	Country	Country	PROPN	NNP	Number=Sing	7	compound	_	I_markable_3
7	region	region	NOUN	NN	Number=Sing	0	root	_	_	I_markable_3
8	of	of	ADP	IN	_	9	case	_	_	_	I_markable_3
9	Oklahoma	Oklahoma	PROPN	NNP	Number=Sing	7	nmod	_	I_markable_3@B_markable_4=set_3
10	.	.	PUNCT	.	_	1	punct	_	_  
```


## The Additional Anaphoric and Reference Layers

In addition to the mandatory Identity layer, we want to be able to encode additional types of anaphoric reference, as well as reference to the outside world.
Although some of these types of anaphoric reference could be seen as types of Identity reference (e.g., split antecedent anaphors, discourse dexis) we suggest to encode each of these  additional layers of anaphoric reference in its own dedicated column. 

### Split antecedent anaphors

  * Proposal: Use an additional SPLIT column (this would be the 13th column), in which one mention of each antecedent of the split anaphor is specified as being an element of the entity to which the split anaphor refers to.
  * In the following example, one mention of set_1 (*He*) and one mention of the father, set_3, are specified in the SPLIT column as being element of  set_4, the plural entity referred to by *them*. (Note that further references to set_4 are still encoded in the Identity column)
  
```
# sent_id = GUM_bio_bernoulli-14
# text = He is said to have had a bad relationship with his father.
# s_type = decl
1	He	he	PRON	PRP	Case=Nom|Gender=Masc|Number=Sing|Person=3|PronType=Prs	3	nsubj:pass	_	B_markable_1=set_1	markable_1	do	set_4
2	is	be	AUX	VBZ	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin	3	aux:pass	_	_			_		_	_
3	said	say	VERB	VBN	Tense=Past|VerbForm=Part				0	root	_	_	_			_		_
4	to	to	PART	TO	_	6	mark	_	_			_	_	_
5	have	have	AUX	VB	VerbForm=Inf	6	aux	_	_		_	_	_
6	had	have	VERB	VBN	Tense=Past|VerbForm=Part	3	xcomp	_	_	_	_	_
7	a	a	DET	DT	Definite=Ind|PronType=Art	9	det	_	B_markable_2=set_2	_	dn	_
8	bad	bad	ADJ	JJ	Degree=Pos	9	amod	_	_	I_markable_2			_	_			_
9	relationship	relationship	NOUN	NN	Number=Sing	6	obj	_	_	I_markable_2	markable_2			_
10	with	with	ADP	IN	_	12	case	_	_	I_markable_2	_	_
11	his	his	PRON	PRP$	Gender=Masc|Number=Sing|Person=3|Poss=Yes|PronType=Prs	12	nmod:poss	_	I_markable_2@B_markable_3=set_1@B_markable_4=set_3	markable_3	do	_
12	father	father	NOUN	NN	Number=Sing	9	nmod	_	I_markable_2@I_markable_3@I_markable_4	markable_4	dn	set_4
13	.	.	PUNCT	.	_	3	punct	_	_	_					_		_

# sent_id = GUM_bio_bernoulli-15
# text = Upon both of them entering and tying for first place in a scientific contest at the University of Paris, Johann, unable to bear the "shame" of being compared Daniel's equal, banned Daniel from his house.
# s_type = decl
1	Upon	upon	SCONJ	IN	_	5	mark	_	_	_	_	_
2	both	both	PRON	DT	_	5	nsubj	_	B_markable_5	markable_5	quantifier	_
3	of	of	ADP	IN	_	4	case	_	I_markable_5	_		_		_
4	them	they	PRON	PRP	Case=Acc|Number=Plur|Person=3|PronType=Prs	2	nmod	_   I_markable_5@B_markable_6=set_4	markable_6	do	_		
```

### Bridging references

  * Proposal: as with Split antecedents,  the Bridging layer is encoded using a separate  Bridging column (the 14th column) specifying bridging references using the same **bridg ref=bridg rel= anchor markable= anchor entity** syntax as in CRAC 2018.

```
# sent_id = GUM_bio_gordon-32
# text = An incomplete and faulty German translation , edited by Dr Moritz Posselt ( Tagebuch des Generals Patrick Gordon ) was published , the first volume at Moscow in 1849, the second at St Petersburg
1	An	a	DET	DT	Definite=Ind|PronType=Art	6	det	_	B_markable_1=set_1 	  _ 	dn	_	  _	 
2	incomplete	incomplete ADJ JJ Degree=Pos|Polarity=Neg	6	amod	_	I_markable_1		  _	_	_	  _	
3	and	and	CCONJ	CC	_		4	cc	_	I_markable_1	_	_	_	_		
4	faulty	faulty	ADJ	JJ	Degree=Pos	2	conj	_	I_markable_1	_	_	_		_
5	German	German	ADJ	JJ	Degree=Pos	6	amod	_	I_markable_1	_	_	_		_
6	translation translation	NOUN NN	Number=Sing	21	nsubj:pass _	I_markable_1	markable_1	_	_	_
7	,	,	PUNCT	,	_		8	punct	_	I_markable_1	_		_	_	_
8	edited	edit	VERB	VBN	Tense=Past|VerbForm=Part	6	acl	_	I_markable_1	_	_	_	_	
9	by	by	ADP	IN	_		10	case	_	_	_	_	_		_	
10	Dr	Dr	PROPN	NNP	Number=Sing	8	obl	_	I_markable_1@B_markable_2=set_2	_	dn	_	_	
11	Moritz	Moritz	PROPN	NNP	Number=Sing	10	flat	_	I_markable_1@I_markable_2	_	_	_	_
12	Posselt	Posselt	PROPN	NNP	Number=Sing	10	flat	_	I_markable_1@I_markable_2	markable_2	_	_	_
13	(	(	PUNCT	-LRB-	_	18	punct	_	I_markable_1@I_markable_2		_	_	_	_	
14	Tagebuch Tagebuch X	FW	_	18	compound _	I_markable_1@I_markable_2@B_markable_3	markable_3	predicative	_	_
15	des	des	X	FW	_	18	compound _	I_markable_1@I_markable_2@I_markable_3	markable_3	_		_	_
16	Generals	Generals	X	FW	_	18	compound	_	I_markable_1@I_markable_2@I_markable_3	markable_3	_	_	_
17	Patrick	Patrick	PROPN	NNP	Number=Sing	18	compound	_	I_markable_1@I_markable_2@I_markable_3	markable_3		_	_	_
18	Gordon	Gordon	PROPN	NNP	Number=Sing	6	appos	_	I_markable_1@I_markable_2@I_markable_3	markable_3 	_	_	_
19	)	)	PUNCT	-RRB-	_	18	punct	_	_	_					_	   	_	_
20	was	be	AUX	VBD	Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin	21	aux:pass	_	_  	_	_	_	_ 
21	published	publish	VERB	VBN	Tense=Past|VerbForm=Part	0	root	_	_		_	_  	_
22	,	,	PUNCT	,	_	25	punct	_	_
23	the	the	DET	DT	Definite=Def|PronType=Art	25	det	_	B_markable_4=set_3	_	dn	_	B_markable_4=poss=markable_1=set_1
24	first	first	ADJ	JJ	Degree=Pos|NumType=Ord	25	amod	_	_	I_markable_4		_	_	_	I_markable_4
25	volume	volume	NOUN	NN	Number=Sing	21	parataxis	_	I_markable_4			markable_4	_	_	I_markable_4
26	at	at	ADP	IN	_	27	case	_	_	_	_				_		_
27	Moscow	Moscow	PROPN	NNP	Number=Sing	25	orphan	_	B_markable_5=set_4			markable_5	dn	_	_
28	in	in	ADP	IN	_	29	case	_	_	_					_		_	_
29	1849	1849	NUM	CD	NumType=Card	25	orphan	_	B_markable_6=set_5			markable_6	dn	_	_
30	,	,	PUNCT	,	_	32	punct	_	_	_					_		_	_
31	the	the	DET	DT	Definite=Def|PronType=Art	32	det	_	B_markable_7=set_6	_		dn	_	B_markable_7=poss=markable_1=set_1
32	second	second	ADJ	JJ	Degree=Pos|NumType=Ord	25	conj	_	I_markable_7			markable_7	_	_	I_markable_7
33	at	at	ADP	IN	_	34	case	_	_	_	_				_		_
34	St	St	PROPN	NNP	Number=Sing	32	orphan	_	B_markable_8=set_7			markable_8	dn	_	_
35	Petersburg	Petersburg	PROPN	NNP	Number=Sing	34	flat	_	I_markable_8		markable_8	_	_	_
```

### Discourse Deixis

  * Proposal: follow the approach adopted in event coreference, i.e., encode discourse deixis as done with normal coreference, with  a Discourse_Deixis column in which both discourse units and references to these units occur as markables, and form coreference chains.
  * Even more than for the case of entity coreference, we may want to have a notion of min, as partial interpretation will be common.

```
# newdoc id = Artificial_example_2
# sent_id = Artificial_example-1
# text = John met Mary.
1	John	_	_	_	_	_	_	_	B_markable_1=set_1	markable_1	dn	_	_	B_dd_markable_1=ddset_1
2	met	_	_	_	_	_	_	_	_ 			_		_	_	_	I_dd_markable_1
3	Mary	_	_	_	_	_	_	_	B_markable_2		markable_2	dn	_	_	I_dd_markable_1	
5	.	_	_	_	_	_	_	_	_			_		_	_	_	I_dd_markable_1	


# sent_id = Artificial_example-2
# text = That is not true .
1	That	_	_	_	_	_	_	_	B_markable_3		markable_3	do	_	_	B_dd_markable_2=ddset_1
2	is	_	_	_	_	_	_	_	_ 			_		_	_	_	_
3	not	_	_	_	_	_	_	_	_			_		_	_	_	_
3	true	_	_	_	_	_	_	_	_			_		_	_	_	_
5	.	_	_	_	_	_	_	_	_			_		_	_	_	_
```

### Reference

  * The Reference column is used to represent direct reference. This can be used both to encode references to the visual situation in multimodal data (e.g., in the TRAINS subset of ARRAU, or in GNOME), and entity linking or 'Wikification' (e.g., in GUM)


```
# newdoc id = GUM_voyage_tulsa
# sent_id = GUM_voyage_tulsa-1
# text = Tulsa
1	Tulsa	_	_	_	_	_	_	_	B_markable_1=set_1	markable_1	dn	_	_	_	Tulsa,_Oklahoma

# sent_id = GUM_voyage_tulsa-2
# text = Tulsa is in the Green Country region of Oklahoma
1	Tulsa	_	_	_	_	_	_	_	B_markable_2=set_1	markable_2	do	_	_	_	Tulsa,_Oklahoma	
2	is	_	_	_	_	_	_	_	_			_		_	_	_	_	_
3	in	_	_	_	_	_	_	_	_			_		_	_	_	_	_		
4	the	_	_	_	_	_	_	_	B_markable_3=set_2	_		dn	_	_	_	Green_Country
5	Green	_	_	_	_	_	_	_	I_markable_3		_		_	_	_	_	_
6	Country	_	_	_	_	_	_	_	I_markable_3		_		_	_	_	_	_
7	region	_	_	_	_	_	_	_	I_markable_3		markable_3	_	_	_	_	_	
8	of	_	_	_	_	_	_	_	I_markable_3		_		_	_	_	_	_
9	Oklahoma	_	_	_	_	_	_	I_markable_3@B_markable_4=set_3	markable_4	dn	_	_	Oklahoma
10	.	_	_	_	_	_	_	_	_			_		_	_	_	_	_

# sent_id = GUM_voyage_tulsa-3
# text = It is also called "T-town"
11	It	_	_	_	_	_	_	_	B_markable_5=set_1	markable_5	do	_	_	_	Tulsa,_Oklahoma
12	is	_	_	_	_	_	_	_	_			_		_	_	_	_	_
13	also	_	_	_	_	_	_	_	_			_		_	_	_	_	_
14	called	_	_	_	_	_	_	_	_			_		_	_	_	_	_
15	“	_	_	_	_	_	_	_	_			_		_	_	_	_	_
16	T-town	_	_	_	_	_	_	_	B_markable_6		markable_6	predicative _	_	_	_
17	”	_	_	_	_	_	_	_	_			_		_	   _	_	_	_
```


## Additional Non-Anaphoric Layers

In addition to the anaphoric layers, we expect documents in Universal Anaphora format will contain other linguistic information relevant to anaphoric interpretation, including the Constituency, Wordsense and Proposition information contained in the Ontonotes corpus, the Nom_Sem information (entity type, genericity, etc) contained in GNOME and ARRAU, the RST information contained in GUM, etc.
The format should allow additional columns for this information. In  the examples below, these additional columns are located after the Anaphoric columns in the order


* Nom_Sem
* Constituency
* Wordsense
* Proposition
* RST

but a different order is possible using the CONLL-U Plus format. In the examples below, empty columns are used except for the core anaphoric layers and the additional non-anaphoric layers.


### Nom_Sem

  * The Nom_Sem layer specifies properties of referential expressions which are relevant for anaphoric interpretation, such as entity type, genericity, etc.
  * This information is specified using the same format as the Feats column 


```
# newdoc id = GUM_voyage_tulsa
# sent_id = GUM_voyage_tulsa-1
# text = Tulsa
1	Tulsa	_	_	_	_	_	_	_	B_markable_1=set_1	markable_1	dn	_	_	_	_	Entity_Type=place|Genericity=generic-no

# sent_id = GUM_voyage_tulsa-2
# text = Tulsa is in the Green Country region of Oklahoma
1	Tulsa	_	_	_	_	_	_	_	B_markable_2=set_1	markable_2	do	_	_	_	_	Entity_Type=place|Genericity=generic-no	
2	is	_	_	_	_	_	_	_	_			_		_	_	_	_	_	_
3	in	_	_	_	_	_	_	_	_			_		_	_	_	_	_	_
4	the	_	_	_	_	_	_	_	B_markable_3=set_2	_		dn	_	_	_	_	Entity_Type=place|Genericity=generic-no
5	Green	_	_	_	_	_	_	_	I_markable_3		_		_	_	_	_	_	_
6	Country	_	_	_	_	_	_	_	I_markable_3		_		_	_	_	_	_	_
7	region	_	_	_	_	_	_	_	I_markable_3		markable_3	_	_	_	_	_	_	
8	of	_	_	_	_	_	_	_	I_markable_3		_		_	_	_	_	_	_
9	Oklahoma	_	_	_	_	_	_	I_markable_3@B_markable_4=set_3	markable_4	dn	_	_	_	Entity_Type=place|Genericity=generic-no		
10	.	_	_	_	_	_	_	_	_			_		_	_	_	_	_	_

# sent_id = GUM_voyage_tulsa-3
# text = It is also called "T-town"
11	It	_	_	_	_	_	_	_	B_markable_5=set_1	markable_5	do	_	_	_	_	Entity_Type=place|Genericity=generic-n
12	is	_	_	_	_	_	_	_	_			_		_	_	_	_	_	_
13	also	_	_	_	_	_	_	_	_			_		_	_	_	_	_	_
14	called	_	_	_	_	_	_	_	_			_		_	_	_	_	_	_
15	“	_	_	_	_	_	_	_	_			_		_	_	_	_	_	_
16	T-town	_	_	_	_	_	_	_	B_markable_6		markable_6	predicative _	_	_	_	_
17	”	_	_	_	_	_	_	_	_			_		_	   _	_	_	_	_
```



### Constituency, Wordsense, Proposition, and other CONLL Coref layers

  * This additional information available in the CONLL 2012 corpus should be encoded using additional columns which could e.g., follow the Nom_Sem column

  
### RST Layer

  * Discourse structure information could be encoded in its own column following the previous layers using existing standards - in the example below I used the GUM format for RST

```
# sent_id = GUM_bio_gordon-32
# text = An incomplete and faulty German translation , edited by Dr Moritz Posselt ( Tagebuch des Generals Patrick Gordon ) was published , the first volume at Moscow in 1849, the second at St Petersburg
1	An	a	DET	DT	Definite=Ind|PronType=Art	6	det	_	B_markable_1=set_1 	  _ 	dn	_	  _	  _  _	_      _  _	_   Discourse=joint:75->74
2	incomplete	incomplete ADJ JJ Degree=Pos|Polarity=Neg	6	amod	_	I_markable_1		  _	_	_	  _	  _  _	_      _  _	_   _
3	and	and	CCONJ	CC	_		4	cc	_	I_markable_1	_	_	_	_ _	_	_	  _	  _  _	_		
4	faulty	faulty	ADJ	JJ	Degree=Pos	2	conj	_	I_markable_1	_	_	_		_	_	  _	  _  _	_
5	German	German	ADJ	JJ	Degree=Pos	6	amod	_	I_markable_1	_	_	_		_	_	  _	  _  _	_
6	translation translation	NOUN NN	Number=Sing	21	nsubj:pass _	I_markable_1	markable_1	_	_	_	_	  _	  _  _	_
7	,	,	PUNCT	,	_		8	punct	_	I_markable_1	_		_	_	_	_	  _	  _  _	_
8	edited	edit	VERB	VBN	Tense=Past|VerbForm=Part	6	acl	_	I_markable_1	_	_	_	_	  _	  _  _	_     _	 _	Discourse=elaboration:76->75
9	by	by	ADP	IN	_		10	case	_	_	_	_	_		_	
10	Dr	Dr	PROPN	NNP	Number=Sing	8	obl	_	I_markable_1@B_markable_2=set_2	_	dn	_	_	
11	Moritz	Moritz	PROPN	NNP	Number=Sing	10	flat	_	I_markable_1@I_markable_2	_	_	_	_
12	Posselt	Posselt	PROPN	NNP	Number=Sing	10	flat	_	I_markable_1@I_markable_2	markable_2	_	_	_
13	(	(	PUNCT	-LRB-	_	18	punct	_	I_markable_1@I_markable_2		_	_	_	_	_	_	_	_	_	_	Discourse=elaboration:77->75|SpaceAfter=No
14	Tagebuch Tagebuch X	FW	_	18	compound _	I_markable_1@I_markable_2@B_markable_3	markable_3	predicative	_	_
15	des	des	X	FW	_	18	compound _	I_markable_1@I_markable_2@I_markable_3	markable_3	_		_	_
16	Generals	Generals	X	FW	_	18	compound	_	I_markable_1@I_markable_2@I_markable_3	markable_3	_	_	_
17	Patrick	Patrick	PROPN	NNP	Number=Sing	18	compound	_	I_markable_1@I_markable_2@I_markable_3	markable_3		_	_	_
18	Gordon	Gordon	PROPN	NNP	Number=Sing	6	appos	_	I_markable_1@I_markable_2@I_markable_3	markable_3 	_	_	_
19	)	)	PUNCT	-RRB-	_	18	punct	_	_	_					_	   	_	_
20	was	be	AUX	VBD	Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin	21	aux:pass	_	_  	_	_	_	_ _	_	_	_	_	_	Discourse=same-unit:78->75
21	published	publish	VERB	VBN	Tense=Past|VerbForm=Part	0	root	_	_		_	_  	_
22	,	,	PUNCT	,	_	25	punct	_	_
23	the	the	DET	DT	Definite=Def|PronType=Art	25	det	_	B_markable_4=set_3	_	dn	_	B_markable_4=poss=markable_1=set_1	_	_	_	_	_	_	_
24	first	first	ADJ	JJ	Degree=Pos|NumType=Ord	25	amod	_	_	I_markable_4		_	_	_	I_markable_4
25	volume	volume	NOUN	NN	Number=Sing	21	parataxis	_	I_markable_4			markable_4	_	_	I_markable_4
26	at	at	ADP	IN	_	27	case	_	_	_	_				_		_
27	Moscow	Moscow	PROPN	NNP	Number=Sing	25	orphan	_	B_markable_5=set_4			markable_5	dn	_	_
28	in	in	ADP	IN	_	29	case	_	_	_					_		_	_
29	1849	1849	NUM	CD	NumType=Card	25	orphan	_	B_markable_6=set_5			markable_6	dn	_	_
30	,	,	PUNCT	,	_	32	punct	_	_	_					_		_	_
31	the	the	DET	DT	Definite=Def|PronType=Art	32	det	_	B_markable_7=set_6	_		dn	_	B_markable_7=poss=markable_1=set_1
32	second	second	ADJ	JJ	Degree=Pos|NumType=Ord	25	conj	_	I_markable_7			markable_7	_	_	I_markable_7
33	at	at	ADP	IN	_	34	case	_	_	_	_				_		_
34	St	St	PROPN	NNP	Number=Sing	32	orphan	_	B_markable_8=set_7			markable_8	dn	_	_
35	Petersburg	Petersburg	PROPN	NNP	Number=Sing	34	flat	_	I_markable_8		markable_8	_	_	_

