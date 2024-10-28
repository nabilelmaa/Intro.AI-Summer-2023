; Define the template for a signal with terminal and value slots
(deftemplate signal
    (multislot terminal)
    (slot value)
    )

; Define the template for a terminal with inOut, number, and gate slots
(deftemplate terminal
    (slot InOut)
    (slot number)
    (slot gate))
; Define the template for a connection between two terminals
(deftemplate connected
    (multislot terminal1)
    (multislot terminal2)
)




; Assert the gates and their types
(assert (gate x1))
(assert (type x1 xor))

(assert (gate x2))
(assert (type x2 xor))

(assert (gate a1))
(assert (type a1 and))

(assert (gate a2))
(assert (type a2 and))

(assert (gate o1))
(assert (type o1 or))

(assert (gate n1))
(assert (type n1 not))

; Assert the gates and their types
(assert (gate c))
(assert (type c circuit))

(defrule initialize-carry
    (declare (salience 100)) ; High salience to run first
    =>
    (assert (signal (terminal out 2 c) (value 0)))
)


; Assert the connections between the terminals according to the slides

(assert (connected (terminal1 in 1 c) (terminal2 in 1 x1)))
(assert (connected (terminal1 in 1 c) (terminal2 in 1 a1)))
(assert (connected (terminal1 in 2 c) (terminal2 in 2 x1)))
(assert (connected (terminal1 in 2 c) (terminal2 in 2 a1)))
(assert (connected (terminal1 in 3 c) (terminal2 in 2 x2)))
(assert (connected (terminal1 in 3 c) (terminal2 in 1 a2)))

(assert (connected (terminal1 out 1 x1) (terminal2 in 1 x2)))
(assert (connected (terminal1 out 1 x1) (terminal2 in 2 a2)))
(assert (connected (terminal1 out 1 a2) (terminal2 in 1 o1)))
(assert (connected (terminal1 out 1 a1) (terminal2 in 2 o1)))
(assert (connected (terminal1 out 1 x2) (terminal2 out 1 c)))
(assert (connected (terminal1 out 1 o1) (terminal2 out 2 c)))



;we plug the first input (A) into In(1,C), the second input (B) into In(2,C), and the carry-in (C) into In(3,C).
;java -cp %JESS_HOME%\jess.jar jess.Main C:\Users\LENOVO\Downloads\Project2\Jess-FC\fulladder\hard_fulladder.clp

(assert (signal (terminal in 1 c) (value 1)))
(assert (signal (terminal in 2 c) (value 1)))
(assert (signal (terminal in 3 c) (value 1)))

(defrule print-in1
    ?f <- (signal (terminal in 1 c) (value ?value))
    =>
    (printout t "(In1) = " ?value crlf)
)

(defrule print-in2
    ?f <- (signal (terminal in 2 c) (value ?value))
    =>
    (printout t "(In2) = " ?value crlf)
)

(defrule print-CarryIn
    ?f <- (signal (terminal in 3 c) (value ?value))
    =>
    (printout t "(C_In) = " ?value crlf)
)

;the first output (the sum S) is Out(1,C) and the second output (the carry C_out) is Out(2,C).


; Define a rule to determine the arity of each gate based on its type
(defrule arity
    (gate ?gate)
    (type ?gate ?type)
    =>
    (bind ?Ninput (if (or (eq ?type xor) (eq ?type or) (eq ?type and)) then 2 else 3))
    (bind ?Noutput (if (or (eq ?type xor) (eq ?type or) (eq ?type and)) then 1 else 2))

    (if (eq ?type not)
    then (bind ?Ninput 1) (bind ?Noutput 1))
    (assert (arity ?Ninput ?Noutput ?gate))

)

; Define a rule to propagate the signal across a connection
(defrule connection
    (connected (terminal1 $?terminal1) (terminal2 $?terminal2))
    (signal (terminal $?terminal1) (value ?value))
    =>
    (assert (signal (terminal $?terminal2) (value ?value)))
)

; Define a rule to assert the commutativity of the connections
(defrule commutativity
    (connected (terminal1 $?terminal1) (terminal2 $?terminal2))
    =>
    (assert (connected (terminal1 $?terminal2) (terminal2 $?terminal1))

)
)

(defrule and
    (type $?gate and)
    (signal (terminal in 1 $?gate) (value ?value1))
    (signal (terminal in 2 $?gate) (value ?value2))
    =>
    (bind ?returned_value (if (and (eq ?value1 1) (eq ?value2 1)) then 1 else 0))
    (assert (signal (terminal out 1 $?gate) (value ?returned_value)))
)

(defrule or
    (type $?gate or)
    (signal (terminal in 1 $?gate) (value ?value1))
    (signal (terminal in 2 $?gate) (value ?value2))
    =>
    (bind ?returned_value (if (or (eq ?value1 1) (eq ?value2 1)) then 1 else 0))
    (assert (signal (terminal out 1 $?gate) (value ?returned_value)))
)

(defrule xor
    (type $?gate xor)
    (signal (terminal in 1 $?gate) (value ?value1))
    (signal (terminal in 2 $?gate) (value ?value2))
    =>
    (bind ?returned_value (if (eq ?value1 ?value2) then 0 else 1))
    (assert (signal (terminal out 1 $?gate) (value ?returned_value)))
)

(defrule not
    (type ?gate not)
    (signal (terminal in 1 $?gate) (value ?value))
    =>
    (bind ?returned_value (if (eq ?value 1) then 0 else 1))
    (assert (signal (terminal out 1 $?gate) (value ?returned_value)))
)



(defrule print-sum
    ?f <- (signal (terminal out 1 c) (value ?value))
    =>
    (printout t "(Sum) = " ?value crlf)
)

(defrule print-carry
    ?f <- (signal (terminal out 2 c) (value ?value))
    =>
    (printout t "(C_out) = " ?value crlf)
)


(watch facts)
(run)