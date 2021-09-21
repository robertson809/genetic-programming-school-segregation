# Addressing SES Segregation in Charlottle-Meckelenburg Schools: A Genetic Programming Approach

by Michael Robertson for Davidson College's Machine Reasoning Final Project

---

### Table of Contents:
- [Abstract](#abstract)
- [Introduction](#introduction)
- [Data](#data)
   - [Given Data] 
          - [Road Populations]\
          - [Road SES Status]\
          - [School Capacities]\
          - [Commuting Times]
   
  - [Prepared Data]\
          - [Road Class]\
          - [School Class]\
          - [District Class]\
          - [Assignment Class]
        
- [Experiments]
     - [Genetic Mechanisms]
     - [Selection and Evolution]

- [Results]

- [Conclusions]

- [Acknowledgements]

- [Refences]


---


### Fitness

<img src="https://render.githubusercontent.com/render/math?math=W(S) = \sum\limits_{i= 1}^{3}\left|(\frac{1}{3} - SES_{i}) \right| + 1">

In Lena’s experiments, she produced solutions based on
three different objective functions, each of which differ-
ently valued the relative importance of reducing commute
time and maximizing school SES diversity. We used only
one of her weighting functions in our experiments,

<p align="center">
<img src="https://render.githubusercontent.com/render/math?math=W(S) = \sum \left|(\frac{1}{3} - SES_{i}) \right| %2B+ 1">
</center>
</p>
where the index *i* ranges from 1 to 3.

= \sum\limits_{i= 1}^{3}\left|(\frac{1}{3} - SES_{i}) \right| %2B+ 1
W(S)=
∑^3

i= 1

#### ∣∣

```
∣(^13 −S ESi)
```
#### ∣∣

```
∣+1, which gave the highest relative weight to
```
SES diversity over commute time. Here the weighting func-
tion takes a school that has already been assigned students

and returns a positive valueW(S)∈[1,^133 ]. We defineS ES 1
as the proportion of students in the school with a low SES
status,S ES 2 as the proportion of medium SES students, and
S ES 3 as the proportion of high SES students. By definition
thenS ES 1 +S ES 2 +S ES 3 =1.
By combining the commuting distances and populations
stored in our road objects with the calculated school weights,
we can find the total fitnessF(A) of an assignmentAby
taking

#### F(A)=

#### ∑S

```
j= 1
```
#### ∑R

```
i= 1
```
```
Ti jPiW(Sj)
```
```
WhereSis the number of schools,Ris the number of
roads,Ti jis the commute time from roadito schoolj,Piis
the population of roadi,Sjis schoolj, andWis as described
above.
We see here that a higher fitness actually corresponds to
a worse solution, in a way that is counterintuitive to the tra-
ditional connotation of fitness. We will refer hereafter to
“improving” the overall fitness as a goal of our algorithm,
with the understanding that fitness improves by decreasing
the value ofFrather than increasing it, and that the most fit
assignment in any given context is the individual with the
smallest image underF.
```
## 4 Experiments

```
For our algorithm we developed a single crossover and a
single mutation method, but we only implemented the mu-
tate method in our experiments due to an implementation
challenge in the crossover method. We defined convergence
through the number of consecutive generations without im-
provement in the fitness of the most fit individual, and al-
lowed the process to run without a time limit.
```
### Genetic Mechanisms

```
Crossover To crossover two assignments, we simply
chose a random integer in the range of 20% to 80% of the
size of the assignment list, and used it as a crossover point
for the two lists. That is, ifnis our crossover point, we cre-
ate a child using the firstn+1 entries of the first parent and
the remaining entries from the second parent.
Using our example from earlier, which we call Parent 1,
with a second example, Parent 2, we will demonstrate how
we might use this crossover point to create a child.
```
```
Parent 1: [4, 5 , 5 , 3 , 1 , 5 , 4 , 3 , 3 ,4]
Parent 2: [3, 1 , 1 , 4 , 4 , 3 , 1 , 5 , 5 ,5]
Crossover point =rand(.2(10),.8(10))= 4
Parent 1: [ 4 , 5 , 5 , 3 , 1 , 5 , 4 , 3 , 3 ,4]
Parent 2: [3, 1 , 1 , 4 , 4 , 3 , 1 , 5 , 5 , 5 ]
Child: [ 4 , 5 , 5 , 3 , 1 , 3 , 1 , 5 , 5 , 5 ]
```
```
After the random function returned 4 from the range
{ 2 , 3 , 4 , 5 , 6 , 7 , 8 }, we chose all the entries up to index 4 from
Parent 1, and all the entries in indices greater than 4 from
Parent 2, and combined them to form the child.
```

Note that while we do not require that a minimum num-
ber of children be assigned to each school other than that it
is non-negative (as illustrated by our examples leaving the
hypothetical school 2 empty), we do require that the number
of students attending every school stay below 125% of the
capacity given in the CMS data.
When applying this constraint to the crossover method,
we chose to repeat the crossover with a new random
crossover point if the any schools in the current assignment
are more than 125% over capacity. However, because of
restricted range of the crossover point, the first 20% of the
first parent and the last 80% of the second parent will always
appear in the child. If these portions cause an overcapacity
assignment in even just one school, the crossover method
will enter an infinite loop.
In present review of the project at the time of writing, it
seems clear that simply removing the 20%/80% restriction
might have fixed this bug, and allowing different parents to
attempt to crossover if a selected pair failed a certain num-
ber of times would have certainly given the method a bet-
ter chance at functioning. However, when the bug appear,
we had no ability to foresee how many more challenges
we would face before producing results. Given our desire
to have at least a running algorithm, we proceeded with
mutation-only genetic programming, and afterward chose
not to return to the crossover method given the success of
mutation-only reproduction.

Mutate A single mutation operation consisted of a number
of element-wise swaps in the parent. Given a parent solu-
tion of list lengthn, we would randomly generatekbetween
0. 001 nand 0. 002 n. Then, we would swap random elements
from the entire listbkcnumber of times. Demonstrating mu-
tation with the actual algorithm would require a list of size at
least 500, so for the sake of illustration we will changekto
be between 0. 1 nand 0. 2 n, and mutate our running example
solution.

```
Parent [4, 5 , 5 , 3 , 1 , 5 , 4 , 3 , 3 ,4]
# of Mutations=brand(0. 1 , 0 .2)(10)c=b.015(10)c= 1
```
Mutation 1 position 1=brand(0,9)c= 6

Mutation 1 position 2=rand(0,9)= 1

Parent [4, 5 , 5 , 3 , 1 , 5 , 4 , 3 , 3 ,4]
Child [4, 4 , 5 , 3 , 1 , 5 , 5 , 3 , 3 ,4]
If this child has an overcapacity assignment to either of
the two schools involved in the swap, then the child is dis-
carded and the parent attempts to mutate again. Though
this challenge is similar to the one that caused us to aban-
don our crossover method, we need only check two schools
for overcapacity assignments here, as opposed to having to
check every school as in the crossover method. We also have
no restriction on our mutation points, so for a given parent,
no school will necessarily be involved in the mutation, thus
avoiding the infinite loop bug in our crossover method.

### Selection and Evolution

We began by generating 100 random solutions, and created
successive generations of size 100 using a tournament se-

```
lection algorithm outlined in Miller et al.’s “Genetic Algo-
rithms, Tournament Selection, and the Effects of Noise.” to
evolove the population until it converged (Miller et al. 1995).
```
```
Tornament Selection Tournament selection chooses indi-
viduals from the population to reproduce by splitting a pop-
ulation of sizeninto some number of groups from 1 tonand
then choosing the most fit individual in each of these groups
as the winner of that tournament. All of these winners then
reproduce – mutate, in our case – and their offspring enter
the next generation.
When choosing the size of the tournaments, we encounter
a conflict between inter-generational diversity and selection
pressure. For large participation in each tournament, few
solutions win, so there is a high selection pressure, but the
diversity of the population as a whole quickly falls. For low
participation in each tournament, diversity remains high, but
more solutions survive to reproduce, so selection pressure
falls. For example, in a population size of 100, a tournament
participation size of 50 (2 tournaments with 50 participants)
allows for two highly fit victors to send offspring to the next
generation, but the genetic diversity of the following gen-
erations quickly shrinks. Conversely, a tournament partici-
pation size of 5 (20 tournaments, with 5 participants each)
allows many individuals to survive, but only requires them to
be more fit than four solutions to do so, thus decreasing the
average fitness of the population, at least in the short term.
In general, we see that
```
```
t·p(t)=s(g)
```
```
wheretis the number of tournaments,p(t) is the number
of participants in each tournament, ands(g) is the size of
the current generation. We chose to take the middle ground
in this trade off, and set the tournament size to be about
equal to the square root of the size of the population, so
t=b
```
#### √

```
s(g)c ⇒p(t)= s(g)
b
```
#### √

```
s(g)c
```
```
≈ b
```
#### √

```
s(g)c=t. Thust≈p(t),
```
```
and we take the most moderate approach.
```
```
Evolution In our implementation, we decided to keep the
generation size constant, except for the special case of the
first generation. To create generationk+1 from generation
k, we produce a combination of new individuals and mu-
tated children. Ten percent of the time, we send a newly
spawned random individual to the next generation. The
other 90% percent of the time, we take the winners of the
t=b
```
#### √

```
(s(g))c=10 tournaments and randomly select one
solution at a time from this group of champions. We then
have the selected champion mutate, and send the mutation
to generationk+1. We continue this process until the new
generation has 100 members. Lastly, we find the most fit
member of the group of tournament champions in genera-
tionkand send this “king” to generationk+1, thereby al-
lowing it to survive until the next generation. Thus, the first
generation has 100 members, every following generation has
101 members. The number of tournamentstis always 10=
b
```
#### √

```
101 c=b
```
#### √

```
100 c, and the number of participantsp(t) is
always^10110 =10 (by integer division).
We let successive generations run and record at each gen-
eration the fitness of the king, the fitness of the “emperor,”
```

Figure 5: The graph shows 2,237 total data points repre-
senting 2,237 generations across three data sets over nearly
80 hours of runtime. The horizontal gap in the bluegreen
data set and the two similiar gaps in the black “All” dataset
correspond to time intervals when my computer temporarily
entered sleep mode or otherwise stopped running. Thus, the
actual code ran for perhaps five or six hours less than the
80 +hours the far-right black data points would indicate.

the most fit individual ever produced, along with the time it
took to produce the generation, and the total running time
of the algorithm. If the fitness of the emperor does not im-
prove in 51 generations, we consider the algorithm to have
converged, and we stop it.

## 5 Results

We ran our evolution algorithm on the three supplied files:
the bluegreen and greyvoilet partitions, and the whole CMS
school district. Both partitions converged, but the full dis-
trict has continued to run and improve its fitness up to the
time of writing.
We see that in figures 5 and 6 the combined dataset starts
with about twice the starting fitness of the partitions, but im-
proves at about the same rate. Given enough time, the com-
bined dataset reaches comparable absolute values of fitness,
and outperforms both partitions in terms of percent change
from the starting value. Though the full dataset represents a
larger problem, it also offers the algorithm more freedom in
assigning roads to schools, especially near the boarders of
the partition. For example, when the algorithm runs on the
BlueGreen dataset, it might struggle to place a road on its
boundary that would greatly improve the SES diversity of a
school in the GreyViolet partition for only a small commute
cost, but it has no ability to make this placement. In con-
trast, the algorithm could easily make this assignment when
running on full dataset, and would likely converge to such a
beneficial decision quickly. This advantage offers one expla-
nation the larger problem’s superior percent improvement.
Whatever the reason for its success, its low fitness values
underscore its promise, especially given that both the parti-
tioned datasets converged at the time of comparison, while
the full data set is still evolving and improving its solutions
at the time of writing.
Given more time, we would like to geographically repre-

```
Dataset Fitinital Fitfinal Size % Diff
Bluegreen 143,567 11,429 25,274 92.
Greyvoilet 129,450 19,305 21,456 85.
All 275,967 17,069 46,730 93.
```
```
Figure 6: Here Fitinitialis the fitness of the most fit individ-
ual of generation 1, and Fitfinalis the fitness of the most fit
individual after convergence (at the time of writing for the
full dataset).
```
```
sent our most fit final assignments across the three datasets,
and compare them to geographical visualizations of solu-
tions Lena’s linear programming approach produced.
To more rigorously evaluate our results, we could rerun
Lena’s MATLAB code and directly compare the final ob-
jective function valuations of her solutions to our converged
fitness values, which are outputs of the same function. We
could appraise our solutions through two additional metrics
Lena describes in her thesis: the average commute time for
all students across the CMS, and the number of schools who
have a low-SES proportion greater than 90%.
```
## 6 Conclusions

```
Though we have yet to directly compare our results to
Lena’s, we have good reason to think ours may compete and
even outperform hers. Though our algorithm has run for
more than three and a half days, the CMS is one of Amer-
ica’s largest school districts, so the potential to apply genetic
programming solutions to other districts across America re-
mains viable. The true struggle to desegregate CMS schools
has political origins and contemporary political challenges,
but our results can contribute to this discussion by showing
that schools can be desegregated without requiring exorbi-
tant commute times.
When the CMS reconsiders its school assignments, we
hope work with Lena to leverage her contacts within the
CMS to obtain real student data for our algorithms, rather us-
ing estimates from the Census and other sources. We further
hope that we can present our solutions to the CMS school
board, and advocate for their implementation.
```
## 7 Acknowledgements

```
I would like to acknowledge Lena Parker for her enthusiasm
in supporting my investigation of this problem, and her will-
ingness to answer questions regarding the data and travel to
see our preliminary results at the Davidson College Verna
Case Symposium May May 8th, 2019.
I would like to thank Dr. Ramanujan for his availability
to answer questions, and for teaching me the methods em-
ployed here.
Lastly, I would like to thank my parents for their support
through the semester and for proofreading this paper.
```
## References

```
Grundy, P. 2017. Color and Character: West Charlotte
High and the American Struggle Over Educational Equality.
University of North Carolina Press.
```

Miller, B. L.; Miller, B. L.; Goldberg, D. E.; and Goldberg,
D. E. 1995. Genetic algorithms, tournament selection, and
the effects of noise.Complex Systems9:193–212.

National Center for Education Statistics, U. S. 2016. Enroll-
ment, poverty, and federal funds for the 120 largest school
districts, by enrollment size in 2016. Digest of Education
Statistics. Retrieved on May 16, 2019.

Parker, L. 2017. A linear programming application for CMS
student assignment boundaries. Davidson College Center
for Interdisciplinary Studies.



