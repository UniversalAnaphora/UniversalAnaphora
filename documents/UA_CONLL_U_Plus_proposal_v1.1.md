# Universal Anaphora in CoNLL-U-Plus ("CoNLL-UA-Exploded")

  Massimo Poesio (with input from Nafise Moosavi, Anja Nedoluzhko, Juntao Yu and Amir Zeldes)

Version 1.1, 2024/05/09

This document illustrates the proposed extensions to Universal Dependencies' CoNLL-U-Plus format to encode the information layers proposed in the Universal Anaphora `exploded' format using separate columns for each type of reference information, including both anaphora and dexis.

The proposed format is meant to encode the same information as, and be convertible to and from,  the 'compact' UA formats  based on the CONLL-U format and using the Misc column to encode all information ("CONLL-U-Compact") proposed by Anna Nedoluzhko and Amir Zeldes.

## Basic Non-Anaphoric Layers

### Basic layers

  * We adopt the CONLL-U spec for all the basic layers up to the MISC column - 10 layers in total including Misc.
  * Following the CONLL-U-PLUS format, each document is preceded by a global.columns line specifying the columns
  * A # newdoc line precedes every document
  * A # sent_id line precedes every sentence, followed by a # text line providing the untokenized text
  * A # text line specifies the sentence and precedes the tokens
  * Token line numbers are sequential for entire document
  * An optional # visual_situation line is used for multimodal data. The line is followed by lines for every object that can be referred to deictically in the Reference column (see below)
  * A Line space separates sentences
  * For more information about UD tagsets, morphological categories, etc. see https://universaldependencies.org/format.html
  * See next for the specification of the IDENTITY line
  
  
```
# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC IDENTITY BRIDGING DISCOURSE_DEIXIS REFERENCE NOM_SEM
# newdoc id = GUM_voyage_tulsa
# sent_id = GUM_voyage_tulsa-1
# text = Tulsa
1	Tulsa	Tulsa	PROPN	NNP	Number=Sing	0	root	_	_	(EntityID=1|MarkableID=markable_1)

# sent_id = GUM_voyage_tulsa-2
# text = Tulsa is in the Green Country region of Oklahoma.
2	Tulsa	Tulsa	PROPN	NNP	Number=Sing	7	nsubj	_	_	(EntityID=1|MarkableID=markable_2)
3	is	be	AUX	VBZ	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin	7	cop	_	_	_
4	in	in	ADP	IN	_	7	case	_	_			_
5	the	the	DET	DT	Definite=Def|PronType=Art	7	det	_	_	(EntityID=2|MarkableID=markable_3
6	Green	Green	PROPN	NNP	Number=Sing	6	amod	_	_	_	_
7	Country	Country	PROPN	NNP	Number=Sing	7	compound	_	_	_
8	region	region	NOUN	NN	Number=Sing	0	root	_	_	_	_
9	of	of	ADP	IN	_	9	case	_	_	_	_	_
10	Oklahoma	Oklahoma	PROPN	NNP	Number=Sing	7	nmod	_	_	(EntityId=3|MarkableID=markable_4))
11	.	.	PUNCT	.	_	1	punct	_	_ 	_ 
```


## The Core Anaphoric Layers

###  The mandatory identity layer




  * identity reference information is specified in the IDENTITY column.
    (The Identity layer is the 11th column, after MISC. Note: in CONLL Coref other layers, such as WordSense, Constituency, and Propbank, were also included before the coreference layer, we need to decide what to do about those. In the present version of the proposal they FOLLOW the anaphoric layers.
  * Identity layer markables are specified by opening and closing brackets  (on one line for single-token entities), as  in the CONLL Coreference layer, and by an EntityID (= clusterid) feature, specifying the integer index of the coreference chain to which the markable belongs.
  * Note that following CONLL and CRAC the entity is specified with the first token of the markable, but perhaps it should be specified on the same line as the MIN
  * In corpora in which singletons are annotated, the EntityID is specified for singletons as well.
  * For non-referring markables, a special 'Pseudo-Entity' is specified.
  * Optionally,  a MarkableID feature may be specified together with the EntityID information, e.g., for corpora encoding bridging information as pointers to mentions.
  * We do not provide any annotations apart from  the anaphoric information in the following examples,  we just include the mandatory non-anaphoric layers.
  
```
# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC IDENTITY BRIDGING DISCOURSE_DEIXIS REFERENCE NOM_SEM
# newdoc id = GUM_voyage_tulsa
# sent_id = GUM_voyage_tulsa-1
# text = Tulsa
1	Tulsa	_	_	_	_	_	_	_	_	(EntityID=1|MarkableID=markable_1)

# sent_id = GUM_voyage_tulsa-2
# text = Tulsa is in the Green Country region of Oklahoma
2	Tulsa	_	_	_	_	_	_	_	_	(EntityID=1|MarkableID=markable_2)
3	is	_	_	_	_	_	_	_	_	_
4	in	_	_	_	_	_	_	_	_	_
5	the	_	_	_	_	_	_	_	_	(EntityID=2|MarkableID=markable_3
6	Green	_	_	_	_	_	_	_	_	_
7	Country	_	_	_	_	_	_	_	_	_
8	region	_	_	_	_	_	_	_	_	_
9	of	_	_	_	_	_	_	_	_	_
10	Oklahoma	_	_	_	_	_	_	_	(EntityID=3|MarkableID=markable_4)) 
11	.	_	_	_	_	_	_	_	_

# sent_id = GUM_voyage_tulsa-3
# text = It is also called "T-town"
12	It	_	_	_	_	_	_	_	_	(EntityID=1|MarkableID=markable_5)
13	is	_	_	_	_	_	_	_	_	_
14	also	_	_	_	_	_	_	_	_	_
15	called	_	_	_	_	_	_	_	_	_
16	“	_	_	_	_	_	_	_	_	(EntityID=4-Pseudo|MarkableID=markable_6
17	T-town	_	_	_	_	_	_	_	_	
18	”	_	_	_	_	_	_	_	_	)
```



### Optional core anaphoric layer: minimum span / entity heads

  * For fuzzy matching and other purposes, it can be useful to have a minimum or core span which systems must identify for each entity, as originally proposed in MUC
  * In most contexts, this will be the syntactic head of the phrase, but there are some cases in which the syntactic head according to UD is not appropriate for anaphoric purposes (e.g., in coordination) and we need some facilities in case the min span is multiple, possible discontinuous tokens 
  * In UA exploded, a MIN feature can added to the IDENTITY column in the line of the first token in the markable.

```
# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC IDENTITY BRIDGING DISCOURSE_DEIXIS REFERENCE NOM_SEM
# newdoc id = GUM_voyage_tulsa
# sent_id = GUM_voyage_tulsa-1
# text = Tulsa
1	Tulsa	_	_	_	_	_	_	_	_	(EntityID=1|MarkableID=markable_1|Min=1)

# sent_id = GUM_voyage_tulsa-2
# text = Tulsa is in the Green Country region of Oklahoma
2	Tulsa	_	_	_	_	_	_	_	_	(EntityID=1|MarkableID=markable_2|Min=2)
3	is	_	_	_	_	_	_	_	_	_
4	in	_	_	_	_	_	_	_	_	_
5	the	_	_	_	_	_	_	_	_	(EntityID=2|MarkableID=markable_3|Min=7
6	Green	_	_	_	_	_	_	_	_	_	_
7	Country	_	_	_	_	_	_	_	_	_
8	region	_	_	_	_	_	_	_	_	_
9	of	_	_	_	_	_	_	_	_	_
10	Oklahoma	_	_	_	_	_	_	_	(EntityID=3|MarkableID=markable_4|Min=10)) 
11	.	_	_	_	_	_	_	_	_

# sent_id = GUM_voyage_tulsa-3
# text = It is also called "T-town"
12	It	_	_	_	_	_	_	_	_	(EntityID=1|MarkableID=markable_5|Min=12)
13	is	_	_	_	_	_	_	_	_	_
14	also	_	_	_	_	_	_	_	_	_
15	called	_	_	_	_	_	_	_	_	_
16	“	_	_	_	_	_	_	_	_	(EntityID=4-Pseudo|MarkableID=markable_6|Min=17
17	T-town	_	_	_	_	_	_	_	_	
18	”	_	_	_	_	_	_	_	_	)
```

* For multi-head words such as *New York*, the range of  the min span is specified

```
# newdoc id = Artificial_example
# sent_id = Artificial_example-1
# text = New York is a big city
1	New	_	_	_	_	_	_	_	_	(EntityID=1|MarkableID=1|Min=1,2
2	York	_	_	_	_	_	_	_	_	)
3	is	_	_	_	_	_	_	_	_ 	_
4	a	_	_	_	_	_	_	_	_	(EntityID=2-Pseudo|MarkableID=2|Min=6
5	big	_	_	_	_	_	_	_	_	_
6	city	_	_	_	_	_	_	_	_	)
```

### Optional core anaphoric layer: SemType

  * The SemType layer provides information about the semantic function of the noun phrase: whether it is referential or not, i.e., whether it refers to a discourse entity (and in  this case, whether the entity is Discourse New - DN - or Discourse Old - DO), or expletive, predicate, quantifier, coordination, or some other type of non-referring expression (e.g., an idiom)
  * In CRAC, the SemType argument was called REFERENCE and was specified for every token of a markable. In UA, this information is provided it only once, as an (optional) feature on the Identity column on the first line of the markable.
  * The values of this attribute for ARRAU are **dn, do, predicate, quantifier, coordination, expletive, idiom, undef_reference, incomplete** but different corpora will use different values, unifiying this aspects could be one of the objectives of UA 2.



```
# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC IDENTITY BRIDGING DISCOURSE_DEIXIS REFERENCE NOM_SEM
# newdoc id = GUM_voyage_tulsa
# sent_id = GUM_voyage_tulsa-1
# text = Tulsa
1	Tulsa	_	_	_	_	_	_	_	_	(EntityID=1|MarkableID=markable_1|Min=1|SemType=dn)

# sent_id = GUM_voyage_tulsa-2
# text = Tulsa is in the Green Country region of Oklahoma
2	Tulsa	_	_	_	_	_	_	_	_	(EntityID=1|MarkableID=markable_2|Min=2|SemType=do)
3	is	_	_	_	_	_	_	_	_	_
4	in	_	_	_	_	_	_	_	_	_
5	the	_	_	_	_	_	_	_	_	(EntityID=2|MarkableID=markable_3|Min=7|SemType=dn
6	Green	_	_	_	_	_	_	_	_	_	_
7	Country	_	_	_	_	_	_	_	_	_
8	region	_	_	_	_	_	_	_	_	_
9	of	_	_	_	_	_	_	_	_
_
10	Oklahoma	_	_	_	_	_	_	_	(EntityID=3|MarkableID=markable_4|Min=10|SemType=dn)) 
11	.	_	_	_	_	_	_	_	_

# sent_id = GUM_voyage_tulsa-3
# text = It is also called "T-town"
12	It	_	_	_	_	_	_	_	_	(EntityID=1|MarkableID=markable_5|Min=12|SemType=do)
13	is	_	_	_	_	_	_	_	_	_
14	also	_	_	_	_	_	_	_	_	_
15	called	_	_	_	_	_	_	_	_	_
16	“	_	_	_	_	_	_	_	_	(EntityID=4-Pseudo|MarkableID=markable_6|Min=17|SemType=predicate
17	T-town	_	_	_	_	_	_	_	_	
18	”	_	_	_	_	_	_	_	_	)
```



## The Additional Anaphoric and Reference Layers

In addition to the mandatory Identity layer, we want to be able to encode additional types of anaphoric reference annotated in a number of existing corpora, as well as deictic reference to the outside world.
Although some of these types of anaphoric reference  (e.g., split antecedent anaphors, discourse deixis) could be seen as types of Identity reference, we suggest to encode each of these  additional layers of anaphoric reference in its own dedicated column. 

### Split antecedent anaphors

  * Split antecedent anaphors are represented in the Identity column, by specifying at the beginning of one mention of each antecedent of the split anaphor that that  entity is an ElementOf the entity to which the split anaphor refers to.
  * This is illustrated in the following highly simplified artificial example.

```
# newdoc id = Artificial_example_2
# sent_id = Artificial_example-1
              Identity						     

1    John     (EntityID=1|MarkableID=markable_1|Min=1|SemType=dn|ElementOf=3) 
2    met                                                                              
3    Mary     (EntityID=2|MarkableID=markable_2|Min=2|SemType=dn|ElementOf=3) 
4    .
5    They     (EntityID=3|MarkableID=markable_3|Min=2|SemType=do)                                 
6    went
7   to
```


  * In the following real life example from GUM, in association with one mention of Entity 1, Bernoulli (*He*) and one mention of his father, Entity 3, it is specified in the Identity column that these entities are  elements of entity 4, the plural entity referred to by *them*. (Note that further references to 4 are still encoded in the Identity column)
  * This example also illustrates the need to specify the Entity which is an element of the set as nested mentions are possible
  * Line 11 illustrates the use of a @ to separate the opening information for markable_3 and markable_4 
  
```
# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC IDENTITY BRIDGING DISCOURSE_DEIXIS REFERENCE NOM_SEM
# newdoc id = GUM_bio_bernoulli
# sent_id = GUM_bio_bernoulli-14
# text = He is said to have had a bad relationship with his father.
# s_type = decl
1	He	he	PRON	PRP	Case=Nom|Gender=Masc|Number=Sing|Person=3|PronType=Prs	3	nsubj:pass	_	_	(EntityID=1|MarkableID=markable_1|Min=1|SemType=do|ElementOf=4)	
2	is	be	AUX	VBZ	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin	3	aux:pass	_	_	_	_
3	said	say	VERB	VBN	Tense=Past|VerbForm=Part			0	root	_	_	_	_		
4	to	to	PART	TO	_	6	mark	_	_		_	_	
5	have	have	AUX	VB	VerbForm=Inf	6	aux	_		_	_	_
6	had	have	VERB	VBN	Tense=Past|VerbForm=Part	3	xcomp	_	_	_	_	
7	a	a	DET	DT	Definite=Ind|PronType=Art	9	det	_	_	(EntityId=2|MarkableId=markable_2|Min=9|SemType=dn	_
8	bad	bad	ADJ	JJ	Degree=Pos	9	amod	_	_	_	_
9	relationship	relationship	NOUN	NN	Number=Sing	6	obj	_	_	_	_
10	with	with	ADP	IN	_	12	case	_	_	_	_
11	his	his	PRON	PRP$	Gender=Masc|Number=Sing|Person=3|Poss=Yes|PronType=Prs	12	nmod:poss	_	_	(EntityId=3|MarkableId=markable_3|Min=12|SemType=dn@(EntityId=1|MarkableId=markable_4|Min=11|SemType=do|ElementOf=4)	
12	father	father	NOUN	NN	Number=Sing	9	nmod	_	_		)	_		
13	.	.	PUNCT	.	_	3	punct	_	_	_					_		_

# sent_id = GUM_bio_bernoulli-15
# text = Upon both of them entering and tying for first place in a scientific contest at the University of Paris, Johann, unable to bear the "shame" of being compared Daniel's equal, banned Daniel from his house.
# s_type = decl
14	Upon	upon	SCONJ	IN	_	5	mark	_	_	_	_	_
15	both	both	PRON	DT	_	5	nsubj	_	_	(EntityID=6_Pseudo|MarkableID=markable_5|Min=2|SemType=quantifier
16	of	of	ADP	IN	_	4	case	_	_	_	_
17	them	they	PRON	PRP	Case=Acc|Number=Plur|Person=3|PronType=Prs	2	nmod	_	_   	(EntityId=4|MarkableID=markable_6|Min=17|SemType=do))	_
```

  * Note that a distinct Split layer was proposed in the original markup document, but was subsequently eliminated.

### Bridging references

  * Bridging information is stored in a separate  Bridging column.
  * The bridging reference informaton is specified in the first line of the bridging mention.
  * The information provided is the same as in CRAC 2018, but using a different syntax. The full specification is  ** MarkableID=**markableID**|Rel=**rel**|MentionAnchor=**mention ID**|EntityAnchory=**entity ID** but it is expected that not all corpora will provide all of this information so only the MarkableID and one of MentionAnchor or EntityAnchor are required
  * The notation is schematically illustrated in the following example:

```
# newdoc id = Artificial_example_3
# sent_id = Artificial_example-1
Form        Identity                              Bridging

the         (EntityID=1|MarkableID=markable_1           
house       )                                                                    
.
.
the         (EntityID=2|MarkableID=markable_2    MarkableID=markable_2|Rel=poss|MentionAnchor=markable_1|EntityAnchor=1
door         )                                                                      
```

* Here is a real life example:

```
# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC IDENTITY BRIDGING DISCOURSE_DEIXIS REFERENCE NOM_SEM
# newdoc id = GUM_bio_gordon
# sent_id = GUM_bio_gordon-32
# text = An incomplete and faulty German translation , edited by Dr Moritz Posselt ( Tagebuch des Generals Patrick Gordon ) was published , the first volume at Moscow in 1849, the second at St Petersburg
1	An	a	DET	DT	Definite=Ind|PronType=Art	6	det	_	_ (EntityID=1|MarkableID=markable_1|Min=6|SemType=dn 	   	_
2	incomplete	incomplete ADJ JJ Degree=Pos|Polarity=Neg	6	amod	_	_ _							  _	_
3	and	and	CCONJ	CC	_		4	cc	_	_	_	_
4	faulty	faulty	ADJ	JJ	Degree=Pos	2	conj	_	_	_	_	_
5	German	German	ADJ	JJ	Degree=Pos	6	amod	_	_	_	_	_
6	translation translation	NOUN NN	Number=Sing	21	nsubj:pass _	_	_	_	_
7	,	,	PUNCT	,	_		8	punct	_	_	_	_	_
8	edited	edit	VERB	VBN	Tense=Past|VerbForm=Part	6	acl	_	_	_	_	_
9	by	by	ADP	IN	_		10	case	_	_	_	_	_
10	Dr	Dr	PROPN	NNP	Number=Sing	8	obl	_	_	(EntityID=2|Markable_ID=markable_2|Min=11,12|SemType=dn		_
11	Moritz	Moritz	PROPN	NNP	Number=Sing	10	flat	_	_	_							_	_
12	Posselt	Posselt	PROPN	NNP	Number=Sing	10	flat	_	_	)							_	_
13	(	(	PUNCT	-LRB-	_	18	punct	_	_	_	_							_
14	Tagebuch Tagebuch X	FW	_	18	compound _	_	(EntityID=1-Pseudo|MarkableID=markable_3|Min=14-17|SemType=predicate		_
15	des	des	X	FW	_	18	compound _	_	_									_	_
16	Generals	Generals	X	FW	_	18	compound	_	_							_	
17	Patrick	Patrick	PROPN	NNP	Number=Sing	18	compound	_	_	_							_	_
18	Gordon	Gordon	PROPN	NNP	Number=Sing	6	appos	_	_	)
19	)	)	PUNCT	-RRB-	_	18	punct	_	_	)	_	_
20	was	be	AUX	VBD	Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin	21	aux:pass	_	_  	_	_	_	_ 
21	published	publish	VERB	VBN	Tense=Past|VerbForm=Part	0	root	_	_		_	_  	_
22	,	,	PUNCT	,	_	25	punct	_	_
23	the	the	DET	DT	Definite=Def|PronType=Art	25	det	_	_	(EntityID=3|MarkableID=markable_4|Min=25|SemType=dn	MarkableID=markable_4|Rel=poss|MentionAnchor=markable_1|EntityAnchor=1
24	first	first	ADJ	JJ	Degree=Pos|NumType=Ord	25	amod	_	_	_	_							_
25	volume	volume	NOUN	NN	Number=Sing	21	parataxis	_	_	)	_
26	at	at	ADP	IN	_	27	case	_	_	_	_				_		_
27	Moscow	Moscow	PROPN	NNP	Number=Sing	25	orphan	_	_	(EntityID=4|MentionID=markable_5|Min=27|SemType=dn)		_
28	in	in	ADP	IN	_	29	case	_	_	_					_		_	_
29	1849	1849	NUM	CD	NumType=Card	25	orphan	_	_					(EntityID=5|MentionID=markable_6|Min=29|SemType=dn)	_
30	,	,	PUNCT	,	_	32	punct	_	_	_					_		_	_
31	the	the	DET	DT	Definite=Def|PronType=Art	32	det	_	_			(EntityID=6|MarkableID=markable_7|Min=31|SemType=dn	MarkableID=markable_7|Rel=poss|MentionAnchor=markable_1|EntityAnchor=1
32	second	second	ADJ	JJ	Degree=Pos|NumType=Ord	25	conj	_	_	_
33	at	at	ADP	IN	_	34	case	_	_	_	_				_		_
34	St	St	PROPN	NNP	Number=Sing	32	orphan	_	_	(EntityID=7|MentionID=markable_8|Min=34,35|SemType=dn	
35	Petersburg	Petersburg	PROPN	NNP	Number=Sing	34	flat	_	_						_
```

### Discourse Deixis

  * For Discourse Deixis we follow the approach adopted in event coreference, i.e., encode discourse deixis in the same way as normal coreference. The Discourse_Deixis column has the same format as the Identity layer, with the antecedent h discourse units and references to these units as markables, and form coreference chains.
  * With discourse deixis  it is even more important to allow for soft matching via a notion of min than it is with entity coreference,  as exact matching of boundaries is very rare even for human annotators (Artstein and Poesio, 2006). We use the same notation as for the Identity layer.
  * Strictly speaking, discourse deixis is a form of coreference, so this information could be encoded in the Identity column. For pragmatic reasons however - discourse deixis is very hard - we are proposing to treat discourse deixis resolution as entirely separate at the moment, meaning that the Discourse_Deixis layer has its own entities and its own markables, and that pronoun **that** in the following example is treated as old in the Discourse_Deixis layer, but dn in the Identity layer. We may reconsider this decision in the future.

```
# newdoc id = Artificial_example_4
# sent_id = Artificial_example-1
# text = John met Mary.
1	John	_	_	_	_	_	_	_	_	(EntityID=1|MarkableID=markable_1|Min=1|SemType=dn)		_	(EntityID=1-DD|MarkableID=dd_markable_1|Min=2|SemType=dn
2	met	_	_	_	_	_	_	_	_	_							_	_	_
3	Mary	_	_	_	_	_	_	_	_	(EntityID=2|MarkableID=markable_2|Min=3|SemType=dn)		_	_
4	.	_	_	_	_	_	_	_	_			_		_	_	)


# sent_id = Artificial_example-2
# text = That is not true .
5	That	_	_	_	_	_	_	_	_	(EntityID=3|MarkableID=markable_3|Min=5|SemType=dn)			_	(EntityID=1-DD|MarkableID=dd_markable_2|Min=5|SemType=do) 
6	is	_	_	_	_	_	_	_	_ 			_		_	_	_	_
7	not	_	_	_	_	_	_	_	_			_		_	_	_	_
8	true	_	_	_	_	_	_	_	_			_		_	_	_	_
9	.	_	_	_	_	_	_	_	_			_		_	_	_	_
```

### Reference

  * The Reference column is used to represent direct reference. This can be used both to encode references to the visual situation in multimodal data (e.g., in the TRAINS subset of ARRAU, or in GNOME), and entity linking or 'Wikification' (e.g., in GUM)
  * In the following example of use of the Reference column to encode entity linking we only illustrate the Reference column ignoring SPlit, Bridging and Discourse_Deixis. The Reference column is filled with the Wikipedia link for the entity.

```
# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC IDENTITY  BRIDGING DISCOURSE_DEIXIS REFERENCE NOM_SEM
# newdoc id = GUM_voyage_tulsa
# sent_id = GUM_voyage_tulsa-1
# text = Tulsa
1	Tulsa	_	_	_	_	_	_	_	_	(EntityID=1|MarkableID=markable_1|Min=1|SemType=dn)		_	_	Tulsa,_Oklahoma

# sent_id = GUM_voyage_tulsa-2
# text = Tulsa is in the Green Country region of Oklahoma
2	Tulsa	_	_	_	_	_	_	_	_	(EntityID=1|MarkableID=markable_2|Min=2|SemType=do)
3	is	_	_	_	_	_	_	_	_	_
4	in	_	_	_	_	_	_	_	_	_
5	the	_	_	_	_	_	_	_	_	(EntityID=2|MarkableID=markable_3|Min=7|SemType=dn		_	_	Green_Country	
6	Green	_	_	_	_	_	_	_	_	_	_
7	Country	_	_	_	_	_	_	_	_	_
8	region	_	_	_	_	_	_	_	_	_
9	of	_	_	_	_	_	_	_	_
_
10	Oklahoma	_	_	_	_	_	_	_	(EntityID=3|MarkableID=markable_4|Min=10|SemType=dn))		_	_	Oklahoma
11	.	_	_	_	_	_		_	_

# sent_id = GUM_voyage_tulsa-3
# text = It is also called "T-town"
12	It	_	_	_	_	_	_	_	_	(EntityID=1|MarkableID=markable_5|Min=12|SemType=do)
13	is	_	_	_	_	_	_	_	_	_
14	also	_	_	_	_	_	_	_	_	_
15	called	_	_	_	_	_	_	_	_	_
16	“	_	_	_	_	_	_	_	_	(EntityID=4-Pseudo|MarkableID=markable_6|Min=17|SemType=predicate
17	T-town	_	_	_	_	_	_	_	_	
18	”	_	_	_	_	_	_	_	_	)
```

* In corpora such as TRAINS, Light, or the Minecraft Dialogue Corpus, the objects referred to are predefined. In such corpora, it is possible to start the annotation by listing these objects at the beginning of the document so that references can be linked to them. This could be done in the present format by adding a # visual_situation line after the # sent_id line, followed by separate lines for every object in the scene. This description of the visual situation may occur only once at the beginning of the document if the visual situation is static, else be repeated every time that the situation changes. (Need to  check if CONLL-U-Plus rules allow this or if we need to add a pseudo-sentence at the beginning of the document / every time the visual situation changes.)

* In the following example from the TRAINS corpus 

```
# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC IDENTITY BRIDGING DISCOURSE_DEIXIS REFERENCE NOM_SEM
# newdoc id = d91-1-1
# sent_id = d91-1-1_1.1
# speaker_id = M
# text = okay
1	okay	_	_	_	_	_	_	_	_	_	_	_	_	_

# sent_id = 1.2
# speaker_id = M
# text = I have to
2	I	_	_	_	_	_	_	_	_	(EntityID=1|MarkableID=markable_1|Min=2|SemType=dn) 	_	_	M	_
3	have	_	_	_	_	_	_	_	_	_
4	to	_	_	_	_	_	_	_	_	_


# sent_id = d91-1-1_1.3
# speaker_id = M
# text = ship a boxcar of oranges to Bath by 8 o'clock today
5	ship	_	_	_	_	_	_	_	_	_	_	_	
6	a	_	_	_	_	_	_	_	_	(EntityID=2|MarkableID=markable_2|Min=7|SemType=dn		_	_	_	_
7	boxcar	_	_	_	_	_	_	_	_	_
8	of	_	_	_	_	_	_	_	_	_
9	oranges	_	_	_	_	_	_	_	_	(EntityID=3|MarkableID=markable_3|Min=9|SemType=dn))
10	to	_	_	_	_	_	_	_	_	
11	Bath	_	_	_	_	_	_	_	_	(EntityID=4|MarkableID=markable_4|Min=11|SemType=dn)		_	_	Bath
12	by	_	_	_	_	_	_	_	_
13	8       _	_	_	_	_	_	_	_
14	o'clock _	_	_	_	_	_	_	_
15	today	_	_	_	_	_	_	_	_
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
# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC IDENTITY BRIDGING DISCOURSE_DEIXIS REFERENCE NOM_SEM
# newdoc id = GUM_voyage_tulsa
# sent_id = GUM_voyage_tulsa-1
# text = Tulsa
1	Tulsa	_	_	_	_	_	_	_	_	(EntityID=1|MarkableID=markable_1|Min=1|SemType=dn)		_	_	Tulsa,_Oklahoma	Entity_Type=place|Genericity=generic-no

# sent_id = GUM_voyage_tulsa-2
# text = Tulsa is in the Green Country region of Oklahoma
2	Tulsa	_	_	_	_	_	_	_	_	(EntityID=1|MarkableID=markable_2|Min=2|SemType=do)		_	_	_	Entity_Type=place|Genericity=generic-no
3	is	_	_	_	_	_	_	_	_	_
4	in	_	_	_	_	_	_	_	_	_
5	the	_	_	_	_	_	_	_	_	(EntityID=2|MarkableID=markable_3|Min=7|SemType=dn		_	_	Green_Country	Entity_Type=place|Genericity=generic-no	
6	Green	_	_	_	_	_	_	_	_	_	_
7	Country	_	_	_	_	_	_	_	_	_
8	region	_	_	_	_	_	_	_	_	_
9	of	_	_	_	_	_	_	_	_
_
10	Oklahoma	_	_	_	_	_	_	_	(EntityID=3|MarkableID=markable_4|Min=10|SemType=dn))	_	_	_	Oklahoma	Entity_Type=place|Genericity=generic-no
11	.	_	_	_	_	_	_	_	_

# sent_id = GUM_voyage_tulsa-3
# text = It is also called "T-town"
12	It	_	_	_	_	_	_	_	_	(EntityID=1|MarkableID=markable_5|Min=12|SemType=do)	_	_	_	Entity_Type=place|Genericity=generic-no
13	is	_	_	_	_	_	_	_	_	_
14	also	_	_	_	_	_	_	_	_	_
15	called	_	_	_	_	_	_	_	_	_
16	“	_	_	_	_	_	_	_	_	(EntityID=4-Pseudo|MarkableID=markable_6|Min=17|SemType=predicate
17	T-town	_	_	_	_	_	_	_	_	
18	”	_	_	_	_	_	_	_	_	)
```


### Constituency, Wordsense, Proposition, and other CONLL Coref layers

  * This additional information available in the CONLL 2012 corpus should be encoded using additional columns which could e.g., follow the Nom_Sem column

  
### RST Layer

  * Discourse structure information could be encoded in its own column following the previous layers using existing standards - the example below follows  the GUM format for RST used in Amir Zeldes' proposal for the compact format.

```
# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC IDENTITY BRIDGING DISCOURSE_DEIXIS REFERENCE NOM_SEM RST
# newdoc id = GUM_bio_gordon
# sent_id = GUM_bio_gordon-32
# text = An incomplete and faulty German translation , edited by Dr Moritz Posselt ( Tagebuch des Generals Patrick Gordon ) was published , the first volume at Moscow in 1849, the second at St Petersburg
1	An	a	DET	DT	Definite=Ind|PronType=Art	6	det	_	_ (EntityID=1|MarkableID=markable_1|Min=6|SemType=dn 	  	_      _  _	_   Discourse=joint:75->74
2	incomplete	incomplete ADJ JJ Degree=Pos|Polarity=Neg	6	amod	_	_ _							  _	_
3	and	and	CCONJ	CC	_		4	cc	_	_	_	_
4	faulty	faulty	ADJ	JJ	Degree=Pos	2	conj	_	_	_	_	_
5	German	German	ADJ	JJ	Degree=Pos	6	amod	_	_	_	_	_
6	translation translation	NOUN NN	Number=Sing	21	nsubj:pass _	_	_	_	_
7	,	,	PUNCT	,	_		8	punct	_	_	_	_	_
8	edited	edit	VERB	VBN	Tense=Past|VerbForm=Part	6	acl	_	_	_	_	_	_	_	_	Discourse=elaboration:76->75
9	by	by	ADP	IN	_		10	case	_	_	_	_	_
10	Dr	Dr	PROPN	NNP	Number=Sing	8	obl	_	_	(EntityID=2|Markable_ID=markable_2|Min=11,12|SemType=dn	_	_
11	Moritz	Moritz	PROPN	NNP	Number=Sing	10	flat	_	_	_							_	_
12	Posselt	Posselt	PROPN	NNP	Number=Sing	10	flat	_	_	)							_	_
13	(	(	PUNCT	-LRB-	_	18	punct	_	_	_	_							_	_	_	_	Discourse=elaboration:77->75|SpaceAfter=No							_
14	Tagebuch Tagebuch X	FW	_	18	compound _	_	(EntityID=1-Pseudo|MarkableID=markable_3|Min=14-17|SemType=predicate	_	_
15	des	des	X	FW	_	18	compound _	_	_									_	_
16	Generals	Generals	X	FW	_	18	compound	_	_							_	
17	Patrick	Patrick	PROPN	NNP	Number=Sing	18	compound	_	_	_							_	_
18	Gordon	Gordon	PROPN	NNP	Number=Sing	6	appos	_	_	)
19	)	)	PUNCT	-RRB-	_	18	punct	_	_	)	_	_
20	was	be	AUX	VBD	Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin	21	aux:pass	_	_  	_	_	_	_ Discourse=same-unit:78->75
21	published	publish	VERB	VBN	Tense=Past|VerbForm=Part	0	root	_	_		_	_  	_
22	,	,	PUNCT	,	_	25	punct	_	_
23	the	the	DET	DT	Definite=Def|PronType=Art	25	det	_	_	(EntityID=3|MarkableID=markable_4|Min=25|SemType=dn		MarkableID=markable_4|Rel=poss|MentionAnchor=markable_1|EntityAnchor=1
24	first	first	ADJ	JJ	Degree=Pos|NumType=Ord	25	amod	_	_	_	_							_
25	volume	volume	NOUN	NN	Number=Sing	21	parataxis	_	_	)	_
26	at	at	ADP	IN	_	27	case	_	_	_	_				_		_
27	Moscow	Moscow	PROPN	NNP	Number=Sing	25	orphan	_	_	(EntityID=4|MentionID=markable_5|Min=27|SemType=dn)		_
28	in	in	ADP	IN	_	29	case	_	_	_					_		_	_
29	1849	1849	NUM	CD	NumType=Card	25	orphan	_	_					(EntityID=5|MentionID=markable_6|Min=29|SemType=dn)	
30	,	,	PUNCT	,	_	32	punct	_	_	_					_		_	_
31	the	the	DET	DT	Definite=Def|PronType=Art	32	det	_	_			(EntityID=6|MarkableID=markable_7|Min=31|SemType=dn	MarkableID=markable_7|Rel=poss|MentionAnchor=markable_1|EntityAnchor=1
32	second	second	ADJ	JJ	Degree=Pos|NumType=Ord	25	conj	_	_	_
33	at	at	ADP	IN	_	34	case	_	_	_	_				_		_
34	St	St	PROPN	NNP	Number=Sing	32	orphan	_	_	(EntityID=7|MentionID=markable_8|Min=34,35|SemType=dn	_
35	Petersburg	Petersburg	PROPN	NNP	Number=Sing	34	flat	_	_						_
```



## Discontinuous markables

* Discontinuous markables are to be represented by bracketing every chunk  of the markable and indicating the markable to which each chunk belongs.

```
# newdoc id = Artificial_example_2
# sent_id = Artificial_example-1
# text = The man I saw with a fancy jacket
                Identity						     
1    The        (EntityID=1|MarkableID=markable_1|Min=2|SemType=dn
2    man     	)
3    I		(EntityID=2|MarkableID=markable_2|Min=3|SemType=dn)
4    saw
5    with
6    a		(EntityID=1|MarkableID=markable_1|Min=2|SemType=dn@(EntityID=3|MarkableID=markable_3|Min=8|SemType=dn    
7    fancy
8    jacket     ))
```

## Ambiguity

* For corpora which allow annotators to mark multiple interpretations, the additional interpretations can be provided by repeating some of the columns - e.g., by adding an Identity2 column, etc.