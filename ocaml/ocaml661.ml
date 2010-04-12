(* -*- coding: utf-8; -*- *)
open List;;

(* Exercise 1 *)
type figure =
  | Point
  | Circle of int
  | Rectangle of int * int
  | Square of int
;;

type loc_fig = {x: int; y: int; fig: figure};;


let overlap lf1 lf2 =
  let square x = x * x in
  let overlap_circle x1 y1 r1 x2 y2 r2 =
	square (x1 - x2) + square (y1 - y2) > square (r1 - r2)
  in
  let rec overlap_rectangle x1 y1 h1 w1 x2 y2 h2 w2 =
	match x1, y1, x2, y2 with
    | x1, y1, x2, y2 when (x1 < x2) && (y1 < y2)
        -> (x1 + w1 > x2) && (y1 + h1 > y2)
    | x1, y1, x2, y2 when (x1 < x2) && (y1 > y2)
        -> (x1 + w1 > x2) && (y1 + h1 > y2 + h2)
    | x1, y1, x2, y2 when (x1 >= x2)
        -> overlap_rectangle x2 y2 h2 w2 x1 y1 h1 w1
	| _, _, _, _
        -> false
  in
  let overlap_square x1 y1 l1 x2 y2 l2 =
	overlap_rectangle x1 y1 l1 l1 x2 y2 l2 l2
  in
	match lf1.fig, lf2.fig with
	| Circle r1, Circle r2
		-> overlap_circle lf1.x lf1.y r1 lf2.x lf2.y r2
	| Rectangle (h1, w1), Rectangle (h2, w2)
		-> overlap_rectangle lf1.x lf1.y h1 w1 lf2.x lf2.y h2 w2
	| Square l1, Square l2
		-> overlap_square lf1.x lf1.y l1 lf2.x lf2.y l2
	| _, _
		-> false
;;


(* Exercise 2 *)
type nat = Zero | OneMoreThan of nat;;
let rec add m n =
  match m with 
  | Zero -> n 
  | OneMoreThan m' -> OneMoreThan (add m' n)
;;

let int_of_nat nat =
  let rec int_of_nat ret = function
	| Zero -> ret
	| OneMoreThan nat -> int_of_nat (ret + 1) nat
  in
	int_of_nat 0 nat
;;

let rec mul m n =
  match m, n with
  | OneMoreThan Zero, _ -> n
  | _, Zero | Zero, _ -> Zero
  | OneMoreThan m', _ -> mul m' (add n n)
;;

let rec monus m n =
  match m, n with
  | Zero, _ -> Zero
  | _, Zero -> m
  | OneMoreThan m', OneMoreThan n' -> monus m' n'
;;


let two = OneMoreThan (OneMoreThan Zero);; 
let three = OneMoreThan (OneMoreThan (OneMoreThan Zero));; 

let print_nat n = Printf.printf "%d\n" (int_of_nat n);;
print_nat three;;
print_nat (mul two three);;
print_nat (monus three two);;


(* Exercise 3 *)

let rec minus m n = 
  match m, n with
  | Zero, OneMoreThan n' -> None
  | _, Zero -> Some m
  | OneMoreThan m', OneMoreThan n' -> minus m' n'
;;

let print_nat_option = function
  | None -> Printf.printf "None\n"
  | Some x -> Printf.printf "%d\n" (int_of_nat x)
;;
  
print_nat_option (minus three two);;
print_nat_option (minus two three);;


(* Exercise 4 *)

type 'a tree = Lf | Br of 'a * 'a tree * 'a tree;;

let rec comptree x n =
  match n with
  | n when n < 0 -> Br (x, Lf, Lf)
  | 0 -> Br (x, Lf, Lf)
  | _ -> Br (x, comptree x (n-1), comptree x (n-1))
;;


(* Exercise 5 *)
let comptree = 
  Br(1, Br(2, Br(4, Lf, Lf),
              Br(5, Lf, Lf)),
        Br(3, Br(6, Lf, Lf),
              Br(7, Lf, Lf)));;  

let rec preorder = function
  | Lf -> []
  | Br (x, left, right) -> x :: (preorder left) @ (preorder right)
;;

let rec inorder = function
  | Lf -> []
  | Br (x, left, right) -> (inorder left) @ (x :: inorder right)
;;

let rec postorder = function
  | Lf -> []
  | Br (x, left, right) -> (postorder left) @ (postorder right) @ [x]
;;

let rec preord t l =
  match t with
  | Lf -> l
  | Br (x, left, right) -> x :: (preord left (preord right l))
;;

let rec inord t l =
  match t with
  | Lf -> l
  | Br (x, left, right) -> inord left (x :: inord right l)
;;

let rec postord t l =
  match t with
  | Lf -> l
  | Br (x, left, right) -> postord left (postord right (x::l))
;;


(* Exercise 6 *)

let rec reflect = function
  | Lf -> Lf
  | Br (x, left, right) -> Br (x, reflect right, reflect left)
;;


(* Exercise 7 *)

type arith =
  | Const of int
  | Add of arith * arith
  | Mul of arith * arith
;;

let exp = Mul (Add (Const 3, Const 4), Add (Const 2, Const 5));;

let rec string_of_arith = function
  | Const n -> string_of_int n
  | Add (m, n) -> "(" ^ (string_of_arith m) ^ "+" ^ (string_of_arith n) ^ ")"
  | Mul (m, n) -> "(" ^ (string_of_arith m) ^ "*" ^ (string_of_arith n) ^ ")"
;;

let rec expand = function
  | Const n -> Const n
  | Add (m, n) 
    -> Add (expand m, expand n)
  | Mul (Add (m, n), Add (m', n'))
    -> Add (Add (expand (Mul (m, m')), expand (Mul (m, n'))), 
            Add (expand (Mul (n, m')), expand (Mul (n, n'))))
  | Mul (m, n) -> Mul (expand m, expand n)
;;

    
(* Exercise 8 *)
let labels = [1; 2; 3; 4];;

let create_tree l =
  let rec create_tree ret l =
    let rec add t x =
      match t with
      | Lf -> Br (x, Lf, Lf)
      | Br (y, left, right) ->
          match y with
          | y when y = x -> Br (y, left, right)
          | y when y < x -> Br (y, left, add right x)
          | _ -> Br (y, add left x, right)
    in
    match l with
    | [] -> ret
    | x::xs -> create_tree (add ret x) xs
  in
  create_tree Lf l
;;


let permutation l =
  let rec perm n xs a b = 
    let remove x xs = List.filter (fun y -> x <> y) xs in
    if n = 0 then a::b
    else List.fold_right (fun x y -> perm (n-1) (remove x xs) (x::a) y) xs b
  in
  perm (List.length l) l [] []
;;


let del_dup l = 
  let rec del_dup rst = function
    | [] -> rst
    | x::xs -> del_dup (x :: List.filter (fun y -> y <> x) rst) xs
  in
  del_dup l l
;;

del_dup (map create_tree (permutation [1;2;3;4]));;


(* Exercise 9 *)

type 'a seq = Cons of 'a * (unit -> 'a seq);;

let head (Cons (x, _)) = x;;
let tail (Cons (_, f)) = f ();;
let rec take n s =
  if n = 0 then [] else head s :: take (n-1) (tail s);;

let rec from n = Cons (n, fun () -> from (n+1));;

let rec sift n (Cons (x, f)) =
  if (x mod n) = 0 then sift n (f ())
  else Cons (x, fun () -> sift n (f ()))
;;

let rec sieve (Cons (x, f)) = Cons (x, fun () -> sieve (sift x (f ())));;

let primes = sieve (from 2);;

let rec nthseq n (Cons (x, f)) =
  if n = 1 then x
  else nthseq (n-1) (f())
;;

(* print_int (nthseq 9999 primes);; *)


(* Exercise 10 *)
type ('a, 'b) sum = Left of 'a | Right of 'b;;

(* 1. val : 'a * ('b, 'c) sum -> ('a * 'b, 'a * 'c) sum *)
let expand_sum (x, y) =
  match y with
  | Left l -> Left (x, l)
  | Right r -> Right (x, r)
;;


(* 2. val: ('a, 'b) sum * ('c, 'd) sum -> 
   (('a * 'c, 'b * 'd) sum, ('a * 'd, 'b * 'c) sum) sum *)
let cross_sum (x, y) =
  match x, y with
  | Left xl, Left yl -> Left (Left (xl, yl))
  | Left xl, Right yr -> Right (Left (xl, yr))
  | Right xr, Left yl -> Right (Right (xr, yl))
  | Right xr, Right yr -> Left (Right (xr, yr))
;;

(* 3. val: ('a -> 'b) * ('c -> 'b) -> ('a, 'c) sum -> 'b *)
let merge_sum (fl, fr) = function
  | Left l -> fl l
  | Right r -> fr r
;;

(* 4. val: (('a, 'b) sum -> 'c) -> ('a -> 'c) * ('b -> 'c) *)
let fun_tuple f c =
  match f with
  | Left fl -> (fl c, None)
  | Right fr -> (None, fr c)
;;

(* 5. val: ('a -> 'b, 'a -> 'c) sum -> ('a -> ('b,'c) sum) *)  
let func_sum f a = 
  match f with
  | Left fl -> Left (fl a)
  | Right fr -> Right (fr a)
;;
