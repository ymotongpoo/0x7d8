open Printf
open List

let print_list l = 
  begin
    Printf.printf "[";
    List.map (Printf.printf "%s; ") l;
    Printf.printf "]\n";
  end;
;;

(* Exercise 4 *)

let f = string_of_float;;
let g = float_of_int;;
let ($) f g x = f (g x);;

let fun1 l = map f (map g l);;
let fun2 l = map (f $ g) l;;

let l = [1;2;3;4;5;6];;

print_list (fun1 l);;

print_list (fun2 l);;


(* Exercise 5 *)
let rec forall_ p = function
  | [] -> true
  | x::rest -> if p x then forall_ p rest else false
;;

let rec exists_ p = function
  | [] -> false
  | x::rest -> (p x) or (exists_ p rest)
;;


let forall p l = List.fold_right (&&) (map p l) true;;

let exists p l = List.fold_right (or) (map p l) false;;


Printf.printf "%b\n" (forall (fun x -> x < 10) [1;2;3;4;5]);;
Printf.printf "%b\n" (forall (fun x -> x > 10) [1;2;3;4;5]);;
Printf.printf "%b\n" (exists (fun x -> x = 1) [1;2;3;4;5]);;
Printf.printf "%b\n" (exists (fun x -> x = 10) [1;2;3;4;5]);;


(* Exercise 6 *)
let rec quick = function
  | [] -> []
  | [x] -> [x]
  | x :: xs ->  (* x is the pivot *)
      let rec partition left right = function
        | [] -> (quick left) @ (x :: quick right)
        | y :: ys -> if x < y then partition left (y :: right) ys
          else partition (y :: left) right ys
      in partition [] [] xs
;;
        
let rec quicker l sorted =
  match l with
  | [] -> sorted
  | x::xs -> 
	  let smallers, biggers = List.partition (fun y -> y < x) xs in
	  quicker smallers (x :: quicker biggers sorted)
;;
   
let partition f l =
  let rec partition_ l fmr ltr =
    match l with
    | [] -> fmr, ltr
    | x::xs ->
        if f x then partition_ xs (x::fmr) ltr
        else partition_ xs fmr (x::ltr)
  in
  partition_ l [] []
;;

let rec quicker_tail l k =
  match l with
  | [] -> k []
  | x::xs ->
      let smallers, biggers = partition (fun y -> y < x) xs in
      let at x y = List.rev_append (List.rev x) y in
      quicker_tail smallers (fun sorted_s -> 
        quicker_tail biggers (fun sorted_b -> k (at sorted_s (at [x] sorted_b))))
;;

let print_list_d l = 
  begin
    Printf.printf "[";
    List.map (Printf.printf "%d; ") l;
    Printf.printf "]\n";
  end;
;;

print_list_d (quicker_tail [2;4;5;3;0;3;10;9;4;7] (fun x -> x));;


(* Exercise 7 *)
let squares r =
  let sqr x = x * x in
  let rec squares_ x y l =
    match x, y with
    | _, y when (sqr y) > r -> l
    | x, y when sqr x + sqr y < r -> squares_ (x+1) y l		
    | x, y when sqr x + sqr y > r -> squares_ (y+1) (y+1) l
    | x, y -> squares_ (y+1) (y+1) ((x,y)::l)
  in
  squares_ 0 0 []
;;

Printf.printf "num of pairs -> %d\n" (List.length (squares 48612265));;


(* Exercise 8 *)
let map2 f l =
  let rec recursive result = function
    | [] -> List.rev result
    | x::xs -> recursive ((f x)::result) xs
  in
  recursive [] l
;;

print_list_d (map2 (fun x -> x*x) [1;2;3;4;5]);;
  
		
