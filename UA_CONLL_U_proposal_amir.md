# Universal Anaphora in CoNLL-U ("CoNLL-UA")

The following examples suggest extensions to CoNLL-U which would allow the publication of merged UD + UA data. Scenarios range from basic token data (no POS tags, sentence splits etc.) to fully treebanked data, which is compatible with UD validation scripts.

## Basic format examples

### A corpus with only tokenization and simple coref

  * There are no sentence breaks so numbers are sequential for entire document
  * There are no annotations, so we just use 10 columns to conform with the conll format
  * Coreference is indicate by co-index opening and closing brackets (on one line for single-token entities)
  * Since CoNLL-U demands capitalized key-value annotations with `=`, we use `Entity=`, which can be used for NER, coref, or both (see below)
  * The contents of the Entity annotation are compatible with the existing conll coref scorer
  
```
# newdoc id = GUM_voyage_tulsa
1	Tulsa	_	_	_	_	_	_	_	Entity=(1)
2	Tulsa	_	_	_	_	_	_	_	Entity=(1)
3	is	_	_	_	_	_	_	_	_
4	in	_	_	_	_	_	_	_	_
5	the	_	_	_	_	_	_	_	Entity=(2
6	Green	_	_	_	_	_	_	_	_
7	Country	_	_	_	_	_	_	_	_
8	region	_	_	_	_	_	_	_	_
9	of	_	_	_	_	_	_	_	_
10	Oklahoma	_	_	_	_	_	_	_	Entity=(3)2)
11	.	_	_	_	_	_	_	_	_
12	It	_	_	_	_	_	_	_	Entity=(1)
13	is	_	_	_	_	_	_	_	_
14	also	_	_	_	_	_	_	_	_
15	called	_	_	_	_	_	_	_	_
16	“	_	_	_	_	_	_	_	_
17	T-town	_	_	_	_	_	_	_	Entity=(1)
18	”	_	_	_	_	_	_	_	_
```

### Same with only entity types

  * This format is usable for NER type annotation (or non-named, and also nested entities) 
  * All entities of the same type have the same label, coref is not indicated
  * Note that if we have spans with conflicting hierarchy, indices must be used as above (but will never repeat, since we have no coref)

```
# newdoc id = GUM_voyage_tulsa
1	Tulsa	_	_	_	_	_	_	_	Entity=(place)
2	Tulsa	_	_	_	_	_	_	_	Entity=(place)
3	is	_	_	_	_	_	_	_	_
4	in	_	_	_	_	_	_	_	_
5	the	_	_	_	_	_	_	_	Entity=(place
6	Green	_	_	_	_	_	_	_	_
7	Country	_	_	_	_	_	_	_	_
8	region	_	_	_	_	_	_	_	_
9	of	_	_	_	_	_	_	_	_
10	Oklahoma	_	_	_	_	_	_	_	Entity=(place)place)
11	.	_	_	_	_	_	_	_	_
12	It	_	_	_	_	_	_	_	Entity=(place)
13	is	_	_	_	_	_	_	_	_
14	also	_	_	_	_	_	_	_	_
15	called	_	_	_	_	_	_	_	_
16	“	_	_	_	_	_	_	_	_
17	T-town	_	_	_	_	_	_	_	Entity=(place)
18	”	_	_	_	_	_	_	_	_
```

### Basic coref and entity types

  * Both types of information are combined
  * Singletons can be expressed by an unrepeated index
  * Note that coref scorers don't have to be disturbed by entity types, since technically we could consider `place-1` to be a monolithic ID, which is just as unique as `1` across mentions

```
# newdoc id = GUM_voyage_tulsa
1	Tulsa	_	_	_	_	_	_	_	Entity=(place-1)
2	Tulsa	_	_	_	_	_	_	_	Entity=(place-1)
3	is	_	_	_	_	_	_	_	_
4	in	_	_	_	_	_	_	_	_
5	the	_	_	_	_	_	_	_	Entity=(place-2
6	Green	_	_	_	_	_	_	_	_
7	Country	_	_	_	_	_	_	_	_
8	region	_	_	_	_	_	_	_	_
9	of	_	_	_	_	_	_	_	_
10	Oklahoma	_	_	_	_	_	_	_	Entity=(place-3)place-2)
11	.	_	_	_	_	_	_	_	_
12	It	_	_	_	_	_	_	_	Entity=(place-1)
13	is	_	_	_	_	_	_	_	_
14	also	_	_	_	_	_	_	_	_
15	called	_	_	_	_	_	_	_	_
16	“	_	_	_	_	_	_	_	_
17	T-town	_	_	_	_	_	_	_	Entity=(place-1)
18	”	_	_	_	_	_	_	_	_
```

## Extensions

### Entity linking (a.k.a. Wikification)

  * Entity linking or 'Wikification' can be added using the same notation, as the last portion after the separator
  * Literal hyphens in the entity link identifier should be escaped as `&#45;` if needed
  * The following example uses GUM's convention of Wikipedia page identifiers as entity identifiers

```
# newdoc id = GUM_voyage_tulsa
1	Tulsa	_	_	_	_	_	_	_	Entity=(place-1-Tulsa)
2	Tulsa	_	_	_	_	_	_	_	Entity=(place-1-Tulsa)
3	is	_	_	_	_	_	_	_	_
4	in	_	_	_	_	_	_	_	_
5	the	_	_	_	_	_	_	_	Entity=(place-2-Green_Country
6	Green	_	_	_	_	_	_	_	_
7	Country	_	_	_	_	_	_	_	_
8	region	_	_	_	_	_	_	_	_
9	of	_	_	_	_	_	_	_	_
10	Oklahoma	_	_	_	_	_	_	_	Entity=(place-3-Oklahoma)place-2-Green_Country)
11	.	_	_	_	_	_	_	_	_
12	It	_	_	_	_	_	_	_	Entity=(place-1-Tulsa)
13	is	_	_	_	_	_	_	_	_
14	also	_	_	_	_	_	_	_	_
15	called	_	_	_	_	_	_	_	_
16	“	_	_	_	_	_	_	_	_
17	T-town	_	_	_	_	_	_	_	Entity=(place-1-Tulsa)
18	”	_	_	_	_	_	_	_	_
```

### POS tags and dependency treebanking

  * Since conllu is built for treebanking, we can just reuse the existing conllu spec
  * Line space separates sentences
  * IDs restart each sentence, but unique sentence IDs can be specified (optional in conllu)
  * Note that multiple annotations in the MISC column (col 10) are pipe-separated, based on the conll spec (see `SpaceAfter` below for example)
  * For more information about UD tagsets, morphological categories, etc. see https://universaldependencies.org/format.html
  
```
# newdoc id = GUM_voyage_tulsa
# sent_id = GUM_voyage_tulsa-1
# text = Tulsa
1	Tulsa	Tulsa	PROPN	NNP	Number=Sing	0	root	_	Entity=(place-1)

# sent_id = GUM_voyage_tulsa-2
# text = Tulsa is in the Green Country region of Oklahoma.
1	Tulsa	Tulsa	PROPN	NNP	Number=Sing	7	nsubj	_	Entity=(place-1)
2	is	be	AUX	VBZ	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin	7	cop	_	_
3	in	in	ADP	IN	_	7	case	_	_
4	the	the	DET	DT	Definite=Def|PronType=Art	7	det	_	Entity=(place-2
5	Green	Green	PROPN	NNP	Number=Sing	6	amod	_	_
6	Country	Country	PROPN	NNP	Number=Sing	7	compound	_	_
7	region	region	NOUN	NN	Number=Sing	0	root	_	_
8	of	of	ADP	IN	_	9	case	_	_
9	Oklahoma	Oklahoma	PROPN	NNP	Number=Sing	7	nmod	_	Entity=(place-3)place-2)|SpaceAfter=No
10	.	.	PUNCT	.	_	1	punct	_	_  
```

### Minimum span / entity heads

  * For fuzzy matching and other purposes, it can be useful to have a minimum or core span which systems must identify for each entity.
  * In many contexts, this will be the syntactic head of the phrase, but we need some facilities in case the min span is multiple, possible discontinuous tokens
  * Proposal: add min spec to entity brackets, with token indices refering to position within entity (not token IDs in sentence, in case the entity spans multiple sentences). Token indices can be comma separated, e.g. `(place-2-min:4,5` means a place entity, unique entity ID 2, begins on this line, and the min span is tokens 4 and 5 of this entity span.
  
```
# newdoc id = GUM_voyage_tulsa
# sent_id = GUM_voyage_tulsa-1
# text = Tulsa
1	Tulsa	Tulsa	PROPN	NNP	Number=Sing	0	root	_	Entity=(place-1-min:1)

# sent_id = GUM_voyage_tulsa-2
# text = Tulsa is in the Green Country region of Oklahoma.
1	Tulsa	Tulsa	PROPN	NNP	Number=Sing	7	nsubj	_	Entity=(place-1-min:1)
2	is	be	AUX	VBZ	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin	7	cop	_	_
3	in	in	ADP	IN	_	7	case	_	_
4	the	the	DET	DT	Definite=Def|PronType=Art	7	det	_	Entity=(place-2-min:4
5	Green	Green	PROPN	NNP	Number=Sing	6	amod	_	_
6	Country	Country	PROPN	NNP	Number=Sing	7	compound	_	_
7	region	region	NOUN	NN	Number=Sing	0	root	_	_
8	of	of	ADP	IN	_	9	case	_	_
9	Oklahoma	Oklahoma	PROPN	NNP	Number=Sing	7	nmod	_	Entity=(place-3-min:1)place-2-min:4)|SpaceAfter=No
10	.	.	PUNCT	.	_	1	punct	_	_  
```

## Multiple anaphora components

### Split antecedent

  * Split antecedent coref is not transitive: in "Kim met Alex ... they", the plural only refers back to both entities together, and not to each mention, or other mentions of the individual entities
  * However, each mentioned entity, including the aggregate one, should be represented as usual in the `Entity` field
  * Since more mentions can appear before and after the split antecedent, we need a way to mark which mention is the anaphor
  * Proposal: Use an additional `Split` annotation referencing each antecedent link from the anaphor to its antecedent, which will appear at the first token of the anaphor, e.g. `Split=person-1<person-3,person-2<person-3` means that person-3, which begins at this line, refers back to `person-1` and `person-2`
  
```
# sent_id = GUM_bio_bernoulli-14
# text = He is said to have had a bad relationship with his father.
# s_type = decl
1	He	he	PRON	PRP	Case=Nom|Gender=Masc|Number=Sing|Person=3|PronType=Prs	3	nsubj:pass	_	Entity=(person-1)
2	is	be	AUX	VBZ	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin	3	aux:pass	_	_
3	said	say	VERB	VBN	Tense=Past|VerbForm=Part	0	root	_	_
4	to	to	PART	TO	_	6	mark	_	_
5	have	have	AUX	VB	VerbForm=Inf	6	aux	_	_
6	had	have	VERB	VBN	Tense=Past|VerbForm=Part	3	xcomp	_	_
7	a	a	DET	DT	Definite=Ind|PronType=Art	9	det	_	Entity=(abstract-54
8	bad	bad	ADJ	JJ	Degree=Pos	9	amod	_	_
9	relationship	relationship	NOUN	NN	Number=Sing	6	obj	_	_
10	with	with	ADP	IN	_	12	case	_	_
11	his	his	PRON	PRP$	Gender=Masc|Number=Sing|Person=3|Poss=Yes|PronType=Prs	12	nmod:poss	_	Entity=(person-45(person-1)
12	father	father	NOUN	NN	Number=Sing	9	nmod	_	Entity=abstract-54)person-45)|SpaceAfter=No
13	.	.	PUNCT	.	_	3	punct	_	_

# sent_id = GUM_bio_bernoulli-15
# text = Upon both of them entering and tying for first place in a scientific contest at the University of Paris, Johann, unable to bear the "shame" of being compared Daniel's equal, banned Daniel from his house.
# s_type = decl
1	Upon	upon	SCONJ	IN	_	5	mark	_	_
2	both	both	PRON	DT	_	5	nsubj	_	Entity=(person-55|Split=person-1<person-55,person-45<person-55
3	of	of	ADP	IN	_	4	case	_	_
4	them	they	PRON	PRP	Case=Acc|Number=Plur|Person=3|PronType=Prs	2	nmod	_	Entity=person-55)
```

### Bridging anaphora

  * Since bridging is also not transitive, we again need a mechanism to indicate what is pointing to what, while assuming that entity IDs already exist in `Entity=`
  * For example, we need to distinguish `The car <- the door <- the handle` (a chain) from `The car <- the door, (the car) <- the wheel` (two bridging anaphora to the same antecedent)
  * Proposal: use the same logic as for Split, using an annotation called `Bridge` (possibly we can add subtypes of bridging as well, similar to dependency subtypes)

```
# sent_id = GUM_bio_gordon-32
1	An	a	DET	DT	Definite=Ind|PronType=Art	6	det	_	Discourse=joint:75->74|Entity=(abstract-142
2	incomplete	incomplete	ADJ	JJ	Degree=Pos|Polarity=Neg	6	amod	_	_
3	and	and	CCONJ	CC	_	4	cc	_	_
4	faulty	faulty	ADJ	JJ	Degree=Pos	2	conj	_	_
5	German	German	ADJ	JJ	Degree=Pos	6	amod	_	_
6	translation	translation	NOUN	NN	Number=Sing	21	nsubj:pass	_	SpaceAfter=No
7	,	,	PUNCT	,	_	8	punct	_	_
8	edited	edit	VERB	VBN	Tense=Past|VerbForm=Part	6	acl	_	Discourse=elaboration:76->75
9	by	by	ADP	IN	_	10	case	_	_
10	Dr	Dr	PROPN	NNP	Number=Sing	8	obl	_	Entity=(person-143
11	Moritz	Moritz	PROPN	NNP	Number=Sing	10	flat	_	_
12	Posselt	Posselt	PROPN	NNP	Number=Sing	10	flat	_	Entity=abstract-142)person-143)
13	(	(	PUNCT	-LRB-	_	18	punct	_	Discourse=elaboration:77->75|SpaceAfter=No
14	Tagebuch	Tagebuch	X	FW	_	18	compound	_	Entity=(abstract-142
15	des	des	X	FW	_	18	compound	_	_
16	Generals	Generals	X	FW	_	18	compound	_	_
17	Patrick	Patrick	PROPN	NNP	Number=Sing	18	compound	_	_
18	Gordon	Gordon	PROPN	NNP	Number=Sing	6	appos	_	Entity=abstract-142)|SpaceAfter=No
19	)	)	PUNCT	-RRB-	_	18	punct	_	_
20	was	be	AUX	VBD	Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin	21	aux:pass	_	Discourse=same-unit:78->75
21	published	publish	VERB	VBN	Tense=Past|VerbForm=Part	0	root	_	SpaceAfter=No
22	,	,	PUNCT	,	_	25	punct	_	_
23	the	the	DET	DT	Definite=Def|PronType=Art	25	det	_	Entity=(abstract-144|Bridge=abstract-142<abstract-144
24	first	first	ADJ	JJ	Degree=Pos|NumType=Ord	25	amod	_	_
25	volume	volume	NOUN	NN	Number=Sing	21	parataxis	_	Entity=abstract-144)
26	at	at	ADP	IN	_	27	case	_	_
27	Moscow	Moscow	PROPN	NNP	Number=Sing	25	orphan	_	Entity=(place-95)
28	in	in	ADP	IN	_	29	case	_	_
29	1849	1849	NUM	CD	NumType=Card	25	orphan	_	Entity=(time-145)|SpaceAfter=No
30	,	,	PUNCT	,	_	32	punct	_	_
31	the	the	DET	DT	Definite=Def|PronType=Art	32	det	_	Entity=(abstract-146|Bridge=abstract-142<abstract-146
32	second	second	ADJ	JJ	Degree=Pos|NumType=Ord	25	conj	_	Entity=abstract-146)
33	at	at	ADP	IN	_	34	case	_	_
34	St	St	PROPN	NNP	Number=Sing	32	orphan	_	Entity=(place-147
35	Petersburg	Petersburg	PROPN	NNP	Number=Sing	34	flat	_	Entity=place-147)
```