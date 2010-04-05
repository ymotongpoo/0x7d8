open Printf

(* Exercise 7 *)
let rec pow1 (x, n) =
  if n = 0 then 1
  else x * pow1 (x, n -1)
;;

let rec pow2 (x, n) = 
  let square x_ = x_ * x_ in
  match n with
	0 -> 1
  |	1 -> x
  |	n when n mod 2 = 0 ->
	  square (pow2 (x, n/2))
  |	_ ->
	  (square (pow2 (x, (n-1)/2))) * x
;;

Printf.printf "pow1 -> %d\n" (pow1 (2, 10));;
Printf.printf "pow2 -> %d\n" (pow2 (2, 10));;


(* Exercise 8 *)
let rec powi (x, n, res) =
  if n = 0 then res
  else powi (x, n-1, x * res)
;;

Printf.printf "powi -> %d\n" (powi (2, 10, 1));;
