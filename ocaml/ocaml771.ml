(* -*- coding: utf-8 -*-; *)

(* Exercise 1 *)

type 'a ref = { mutable contents : 'a };;

let ref' x = { contents = x };;
let ex x = x.contents;;
let subst x y = x.contents <- y;;


(* Exercise 2 *)
let incr x = x := (!x + 1);;


(* Exercise 3 *)
let f = ref (fun y -> y+1)
let funny_fact x =
  if x = 1 then 1
  else x * (!f (x-1))
;;

f := funny_fact;;
(* f = ref funny_fact となっているので !f = funny_fact *)
funny_fact 5;;


(* Exercise 4 *)
let fact_imp n =
  let i = ref n and res = ref 1 in
  while (!i <> 0) do
    res := !res * !i;
    i := !i - 1;
  done;
  !res
;;


(* Exercise 5 *)
let fact = function
  | n when n < 0 -> raise (Invalid_argument (string_of_int n))
  | n -> fact_imp n
;;
