/* facts */

parent(peggy, paige).
parent(peggy, paula).
parent(peggy, tim).
parent(peggy, amy).
parent(peggy, ouma).

parent(woody, amy).
parent(woody, paige).
parent(woody, paula).
parent(woody, tim).
parent(woody, yasser).

parent(rose, dianne).
parent(rose, dan).
parent(rose, jack).
parent(rose, paul).
parent(rose, lina).

parent(george, dianne).
parent(george, dan).
parent(george, jack).
parent(george, paul).
parent(george, ali).

parent(amy, ginger).
parent(amy, jackie).
parent(amy, andrew).
parent(amy, alex).
parent(amy, aymane).

parent(jack, ginger).
parent(jack, jackie).
parent(jack, andrew).
parent(jack, alex).

parent(ginger, katelyn).
parent(zack, katelyn).

parent(tim, carol).

parent(carol, ashley).
parent(carol, chelsea).


parent(paula, amine).
parent(tim, ahmed).

parent(ahmed, salma).
parent(amine, nora).

married(emma, adnane).
married(rime, hamza).
married(peggy, woody).

male(yasser).
male(ali).
male(jack).
male(andrew).
male(alex).
male(woody).
male(tim).
male(george).
male(dan).
male(paul).
male(zack).
male(adnane).
male(hamza).
male(amine).
male(ahmed).

female(salma).
female(nora).
female(emma).
female(rime).
female(lina).
female(ouma).
female(amy).
female(ginger).
female(jackie).
female(peggy).
female(paige).
female(paula).
female(rose).
female(dianne).
female(katelyn).
female(carol).
female(ashley).
female(chelsea).

/* rules */
spouse(X, Y) :-
    female(X),
    male(Y);
    female(Y),
    male(X);
    married(X, Y).

mother(X, Y) :-
    parent(X, Y),
    female(X).

father(X, Y) :-
    parent(X, Y),
    male(X).

child(X, Y) :-
    parent(Y, X).

husband(X, Y) :- 
    male(X), 
    female(Y),
    partner(X, Y).

wife(X, Y) :- 
    male(Y), 
    female(X), 
    partner(X, Y).

partner(X, Y) :-
    child(Z, X),
    child(Z, Y),
    X \= Y.

grandparent(X, Y) :-
    parent(X, Z),
    parent(Z, Y).

grandchild(X, Y) :-
    grandparent(Y, X).

grandfather(X, Y) :-
    grandparent(X, Y),
    male(X).

grandmother(X, Y) :-
    grandparent(X, Y),
    female(X).

son(X, Y) :-
    child(X, Y),
    male(X).

daughter(X, Y) :-
    child(X, Y),
    female(X).

ancestor(X, Y) :-
    parent(X, Y).

ancestor(X, Y) :-
    parent(Z, Y),
    ancestor(X, Z).

descendant(X, Y) :-
    ancestor(Y, X).

cousinanydegree(X, Y) :-
    ancestor(Z, X),
    ancestor(W, Y),
    halfsibling(Z, W).
	
sibling(X, Y) :-
    mother(Z, X),
    father(W, Y),
    mother(Z, Y),
    father(W, X),
    X \= Y.

halfsibling(X, Y) :-
    parent(Z, X),
    parent(Z, Y),
    X \= Y.

halfsister(X, Y) :-
    halfsibling(X, Y),
    female(X),
    X \= Y.

sister(X, Y) :-
    sibling(X, Y),
    female(X),
    X \= Y.

halfbrother(X, Y) :-
    halfsibling(X, Y),
    male(X),
    X \= Y.

brother(X, Y) :-
    sibling(X, Y),
    male(X),
    X \= Y.

uncle(X, Y) :-
    halfbrother(X, Z),
    child(Y, Z).

aunt(X, Y) :-
    halfsister(X, Z),
    child(Y, Z).

cousin(X, Y) :-
    grandparent(Z, X),
    grandparent(Z, Y),
    \+sibling(X, Y),
    X \= Y.

unclematernal(X, Y) :-
    halfbrother(X, Z),
    child(Y, Z),
    female(Z).

unclepaternal(X, Y) :-
    halfbrother(X, Z),
    child(Y, Z),
    male(Z).

auntmaternal(X, Y) :-
    halfsister(X, Z),
    child(Y, Z),
    female(Z).

auntpaternal(X, Y) :-
    halfsister(X, Z),
    child(Y, Z),
    male(Z).