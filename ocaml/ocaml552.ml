open Printf
open List

(* Exercise 2 *)
let hd (x::_) = x;;
let tl (_::xs) = xs;;

let null = function
  | [] -> true;
  | _ -> false;
;;

let rec sum_list_ l =
  match l with
  | [] -> 0
  | n::rest -> n + sum_list_ rest
;;

let rec sum_list l =
	if (null l) then 0
	else (hd l) + (sum_list (tl l))
;;

let rec sum_list2 s l =
  if (null l) then s
  else sum_list2 (s + (hd l)) (tl l)
;;

let sum_list' l = List.fold_left (+) 0 l;;

Printf.printf "%d\n" (sum_list [1; 2; 3; 4; 5]);;
Printf.printf "%d\n" (sum_list2 0 [1; 2; 3; 4; 5]);;
Printf.printf "%d\n" (sum_list' [1; 2; 3; 4; 5]);;


(* Exercise 3-1 *)

let rec downto0 = function 
  | 0 -> [0]
  | n -> [n] @ downto0 (n-1)
;;

let print_list l = 
  begin
    Printf.printf "[";
    List.map (Printf.printf "%d; ") l;
    Printf.printf "]\n";
  end;
;;

print_list [];;
print_list (downto0 10);;
Printf.printf "\n";;

(* Exercise 3-2 *)
let dict = 
  [(1000, "M"); (900, "CM"); (500, "D"); (400, "CD");
  (100,"C"); (90, "XC"); (50, "L"); (40, "XL"); (10, "X"); 
  (9, "IX"); (5,"V"); (4, "IV"); (1, "I")];;


let rec rom_part_str rom_num = function
  | 0 -> ""
  | n -> rom_num ^ rom_part_str rom_num (n-1)
;;


let roman defdict num =
  let rec roman_part defdict' num' m str =
    match (num', m) with
    | (0, 0) -> str
    | (_, _) ->
        let (b, rc) = (hd defdict') in
        let q = (m / b) in 
        roman_part (tl defdict') q (m mod b) (str ^  (rom_part_str rc q))
  in
  roman_part defdict num num ""
;;

Printf.printf "%s\n" (roman dict 10504);;

(* Exercise 3-3 *)

let concat = fold_left (@) [];;

print_list (concat [[1; 2; 3]; [2]; [4; 5;]; []]);;


(* Exercise 3-4 *)
let zip l1 l2 =
  let rec zip l1 l2 zipped =
    match (l1, l2) with
    | ([], _) | (_, []) -> zipped
    | (_, _) -> 
        zip (List.tl l1) (List.tl l2) (zipped @ [(List.hd l1, List.hd l2)])
  in
  zip l1 l2 []
;;


(* Exercise 3-5 *)
let filter p l =
  let filter_elem e = if p e then [e] else [] in
  List.fold_left (@) [] (List.map filter_elem l)
;;



(* Exercise 3-6-a*)
let rec belong a = function
  | [] -> false
  | (x::xs) -> if a=x then true else (belong a xs)
;;

(* Exercise 3-6-b*)
let intersect s1 s2 =
  let rec intersect s1 s2 set =
	match (s1, s2) with
    | ([], _) | (_ ,[]) -> set
    | (x1::xs1, x2::xs2) -> 
        if x1=x2 then (intersect xs1 xs2 (x1::set))
        else (intersect xs1 xs2 set)
  in intersect s1 s2 []
;;

(* Exercise 3-6-c *)		
let set l =
  let rec set s = function
    | [] -> s
    | (x::xs) -> 
        if belong x s then set s xs
        else set (x::s) xs
  in
  set [] l
;;

let union s1 s2 =
  let rec union s1 s2 t u =
	match (s1, s2) with
    | ([], []) -> u
    | ([], s) -> s @ u
    | (x1::xs1, []) -> union xs1 t [] (x1::u)
    | (x1::xs1, x2::xs2) ->
        if x1=x2 then union xs1 (xs2 @ t) [] (x1::u)
        else union (x1::xs1) xs2 (x2::t) u
  in
  let l1 = set s1 
  and l2 = set s2 in
  union l1 l2 [] []
;;

Printf.printf "\n%s" "union ->";;
print_list (union [8;1;1;2;3;4;5;3] [2;2;4;4;6;7;7;5;5;9]);;
Printf.printf "\n";;


(* Exercise 3-6-d *)
let diff s1 s2 =
  let rec diff s1 s2 t d =
    match (s1, s2) with
    | ([], _) -> d
    | (x1::xs1, []) -> diff xs1 t [] (x1::d) 
    | (x1::xs1, x2::xs2) ->
        if x1=x2 then diff xs1 xs2 [] d
        else diff (x1::xs1) xs2 (x2::t) d
  in
  let l1 = set s1
  and l2 = set s2 in
  diff l1 l2 [] []
;;
		
Printf.printf "\n%s" "diff ->";;
print_list (diff [8;1;1;2;3;4;5;3] [2;2;4;4;6;7;7;5;5;9]);;
Printf.printf "\n";;
