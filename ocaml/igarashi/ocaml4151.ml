open Printf

(* Exercise 1 *)

let integral n f a b =
  let trapezoid x y h = (x +. y) *. h /. 2.0 in
  let h = (b -. a) /. (float_of_int n) in
  let rec sigma f n sum =
	if n = 0 then sum
	else 
	  let x' = f (a +. (float_of_int (n-1)) *. h) 
	  and y' = f (a +. (float_of_int n) *. h) in
	    sigma f (n-1) (sum +. trapezoid x' y' h)
  in
  sigma f n 0.0
;;

let integral = integral 10000000;; 

let integral_sin = integral sin;;

let print_integral_sin a b =
  Printf.printf "sin : %f -> %f = %f\n" a b (integral_sin a b);;

let pi = 3.1415926;;
print_integral_sin 0.0 pi;;

type 'a recc = In of ('a recc -> 'a);;
let out (In x) = x;;

let y f = (fun x a -> f (out x x) a) (In (fun x a -> f (out x x) a));;

let f fact x = if x = 1 then 1 else fact (x - 1) * x;;
let z = y f 10;;

Printf.printf "%d\n" z;;
