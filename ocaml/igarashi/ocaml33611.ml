open Printf
open String

(* Exercise 11-1 *)

let rec gcd (m, n) =
  match (m, n) with
  |	(_, n) when n = 0 -> m
  | (m, n) when m mod n = 0 -> n
  | (_, _) -> gcd (n, m mod n)
;;
  

let print_gcd (m, n) =
  let ret = gcd (m, n) in
  Printf.printf "(%d, %d) -> %d\n" m n ret
;;

print_gcd (1071, 1029);;
print_gcd (1029, 1071);;

(* Exercise 11-2 *)

let rec comb (n, m) =
  match (n, m) with
  |	(n, m) when n * m = 0 -> 1
  |	(n, m) when n = m -> 1
  |	(n, m) when m > n -> comb (m, n)
  |	(_, _) -> comb (n-1, m) + comb (n-1, m-1)
;;

let print_comb (n, m) =
  let ret = comb (n, m) in
  Printf.printf "comb (%d, %d) -> %d\n" n m ret
;;

print_comb (6, 3);;
  
(* Exercise 11-3 *)

let rec fact n ret =
  if n = 1 then ret
  else fact (n-1) n*ret
;;

let print_fact n = 
  Printf.printf "fact(%d) -> %d\n" n (fact n 1);;

print_fact 5;;

let rec fib = function
  | 1 | 2 -> 1
  | n -> fib (n-1) + fib (n-2)
;;

let rec fib n p c =
  if n = 1 then c + p
  else fib (n-1) c (c+p)
;;

let print_fib n =
  Printf.printf "fib(%d) -> %d\n" n (fib n 0 1);;

(* 1 1 2 3 5 8 13 21 *)
print_fib 7;;

(* Exercise 11-4 *)

let max_ascii str =
  let rec max_char n max_c =
	if n = 0 then max str.[n] max_c
	else max_char (n-1) (max max_c str.[n])
  in
  max_char (String.length str - 1) str.[0]
;;

Printf.printf "max_ascii -> %c\n" (max_ascii "abcdzefg")


(* Exercise 12 *)
let rec pos n =
  neg (n-1) +. 1.0 /. (float_of_int (4 * n + 1))
and neg n =
  if n < 0 then 0.0
  else pos n -. 1.0 /. (float_of_int (4 * n + 3))

let rec arctan1 ret = function
  |	0 -> ret
  |	n when n < 0 -> 0.0
  |	n when n mod 2 = 1 -> arctan1 (ret +. 1.0 /. (float_of_int (2 * n - 1))) (n-1)
  |	n -> arctan1 (ret -. 1.0 /. (float_of_int (2 * n - 1))) (n-1)
;;

let arctan1 = arctan1 0.0;;

Printf.printf "%f\n" (4.0 *. (arctan1 10000000));;
Printf.printf "%f\n" (4.0 *. (pos 1000000));;
