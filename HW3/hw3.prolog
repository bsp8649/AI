/* Facts */
male(george).
male(philip).
male(spencer).
male(charles).
male(mark).
male(andrew).
male(edward).
male(william).
male(harry).
male(peter).
male(james).
female(mum).
female(kydd).
female(elizabeth).
female(margaret).
female(diana).
female(anne).
female(sarah).
female(sophie).
female(zara).
female(beatrice).
female(eugenie).
female(louise).
parent(diana, william).
parent(charles, william).
parent(diana, harry).
parent(charles, harry).
parent(anne, peter).
parent(mark, peter).
parent(anne, zara).
parent(mark, zara).
parent(andrew, beatrice).
parent(sarah, beatrice).
parent(andrew, eugenie).
parent(sarah, eugenie).
parent(edward, louise).
parent(sophie, louise).
parent(edward, james).
parent(sophie, james).
parent(spencer, diana).
parent(kydd, diana).
parent(elizabeth, charles).
parent(philip, charles).
parent(elizabeth, anne).
parent(philip, anne).
parent(elizabeth, andrew).
parent(philip, andrew).
parent(elizabeth, edward).
parent(philip, edward).
parent(george, elizabeth).
parent(mum, elizabeth).
parent(george, margaret).
parent(mum, margaret).
married(diana, charles).
married(charles, diana).
married(anne, mark).
married(mark, anne).
married(andrew, sarah).
married(sarah, andrew).
married(edward, sophie).
married(sophie, edward).
married(elizabeth, philip).
married(philip, elizabeth).
married(george, mum).
married(mum, george).

/* Rules */
grandchild(X,Y) :- parent(Y,Z), 
    parent(Z,X).

greatgrandparent(X,Y) :- parent(X,Z), 
    grandchild(Y,Z).

sibling(X,Y) :- parent(Z,X), 
    parent(Z,Y), 
    X \= Y.

sibling(X,Y) :- sibling(Y,X).

brother(X,Y) :- sibling(X,Y), 
    male(X).

sister(X,Y) :- sibling(X,Y), 
    female(X).

son(X,Y) :- parent(Y,X), 
    male(X).

daughter(X,Y) :- parent(Y,X), 
    female(X).

uncle(X,Y) :- parent(Z,Y), 
    brother(Z,X).

aunt(X,Y) :- parent(Z,Y), 
    sister(Z,X).

brotherinlaw(X,Y) :- male(X),
    sibling(Z,Y),
    married(X,Z).

brotherinlaw(X,Y) :- male(X),
    married(Z,Y),
    sibling(X,Z).

brotherinlaw(X,Y) :- male(X),
    married(Z,Y),
	sibling(W,Z),
    married(X,W).

sisterinlaw(X,Y) :- female(X),
    sibling(Z,Y),
    married(X,Z).

sisterinlaw(X,Y) :- female(X),
    married(Z,Y),
    sibling(X,Z).

sisterinlaw(X,Y) :- female(X),
    married(Z,Y),
	sibling(W,Z),
    married(X,W).

firstcousin(X,Y) :- parent(Z,X), 
    parent(W,Y), 
    sibling(Z,W).

ancestor(X, Y) :- parent(X, Y).

ancestor(X, Y) :- parent(X, Z), 
    ancestor(Z, Y).