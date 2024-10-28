(assert (parent kevin alex))
(assert (parent paige kevin))
(assert (parent andrew katelyn))
(assert (parent jack ginger))
(assert (parent jack andrew))
(assert (parent amy ginger))
(assert (parent amy andrew))
(assert (parent tim carol))
(assert (parent woody amy))
(assert (parent woody paige))
(assert (parent woody paula))
(assert (parent woody tim))
(assert (parent woody samual))
(assert (parent peggy paige))
(assert (parent peggy paula))
(assert (parent peggy tim))
(assert (parent peggy amy))
(assert (parent peggy ouma))

(assert (female carol))
(assert (female ginger))
(assert (female amy))
(assert (female paige))
(assert (female paula))
(assert (female katelyn))
(assert (male tim))
(assert (female ouma))
(assert (male samual))
(assert (male jack))
(assert (male andrew))
(assert (female peggy))
(assert (male woody))
(assert (male kevin))
(assert (male alex))
(assert (spouse woody peggy))
(assert (spouse jack amy))



; (defrule spouce_commut
;     (spouse ?x ?y)
;     =>
;     (assert (spouce ?y ?x))
; )

(defrule mother
    (parent ?x ?y)
    (female ?x)
    =>
    (assert (mother ?x ?y))
)

(defrule father
    (parent ?x ?y)
    (male ?x)
    =>
    (assert (father ?x ?y))
)

; masked
(defrule child
    (parent ?y ?x)
     =>
    (assert (child ?x ?y))
)


(defrule husband
    (male ?x)
    (female ?y)
    (spouse ?x ?y)
    =>

    (assert (husband ?x ?y))
)

(defrule wife
    (female ?x)
    (male ?y)
    (spouse ?y ?x)
    =>

    (assert (wife ?x ?y))
)

(defrule grandparent
    (parent ?x ?z)
    (parent ?z ?y)
    =>
    (assert (grandparent ?x ?y))
)


(defrule grandchild
    ?x <- (grandparent ?y ?x)
    =>
    (unwatch facts)
    (assert (grandchild ?x ?y))
    (watch facts)
)

(defrule grandfather
    (grandparent ?x ?y)
    (male ?x)
    =>
    (assert (grandfather ?x ?y))
)

(defrule grandmother
    (grandparent ?x ?y)
    (female ?x)
    =>
    (assert (grandmother ?x ?y))
)


; (defrule son
;     ?x <- (child ?x ?y)
;     (male ?x)
;     =>
;     (assert (son ?x ?y))
; )

; (defrule daughter
;     ?x <- (child ?x ?y)
;     (female ?x)
;     =>
;     (assert (daughter ?x ?y))
; )


; (defrule sibling
;    (or 
;      (and
;       (mother ?z ?x)
;       (father ?w ?y)
;      )
;      (and 
;       (mother ?z ?y)
;       (father ?w ?x)
;       )
;      )
;     (neq ?x ?y)
;     =>
;     (assert (sibling ?x ?y))
; )

(defrule ancestor
    (parent ?x ?y)
    =>
    (assert (ancestor ?x ?y))
)

(defrule ancestor
    (or (parent ?x ?y) ( and
    (parent ?z ?y)
    (ancestor ?x ?z)
    ))
    =>
    (assert (ancestor ?x ?y))
)
; (defrule descendant
;     ?x <- (ancestor ?y ?x)
;     =>
;     (assert (descendant ?x ?y))
; )


(defrule halfsibling
    (parent ?z ?x)
    (parent ?z ?y)
    (neq ?x ?y)
    =>
    (assert (halfsibling ?x ?y))
)
(defrule cousin
    (parent ?z ?x)
    (parent ?w ?y)
    (halfsibling ?z ?w)
    =>
    (assert (cousin ?x ?y))
)

(defrule cousinanydegree
    (ancestor ?z ?x)
    (ancestor ?w ?y)
    (halfsibling ?z ?w)
    =>
    (assert (cousinanydegree ?x ?y))
)




; (defrule halfsister
;     ?x <- (halfsibling ?x ?y)
;     (female ?x)
;     (neq ?x ?y)
;     =>
;     (assert (halfsister ?x ?y))
; )

; (defrule sister
;     ?x <- (sibling ?x ?y)
;     (female ?x)
;     (neq ?x ?y)
;     =>
;     (assert (sister ?x ?y))
; )

; (defrule halfbrother
;     ?x <- (halfsibling ?x ?y)
;     (male ?x)
;     (neq ?x ?y)
;     =>
;     (assert (halfbrother ?x ?y))
; )

; (defrule brother
;     ?x <- (sibling ?x ?y)
;     (male ?x)
;     (neq ?x ?y)
;     =>
;     (assert (brother ?x ?y))
; )

; (defrule uncle
;     ?x <- (halfbrother ?x ?z)
;     ?y <- (child ?y ?z)
;     =>
;     (assert (uncle ?x ?y))
; )

; (defrule aunt
;     ?x <- (halfsister ?x ?z)
;     ?y <- (child ?y ?z)
;     =>
;     (assert (aunt ?x ?y))
; )


(watch facts)
(run)

