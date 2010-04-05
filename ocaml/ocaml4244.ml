open Printf

(* Exercise 4 *)

let curry f x y = f (x, y);;
let average (x, y) = (x +. y) /. 2.0;;
let curried_avg = curry average;;

let uncurry f (x, y) = f x y;;

let avg = uncurry curried_avg;;

Printf.printf "avg -> %f\n" (avg (4.0, 5.3));;


(* Exercise 5 *)
let rec repeat f n x =
  if n > 0 then repeat f (n-1) (f x) else x;;

let fib n =
  let (fibn, _) = repeat (fun (p, c) -> (c, c+p)) n (0, 1)
  in fibn
;;

let print_fib n =
  Printf.printf "fib %d -> %d\n" n (fib n)
;;

print_fib 5;;


(* Y combinator *)
let f fact x = if x = 1 then 1 else fact (x - 1) * x
let rec y f x = f (y f) x
let z = y f 10;;

Printf.printf "%d\n" z;;
