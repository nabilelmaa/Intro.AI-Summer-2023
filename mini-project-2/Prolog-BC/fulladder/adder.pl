% Define gate types
gate_type(x1, xor).
gate_type(x2, xor).
gate_type(a1, and).
gate_type(a2, and).
gate_type(o1, or).
gate_type(n1, not).
gate_type(c, circuit).

% Define the connections between the terminals
connected([in, 1, c], [in, 1, x1]).
connected([in, 1, c], [in, 1, a1]).
connected([in, 2, c], [in, 2, x1]).
connected([in, 2, c], [in, 2, a1]).
connected([in, 3, c], [in, 2, x2]).
connected([in, 3, c], [in, 1, a2]).

% Define signal
signal([in, 1, c], 1).
signal([in, 2, c], 1).
signal([in, 3, c], 0).

% Define rules for gates
and_gate(X, Y, Z) :- Z is X * Y.
or_gate(X, Y, Z) :- Z is max(X, Y).
xor_gate(X, Y, Z) :- Z is abs(X - Y).
not_gate(X, Z) :- Z is abs(1 - X).

% Propagate the signal across a connection
propagate(Terminal1, Value) :-
    connected(Terminal1, Terminal2),
    signal(Terminal2, Value).

% Define the query_signals/5 predicate
signals(A, B, Cin, Sum, Cout) :-
    xor_gate(A, B, Temp),
    xor_gate(Temp, Cin, Sum),
    and_gate(A, B, Temp2),
    and_gate(Temp, Cin, Temp3),
    or_gate(Temp2, Temp3, Cout).
