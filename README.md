# Addressing SES Segregation in Charlottle-Meckelenburg Schools: A Genetic Programming Approach

by Michael Robertson for Davidson College's Machine Reasoning Final Project

---

### Table of Contents:
- [Abstract](#abstract)
- [Introduction](#introduction)
- [Data](#Data)
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

## Abstract
```
```
Lena Parker’s (Davidson College class of 2017) thesis ad-
dressed the problem of reducing socioeconomic segregation
in Charlottle-Meckelenburg Schools without unreasonably
increasing student commute times. Her linear programming
approach struggled to run in a reasonable amount of time
given the size of the problem, so we attempt to find a more ef-
ficient solution through genetic programming. Over 80 hours,
our algorithm evolved solutions which improved upon the
baseline fitness of random assignments by over 90%. We
hope the assignments we produced would compete with and
perhaps improve upon Lena’s final solution. Though our re-
sults require further analysis and verification before potential
presentation to the CMS (Charlotte-Mecklenburg Schools),
the large relative improvement of our solutions in a compar-
atively short period of time demonstrates the promise of ge-
netic programming in this problem space.


## Introduction

The CMS schools district contained 154,434 students in
2014, and was the 18thlargest district out of 121 in Amer-
ica (National Center for Education Statistics 2016). The
mathematical problem of desegregating schools by SES
(SocioEconomicStatus) could be simply solved by assign-
ing equal numbers of children of each SES level to each
school. However, as Grundy describes in her 2017 book
Color and Character, when the U.S. Supreme Court de-
clined to hear an appeal toCappachione v. Charlotte-
Mecklenburg Board of Educationin April 2002, it effec-
tively upheld the ruling of two lower courts that “prior ves-
tiges of racial discrimination had been eliminated to the ex-
tent practicable,” and released the CMS from the obligation
to racially desegrate placed upon it by the landmark 1971
U.S. Supreme Court caseSwann v. Charlotte-Mecklenburg
Board of Education(Grundy 2017). Later in 2002, the CMS
implemented a ”School Choice Plan” which led to the near
immediate resegregation of schools, and they have only be-
come “increasingly racially and socioeconomically segre-
gated” since (Grundy 2017) (Parker 2017).
Though discussions surrounding school assignment in
Charlotte have traditionally focused on racial segregation
because of America’s history of racial discrimination, we
will here focus on SES as the segregating factor, due to
the availability of student SES data provided to us through
